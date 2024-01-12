# 项目名称：数字供应链创新技术与应用研究V1.0 - 四川省科技计划项目（重点研发项目）2022YFG0159数字供应链创新技术与应用研究
# 创建：2023-12-25
# 更新：2024-01-04
# 用意：将OCR返回的结果合并用于相似度计算


import json
import os

def load_json_file(file_path):
    """加载JSON文件并返回内容"""
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def combine_json_files(directory):
    """合并目录中的所有JSON文件中的对象到一个新的列表"""
    combined_res = []
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            file_path = os.path.join(directory, filename)
            data = load_json_file(file_path)
            # 假设每个文件的内容是一个字典，包含一个名为'res'的列表
            for item in data['res']:
                combined_res.append(item)
    return combined_res

# 文件夹路径
json_files_directory = '../'

# 合并文件夹中所有JSON文件的内容
combined_res = combine_json_files(json_files_directory)

# 最终的JSON结构
final_json_structure = {
    "res": combined_res
}

# 保存合并后的数据到一个新的JSON文件
output_file_path = '../result/combined_texts.json'
with open(output_file_path, 'w', encoding='utf-8') as output_file:
    json.dump(final_json_structure, output_file, ensure_ascii=False, indent=4)

print(f"合并的文件已保存到：{output_file_path}")

