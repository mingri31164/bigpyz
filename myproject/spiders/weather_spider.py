import urllib.parse
from scrapy_redis.spiders import RedisSpider
import json
import redis
from myproject.items import TemperatureItem, HumidityItem, PrecipitationItem, WindVelocityItem


class WeatherSpider(RedisSpider):
    name = 'weather_spider'  # 爬虫名称
    redis_key = 'weather_spider:start_url'  # redis服务上管理url的键

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._redis_conn = redis.Redis(host='113.45.148.34', password="mingri1234", port=6379, db=3)

    # 开始请求前，将要爬取的多个url封装好并批量push到redis上
    def start_requests(self):
        base_url = self.redis_get()
        self.build_urls(base_url)
        return super().start_requests()

    # 从Redis获取URL
    def redis_get(self):
        return self._redis_conn.lpop(self.redis_key)

    # 批量将url push到redis服务上
    def redis_push_batch(self, urls):
        pipeline = self._redis_conn.pipeline()
        for url in urls:
            pipeline.lpush(self.redis_key, url)
        pipeline.execute()  # 批量推送到 Redis

    # 构建要爬取的url
    def build_urls(self, base_url):
        base_url = base_url.decode('utf-8')
        start_dates = [20240101, 20230101, 20220101, 20210101, 20200101]
        end_dates = [20241231, 20231231, 20221231, 20211231, 20201231]
        weather_trends_scenarios = [
            "TemperatureTrend,OverviewSummary,Summary,ClimateSummary",
            "PrecipitationTrend",
            "HumidityTrend",
            "WindTrend"
        ]

        urls = []
        for start_date, end_date in zip(start_dates, end_dates):
            for weather_special in weather_trends_scenarios:
                url_parts = urllib.parse.urlparse(base_url)
                query_params = urllib.parse.parse_qs(url_parts.query)
                query_params['weatherTrendsScenarios'] = [weather_special]
                query_params['startDate'] = [start_date]
                query_params['endDate'] = [end_date]
                updated_query = urllib.parse.urlencode(query_params, doseq=True)

                url = urllib.parse.urlunparse((
                    url_parts.scheme,
                    url_parts.netloc,
                    url_parts.path,
                    url_parts.params,
                    updated_query,
                    url_parts.fragment
                ))
                urls.append(url)

        self.redis_push_batch(urls)  # 批量推送到 Redis

    # 解析返回的网络请求数据
    def parse(self, response, **kwargs):
        try:
            json_response = json.loads(response.body)
            trend_chart_data = json_response['value'][0]['responses'][0]['trendChart']
        except (KeyError, json.JSONDecodeError) as e:
            self.logger.error(f"JSON解析错误或数据不完整: {e}")
            return

        for date, trends in trend_chart_data.items():
            trend_days = trends.get('trendDays', {})
            if not trend_days:
                continue

            temperature_item, precipitation_item, humidity_item, wind_velocity_item = None, None, None, None

            # 优先处理温度数据
            if '1' in trend_days:
                temperature_item = TemperatureItem(date=date, height_temperature=trend_days['1'])
                if '3' in trend_days:
                    temperature_item['height_history_temperature'] = trend_days['3']
                if '6' in trend_days:
                    temperature_item['low_temperature'] = trend_days['6']
                if '8' in trend_days:
                    temperature_item['low_history_temperature'] = trend_days['8']
                yield temperature_item

            # 处理降水量数据
            if '11' in trend_days:
                precipitation_item = PrecipitationItem(date=date, precipitation=trend_days['11'])
                yield precipitation_item

            # 处理湿度数据
            if '58' in trend_days:
                humidity_item = HumidityItem(date=date, humidity=trend_days['58'])
                if '60' in trend_days:
                    humidity_item['humidity_history'] = trend_days['60']
                yield humidity_item

            # 处理风速数据
            if '41' in trend_days:
                wind_velocity_item = WindVelocityItem(date=date, wind_velocity=trend_days['41'])
                if '43' in trend_days:
                    wind_velocity_item['wind_velocity_history'] = trend_days['43']
                yield wind_velocity_item
