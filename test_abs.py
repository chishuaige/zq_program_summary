from flask import Flask, request
import json
import pymysql
import datetime as dt
import time
from script.keywords_tfidf import TFIDF
from script.abstract_tfidf import TFIDF_ABS
import jieba

app = Flask(__name__)


# 预加载jieba
def preloading():
    sentence = '阿拉善当地路桥企业于2020年1-3月份陆续从金和众经销商处购买12台自卸车，此批车辆从4月份开始陆续出现油缸漏油现象'
    _ = [i for i in jieba.cut(sentence)]  # 将sentence分词


# 获取摘要
def get_abstract(text, num):
    abstract_tfidfer = TFIDF_ABS(text, num)
    abstract_list_res = abstract_tfidfer.dic_order_value_and_get_key()
    print(abstract_list_res)
    print('abstract done')
    return abstract_list_res

# step1读取文件
infile = r'E:\重汽代码\质量云文本摘要\新代码\demo_data\demo3.txt'
f = open(infile, encoding='utf-8')
data = f.readlines()  # 直接将文件中按行读到list里，效果与方法2一样
f.close()  # 关
# 将文件转换成字符串
text = ""
for line in data:
    text += line
print('text', text)


def test():
    abstract_tfidfer = TFIDF_ABS(text, 5)
    final_result = abstract_tfidfer.dic_order_value_and_get_key()
    print('final_result', final_result)

test()

