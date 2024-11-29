from http.server import HTTPServer, BaseHTTPRequestHandler
from server import func
from decoratorFunc.analyzeRoute import route_dispatcher_decorator


data = {'result': 'Attempt to build HTTP'}
host = ('localhost', 8888)

@route_dispatcher_decorator
class Request(BaseHTTPRequestHandler):
    pass

if __name__ == '__main__':
    server = HTTPServer(host, Request)
    print("Starting server, listen at: %s:%s" % host)
    server.serve_forever() # 启动服务器并开始监听和处理请求，直到程序被手动停止（例如调用调用 server.shutdown()）