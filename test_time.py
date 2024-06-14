# import datetime
#
# current_time = datetime.datetime.now()
# print("Current Time:", current_time)
# formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
# print("Formatted Time:", formatted_time)
# print(type(formatted_time))


idf_dict = {'反腐': 9.84023464143, '初级线圈': 13.900677652, '所言': 7.91422564669, '北仑区': 12.2912397395,
            '实实': 10.2630914922, '秦艽汤': 13.2075304714, '理论家': 8.51618258919}

common_idf = 12
out = idf_dict.get('反腐1', common_idf)
print(out)