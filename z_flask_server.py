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
                    filename=os.path.join(base_path, 'new.log'),
                    filemode='a',  ##模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志 #a是追加模式，默认如果不写的话，就是追加模式
                    format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'  # 日志格式
                    )


app = Flask(__name__)


# 预加载jieba
def preloading():
    sentence = '阿拉善当地路桥企业于2020年1-3月份陆续从金和众经销商处购买12台自卸车，此批车辆从4月份开始陆续出现油缸漏油现象'
    _ = [i for i in jieba.cut(sentence)]  # 将sentence分词


preloading()


# 使用python连接mysql数据库，并对数据库添加数据的数据的操作
# 创建连接，数据库主机地址 数据库用户名称 密码 数据库名 数据库端口 数据库字符集编码
def connect_mysql():
    global conn
    global cursor
    conn = pymysql.connect(host='10.100.111.24',
                           user='finebi',
                           password='fine%TGB',
                           database='finebi_data',
                           port=3306,
                           charset='utf8')
    if conn:
        logging.info('连接成功')

    # 创建游标
    cursor = conn.cursor()


def selectdata(user_id):
    # 查找数据
    # sql_str = 'select * from finebi_data.finebi_fill_disposalmx_df limit 20'
    # user_id = '079685'
    sql_str = f'select * from finebi_data.finebi_fill_disposalmx_df where create_time= (select update_time from (select emp_no,max(create_time) as update_time from finebi_data.finebi_fill_disposalmx_df where emp_no = {user_id} group by emp_no) a )'
    cursor.execute(sql_str)
    # 接收返回结果
    input_data = cursor.fetchall()
    # print(input_data)
    # print(type(input_data))
    content_list = []
    for i in input_data:
        if i[2] != None:
            content_list.append(i[2])
    # print(content_list)
    text = '\n'.join(content_list)
    # print("select done")
    logging.info('select done')
    return text


# ==========================================添加示例数据==========================================
def insertdata_demo():
    # (('077069', datetime.datetime(2024, 4, 15, 11, 17, 24), '第一次保养换全车油'), ('077069', datetime.datetime(2024, 4, 15, 11, 17, 24), '第一次保养换全车油')
    # 添加单条数据
    value_str = "('077069', '2024-04-15 15:03:29', '文本摘要','文本关键词')"
    insert_emp_sql_command = "INSERT INTO `finebi_fill_disposalsc_df` (`emp_no`, `create_time`, `disposalsc`, `keywordsc`) VALUES "
    insert_emp_sql_single = insert_emp_sql_command + value_str
    # print(insert_emp_sql_single)
    logging.info(insert_emp_sql_single)
    # 执行语句
    cursor.execute(insert_emp_sql_single)
    # 提交数据
    conn.commit()
    # print("insert done")
    logging.info("insert done")


def insertdata(user_id, keyword_list_res_noweight, keyword_list_res_weight, abstract_list_res):
    keyword_list_res1 = ',\t'.join(keyword_list_res_noweight)
    keyword_list_res2 = '\n'.join(keyword_list_res_weight)
    keyword_list_res = '不带权重：' + keyword_list_res1 + '\n' + '带权重：\n' + keyword_list_res2
    print('keyword_list_res', keyword_list_res)
    logging.info(keyword_list_res)
    abstract_res = '\n'.join(abstract_list_res)
    current_time = datetime.datetime.now()
    formatted_time = str(current_time.strftime("%Y-%m-%d %H:%M:%S"))
    value_str = f"('{user_id}', '{formatted_time}', '{abstract_res}','{keyword_list_res}')"
    insert_emp_sql_command = "INSERT INTO `finebi_fill_disposalsc_df` (`emp_no`, `create_time`, `disposalsc`, `keywordsc`) VALUES "
    insert_emp_sql_single = insert_emp_sql_command + value_str
    # print(insert_emp_sql_single)
    # 执行语句
    cursor.execute(insert_emp_sql_single)
    # 提交数据
    conn.commit()
    print("insert done")
    logging.info("insert done")


# 获取关键词 默认只获取名词
def get_keyword(text):
    kewords_tfidfer = TFIDF()
    keyword_list = kewords_tfidfer.extract_keywords(text, 20)
    keyword_list_res_noweight = [i[0] for i in keyword_list]
    keyword_list_res_weight = [(i[0] + ',' + str(i[1])) for i in keyword_list]
    # print(keyword_list_res_noweight)
    # print(keyword_list_res_weight)
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


def handle_process(user_id, abs_num):
    print('server start')
    logging.info("server start")
    # step0 每次都重连服务器
    connect_mysql()
    # step1 从gbase数据表获取数据
    text = selectdata(user_id)
    # step2 经过模型，返回输出
    # 获取关键词         ##默认只获取名词，数量20
    keyword_list_res_noweight, keyword_list_res_weight = get_keyword(text)

    # 获取摘要          ##  默认输出数量5
    abstract_list_res = get_abstract(text, abs_num)

    # step3 将结果输出到gbase新表
    insertdata(user_id, keyword_list_res_noweight,keyword_list_res_weight, abstract_list_res)
    # step4 返回服务结果
    res_total_out = True
    print('server end')
    logging.info("server end")
    return res_total_out


@app.route("/hello", methods=["post"])
def hello():
    print('hello')
    return json.dumps('hello ok')


@app.route("/", methods=["post", "get"])
def run():
    size = request.get_json()
    # {'size': 5, 'emp_no': '079685'}
    abs_num = size['size']
    user_id = size['emp_no']
    print('abs_num', abs_num)
    print('user_id', user_id)

    try:
        start_t = time.time()
        res_total_out = handle_process(user_id, abs_num)
        end_t = time.time()
        print('响应时间', end_t-start_t)
        print(res_total_out)
    except Exception as e:
        print(e)
        logging.info(e)
        res_total_out = False
    print(res_total_out)
    logging.info(res_total_out)
    return json.dumps(res_total_out)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8081)
