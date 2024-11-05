import os
from weather_predictor.csv_file_processor import processor
from weather_predictor.predictor_impl import predictor_impl
from datetime import datetime

def get_user_input(prompt, valid_responses=None):
    """
    获取用户输入并验证

    Args:
        prompt (str): 提示用户输入的消息
        valid_responses (list, optional): 有效的响应列表. Defaults to None.

    Returns:
        str: 用户输入的响应

    Raises:
        None

    """
    while True:
        response = input(prompt).strip().lower()
        if valid_responses is None or response in valid_responses:
            return response
        print(f"无效输入，请输入: {'/'.join(valid_responses)}")


def get_file_path():
    """自动获取项目根目录"""
    current_file = os.path.abspath(__file__)
    path_parts = current_file.split(os.sep)
    
    try:
        # 注意这里改成小写的 'bigpyz'
        bigpyz_index = path_parts.index('bigpyz')
        root_dir = os.sep.join(path_parts[:bigpyz_index + 1])
        return root_dir
    except ValueError:
        return os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(current_file))))

def run_prediction(file_path):
    """运行预测流程"""
    try:
       
        # 获取预测起始日期
        while True:
            date_str = input("请输入预测起始日期 (格式: YYYY-MM-DD): ").strip()
            period = input("请输入预测天数 (默认10): ").strip()
            try:
                period = int(period)
                datetime.strptime(date_str, "%Y-%m-%d")                
                break
            except ValueError:
                print("日期格式错误，请使用 YYYY-MM-DD 格式")
                
         # 初始化处理器
        proc = processor(file_path)
        
        # 创建预测器并运行预测
        predictor = predictor_impl(os.path.join(file_path, "all_in_one_processed.csv"), period)
              
                
                
        
        predictor.set_base_date(date_str)
        predictor.create_predictor_from_csv()
        predictor.predict()
        predictor.predicton_data_saver()
        
        # 处理预测数据
        proc.predicted_csv()
        
    except Exception as e:
        print(f"预测过程出错: {str(e)}")
        return False
    return True

def start_all(start_scrapy):    # 终极方法, 一切的开始
    try:
        # 获取文件路径
        file_path = get_file_path()
        if not os.path.exists(file_path):
            print(f"错误：路径 {file_path} 不存在")
            return

        temperature_file = os.path.join(file_path, "temperature.csv")
        data_exists = os.path.exists(temperature_file)

        # 确定是否需要爬取数据
        need_crawl = False
        if not data_exists:
            print("原始爬虫数据不存在")
            need_crawl = get_user_input("是否启动爬虫? (y/n): ", ['y', 'n']) == 'y'
            if not need_crawl:
                print("请先启动爬虫")
                return
        else:
            print("原始爬虫数据已存在")
            need_crawl = get_user_input("是否重新爬取数据? (y/n): ", ['y', 'n']) == 'y'

        # 爬虫流程
        if need_crawl:
            try:
                # 在这里添加爬虫代码
                start_scrapy()
                print("爬虫执行完成")
            except Exception as e:
                print(f"爬虫过程出错: {str(e)}")
                return

        # 数据处理流程
        if get_user_input("是否启动数据处理? (y/n): ", ['y', 'n']) == 'y':
            try:
                proc = processor(file_path)
                proc.processed_csv()
                print("数据处理完成")
            except Exception as e:
                print(f"数据处理出错: {str(e)}")
                return

            # 预测流程
            if get_user_input("是否启动天气预测? (y/n): ", ['y', 'n']) == 'y':
                if run_prediction(file_path):
                    print("全部流程执行完成")
                else:
                    print("预测流程执行失败")
            else:
                print("天气数据已保存到all_in_one_processed.csv, 但未进行预测")
        else:
            if os.path.join(file_path, "all_in_one_processed.csv"):
                if get_user_input("处理后的数据已存在, 是否进行预测? (y/n): ", ['y', 'n']) == 'y':
                    if run_prediction(file_path):
                        print("全部流程执行完成")
                    else:
                        print("预测流程执行失败")
                else:
                    print("天气数据已保存到all_in_one_processed.csv, 但未进行预测")
            else:
                print("处理后的数据不存在, 结束")
    except Exception as e:
        print(f"程序执行出错: {str(e)}")

# if __name__ == "__main__":
#     start_all()
    
# 调用顺序：
# 1.爬虫
# 2.csv_file_processor.py->processed_csv()
# 3.predicoctor_impl.py
# 4.csv_file_processor.py->predicted_csv()
