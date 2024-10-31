from scrapy_redis.spiders import RedisSpider  

class CnkiSpider(RedisSpider):
    name = 'cnki_spider'
    redis_key = 'cnki_spider:start_url'

    def __init__(self, *args, **kwargs):
        super(CnkiSpider, self).__init__(args, **kwargs)

    def parse(self, response):
        print(response)