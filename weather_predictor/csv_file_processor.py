import csv
import os
from datetime import datetime

class processor:
    def __init__(self, file_path):
        self.file_relative_path = file_path
        self.csv_prefix = ["temperature", "humidity", "precipitation", "wind_velocity"]
        self.csv_suffix = "_predicted"
        self.csv_processed = "all_in_one_processed"
        self.csv_predicted = "all_in_one_predicted"
    
    def processed_csv(self):
        if not self.file_relative_path == "":
            if os.path.exists(os.path.join(self.file_relative_path, f"result\\{self.csv_prefix[0]}.csv")):
                
                # 用于存储所有文件的数据
                all_files_data = []
                all_headers = []

                # 读取所有文件的内容
                for prefix in self.csv_prefix:
                    file_path = os.path.join(self.file_relative_path, f"result\\{prefix}.csv")
                    with open(file_path, 'r') as csvfile:
                        reader = csv.reader(csvfile)
                        # 读取表头
                        headers = next(reader)
                        # 如果不是第一个文件，去掉date列
                        if all_headers:
                            headers = headers[1:]  # 跳过date列
                        all_headers.extend(headers)

                        # 如果是第一个文件，保存完整数据；否则，跳过date列
                        if not all_files_data:
                            file_data = list(reader)
                            all_files_data.append(file_data)
                        else:
                            file_data = []
                            for row in reader:
                                file_data.append(row[1:])  # 跳过date列
                            all_files_data.append(file_data)

                # 合并数据并添加日期
                merged_data = []
                rows_count = len(all_files_data[0])

                for row_idx in range(rows_count):
                    merged_row = []
                    # 添加第一个文件的所有列（包括日期）
                    merged_row.extend(all_files_data[0][row_idx])
                    # 添加其他文件的非日期列
                    for file_idx in range(1, len(all_files_data)):
                        merged_row.extend(all_files_data[file_idx][row_idx])
                    merged_data.append(merged_row)

                # 按日期倒序排序
                merged_data.sort(key=lambda x: datetime.strptime(x[0], '%Y-%m-%dT%H:%M:%S'), reverse=False)

                # 写入合并后的CSV文件
                output_path = os.path.join(self.file_relative_path, f"result/{self.csv_processed}.csv")
                with open(output_path, 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    # 写入表头
                    writer.writerow(all_headers)
                    # 写入排序后的数据，处理日期格式
                    for row in merged_data:
                        # 将日期格式从 "2023-01-01T00:00:00" 转换为 "2023-01-01"
                        row[0] = row[0].split('T')[0]
                        writer.writerow(row)
            else:
                print(f"原始数据{self.csv_processed}.csv不存在")
            
            
            
    def predicted_csv(self):
        if not self.file_relative_path == "" and os.path.exists(os.path.join(self.file_relative_path, f"result\\{self.csv_processed}.csv")):
            processed_file = os.path.join(self.file_relative_path, f"result\\{self.csv_processed}.csv")
            predicted_file = os.path.join(self.file_relative_path, f"result\\all{self.csv_suffix}.csv")
            output_file = os.path.join(self.file_relative_path, f"result\\{self.csv_predicted}.csv")

            # 读取原始数据，使用日期作为键创建字典
            original_data = {}
            with open(processed_file, 'r') as csvfile:
                reader = csv.DictReader(csvfile)
                original_headers = reader.fieldnames
                for row in reader:
                    original_data[row['date']] = row

            # 创建新的表头：原表头 + 预测列
            new_headers = original_headers + [
                'height_temperature_predicted',
                'low_temperature_predicted',
                'humidity_predicted',
                'precipitation_predicted'
            ]

            # 读取预测数据并合并到原始数据中
            with open(predicted_file, 'r') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    date = row['date']
                    # 如果这个日期已经存在，就更新预测数据
                    if date in original_data:
                        original_data[date].update({
                            'height_temperature_predicted': row['height_temperature_predicted'],
                            'low_temperature_predicted': row['low_temperature_predicted'],
                            'humidity_predicted': row['humidity_predicted'],
                            'precipitation_predicted': row['precipitation_predicted']
                        })
                    else:
                        # 如果是新日期，创建新行，原始数据列为空
                        new_row = {header: '' for header in original_headers}
                        new_row['date'] = date
                        new_row.update({
                            'height_temperature_predicted': row['height_temperature_predicted'],
                            'low_temperature_predicted': row['low_temperature_predicted'],
                            'humidity_predicted': row['humidity_predicted'],
                            'precipitation_predicted': row['precipitation_predicted']
                        })
                        original_data[date] = new_row

            # 按日期排序并写入输出文件
            with open(output_file, 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=new_headers)
                writer.writeheader()

                # 将字典转换为列表并按日期排序
                sorted_data = sorted(original_data.values(), 
                                   key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d'))

                # 写入所有数据
                for row in sorted_data:
                    # 确保所有预测列都存在，如果不存在则设为空字符串
                    for header in new_headers:
                        if header not in row:
                            row[header] = ''
                    writer.writerow(row)
            print(f"所有数据(包含预测)已保存到: {output_file}")
                    
# # 使用示例
# if __name__ == "__main__":
#     file_path = "C:\\Users\\Administrator\\Desktop\\bigpyz"
#     proc = processor(file_path)
#     proc.processed_csv()  # 首先处理原始数据
#     proc.predicted_csv()  # 然后添加预测数据