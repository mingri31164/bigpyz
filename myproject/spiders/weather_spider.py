from scrapy_redis.spiders import RedisSpider  
from scrapy_selenium import SeleniumRequest  
from selenium.webdriver.common.by import By  
from selenium.webdriver.support.ui import WebDriverWait  
from selenium.webdriver.support import expected_conditions as EC  

class CnkiSpider(RedisSpider):  
    name = 'weather_spider'  
    redis_key = 'weather_spider:start_url'  
    max_pages = 64

    def start_requests(self):
        return super().start_requests()

    def parse(self, response, **kwargs):
        data = []  
        tr_elements = response.css('tr')
        
        for tr in tr_elements:  
            ths = tr.css("th::text").getall()  
            tds = tr.css("td::text").getall()  
            if ths:  
                row_data = {"headers": ths}  
            else:  
                row_data = {"data": tds}  
            
            data.append(row_data) 

        yield SeleniumRequest(  
            url=response.url,
            callback=self.parse_previous_month,
            wait_time=3,
            wait_until=lambda driver: driver.find_element(By.CSS_SELECTOR, '#js_prevMonth')
        )  

    def parse_previous_month(self, response, driver):  
        print("该函数被执行！！")

        prev_month_button = WebDriverWait(driver, 10).until(  
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#js_prevMonth'))  
        )  

        prev_month_button.click()

        WebDriverWait(driver, 10).until(  
            EC.presence_of_element_located((By.CSS_SELECTOR, 'tr')) 
        )  

        data1 = []  
        tr_elements = driver.find_elements(By.TAG_NAME, 'tr')  

        for tr in tr_elements:  
            ths = tr.find_elements(By.TAG_NAME, 'th') 
            tds = tr.find_elements(By.TAG_NAME, 'td')  

            row_data = {  
                "headers": [th.text for th in ths],  
                "data": [td.text for td in tds]  
            }  

            data1.append(row_data)  

        print(data1)