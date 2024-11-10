#飞书机器人群发消息汇报考生签到信息
feishu_url = "https://open.feishu.cn/open-apis/bot/v2/hook/xxxx"

# Redis配置信息
REDIS_HOST = '113.45.148.34' # Redis服务器的端口
REDIS_PORT = '6379' # redis端口号
REDIS_PASSWORD = 'mingri1234' #redis密码
REDIS_DB = '3'
REDIS_DECODE = True # 如果为True，将返回的数据解码为字符串

# 爬虫初始化url
first_url = ("https://assets.msn.cn/service/weather/weathertrends?apiKey=j5i4gDqHL6nGYwx5wi5kRhXjtf2c5qgFX9fzfk0TOo&cm=zh-cn"
       "&locale=zh-cn&lon=110.18000030517578&lat=25.235000610351562&units=C&user=m-2BE64755C83A64071FC6546FC9406530"
       "&ocid=msftweather&includeWeatherTrends=true&includeCalendar=false&fdhead=&weatherTrendsScenarios=WindTrend"
       "&days=30&insights=1&startDate=20200101&endDate=20201231")

# openai apiKey
api_key = 'sk-qGXAAEMyG5J7Gfzh5298A39214D243E59799Db210fBfE2Db'
chatgpt_path = 'https://api.xiaoai.plus'


# 数据文件
csv_path = "./result/all_in_one_processed.csv"
