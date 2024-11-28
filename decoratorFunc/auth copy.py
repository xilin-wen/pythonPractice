import json

def auth_required(func):
    """
    全局鉴权装饰器，检查请求的 Authorization token 是否有效。
    如果无效，返回 401 错误。
    """
    def wrapper(self, *args, **kwargs):
        if not is_token_valid(self.headers):  # 验证 token
            return unauthorized_response(self)  # 如果无效，返回 401 错误
        return func(self, *args, **kwargs)  # 如果 token 有效，继续执行原函数
    return wrapper

# 简单的 token 校验函数
def is_token_valid(headers):
    """
    验证请求头中的 Authorization token 是否有效
    """
    token = headers.get('Authorization')
    if token is None:
        return False  # 没有 token，返回无效
    return token == 'Bearer valid_token'  # 假设这里是验证 token 的方式，可以根据需要扩展

# 鉴权响应
def unauthorized_response(self):
    """
    返回 401 未授权响应
    """
    self.send_response(401)  # Unauthorized
    self.send_header('Content-type', 'application/json')
    self.end_headers()
    self.wfile.write(json.dumps({"错误": "令牌已过期或无效"}, ensure_ascii=False).encode())
