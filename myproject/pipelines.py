# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import csv

# 保存数据的类
class MyprojectPipeline:
    def __init__(self):
        self.temp_fields = ['date', 'height_temperature', 'low_temperature', 'height_history_temperature', 'low_history_temperature']
        self.hum_fields = ['date', 'humidity', 'humidity_history']
        self.pre_fields = ['date', 'precipitation']
        self.wind_fields = ['date', 'wind_velocity', 'wind_velocity_history']
        
    def open_spider(self, spider):
        # 打开四个CSV文件
        self.temp_file = open('temperature.csv', 'w', newline='', encoding='utf-8')
        self.hum_file = open('humidity.csv', 'w', newline='', encoding='utf-8')
        self.pre_file = open('precipitation.csv', 'w', newline='', encoding='utf-8')
        self.wind_file = open('wind_velocity.csv', 'w', newline='', encoding='utf-8')
        
        # 创建csv.writer实例
        self.temp_writer = csv.writer(self.temp_file)
        self.hum_writer = csv.writer(self.hum_file)
        self.pre_writer = csv.writer(self.pre_file)
        self.wind_writer = csv.writer(self.wind_file)
        
        # 写入标题行
        self.temp_writer.writerow(self.temp_fields)
        self.hum_writer.writerow(self.hum_fields)
        self.pre_writer.writerow(self.pre_fields)
        self.wind_writer.writerow(self.wind_fields)

    def close_spider(self, spider):
        # 关闭文件
        self.temp_file.close()
        self.hum_file.close()
        self.pre_file.close()
        self.wind_file.close()

    def process_item(self, item, spider):
        # 将所有字段值转换为字符串
        for field in item:
            if field in item:
                item[field] = str(item[field])
        
        print(f"item的值: {item}")
        
        # 检查项目是否包含温度相关字段，并且写入温度CSV文件
        if all(field in item for field in self.temp_fields):
            self.temp_writer.writerow([item[field] for field in self.temp_fields])
        
        # 检查项目是否包含湿度相关字段，并且写入湿度CSV文件
        if all(field in item for field in self.hum_fields):
            self.hum_writer.writerow([item[field] for field in self.hum_fields])
        
        # 检查项目是否包含降水量相关字段，并且写入降水量CSV文件
        if all(field in item for field in self.pre_fields):
            self.pre_writer.writerow([item[field] for field in self.pre_fields])
        
        # 检查项目是否包含风速相关字段，并且写入风速CSV文件
        if all(field in item for field in self.wind_fields):
            self.wind_writer.writerow([item[field] for field in self.wind_fields])
        
        return item