import asyncio
import aiohttp
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from typing import Dict, List, Tuple
import openpyxl

tenki_items=[]
tenki_items_text=[]

class crawler_meta:
    def __init__(self, browser):
        self.browser = browser

    def drop_scroll(self):
        '''滚动页面到最后'''
        last_height = self.browser.execute_script("return document.documentElement.scrollHeight")
        while True:
            self.browser.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
            time.sleep(2)
            new_height = self.browser.execute_script("return document.documentElement.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    def start_crawl(self):
        '''开始爬取'''
        raise NotImplementedError("请实现执行方法")
    
    def get_page_data(self):
        pass
    


class tenkiCrawler(crawler_meta):
    def __init__(self, tenki_url_raw: str, relative_path ='my_tenki_infos'):
        self.tenki_url_raw = tenki_url_raw
        # self.tenki_rankings = tenki_rankings
        self.relative_path = relative_path
        self.browser = None

    def get_page_data(self):
        '''页面数据获取'''
        for i in range(20):
            
            time.sleep(2)
            wait = WebDriverWait(self.browser, 10)

            tenki_items_ = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//tr")))
            tenki_items.append(tenki_items_)
            tenki_items_text_ = [item.text for item in tenki_items_]
            tenki_items_text.append(tenki_items_text_)
            
            try:
                node = self.browser.find_element(By.XPATH, "//a[contains(@id, 'js_prevMonth')]")
                # node = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//a[contains(@id, 'js_prevMonth')]")))
                node.click()
                # print("clicked!")
            except TypeError:
                break
            
     

    # def get_page_imgs(self, tenki_items_raw, folder_name):
    #     '''图片获取'''
    #     folder_path = self.relative_path + '/' + folder_name + '图片'    # 文件夹路径
    #     img_urls = {}

    #     for item in tenki_items_raw:
    #         # 图片URL
    #         img_element = item.find_element(By.CSS_SELECTOR, 'img.i71-img')
    #         img_url = img_element.get_attribute('src')

    #         # 电影/节目名称
    #         title_element = item.find_element(By.CLASS_NAME, 'rvi__tit1')
    #         movie_name = title_element.text.split('\n')[-1].strip()

    #         img_urls[movie_name] = img_url

    #     # 如果文件夹不存在则创建
    #     if not os.path.exists(folder_path):
    #         os.makedirs(folder_path)

    #     # 保存
    #     for img_name, img_url_ in img_urls.items():
    #         response = requests.get(img_url_)
    #         with open(f'{folder_path}/{img_name}.jpg', 'wb') as f:
    #             f.write(response.content)

    #     print(f"已完成 {folder_name} 的爬取和图片保存。")

    def start_crawl(self):
        '''开始爬取'''
        options = Options()
        options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0")
        self.browser = webdriver.Chrome(options=options)

        try:
            self.browser.get(self.tenki_url_raw)
            time.sleep(2)  #等待
            
            self.get_page_data()
            
            for item in tenki_items_text:
                print(item)
           
        finally:
            # 关闭
            self.browser.quit()

        print("已完成对所有榜单的爬取。")

if __name__ == '__main__':
    # 开始爬取
    crawler = tenkiCrawler(
        tenki_url_raw = 'https://tianqi.2345.com/wea_history/59431.htm',
        relative_path = 'my_tenki_infos'
    )
        # tenki_rankings = { '飙升榜':'-1','必看榜':'-6','期待榜':'-8','上新榜':'-5','热播榜': '0' },
    crawler.start_crawl()