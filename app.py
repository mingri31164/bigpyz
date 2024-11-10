import pandas
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_cors import CORS
import pandas as pd
from openai import OpenAI
import config

app = Flask(__name__)

#跨域启用
CORS(app)

# 读取文件数据
df = pd.read_csv(config.csv_path)
df = pandas.DataFrame(df)

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
@app.route("/tem/<int:year>", methods=["GET"])
def get_temperature(year):
    # 读取文件
    if df.empty:
        response = {
            "message": "温度数据为空",
            "code": 400,
            "data": None
        }
        return jsonify(response)

    # 转换为datetime对象
    df['date'] = pd.to_datetime(df['date'], errors='coerce')  # 转换为datetime，并处理无效日期
    # 过滤出指定年份的数据
    filtered_df = df[df['date'].dt.year == year]

    # 如果没有找到数据
    if filtered_df.empty:
        response = {
            "message": f"{year}年的温度数据为空",
            "code": 404,
            "data": None
        }
        return jsonify(response)

    # 转换为指定格式并放入列表
    dates = filtered_df['date'].dt.strftime('%Y年%m月%d日').tolist()

    # 将数据转换为字符串形式
    height_temperature = list(map(str, filtered_df['height_temperature'].tolist()))
    height_history_temperature = list(map(str, filtered_df['height_history_temperature'].tolist()))
    low_temperature = list(map(str, filtered_df['low_temperature'].tolist()))
    low_history_temperature = list(map(str, filtered_df['low_history_temperature'].tolist()))

    # 预测数据
    predicted_height_temperature = list(map(str, filtered_df['height_temperature_predicted'].tolist()))
    predicted_low_temperature = list(map(str, filtered_df['low_temperature_predicted'].tolist()))

    # 将数据放入一个大集合中
    data = {
        'dates': dates,
        'hei_temps': height_temperature,
        'hei_his_temps': height_history_temperature,
        'low_temps': low_temperature,
        'low_his_temps': low_history_temperature,
        'pre_hei_temps': predicted_height_temperature,
        'pre_low_temps': predicted_low_temperature
    }

    response = {
        "message": "温度数据获取成功",
        "code": 200,
        "data": data
    }

    return jsonify(response)



# 查询湿度数据
@app.route("/hum/<int:year>", methods=["GET"])
def get_humidity(year):
    # 读取文件
    if df.empty:
        response = {
            "message": "湿度数据为空",
            "code": 400,
            "data": None
        }
        return response
    # 转换为datetime对象
    df['date'] = pd.to_datetime(df['date'], errors='coerce')  # 转换为datetime，并处理无效日期
    # 过滤出指定年份的数据
    filtered_df = df[df['date'].dt.year == year]

    # 如果没有找到数据
    if filtered_df.empty:
        response = {
            "message": f"{year}年的湿度数据为空",
            "code": 400,
            "data": None
        }
        return jsonify(response)

    dates = filtered_df['date'].dt.strftime('%Y年%m月%d日').tolist()  # 转换为指定格式并放入列表
    humidity = list(map(str, filtered_df['humidity'].tolist()))
    humidity_history = list(map(str, filtered_df['humidity_history'].tolist()))

    predicted_humidity = list(map(str, filtered_df['humidity_predicted'].tolist()))


    data = {
        'dates': dates,
        'hums': humidity,
        'hums_his': humidity_history,
        'pre_hums': predicted_humidity,
    }
    response = {
        "message": "湿度数据获取成功",
        "code": 200,
        "data": data
    }
    return response




# 查询风速数据
@app.route("/wind/<int:year>", methods=["GET"])
def get_wind(year):
    # 读取文件
    if df.empty:
        response = {
            "message": "风速数据为空",
            "code": 400,
            "data": None
        }
        return response

    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    # 过滤出指定年份的数据
    filtered_df = df[df['date'].dt.year == year]

    # 如果没有找到数据
    if filtered_df.empty:
        response = {
            "message": f"{year}年的风速数据为空",
            "code": 400,
            "data": None
        }
        return jsonify(response)

    dates = filtered_df['date'].dt.strftime('%Y年%m月%d日').tolist()  # 转换为指定格式并放入列表

    wind_velocity = list(map(str, filtered_df['wind_velocity'].tolist()))
    wind_velocity_history = list(map(str, filtered_df['wind_velocity_history'].tolist()))


    data = {
        'dates': dates,
        'winds': wind_velocity,
        'winds_his': wind_velocity_history,
    }
    response = {
        "message": "风速数据获取成功",
        "code": 200,
        "data": data
    }
    return response


# 查询降水量数据
@app.route("/preci/<int:year>", methods=["GET"])
def get_preci(year):
    # 读取文件
    if df.empty:
        response = {
            "message": "降水数据为空",
            "code": 400,
            "data": None
        }
        return response

    # 获取参数
    # 获取日期列并转换格式
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    # 过滤出指定年份的数据
    filtered_df = df[df['date'].dt.year == year]

    # 如果没有找到数据
    if filtered_df.empty:
        response = {
            "message": f"{year}年的降水量数据为空",
            "code": 400,
            "data": None
        }
        return jsonify(response)

    dates = filtered_df['date'].dt.strftime('%Y年%m月%d日').tolist()  # 转换为指定格式并放入列表

    preci = list(map(str, filtered_df['precipitation'].tolist()))

    pre_preci = list(map(str, filtered_df['precipitation_predicted'].tolist()))


    data = {
        'dates': dates,
        'preci': preci
    }
    response = {
        "message": "降水量数据获取成功",
        "code": 200,
        "data": data
    }
    return response



if __name__ == "__main__":
    # 静态文件缓存自动刷新
    app.jinja_env.auto_reload = True
    app.run(host="127.0.0.1", port=8002, debug=True)
