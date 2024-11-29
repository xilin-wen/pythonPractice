route_handlers={}
def route(path, method='GET', token_required=True, role_required=False):
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
        if path not in route_handlers:
            route_handlers[path] = {}  # 如果路径没有注册过，则初始化为一个空字典

        route_handlers[path][method] = {
            "token_required": token_required,
            "role_required": role_required,
            "func": func # 将处理函数存储到对应的请求方法下
        }

    return decorator

def validate_token(token):
    try:
        return 'valid_token' + token
    except Exception:
        return False

# 角色验证函数
def validate_role(role, required_role):
    return role == required_role