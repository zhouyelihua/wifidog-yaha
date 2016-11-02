#!/usr/bin/env python
#coding=utf-8
import web
import time

urls = (
    '/', 'index',
    '/xml/.*', 'pushxml',
    '/login/.*', 'login',
    '/logout/.*', 'logout',
    '/auth.*','auth',
    '/auth/.*','auth',
    '/ping/.*','ping',
    '/ping.*','ping',
    '/login','login',
    '/portal/.*','portal',
    '/portal.*','portal',

)
render = web.template.render('templates/')
web.config.debug = False
app = web.application(urls, locals())
session = web.session.Session(app, web.session.DiskStore('sessions'))      
session.login=False
class index():
    def GET(self):
        try:
            if session.logged_in == True:
                return '<h1>You are logged in</h1><a href="/logout">Logout</a>'
        except AttributeError:
            pass
        return '<h1>You are not logged in.</h1><a href="/login">Login now</a>'

def authorize(func):
    def logged(*args,**dic):
        if session.logged_in==True:
            func(*args,**dic)
        else:
            raise web.seeother('/login')
    return logged

class pushxml():
    # @authorize
    def GET(self):
        try:
            if session.logged_in == True:
                web.header('Content-Type', 'text/xml')
                i = web.input(data=None)
                return render.response(i.data)
        except AttributeError:
            pass
       
class login():
    def GET(self):
        try:
            session.logged_in = False
        except AttributeError:
            pass
        return """
              <html lang="utf-8">
            <head>
            <title>菜鸟驿站de</title>
            <meta charset="utf-8"/>

                <script>
//产生日期随机数
                var now=new Date(); 
                var number = now.getSeconds() * now.getMinutes() * now.getHours() * now.getDate() * now.getYear() + Math.floor(Math.random()*10099+99);
//输出查看 
                document.write(number) 
                </script>

                </head>
                <body>
                <center>
                <h1>免费热点登录</h1><br />
                <a href="#" onclick="this.href='http://192.168.1.1:2060/wifidog/auth?token=123445'"><h2>点此登录<h2></a>
                </center>
                </body>
                </html>
        """
           
    def POST(self):
        login_data = web.input()
        if login_data.user == 'a' and login_data.passwd == 'a':
            session.logged_in = True
            print "posted"
            print session
            raise web.seeother('/auth?token=122')
       
class logout():
    def GET(self):
        try:
            session.logged_in = False
            session.kill()
        except AttributeError:
            pass
        raise web.seeother('/auth')
class auth():
    """docstring for ClassName"""
    def GET(self):
        return "Auth: 1"
class portal():
    """docstring for ClassName"""
    def GET(self):
        return """
        <html lang="utf-8">
        <head>
        <title>欢迎界面</title>
        <meta charset="utf-8"/>
        </head>
        <body>
        <center>
        <h1>你已经成功登录网络！</h1><br />
        <!-- <a href="http://100.64.100.100:2060/wifidog/auth?logout=1&token="><h2>点此退出<h2></a> -->
        </center>
        </body>
        </html>
        """
class ping():
    """docstring for ClassName"""
    def GET(self):
        return "Pong"
if __name__ == '__main__':
    app.run()