from scrapy_redis.spiders import RedisSpider  
import json
import redis
import urllib.parse

class WeatherSpider(RedisSpider):  
    name = 'weather_spider'  
    redis_key = 'weather_spider:start_url'  

    def start_requests(self):
        self.redis_conn = self._get_redis_connection()
        self.start_urls = self.redis_conn.lrange(self.redis_key, 0, -1)
        base_url = self.start_urls[0]
        self.buildUrls(base_url)
        return super().start_requests()

    def _get_redis_connection(self):
        return redis.Redis(host='113.45.148.34', password= "mingri1234", port=6379, db=3)
    
    def redis_push(self, url):
        self.redis_conn.lpush(self.redis_key, url)

    def redis_conn(self):
        return self._get_redis_connection()
    
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
                # 确保所有参数都是字符串类型
                scheme = str(url_parts.scheme)
                netloc = str(url_parts.netloc)
                path = str(url_parts.path)
                params = str(url_parts.params)
                query = str(updated_query)
                fragment = str(url_parts.fragment)
                
                url = urllib.parse.urlunparse((scheme, netloc, path, params, query, fragment))
                print(url)
                self.redis_push(url)

    def parse(self, response, **kwargs):
        json_response = json.loads(response.body)
        
        trend_chart_data = json_response['value'][0]['responses'][0]['trendChart']

        for date, trends in trend_chart_data.items():
            print(f"Date: {date}")
            for day, value in trends['trendDays'].items():
                print(f"  Day: {day}, Value: {value}")
            print()
    
    
        
        # url = 'https://assets.msn.cn/service/weather/weathertrends?apiKey=j5i4gDqHL6nGYwx5wi5kRhXjtf2c5qgFX9fzfk0TOo&cm=zh-cn&locale=zh-cn&lon=110.18000030517578&lat=25.235000610351562&units=C&user=m-2BE64755C83A64071FC6546FC9406530&ocid=msftweather&includeWeatherTrends=true&includeCalendar=false&fdhead=&weatherTrendsScenarios=TemperatureTrend,OverviewSummary,Summary,ClimateSummary,PrecipitationTrend,HumidityTrend,WindTrend&days=30&insights=1&startDate=20230101&endDate=20231231'