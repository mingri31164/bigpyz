#飞书机器人群发消息汇报考生签到信息
feishu_url = "https://open.feishu.cn/open-apis/bot/v2/hook/xxxx"

# 数据库的配置信息
HOSTNAME = '185.106.176.190'
PORT     = '3306'
DATABASE = 'csd_website_server'
USERNAME = 'delyr1c'
PASSWORD = 'SZLnMWh73LrMGPKz'
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME,PASSWORD,HOSTNAME,PORT,DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI



# Redis配置信息
REDIS_HOST = '113.45.148.34' # Redis服务器的端口
REDIS_PORT = '6379' # redis端口号
REDIS_PASSWORD = 'mingri1234' #redis密码
REDIS_DB = '3'
REDIS_DECODE = True # 如果为True，将返回的数据解码为字符串


# openai apiKey
api_key = 'sk-qGXAAEMyG5J7Gfzh5298A39214D243E59799Db210fBfE2Db'
chatgpt_path = 'https://api.xiaoai.plus'


# 预测数据文件
predict_path = "./result/all_in_one_predicted.csv"
# 温度数据文件
temperature_path = "./result/temperature.csv"
# 湿度数据文件
humidity_path = "./result/humidity.csv"
# 风速数据文件
wind_velocity_path = "./result/wind_velocity.csv"
