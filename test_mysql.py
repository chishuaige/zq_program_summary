from flask import Flask, request
import pymysql
import time
import datetime as dt
# from script.abstract_tfidf import TFIDF_ABS

app = Flask(__name__)

# 使用python连接mysql数据库，并对数据库添加数据的数据的操作
# 创建连接，数据库主机地址 数据库用户名称 密码 数据库名 数据库端口 数据库字符集编码
conn = pymysql.connect(host='10.100.111.24',
                       user='finebi',
                       password='fine%TGB',
                       database='finebi_data',
                       port=3306,
                       charset='utf8')
if conn:
    print("连接成功")

# 创建游标
cursor = conn.cursor()


def selectdata():
    # 查找数据
    # sql_str = 'select * from finebi_data.finebi_fill_disposalmx_df limit 20'
    user_id = "079685"
    sql_str = f'select * from finebi_data.finebi_fill_disposalmx_df where create_time= (select update_time from (select emp_no,max(create_time) as update_time from finebi_data.finebi_fill_disposalmx_df where emp_no = {user_id} group by emp_no) a )'

    cursor.execute(sql_str)
    # 接收返回结果
    input_data = cursor.fetchall()
    print(input_data)
    print(type(input_data))
    content_list = []

    for i in input_data:
        if i[2]!= None:
            content_list.append(i[2])
    print(content_list)
    text = '\n'.join(content_list)
    print("select done")
    return text


start_time = time.time()
text = selectdata()
end_time = time.time()
print(end_time - start_time)


# def test():
#     abstract_tfidfer = TFIDF_ABS(text, 5)
#     final_result = abstract_tfidfer.dic_order_value_and_get_key()
#     print(final_result)

# test()


#
# # ==========================================添加示例数据==========================================
# def insertdata_demo():
#     # (('077069', datetime.datetime(2024, 4, 15, 11, 17, 24), '第一次保养换全车油'), ('077069', datetime.datetime(2024, 4, 15, 11, 17, 24), '第一次保养换全车油')
#     # 添加单条数据
#     value_str = "('077069', '2024-04-15 15:03:29', '文本摘要测试1','文本摘要测试2')"
#     insert_emp_sql_command = "INSERT INTO `finebi_fill_disposalsc_df` (`emp_no`, `create_time`, `disposalsc`, `keywordsc`) VALUES "
#     insert_emp_sql_single = insert_emp_sql_command + value_str
#     print(insert_emp_sql_single)
#     # 执行语句
#     cursor.execute(insert_emp_sql_single)
#     # 提交数据
#     conn.commit()
#     print("insert done")


# insertdata_demo()

#
# def insertdata():
#     str_time = str(dt.datetime(2024, 4, 15, 11, 17, 24))
#     # str_time = str(dt.datetime.now().strftime("%Y-%m-%d %H:%M"))
#     line = "'" + "077069" + "'"
#     line = line + ',' + "'" + "2" + "'"
#     line = line + ',' + "'" + "3" + "'"
#     line = line + ',' + "'" + str_time + "')"
#     line = line + ',' + "'" + "2" + "'"
#     print(line)
#     insert_emp_sql_month_command = "INSERT INTO `finebi_fill_disposalsc_df` (`emp_no`, `create_time`, `disposalsc`) VALUES " + line
#     # 执行语句
#     cursor.execute(insert_emp_sql_month_command)
#     # 提交数据
#     conn.commit()
#     print("insert done")
