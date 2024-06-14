import os
os.system("ps -ef | grep python | grep -v grep | awk '{print $2}' | xargs kill -9")  # 在UNIX/Linux系统中列出当前目录下的文件和文件夹

print('kill done')
