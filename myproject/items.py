# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class TemperatureItem(scrapy.Item):
    # 温度相关的字段
    date = scrapy.Field()
    height_temperature = scrapy.Field()
    low_temperature = scrapy.Field()
    height_history_temperature = scrapy.Field()
    low_history_temperature = scrapy.Field()

class HumidityItem(scrapy.Item):
    # 湿度相关的字段
    date = scrapy.Field()
    humidity = scrapy.Field()
    humidity_history = scrapy.Field()

class PrecipitationItem(scrapy.Item):
    # 降水量相关的字段
    date = scrapy.Field()
    precipitation = scrapy.Field()

class WindVelocityItem(scrapy.Item):
    # 风速相关的字段
    date = scrapy.Field()
    wind_velocity = scrapy.Field()
    wind_velocity_history = scrapy.Field()

    
    
