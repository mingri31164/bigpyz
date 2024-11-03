from predictor_interface import weather_predictor  # 导入weather_predictor接口
import pandas as pd  # 导入pandas库
import numpy as np  # 导入numpy库
from statsmodels.tsa.statespace.sarimax import SARIMAX  # 导入SARIMAX模型
from datetime import datetime, timedelta  # 导入datetime和timedelta类

class predicoctor_impl(weather_predictor): # 定义predicoctor_impl类，继承自weather_predictor接口
    def __init__(self, csv_path: str):  # 构造函数，接收一个csv文件路径作为参数
        super().__init__(csv_path)  # 调用父类的构造函数
        self.df = None  # 初始化df属性为空
        self.high_temp_model = None  # 初始化high_temp_model属性为空
        self.low_temp_model = None  # 初始化low_temp_model属性为空
        self.predicted_data = None  # 初始化predicted_data属性为空
        self.base_date = None  # 初始化base_date属性为空，用于存储基准日期
    
    def set_base_date(self, date_str: str):  # 设置基准日期的方法，接收一个日期字符串作为参数
        """设置基准日期，格式为'MM-dd'"""
        try:
            self.base_date = datetime.strptime(f"{date_str}", "%Y-%m-%d")  # 将日期字符串解析为datetime对象
            return True  # 返回True表示设置成功
        except ValueError as e:
            print(f"日期格式错误: {e}")  # 打印日期格式错误信息
            return False  # 返回False表示设置失败
    
    def create_predictor_from_csv(self):  # 基于历史相似日期创建预测模型的方法
        """基于历史相似日期创建预测模型"""
        if self.base_date is None:  # 如果基准日期为空
            raise ValueError("请先设置基准日期")  # 抛出ValueError异常，提示先设置基准日期

        self.df = pd.read_csv(self.csv_path)  # 读取CSV文件到DataFrame对象
        self.df['date'] = pd.to_datetime(self.df['date'])  # 将'date'列转换为日期类型
        self.df.set_index('date', inplace=True)  # 将'date'列设置为索引

        similar_dates = []  # 存储相似日期的列表
        for year in self.df.index.year.unique():  # 遍历数据中的每个年份
            date_range_start = (self.base_date.replace(year=year) - timedelta(days=15))  # 计算基准日期前15天的日期
            date_range_end = (self.base_date.replace(year=year) + timedelta(days=15))  # 计算基准日期后15天的日期
            mask = (self.df.index >= date_range_start) & (self.df.index <= date_range_end)  # 创建布尔掩码，筛选出在日期范围内的数据
            similar_dates.extend(self.df[mask].index.tolist())  # 将符合条件的日期添加到similar_dates列表中

        train_data = self.df[self.df.index.isin(similar_dates)].sort_index()  # 根据相似日期筛选出的数据进行训练

        self.high_temp_model = SARIMAX(
            train_data['height_temperature'],  # 使用高温数据训练模型
            order=(2, 1, 2),  # SARIMA模型的阶数参数
            seasonal_order=(1, 1, 1, 7),  # SARIMA模型的季节性阶数参数
            enforce_stationarity=False,  # 不强制稳定性
            enforce_invertibility=False  # 不强制可逆性
        ).fit(disp=False)  # 拟合模型

        self.low_temp_model = SARIMAX(
            train_data['low_temperature'],  # 使用低温数据训练模型
            order=(2, 1, 2),  # SARIMA模型的阶数参数
            seasonal_order=(1, 1, 1, 7),  # SARIMA模型的季节性阶数参数
            enforce_stationarity=False,  # 不强制稳定性
            enforce_invertibility=False  # 不强制可逆性
        ).fit(disp=False)  # 拟合模型
        
    def predict(self):  # 预测未来10天温度的方法
        """基于基准日期预测未来10天温度"""
        if self.high_temp_model is None or self.low_temp_model is None:  # 如果模型未训练
            raise ValueError("模型未训练，请先调用 create_predictor_from_csv()")  # 抛出ValueError异常，提示先调用create_predictor_from_csv()方法

        future_dates = pd.date_range(start=self.base_date, periods=10, freq='D')  # 生成未来10天的日期范围

        high_temp_forecast = self.high_temp_model.forecast(steps=10)  # 预测未来10天的高温
        low_temp_forecast = self.low_temp_model.forecast(steps=10)  # 预测未来10天的低温

        self.predicted_data = pd.DataFrame({  # 创建预测结果DataFrame
            'date': future_dates.strftime('%Y-%m-%d'),  # 日期列
            'height_temperature': np.round(high_temp_forecast, 1),  # 高温列
            'low_temperature': np.round(low_temp_forecast, 1),  # 低温列
            'height_history_temperature': '',  # 空值列
            'low_history_temperature': ''  # 空值列
        })

        return self.predicted_data  # 返回预测结果

    def predicton_data_saver(self):  # 保存预测结果到CSV文件的方法
        """保存预测结果到CSV文件"""
        if self.predicted_data is None:  # 如果没有预测数据
            raise ValueError("没有预测数据，请先调用 predict()")  # 抛出ValueError异常，提示先调用predict()方法
    
        output_path = self.csv_path.replace('.csv', '_predicted.csv')  # 生成输出文件名

        self.predicted_data.to_csv(output_path, index=False)  # 将预测结果保存到CSV文件
        print(f"预测结果已保存到: {output_path}")  # 打印保存成功的信息
    
    
# 使用示例
if __name__ == "__main__":
    predictor = predicoctor_impl("C:\\Users\\Administrator\\Desktop\\bigpyz\\temperature.csv")  # 创建预测器对象，传入CSV文件路径
    
    predictor.set_base_date("2024-07-15")  # 设置基准日期
    predictor.create_predictor_from_csv()  # 创建预测模型
    
    predicted_data = predictor.predict()  # 进行预测
    predictor.predicton_data_saver()  # 保存预测结果到CSV文件
    
    print("预测结果预览：")
    print(predicted_data)  # 打印预测结果
