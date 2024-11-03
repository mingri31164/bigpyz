class weather_predictor:  
    def __init__(self, csv_path:str):
        
        self.csv_prefix = ["temperature_processed", "humidity_processed", "precipitation_processed", "wind_velocity_processed"]
        self.csv_path = csv_path
        self.date = "1970-01-01"
        self.height_temperature = 0  # 最高温度
        self.low_temperature = 0 # 最低温度
        self.height_temperature_history = 0 # 历史最高温度
        self.low_temperature_history = 0 # 历史最低温度
        self.humidity = 0  # 湿度
        self.humidity_history = 0  # 历史湿度
        self.precipitation = 0  # 降水量
        self.wind_velocity = 0  # 风速
        self.wind_velocity_history = 0  # 历史风速
    
    def read_data_from_csv(self):
        pass
    
    
    def predict(self):
        pass
    
    def predicton_data_saver(self):
        pass