from decoratorFunc.auth import route
import json
from multiprocessing import Process, Value

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
    print("token", self.token)
    self.send_response(200)
    self.send_header('Content-type', 'application/json')
    self.end_headers()
    self.wfile.write(json.dumps(data_goodbye).encode())

# 定义全局变量，使用 Value 来实现多进程共享
counter = Value('i', 0)  # 'i' 是整数类型
@route('/count', token_required=False)
def handle_count(self):
    # 每次接收到请求时，增加全局变量
    with counter.get_lock():  # 使用锁确保线程安全
        counter.value += 1

    response = {
        "message": "请求成功",
        "counter": counter.value
    }

    self.send_response(200)
    self.send_header('Content-type', 'application/json')
    self.end_headers()
    self.wfile.write(json.dumps(response).encode())