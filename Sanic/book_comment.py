from sanic import Sanic, response
# Sanic，用于创建应用实例；response，虽然在这里没有直接使用，但它通常用于处理HTTP响应。
from sanic.response import text, json
# 从Sanic的response模块中导入了两个函数：text和json。
# 这两个函数用于生成不同类型的HTTP响应。这里只用了json函数来返回JSON格式的响应。
import os
import requests
import time


app = Sanic("mySanic")
# 创建了一个Sanic应用实例，名为mySanic。这个实例将会包含所有的路由和配置信息。

@app.route("/v1/book/crawled/upload", methods=['POST'])
# 这是一个路由装饰器，定义了一个路由/v1/book/crawled/upload，并指定此路由只接受POST方法的请求。
# 这个装饰器会将下面定义的函数与这个路由关联起来。
async def upload(request):
    # 这行代码定义了一个异步函数upload，它会处理所有发送到/v1/book/crawled/upload路径的POST请求。
    # request参数包含了客户端发送的请求信息。
    allow_type = ['.json']
    file = request.files.get('file')
    type = os.path.splitext(file.name)
    if len(type) == 1 or type[1] not in allow_type:
        return json({"code": 0, "message": "file's format is error!"})
    
    path = "./upload"
    now_time = time.strftime('%Y%m%d%H%M%S', time.localtime())
    filename = now_time+"_"+type[0]+".json"
    with open(path + "/" + filename, 'wb') as f:
        f.write(file.body)
    f.close
    return json({"code": 1, "msg": "upload successfully!", "data": {"name": filename}})

# 当有请求到达/v1/book/crawled/upload路径时，upload函数会执行这行代码，返回一个JSON格式的响应给客户端。
# 这个响应包含一个状态码code，一个消息msg，以及一个数据字段data。


@app.route("/v1/book/info", methods=['GET'])
# 路由装饰器，定义了一个路由/v1/book/info，并指定此路由只接受GET方法的请求。
async def get_books_info(request):
    # 这行代码定义了一个异步函数get_books_info，它会处理所有发送到/v1/book/info路径的GET请求。
    return json({"code": 1, "msg": "query successfully!", "data": None})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
# 如果当前模块是主程序入口，则运行Sanic应用实例app。host='0.0.0.0'表示服务器将监听所有网络接口，
# port=8000表示服务器将在8000端口上监听请求。这意味着其他机器可以通过网络访问这个服务器，
# 只要知道服务器的IP地址，并且访问8000端口即可。












