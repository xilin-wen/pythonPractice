# json库用于字符串和 Python 数据结构之间的相互转换
import json
from server import func
# 装饰器：根据请求的路径执行相应的路由处理函数
route_handlers = {
    "/hello": {
        "GET": func.handle_hello
    },
    "/goodbye": {
        "GET": func.handle_goodbye
    },
    "/count": {
        "GET": func.handle_count
    },
}
# route_handlers={}
def route_dispatcher_decorator(cls):
    # original_do_get = cls.do_GET  # 原始的 do_GET 方法
    # original_do_post = cls.do_POST  # 原始的 do_POST 方法

    # 定义新的 do_GET 方法
    def new_do_get(self):
        path = self.path
        handler = route_handlers.get(path, {}).get('GET')  # 查找对应 GET 方法的处理函数
        if handler:
            return handler(self) # 如果找到对应的路由处理函数，则执行它
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"错误": "路由错误，请检查拼写"}, ensure_ascii=False).encode())

    # 定义新的 do_POST 方法
    def new_do_post(self):
        path = self.path
        handler = route_handlers.get(path, {}).get('POST')  # 查找对应 POST 方法的处理函数
        if handler:
            return handler(self)
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Route not found"}).encode())

    # 替换类中的 do_GET 和 do_POST 方法
    cls.do_GET = new_do_get
    cls.do_POST = new_do_post

    return cls
