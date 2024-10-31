from scrapy_redis.spiders import RedisSpider  
from scrapy_splash import SplashRequest

class CnkiSpider(RedisSpider):
    name = 'weather_spider'
    redis_key = 'weather_spider:start_url'

    def __init__(self, *args, **kwargs):
        super(CnkiSpider, self).__init__(args, **kwargs)
    
    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, callback=self.parse, endpoint='render.json', args={'wait': 0.5})

    def parse(self, response):
        tr_elements = response.css('tr')
        print(tr_elements)

        # 或者使用 XPath 选择器  
        # tr_elements = response.xpath('//tr')  

        for tr in tr_elements:  
            tr_content = tr.css('::text').getall()  
            tr_cleaned_content = [text.strip() for text in tr_content if text.strip()]
            if tr_cleaned_content: 
                print(tr_cleaned_content)
            else:
                print("爬取的数据为空!")