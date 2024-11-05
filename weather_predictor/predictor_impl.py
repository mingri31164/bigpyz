from weather_predictor.predictor_interface import weather_predictor  # 导入weather_predictor接口
import pandas as pd  # 导入pandas库
import numpy as np  # 导入numpy库
from statsmodels.tsa.statespace.sarimax import SARIMAX  # 导入SARIMAX模型
from datetime import datetime, timedelta  # 导入datetime和timedelta类

class predictor_impl(weather_predictor): # 定义predicoctor_impl类，继承自weather_predictor接口
    
    def __init__(self, csv_path: str, predict_period=10):  # 初始化方法，接收一个CSV文件路径作为参数
        super().__init__(csv_path)
        self.df = None
        self.high_temp_model = None
        self.low_temp_model = None
        self.humidity_model = None
        self.precipitation_model = None
        self.predicted_data = None
        self.base_date = None
        
        self.predict_period = predict_period
        
    def set_base_date(self, date_str: str):  # 设置基准日期的方法，接收一个日期字符串作为参数
        """设置基准日期，格式为'MM-dd'"""
        try:
            self.base_date = datetime.strptime(f"{date_str}", "%Y-%m-%d")  # 将日期字符串解析为datetime对象
            return True  # 返回True表示设置成功
        except ValueError as e:
            print(f"日期格式错误: {e}")  # 打印日期格式错误信息
            return False  # 返回False表示设置失败

    def create_predictor_from_csv(self):
        """基于历史相似日期创建预测模型"""
        if self.base_date is None:
            raise ValueError("请先设置基准日期")

        # 读取CSV文件
        self.df = pd.read_csv(self.csv_path)
        self.df['date'] = pd.to_datetime(self.df['date'])
        self.df.set_index('date', inplace=True)

        similar_dates = []
        for year in self.df.index.year.unique():
            date_range_start = (self.base_date.replace(year=year) - timedelta(days=15))
            date_range_end = (self.base_date.replace(year=year) + timedelta(days=15))
            mask = (self.df.index >= date_range_start) & (self.df.index <= date_range_end)
            similar_dates.extend(self.df[mask].index.tolist())

        train_data = self.df[self.df.index.isin(similar_dates)].sort_index()

        # 训练高温模型
        self.high_temp_model = SARIMAX(
            train_data['height_temperature'],
            order=(2, 1, 2),
            seasonal_order=(1, 1, 1, 7),
            enforce_stationarity=False,
            enforce_invertibility=False
        ).fit(disp=False)

        # 训练低温模型
        self.low_temp_model = SARIMAX(
            train_data['low_temperature'],
            order=(2, 1, 2),
            seasonal_order=(1, 1, 1, 7),
            enforce_stationarity=False,
            enforce_invertibility=False
        ).fit(disp=False)

        # 训练湿度模型
        self.humidity_model = SARIMAX(
            train_data['humidity'],  # 使用当前湿度数据
            order=(1, 1, 1),
            seasonal_order=(1, 1, 1, 7),
            enforce_stationarity=False,
            enforce_invertibility=False
        ).fit(disp=False)

        # 训练降水量模型
        self.precipitation_model = SARIMAX(
            train_data['precipitation'],
            order=(2, 0, 2),
            seasonal_order=(1, 1, 1, 7),
            enforce_stationarity=False,
            enforce_invertibility=False
        ).fit(disp=False)

    def predict(self):
        """基于基准日期预测未来10天天气"""
        if any(model is None for model in [self.high_temp_model, self.low_temp_model, 
                                         self.humidity_model, self.precipitation_model]):
            raise ValueError("模型未训练，请先调用 create_predictor_from_csv()")

        future_dates = pd.date_range(start=self.base_date, periods=self.predict_period, freq='D')

        # 预测各个指标
        high_temp_forecast = self.high_temp_model.forecast(steps=self.predict_period)
        low_temp_forecast = self.low_temp_model.forecast(steps=self.predict_period)
        humidity_forecast = self.humidity_model.forecast(steps=self.predict_period)
        precipitation_forecast = self.precipitation_model.forecast(steps=self.predict_period)

        # 处理预测结果
        humidity_forecast = np.clip(humidity_forecast, 0, 100)  # 湿度限制在0-100之间
        precipitation_forecast = np.maximum(precipitation_forecast, 0)  # 降水量不能为负

        # 创建预测结果DataFrame
        self.predicted_data = pd.DataFrame({
            'date': future_dates.strftime('%Y-%m-%d'),
            'height_temperature_predicted': np.round(high_temp_forecast, 1),
            'low_temperature_predicted': np.round(low_temp_forecast, 1),
            'humidity_predicted': np.round(humidity_forecast, 1),
            'precipitation_predicted': np.round(precipitation_forecast, 1)
        })

        return self.predicted_data

    def predicton_data_saver(self):
        """保存预测结果到CSV文件"""
        if self.predicted_data is None:
            raise ValueError("没有预测数据，请先调用 predict()")

        output_path = self.csv_path.replace('all_in_one_processed.csv', 'all_predicted.csv')
        self.predicted_data.to_csv(output_path, index=False)
        print(f"预测结果已保存到: {output_path}")


# # 使用示例
# if __name__ == "__main__":
#     predictor = predicoctor_impl("all_in_one_processed.csv",20)  # 使用新的CSV文件路径
    
#     predictor.set_base_date("2024-07-15")
#     predictor.create_predictor_from_csv()
    
#     predicted_data = predictor.predict()
#     predictor.predicton_data_saver()
    
#     print("预测结果预览：")
#     print(predicted_data)
