import requests
import time


if __name__ == '__main__':
    start_time = time.time()
    body = '20221209143031'
    headers = {'content-type': 'application/json'}
    # r = requests.post("http://10.2.82.101:8081/hello", headers=headers)
    r = requests.post("http://124.221.238.156:8081/hello", headers=headers)

    # r = requests.post("https://veroad.com:8081", headers=headers, data=body)

    end_time = time.time()
    print(end_time - start_time)
    print(r)
    print(r.json())

