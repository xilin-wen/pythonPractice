import json
route_handlers={}
def route(path, method='GET', disposal_mode='normal', token_required=True, role_required=False):
    """
    路由装饰器，支持开启鉴权。
    :param path: 路由路径
    :param method: 请求方法，默认为 'GET'
    :param disposal_mode method: 处理方式normal为单核处理
    :param token_required: 是否需要 Token 鉴权，默认 True
    :param role_required: 是否需要角色鉴权，默认 False
    :return: 装饰后的函数
    """
    def decorator(func):
        # print(f"Registering handler for {path} with method {method}")
        # if path not in route_handlers:
        #     route_handlers[path] = {}  # 如果路径没有注册过，则初始化为一个空字典
        #
        # route_handlers[path][method] = func  # 将处理函数存储到对应的请求方法下



        # route_handlers[path][disposal_mode] = True  # 写入函数是否需要特殊处理，如果需要如何处理

        def wrapper(self, *args, **kwargs):
            headers = self.headers
            token = headers.get('Authorization') # 先初始化 token

            # Token 鉴权
            if token_required:
                token = validate_token(token)
                self.token = token
                if not token:
                    self.send_response(401)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({"错误": "令牌已过期或无效"}, ensure_ascii=False).encode())
                    return  # 鉴权失败，返回 401 错误，终止请求处理

            # 角色鉴权
            if role_required:
                # user_role = headers.get('X-User-Role', None)  # 假设角色信息通过 'X-User-Role' 头部传递
                user_role = headers.get('Authorization')
                if not user_role or not validate_role(user_role, role_required):
                    self.send_response(403)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({"错误": "当前角色暂无权限"}, ensure_ascii=False).encode())
                    return  # 角色鉴权失败，返回 403 错误，终止请求处理

            # 鉴权通过，调用原始处理函数
            return func(self, *args, **kwargs)  # 将 token 作为参数传递给原函数

        return wrapper  # 返回包装后的函数

    return decorator

def validate_token(token):
    try:
        return 'valid_token' + token
    except Exception:
        return False

# 角色验证函数
def validate_role(role, required_role):
    return role == required_role