from scrapy_redis.spiders import RedisSpider  
from scrapy_splash import SplashRequest

class CnkiSpider(RedisSpider):
    name = 'cnki_spider'
    redis_key = 'cnki_spider:start_url'

    def __init__(self, *args, **kwargs):
        super(CnkiSpider, self).__init__(args, **kwargs)
    
    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, callback=self.parse, endpoint='render.json', args={'wait': 3})

    def parse(self, response):
        print(response.text)