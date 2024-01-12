# 项目名称：数字供应链创新技术与应用研究V1.0 - 四川省科技计划项目（重点研发项目）2022YFG0159数字供应链创新技术与应用研究
# 创建：2023-12-25
# 更新：2024-01-04
# 用意：准确度计算

import json

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import re

import jieba
import glob
import os

image_base_path = '../'


def load_json_file(file_path):
    """加载JSON文件并返回内容"""
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)


def extract_text_from_combined_json(file_path):
    """从combined_texts.json文件中提取所有条目的text字段"""
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # 提取'res'列表中每个字典的'text'字段
    texts = [item['text'] for item in data['res']]

    # 返回合并后的文本字符串
    return ' '.join(texts)


def extract_text_from_zh_val_json(file_path):
    """提取zh.val.json文件中的所有text内容"""
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    texts = []
    for document in data['documents']:
        for item in document['document']:
            texts.append(item['text'])

    # 返回合并后的文本字符串
    return ' '.join(texts)

def preprocess_text_chinese(text):
    """对中文文本进行预处理"""
    # 使用 jieba 进行分词
    words = jieba.cut(text)
    # 移除中文标点符号
    text = re.sub(r'[^\w\s]', '', ' '.join(words))
    # 移除停用词（此处需要提供中文停用词列表）
    # 停用词列表可以自行在网上找到，或者根据需求自定义
    stop_words = set(['的', '了', '在', '是', '我', '有', '和', '就'])  # 示例，实际应更全面
    return ' '.join([word for word in text.split() if word not in stop_words])

def calculate_tfidf_similarity(text1, text2):
    """计算两个文本基于TF-IDF加权的余弦相似度"""
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([text1, text2])
    vector1, vector2 = vectors.toarray()
    return cosine_similarity([vector1], [vector2])[0, 0]


# 加载两个JSON文件
file_path1 = '../result/combined_texts.json'
file_path2 = '../result/zh.train.json'

# 提取并合并文本
text1 = extract_text_from_combined_json(file_path1)
text2 = extract_text_from_zh_val_json(file_path2)

# 应用预处理
preprocessed_text1 = preprocess_text_chinese(text1)
preprocessed_text2 = preprocess_text_chinese(text2)

#打印比较的文件名称以及所用的样本总数
file_pattern = os.path.join(image_base_path, 'zh_train_*.jpg')
file_list = glob.glob(file_pattern)

file_list.sort(key=lambda f: int(os.path.splitext(os.path.basename(f))[0].split('_')[2]))

for filepath in file_list:
    print(os.path.basename(filepath))

print(f"样本总数{len(file_list)}")

# 计算相似度
similarity_percentage = calculate_tfidf_similarity(preprocessed_text1, preprocessed_text2) * 100
print(f"文本相似度: {similarity_percentage:.2f}%")

input("按回车键退出...")