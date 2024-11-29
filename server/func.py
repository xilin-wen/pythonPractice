import multiprocessing
from multiprocessing import Value, Lock

from decoratorFunc.auth import route
import json

data_hello = {"message": "Hello, world!"}
data_goodbye = {"message": "Goodbye, world!"}

# 定义多个路由处理函数
@route('/hello', method='GET', token_required=False, role_required=True)
def handle_hello(self):
    self.send_response(200)
    self.send_header('Content-type', 'application/json')
    self.end_headers()
    self.wfile.write(json.dumps(data_hello).encode())

@route('/goodbye')
def handle_goodbye(self):
    self.send_response(200)
    self.send_header('Content-type', 'application/json')
    self.end_headers()
    self.wfile.write(json.dumps(data_goodbye).encode())

# 使用 Manager 创建共享的字典
def countFunc(counter):
    # 每次接收到请求时，增加全局变量
    counter['value'] += 1

@route('/count', method='GET', token_required=False)
def handle_count(self):
    processes = []

    with multiprocessing.Manager() as manager:
        # 使用 Manager 创建一个共享的字典
        counter = manager.dict()
        counter['value'] = 0  # 初始化计数值为 0

        for i in range(6):
            count_process = multiprocessing.Process(target=countFunc, args=(counter,))
            processes.append(count_process)
            count_process.start()

        # 等待所有进程完成
        for p in processes:
            p.join()


        response = {
            "message": "请求成功",
            "counter": counter['value']
        }

        print("counter.value", counter['value'])

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())