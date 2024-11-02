from scrapy_redis.spiders import RedisSpider  
import json
import redis
import urllib.parse
from myproject.items import TemperatureItem,HumidityItem,PrecipitationItem,WindVelocityItem

class WeatherSpider(RedisSpider):  
    name = 'weather_spider'  # 爬虫开始的名称
    redis_key = 'weather_spider:start_url' # redis服务上管理url的键

    # 开始请求前，先进行将要爬取的多个url给封装好，并push到redis上
    def start_requests(self):
        self.redis_conn = self._get_redis_connection()
        self.start_urls = self.redis_conn.lrange(self.redis_key, 0, -1)
        base_url = self.start_urls[0]
        self.buildUrls(base_url)
        return super().start_requests()

    # 连接留得爆的远程redis服务
    def _get_redis_connection(self):
        return redis.Redis(host='113.45.148.34', password= "mingri1234", port=6379, db=3)
    
    # 将url给push到redis服务上
    def redis_push(self, url):
        self.redis_conn.lpush(self.redis_key, url)

    # 返回redis连接实例
    def redis_conn(self):
        return self._get_redis_connection()
    
    # 构建要爬取的url
    def buildUrls(self, base_url):
        base_url = base_url.decode('utf-8')
        startDates = [20200101, 20210101, 20220101, 20230101, 20240101]
        endDates = [20201231, 20211231, 20221231, 20241231]
        weatherTrendsScenarios = ["TemperatureTrend,OverviewSummary,Summary,ClimateSummary", "PrecipitationTrend", "HumidityTrend", "WindTrend"]
        for startDate, endDate in zip(startDates, endDates):
            for weatherSpecial in weatherTrendsScenarios:
                url_parts = urllib.parse.urlparse(base_url)
                query_params = urllib.parse.parse_qs(url_parts.query)
                query_params['weatherTrendsScenarios'] = [weatherSpecial]
                query_params['startDate'] = [startDate]
                query_params['endDate'] = [endDate]
                updated_query = urllib.parse.urlencode(query_params, doseq=True)
                
                scheme = str(url_parts.scheme)
                netloc = str(url_parts.netloc)
                path = str(url_parts.path)
                params = str(url_parts.params)
                query = str(updated_query)
                fragment = str(url_parts.fragment)
                
                url = urllib.parse.urlunparse((scheme, netloc, path, params, query, fragment))
                print(url)
                self.redis_push(url)

    # 解析返回的网络请求数据
    def parse(self, response, **kwargs):
        json_response = json.loads(response.body)
        
        trend_chart_data = json_response['value'][0]['responses'][0]['trendChart']

        for date, trends in trend_chart_data.items():
            temperature_item = None
            precipitation_item = None
            humidity_item = None
            windVelocity_item = None
            
            for key, value in trends.get('trendDays', {}).items():
                if key == '1':
                    temperature_item = TemperatureItem()
                    temperature_item['date'] = date
                    temperature_item['height_temperature'] = value
                elif key == '3' and temperature_item:
                    temperature_item['height_history_temperature'] = value
                elif key == '6' and temperature_item:
                    temperature_item['low_temperature'] = value
                elif key == '8' and temperature_item:
                    temperature_item['low_history_temperature'] = value
                elif key == '11':
                    precipitation_item = PrecipitationItem()
                    precipitation_item['date'] = date
                    precipitation_item['precipitation'] = value
                elif key == '41':
                    windVelocity_item = WindVelocityItem()
                    windVelocity_item['date'] = date
                    windVelocity_item['wind_velocity'] = value
                elif key =='43' and windVelocity_item:
                    windVelocity_item['wind_velocity_history'] = value
                elif key == '58':
                    humidity_item = HumidityItem()
                    humidity_item['date'] = date
                    humidity_item['humidity'] = value
                elif key == '60' and humidity_item:
                    humidity_item['humidity_history'] = value

            # 根据具体item实例情况，合理的将数据发送到管道上    
            if temperature_item:
                print(f"保存温度相关数据: {date}")
                yield temperature_item
            if precipitation_item:
                print(f"保存降水量相关数据: {date}")
                yield precipitation_item
            if humidity_item:
                print(f"保存湿度相关数据: {date}")
                yield humidity_item
            if windVelocity_item:
                print(f"保存风速相关数据: {date}")
                yield windVelocity_item
