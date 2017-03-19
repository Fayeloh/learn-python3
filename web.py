#---------------------------------------------------Web开发 
#cs->bs
#web开发经历的几个阶段：静态页面->CGI->asp/JSP/PHP->MVC
#---------------------------------------------------Http协议简介
##---------------------------------------------------安装调试用的浏览器
##---------------------------------------------------Http请求
##---------------------------------------------------Http格式

#---------------------------------------------------HTML简介
#标签，css，js

#---------------------------------------------------WSGI接口
#web应用的本质（一个过程四个阶段）
#WSGI：Web Server Gateway Interface。封装了底层信息，如TCP连接、HTTP原始请求、响应模式
def application(environ,start_response):			#environ:包含所有http请求信息的dict对象，start_response：一个发送http相应的函数
	start_response('200 OK',[('Content-Type','text/html')])		#headers....注意是哦了的那个200 ok不是两千k
	return [b'<h1>Hello,web!<h1/>']

##---------------------------------------------------运行WSGI服务

#从wsgiref模块导入
from wsgiref.simple_server import make_server
#导入我们自己编写的application函数
from hello import application

#创建一个服务器，IP地址为空，端口是8000，处理函数是application
httpd = make_server('',8000,application)
print('Serving HTTP on port 8000...')
#开始监听HTTP请求
httpd.serve_forever()			#serve而不是server

#---------------------------------------------------使用web框架
#WSGI抽象成专注用一个函数处理URL，用web框架来处理URL到函数的映射

#试试较为流行的flask框架
#命令行：pip install flask

#然后写一个app.py，处理3个URL，分别是：
#GET /：首页，返回Home；
#GET /signin：登录页，显示登录表单；
#POST /signin：处理登录表单，显示登录结果。

from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    return '<h1>Home</h1>'

@app.route('/signin', methods=['GET'])
def signin_form():
    return '''<form action="/signin" method="post">
              <p><input name="username"></p>
              <p><input name="password" type="password"></p>
              <p><button type="submit">Sign In</button></p>
              </form>'''

@app.route('/signin', methods=['POST'])
def signin():
    # 需要从request对象读取表单内容：
    if request.form['username']=='admin' and request.form['password']=='password':
        return '<h3>Hello, admin!</h3>'
    return '<h3>Bad username or password.</h3>'

if __name__ == '__main__':
    app.run()

#其他web模板：
#			Django：全能型web框架
#			web.py:一个小巧的web框架
#			Bottle：与flask相似的框架
#			Tomado：Fackbook的开源异步Web框架
#Flask通过request.form['name']来获取表单的内容

#---------------------------------------------------使用模板
from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route('/signin', methods=['GET'])
def signin_form():
    return render_template('form.html')

@app.route('/signin', methods=['POST'])
def signin():
    username = request.form['username']
    password = request.form['password']
    if username=='admin' and password=='password':
        return render_template('signin-ok.html', username=username)
    return render_template('form.html', message='Bad username or password', username=username)

if __name__ == '__main__':
    app.run()

#Flask通过render_template()函数来实现模板的渲染。和Web框架类似，Python的模板也有很多种。Flask默认支持的模板是jinja2，所以我们先直接安装jinja2：
#一定要把模板放到正确的templates目录下，templates和app.py在同级目录下