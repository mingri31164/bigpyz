from scrapy_redis.spiders import RedisSpider
from scrapy_splash import SplashRequest
import redis

class MySpider(RedisSpider):
    name = 'my_spider'
    redis_key = 'my_spider:start_urls'

    def start_requests(self):
        # 从Redis获取起始URL
        url = self.redis_get()
        if url:
            yield SplashRequest(url, callback=self.parse, endpoint='render.json', args={'wait': 3})

    def parse(self, response):
        # 假设我们找到了下一页的URL
        next_page_url = response.css('a.next_page::attr(href)').get()

        # 将新发现的URL推送到Redis
        if next_page_url:
            self.redis_push(next_page_url)

        # 继续处理其他数据爬取逻辑

    def redis_get(self):
        # 从Redis获取URL
        return self.redis_conn.lpop(self.redis_key)

    def redis_push(self, url):
        # 将新URL推送到Redis
        self.redis_conn.lpush(self.redis_key, url)

    @property
    def redis_conn(self):
        # 获取Redis连接
        return self._get_redis_connection()

    def _get_redis_connection(self):
        # 实现获取Redis连接的方法
        return redis.Redis(host='localhost', port=6379, db=0)