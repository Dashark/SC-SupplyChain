# 项目名称：数字供应链创新技术与应用研究V1.0 - 四川省科技计划项目（重点研发项目）2022YFG0159数字供应链创新技术与应用研究
# 创建：2023-12-25
# 更新：2024-01-04
# 用意：获取OCR的返回内容并保存

import requests
import base64
import json
import os

# OCR服务的URL
ocr_api_url = 'http://182.92.66.252:8080/ocr'  # 实际的OCR服务URL

# 图片的基础路径和文件名格式
image_base_path = '../'
image_name_pattern = 'zh_train_{}.jpg'  # 图片命名格式

# 要处理的图片数量
number_of_images = 149  # 如果您有10张图片，例如


# 将图片转换为BASE64编码的函数
def image_to_base64(image_path):
    with open(image_path, 'rb') as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return encoded_string


# 发送图片并获取OCR识别结果的函数
def get_ocr_result(image_base64, api_url):
    data = {
        "imgString": image_base64,
        # ... 添加其他需要的字段 ...
    }
    response = requests.post(api_url, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"请求失败，状态码：{response.status_code}")


# 循环处理图片
# 循环处理图片
for i in range(number_of_images):
    image_path = os.path.join(image_base_path, image_name_pattern.format(i))
    image_base64 = image_to_base64(image_path)
    ocr_result = get_ocr_result(image_base64, ocr_api_url)

    # 为每张图片的OCR结果创建一个单独的JSON文件
    json_file_path = os.path.join(image_base_path, f"zh_train_{i}_recognized_text.json")

    # 将识别的文本保存到JSON文件
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(ocr_result, json_file, ensure_ascii=False, indent=4)