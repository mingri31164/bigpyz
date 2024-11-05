import subprocess
import signal
import time
import threading
import platform
import os

from weather_predictor.entry import start_all

redis_url_cmd = 'redis-cli.exe -h 113.45.148.34 -a "mingri1234" -p 6379 -n 3 lpush weather_spider:start_url "https://assets.msn.cn/service/weather/weathertrends?apiKey=j5i4gDqHL6nGYwx5wi5kRhXjtf2c5qgFX9fzfk0TOo&cm=zh-cn&locale=zh-cn&lon=110.18000030517578&lat=25.235000610351562&units=C&user=m-2BE64755C83A64071FC6546FC9406530&ocid=msftweather&includeWeatherTrends=true&includeCalendar=false&fdhead=&weatherTrendsScenarios=WindTrend&days=30&insights=1&startDate=20200101&endDate=20201231""'
launch_scrapy_cmd = 'scrapy crawl weather_spider'

def send_ctrl_c_twice(process):
    """发送两次 Ctrl+C 信号到进程"""
    try:
        if platform.system() == 'Windows':
            # Windows系统
            process.send_signal(signal.CTRL_C_EVENT)
            time.sleep(1)  # 等待1秒
            process.send_signal(signal.CTRL_C_EVENT)
        else:
            # Unix系统
            os.killpg(os.getpgid(process.pid), signal.SIGINT)
            time.sleep(1)
            os.killpg(os.getpgid(process.pid), signal.SIGINT)
    except Exception as e:
        print(f"发送Ctrl+C信号时出错: {e}")

def monitor_user_input(process):
    """监控用户输入"""
    while True:
        user_input = input().strip().lower()
        if user_input == 'exit':
            print("收到退出命令，正在发送两次Ctrl+C...")
            send_ctrl_c_twice(process)
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
        result = subprocess.run(redis_url_cmd, shell=True, capture_output=True, text=True)
        print("输出:", result.stdout)
        
        if result.stderr is None or result.stderr.strip() == "":
            print("Redis命令执行成功")
        else:
            print("错误:", result.stderr)
            return  # 如果Redis命令出错，直接返回

        # 启动主程序
        start_all(launch_scrapy)
        
    except subprocess.CalledProcessError as e:
        print(f"执行出错: {e}")
    except KeyboardInterrupt:
        print("\n程序被用户中断")
    except Exception as e:
        print(f"程序执行出错: {e}")

if __name__ == "__main__":
    main()