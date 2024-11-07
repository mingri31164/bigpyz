from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_cors import CORS
import pandas as pd
from openai import OpenAI
import config

app = Flask(__name__)
#跨域启用
CORS(app)

# 读取预测数据
predicted_df = pd.read_csv(config.predict_path)

# 初始化openai配置
client = OpenAI(
    base_url = 'https://xiaoai.plus/v1',
    # sk-xxx替换为自己的key
    api_key = config.api_key
)


# 统一请求拦截
@app.before_request
def before_request():
    return None;


# 首页
@app.route("/")
def index():
    return render_template("index.html")



# chatGPT
@app.route("/chat", methods=["POST"])
def chat():
    text = request.args.get('text')
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": text}
        ]
    )
    msg = completion.choices[0].message.content
    return msg



# 查询温度数据
@app.route("/tem", methods=["GET"])
def get_temperature():
    # 读取文件
    df = pd.read_csv(config.temperature_path)
    if df.empty:
        return jsonify({"message": "温度数据为空"}), 400

    # 获取参数
    # 获取日期列并转换格式
    df['date'] = pd.to_datetime(df['date'])  # 转换为datetime对象
    dates = df['date'].dt.strftime('%Y年%m月%d日').tolist()  # 转换为指定格式并放入列表
    height_temperature = df['height_temperature'].tolist()
    height_history_temperature = df['height_history_temperature'].tolist()
    low_temperature = df['low_temperature'].tolist()
    low_history_temperature = df['low_history_temperature'].tolist()
    predicted_height_temperature = predicted_df['height_temperature'].tolist()
    predicted_low_temperature = predicted_df['low_temperature'].tolist()

    # 将四个集合放入一个大集合中
    data = {
        'dates': dates,
        'height_temperature': height_temperature,
        'height_history_temperature': height_history_temperature,
        'low_temperature': low_temperature,
        'low_history_temperature': low_history_temperature,
        'predicted_height_temperature': predicted_height_temperature,
        'predicted_low_temperature': predicted_low_temperature
    }
    response = {
        "message": "温度数据获取成功",
        "code": 200,
        "data": data
    }
    return response


# 查询湿度数据
@app.route("/hum", methods=["GET"])
def get_humidity():
    # 读取文件
    df = pd.read_csv(config.humidity_path)
    if df.empty:
        return jsonify({"message": "湿度数据为空"}), 400

    # 获取参数
    # 获取日期列并转换格式
    df['date'] = pd.to_datetime(df['date'])  # 转换为datetime对象
    dates = df['date'].dt.strftime('%Y年%m月%d日').tolist()  # 转换为指定格式并放入列表
    humidity = df['humidity'].tolist()
    humidity_history = df['humidity_history'].tolist()
    predicted_humidity = predicted_df['humidity'].tolist()


    # 将四个集合放入一个大集合中
    data = {
        'dates': dates,
        'humidity': humidity,
        'humidity_history': humidity_history,
        'predicted_humidity': predicted_humidity,
    }
    response = {
        "message": "湿度数据获取成功",
        "code": 200,
        "data": data
    }
    return response




# 查询湿度数据
@app.route("/wind", methods=["GET"])
def get_wind():
    # 读取文件
    df = pd.read_csv(config.humidity_path)
    if df.empty:
        return jsonify({"message": "风速数据为空"}), 400

    # 获取参数
    # 获取日期列并转换格式
    df['date'] = pd.to_datetime(df['date'])  # 转换为datetime对象
    dates = df['date'].dt.strftime('%Y年%m月%d日').tolist()  # 转换为指定格式并放入列表
    wind_velocity = df['wind_velocity'].tolist()
    wind_velocity_history = df['wind_velocity_history'].tolist()
    predicted_wind_velocity = predicted_df['wind_velocity'].tolist()


    # 将四个集合放入一个大集合中
    data = {
        'dates': dates,
        'humidity': wind_velocity,
        'humidity_history': wind_velocity_history,
        'predicted_humidity': predicted_wind_velocity,
    }
    response = {
        "message": "风速数据获取成功",
        "code": 200,
        "data": data
    }
    return response


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


@app.errorhandler(500)
def system_error(error):
    return render_template("500.html"), 500


if __name__ == "__main__":
    # 静态文件缓存自动刷新
    app.jinja_env.auto_reload = True
    app.run(host="127.0.0.1", port=8002, debug=True)
