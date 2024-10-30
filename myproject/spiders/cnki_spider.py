import scrapy
from scrapy_redis.spiders import RedisSpider

class CnkiSpider(RedisSpider):
    name = 'cnki_spider'
    allowed_domains = ['www.cnki.net']
    redis_key = 'cnki_spider:start_urls'

    def __init__(self, name = None, **kwargs):
        domin = kwargs.pop('domin','')
        self.allowed_domains = list(filter(None,domin.split('.')))
        super(CnkiSpider, self).__init__(name, **kwargs)

    def parse(self, response):
        """
        解析报刊页面，提取报刊标题、作者、摘要等信息
        """
        for article in response.css('.s-item'):
            yield {
                'title': article.css('.s-title::text').get(),
                'date': article.css('.s-author::text').get(),
                'author': article.css('.s-author::text').get(),
                'des': article.css('.s-abstr::text').get(),
            }

        # 提取分页所需的参数
        next_page_data = response.xpath("//a[@class='page-prev']/@onclick").get()
        if next_page_data:
            # 提取 CommonDealAction 函数中的各个参数
            params = self.extract_params_from_js(next_page_data)
            
            # 构造 POST 请求
            if params:
                form_data = {
                    'curpage': params['curpage'],
                    'RecordsPerPage': params['RecordsPerPage'],
                    'turnpage': params['turnpage'],
                    'DisplayMode': params['DisplayMode'],
                    'PageName': params['PageName'],
                    'DbPrefix': params['DbPrefix'],
                    'Fields': params['Fields'],
                    'sortorder': params['sortorder'],
                    'sortfield': params['sortfield'],
                }
                
                # 发送 POST 请求，继续爬取下一页
                yield scrapy.FormRequest(
                    url="https://www.cnki.net/KNS/request/SearchHandler.ashx",
                    formdata=form_data,
                    callback=self.parse
                )

    def extract_params_from_js(self, js_code):
        """
        提取 JavaScript onclick 中的参数
        """
        try:
            # 手动解析 js_code 中的参数，提取用于构造 POST 请求的参数
            params = {}
            js_code = js_code[js_code.index('(') + 1: js_code.rindex(')')]  # 提取括号内的内容
            param_values = js_code.split(',')
            params['curpage'] = param_values[0].strip().replace("'", "")
            params['RecordsPerPage'] = param_values[1].strip().replace("'", "")
            params['turnpage'] = param_values[2].strip().replace("'", "") 
            params['DisplayMode'] = param_values[3].strip().replace("'", "")
            params['PageName'] = param_values[4].strip().replace("'", "")
            params['DbPrefix'] = param_values[5].strip().replace("'", "")
            params['Fields'] = param_values[6].strip().replace("'", "")
            params['sortorder'] = param_values[7].strip().replace("'", "")
            params['sortfield'] = param_values[8].strip().replace("'", "")
            return params
        except Exception as e:
            self.logger.error(f"Error extracting parameters: {e}")
            return None