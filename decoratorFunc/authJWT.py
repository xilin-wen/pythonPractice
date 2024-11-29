import json
from datetime import time

import jwt
from functools import wraps
from http.server import BaseHTTPRequestHandler

# 假设这个是你的密钥
SECRET_KEY = "your-secret-key"


# 装饰器定义
def verify_token(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        # 获取请求头中的token
        token = self.headers.get('Authorization')

        # 如果没有token，返回401错误
        if not token:
            self.send_response(401)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"错误": "令牌已过期或无效"}, ensure_ascii=False).encode())
            return

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
                self.wfile.write(json.dumps({"error": "Token expired"}).encode())
                return
        except (jwt.ExpiredSignatureError, jwt.DecodeError, IndexError):
            # 如果token无效或解析错误，返回401
            self.send_response(401)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Invalid token"}).encode())
            return

        # 如果token有效，调用实际的请求处理函数
        return func(self, *args, **kwargs)

    return wrapper


# 请求处理类
class Request(BaseHTTPRequestHandler):

    # 示例：一个需要token验证的GET请求
    @verify_token
    def do_GET(self):
        # 如果token有效，这里会继续执行
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"message": "Token valid, access granted!"}).encode())

    # 其他请求方法...
