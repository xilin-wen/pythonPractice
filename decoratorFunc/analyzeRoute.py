# json库用于字符串和 Python 数据结构之间的相互转换
import json
import multiprocessing
from datetime import time

from decoratorFunc.auth import route_handlers
import jwt

SECRET_KEY = "pandag-secret-key"

def verify_token_func(self):
    token = self.headers.get('Authorization')

    if not token:
        self.send_response(401)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"错误": "令牌已过期或无效"}, ensure_ascii=False).encode())
        return False  # 返回 False 表示 token 验证失败

    try:
        # 移除"Bearer "前缀
        token = token.split(" ")[1]

        # 解码token，验证过期时间
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

        # 判断token是否过期
        if decoded_token.get("exp") < time.time():
            self.send_response(401)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"错误": "令牌已过期或无效"}, ensure_ascii=False).encode())
            return False  # 返回 False 表示 token 验证失败
    except (jwt.ExpiredSignatureError, jwt.DecodeError, IndexError):
        # 如果token无效或解析错误，返回401
        self.send_response(401)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"错误": "令牌已过期或无效"}, ensure_ascii=False).encode())
        return False  # 返回 False 表示 token 验证失败

    return True  # 返回 True 表示 token 验证成功


def route_dispatcher_decorator(cls):
    # original_do_get = cls.do_GET  # 原始的 do_GET 方法
    # original_do_post = cls.do_POST  # 原始的 do_POST 方法

    # 定义新的 do_GET 方法
    def new_do_get(self):
        path = self.path
        handler = route_handlers.get(path, {}).get('GET')  # 查找对应 GET 方法的处理函数
        is_verify_token = handler.get('token_required') # 是否需要验证token
        is_verify_role = handler.get('role_required')
        handler_func = handler.get('func')

        if is_verify_token:
            if not verify_token_func(self):  # 如果token验证失败，直接返回
                return

        if handler_func:
            return handler_func(self)  # 如果找到对应的路由处理函数，则执行它
        # if handler_func:
        #     multi_process_set = []
        #     for i in range(6):
        #         multi_process = multiprocessing.Process(target=handler_func, args=(self,))
        #         multi_process_set.append(multi_process)
        #         multi_process.start()
        #
        #     for process in multi_process_set:
        #         process.join()
        #     # return handler_func(self) # 如果找到对应的路由处理函数，则执行它
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"错误": "路由错误，您当前访问的页面不存在"}, ensure_ascii=False).encode())

    # 定义新的 do_POST 方法
    def new_do_post(self):
        path = self.path

        handler = route_handlers.get(path, {}).get('POST')  # 查找对应 GET 方法的处理函数
        is_verify_token = handler.get('token_required')
        is_verify_role = handler.get('role_required')
        handler_func = handler.get('func')

        if is_verify_token:
            verify_token_func(self)

        if handler_func:
            return handler_func(self)  # 如果找到对应的路由处理函数，则执行它

        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"错误": "路由错误，您当前访问的页面不存在"}).encode())

    # 替换类中的 do_GET 和 do_POST 方法
    cls.do_GET = new_do_get
    cls.do_POST = new_do_post

    return cls