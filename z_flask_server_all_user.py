from flask import Flask, request
import os
import json
import pymysql
import datetime
import time
from script.keywords_tfidf import TFIDF
from script.abstract_tfidf import TFIDF_ABS
import jieba
import logging

base_path = os.path.abspath(os.path.dirname(__file__))
logging.basicConfig(level=logging.DEBUG,  # 控制台打印的日志级别
                    filename=os.path.join(base_path, 'all_user.log'),
                    filemode='a',  ##模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志 #a是追加模式，默认如果不写的话，就是追加模式
                    format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'  # 日志格式
                    )

app = Flask(__name__)


# 预加载jieba
def preloading():
    sentence = '阿拉善当地路桥企业于2020年1-3月份陆续从金和众经销商处购买12台自卸车，此批车辆从4月份开始陆续出现油缸漏油现象'
    _ = [i for i in jieba.cut(sentence)]  # 将sentence分词


preloading()


# 获取关键词 默认只获取名词
def get_keyword(text):
    kewords_tfidfer = TFIDF()
    keyword_list = kewords_tfidfer.extract_keywords(text, 20)
    keyword_list_res_noweight = [i[0] for i in keyword_list]
    keyword_list_res_weight = [(i[0] + ',' + str(i[1])) for i in keyword_list]
    print('keyword done')
    logging.info("keyword done")
    return keyword_list_res_noweight, keyword_list_res_weight


# 获取摘要
def get_abstract(text, num):
    abstract_tfidfer = TFIDF_ABS(text, num)
    abstract_list_res = abstract_tfidfer.dic_order_value_and_get_key()
    print(abstract_list_res)
    print('abstract done')
    logging.info("abstract done")
    return abstract_list_res


def handle_process(abstract_num, input_content):
    # size = {'abstract_num': 5, 'input_content': 'xxxxx'}
    #     abstract_num = size['abstract_num']
    #     input_content = size['input_content']
    logging.info("server start")
    # step2 经过模型，返回输出
    # 获取关键词         ##默认只获取名词，数量20
    keyword_list_res_noweight, keyword_list_res_weight = get_keyword(input_content)
    # 获取摘要          ##  默认输出数量5
    abstract_list_res = get_abstract(input_content, abstract_num)
    logging.info("server end")
    # print('keyword_list_res_weight', keyword_list_res_weight)
    # print('abstract_list_res', abstract_list_res)
    return keyword_list_res_weight, abstract_list_res


# abstract_num = 2
# input_content = '''（原标题：央视独家采访：陕西榆林产妇坠楼事件在场人员还原事情经过）
# 央视新闻客户端11月24日消息，2017年8月31日晚，在陕西省榆林市第一医院绥德院区，产妇马茸茸在待产时，从医院五楼坠亡。事发后，医院方面表示，由于家属多次拒绝剖宫产，最终导致产妇难忍疼痛跳楼。但是产妇家属却声称，曾向医生多次提出剖宫产被拒绝。
# 事情经过究竟如何，曾引起舆论纷纷，而随着时间的推移，更多的反思也留给了我们，只有解决了这起事件中暴露出的一些问题，比如患者的医疗选择权，人们对剖宫产和顺产的认识问题等，这样的悲剧才不会再次发生。央视记者找到了等待产妇的家属，主治医生，病区主任，以及当时的两位助产师，一位实习医生，希望通过他们的讲述，更准确地还原事情经过。
# 产妇待产时坠亡，事件有何疑点。公安机关经过调查，排除他杀可能，初步认定马茸茸为跳楼自杀身亡。马茸茸为何会在医院待产期间跳楼身亡，这让所有人的目光都聚焦到了榆林第一医院，这家在当地人心目中数一数二的大医院。
# 就这起事件来说，如何保障患者和家属的知情权，如何让患者和医生能够多一份实质化的沟通？这就需要与之相关的法律法规更加的细化、人性化并且充满温度。用这种温度来消除孕妇对未知的恐惧，来保障医患双方的权益，迎接新生儿平安健康地来到这个世界。'''
# handle_process(abstract_num, input_content)


@app.route("/hello", methods=["post"])
def hello():
    print('hello')
    return json.dumps('hello ok')


@app.route("/", methods=["post", "get"])
def run():
    size = request.get_json()
    # {'abstract_num': 5, 'input_content': 'xxxxx'}
    abstract_num = size['abstract_num']
    input_content = size['input_content']

    try:
        start_t = time.time()
        keyword_list_res_weight, abstract_list_res = handle_process(abstract_num, input_content)
        res_out = {'errmsg': 'ok', 'keyword_res': keyword_list_res_weight, 'abstract_res': abstract_list_res}
        end_t = time.time()
        print('响应时间', end_t - start_t)
        print(res_out)
        return json.dumps(res_out)
    except Exception as e:
        logging.info(e)
        res_out = {'errmsg': 'error'}
        return json.dumps(res_out)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8080)
