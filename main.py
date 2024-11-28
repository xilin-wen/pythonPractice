from http.server import HTTPServer, BaseHTTPRequestHandler
from decoratorFunc.analyzeRoute import route_dispatcher_decorator

data = {'result': 'Attempt to build HTTP'}
host = ('localhost', 8888)

# class Request(BaseHTTPRequestHandler):
#     @analyzeRoute.route_dispatcher_decorator
#     def do_GET(self):
#         # self.send_response(200) # 发送 HTTP 响应头，200为状态码
#         # self.send_header('Content-type', 'application/json') # 设置响应头的 Content-type 为 application/json，告知客户端返回的数据格式是 JSON
#         # self.end_headers() # 结束响应头的发送 --为什么需要主动结束响应头的发送
#         # self.wfile.write(json.dumps(data).encode()) # json.dumps(data)将 Python 数据结构（通常是字典或列表）转换为 JSON 格式的字符串；通过 encode() 转换为字节流并发送给客户端
#         pass
#
#     @analyzeRoute.route_dispatcher_decorator
#     def do_POST(self):
#         content_length = int(self.headers['Content-Length'])  # 获取请求体的长度 --为什么需要获取请求体的长度？
#         post_data = self.rfile.read(content_length)  # self.rfile.read() 方法读取请求体数据
#
#         try:
#             # 尝试解析 JSON 数据
#             received_data = json.loads(post_data.decode('utf-8')) # 将读取到的字节数据解码为字符串，并尝试将其解析为 JSON 格式。
#             response = {
#                 "status": "success",
#                 "received_data": received_data
#             }
#             self.send_response(200)
#             self.send_header('Content-type', 'application/json')
#             self.end_headers()
#             self.wfile.write(json.dumps(response).encode())
#         except json.JSONDecodeError:
#             # 如果解析 JSON 失败，返回错误信息
#             self.send_response(400)
#             self.send_header('Content-type', 'application/json')
#             self.end_headers()
#             self.wfile.write(json.dumps({"error": "Invalid JSON format"}).encode())

@route_dispatcher_decorator
class Request(BaseHTTPRequestHandler):
    pass

if __name__ == '__main__':
    server = HTTPServer(host, Request)
    print("Starting server, listen at: %s:%s" % host)
    server.serve_forever() # 启动服务器并开始监听和处理请求，直到程序被手动停止（例如调用调用 server.shutdown()）