import subprocess
import signal
import time
import threading
import platform
import os
import redis
from weather_predictor.entry import start_all

# 连接到 Redis
r = redis.Redis(
    host='113.45.148.34',
    port=6379,
    password='mingri1234',
    db=3
)

# 要推送的 URL
url = ("https://assets.msn.cn/service/weather/weathertrends?apiKey=j5i4gDqHL6nGYwx5wi5kRhXjtf2c5qgFX9fzfk0TOo&cm=zh-cn"
       "&locale=zh-cn&lon=110.18000030517578&lat=25.235000610351562&units=C&user=m-2BE64755C83A64071FC6546FC9406530"
       "&ocid=msftweather&includeWeatherTrends=true&includeCalendar=false&fdhead=&weatherTrendsScenarios=WindTrend"
       "&days=30&insights=1&startDate=20200101&endDate=20201231")

launch_scrapy_cmd = 'scrapy crawl weather_spider'

# remote server url
remote_server_url = '127.0.0.1:8080'

# 强行终止可能会导致数据缺失，因为爬取完之后，还有一段时间是scrapy整理数据，这个时候终止会出导致部分数据缺失
def monitor_user_input(process):  
    """监控用户输入"""  
    while True:  
        user_input = input().strip().lower()  
        if user_input == 'exit':  
            print("收到退出命令，正在发送退出信号...")  
            process.terminate()  # 发送终止信号  
            break  

def launch_scrapy():
    """执行Scrapy命令"""
    print("启动Scrapy爬虫...")
    print("如果你觉得爬取已结束, 输入exit并回车来结束爬虫")
    
    try:
        if platform.system() == 'Windows':
            process = subprocess.Popen(
                launch_scrapy_cmd,
                shell=True,
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
            )
        else:
            process = subprocess.Popen(
                launch_scrapy_cmd,
                shell=True,
                preexec_fn=os.setsid
            )

        # 创建监控用户输入的线程
        input_thread = threading.Thread(target=monitor_user_input, args=(process,))
        input_thread.daemon = True  # 设置为守护线程
        input_thread.start()

        # 等待进程结束
        process.wait()
        
    except Exception as e:
        print(f"执行Scrapy命令时出错: {e}")
        raise e

def main():
    try:
        # 执行Redis命令
        print("执行Redis命令...")
        # 检查键是否存在并获取当前值
        len = r.llen('weather_spider:start_url')

        # 如果键不存在或当前值为空，则执行 lpush
        if len == 0:
            r.lpush('weather_spider:start_url', url)
        elif len >= 1:
            print("url已存在，跳过添加操作")

        # 启动主程序
        start_all(launch_scrapy,remote_server_url)
        
    except subprocess.CalledProcessError as e:
        print(f"执行出错: {e}")
    except KeyboardInterrupt:
        print("\n程序被用户中断")
    except Exception as e:
        print(f"程序执行出错: {e}")

if __name__ == "__main__":
    main()