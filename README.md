#热点认证技术实现

##背景
&emsp;&emsp;&emsp;当用户靠近路由器时候，打开App时候，会自动连接上金猪酒店提供的网络，当用户离开路由器的时候，或者关闭app之后会断开相关的网络连接。

##方案一：

##目前的技术调研

###IOS的局限性

  &emsp;apple公司关于wifi的相关api很少其中开放的api只有以下的代码可以实现扫描周边的wifi列表

  ```objectivee-c
  - (id)fetchSSIDInfo {
    NSArray *ifs = (__bridge_transfer id)CNCopySupportedInterfaces();
    NSLog(@"Supported interfaces: %@", ifs);
    id info = nil;
    for (NSString *ifnam in ifs) {
        info = (__bridge_transfer id)CNCopyCurrentNetworkInfo((__bridge CFStringRef)ifnam);
        self.textview.text=[NSString stringWithFormat:@"%@ => %@", ifnam, info];
          self.label.text=[NSString stringWithFormat:@"%@ => %@", ifnam, info];
        NSLog(@"%@ => %@", ifnam, info);
        if (info && [info count]) { break; }
    }
    return info;
}
  ```
 
  &emsp;所以苹果是不允许第三方连接的，所有的链接都只能跳转到wifi设置页面进行链接。对于开发者来说，想要在APP store上线你的应用，是不能调用私有的api。现在可以用的接口只能获取到Bssid,ssid,ssiddata,但是没有密码。但是，有些公司和苹果合作了，就会多开放一些接口。（好比开启wifi万能助手，在无线界面，在搜索到的wifi名称下有个一键连接wifi，这个效果就是苹果开放给某些公司的接口）。

  &emsp;[私有api的一个实现wifi链接](http://blog.csdn.net/jiangnanshuilu/article/details/41145663)  (http://blog.csdn.net/jiangnanshuilu/article/details/41145663)

  &emsp;但是由于私有的api实现是不能再在app store上线的，所以这个方法是不可行。


###IOS的相关可行的技术

**可利用的技术**

1. 地理位置上传（技术成熟，未深入了解）

2. iOS Configuration Profiles（http://nshipster.com/configuration-profiles/ ）
&emsp;一个 configuration profile 可用于对设备进行多种设置。
   每个配置文件包括多个设置，其中每个可指定的配置，包括：

   * 白名单、AirPlay 的身份验证和 AirPrint 的目标
   
   * 建立 VPN，HTTP 代理服务器，无线网络和蜂窝网络

   * 配置电子邮件（SMTP，Exchange），日历（CalDAV），和联系人（CardDAV，LDAP，AD）

   * 限制访问应用程序，设备功能，Web内容和媒体回放
   
   * 管理证书和 SSO 凭据
   
   * 安装网页剪辑，应用程序和自定义字体

   该网站（http://support.citrix.com/content/dam/supportWS/kA460000000CcBICA0/iPhoneConfiguration.pdf）给出了一个Configuration Profiles能做的事情的详细描述

   有以下几种方法来部署配置文件：

    * 附加到电子邮件
    
    * 链接到一个网页
    
    * 使用无线配置
    
    * 使用 Apple Configurator
    
    而其中除了部署配置文件，在 Apple Configurator 还可以生成配置文件，以替代你自己手写 XML。（在实现的demo中也是采用这个方法的）



##可行的方案

#方案一

**步骤**

1. 利用用户的app 检测到当前的位置

2. 扫描附近的ssid,bssid与服务器端进行匹配获得相关的密码，

3. 调其WiFi连接接口，要求用户手动输入wifi密码

**分析**

优点: 实现简单

缺点：每次都需要用户手动输入

###方案二

**步骤**

1. 利用用户的app 检测到当前的位置

2. 扫描附近的ssid,bssid与服务器端进行匹配获得相关的密码，

3. 构建iOS Configuration Profiles，通过iOS Configuration Profiles一键连接wifi

4.如果是通过网页形式配置profile可以添加一个确认页面，在这个页面上进行相关产品推荐 

**分析**

优点:减少用户的手工输入

缺点：实现较为复杂

**不足点分析**

1. 不能实现退出app的同时退出网络，只能给路由器设置相关密码，定时更换

2. 需要服务器端记录不同位置的wifi的密码

3. 需要app启动位置的相关服务

##Demo实现

利用已知的一个ssid和密码，将这个保存为iOS Configuration Profiles。将生成的profile放在github上(https://raw.githubusercontent.com/zhouyelihua/wifi/master/wifi2.mobileconfig)，采用以下代码

```objective-c
     NSURL *url = [NSURL URLWithString:@"https://raw.githubusercontent.com/zhouyelihua/wifi/master/wifi2.mobileconfig"];
     [[UIApplication sharedApplication] openURL:url];

```
系统会提示安装profile之后就可以连接上网络。

#Android的可行性分析

1.android可以调用系统的android.hardware.wifi，好吧问题解决

2.android通过(String SSID, String Password, WifiCipherType Type) 就可以连接ssid的wifi

3.android的实现具体流程：
   
   3.1 android 检测到酒店SSId 

   3.2通过地址或者bssid从服务端获得相关密码

   3.3利用得到的相关密码直接连接网络

#方案二：

##调查
###现状调查
&emsp;你一定有过以下经历：你到一个饭店吃饭，饭店提供了免费WiFi上网服务，你用手机连接饭店的WiFi信号，连接成功之后，在浏览器输入任意网址，都会自动跳出来一个认证界面，然后你需要进行认证登陆，认证登陆的方式多种多样，QQ登陆，微信登陆，或者是专用软件的登陆。认证登陆通过之后，就可以上网了。

&emsp;&emsp;该服务的流程:

&emsp;&emsp;&emsp;&emsp;1. 用户打开手机发现不需要密码的wifi，连接wifi

&emsp;&emsp;&emsp;&emsp;2. 用户打开网页跳转到相关的页面，要求用户输入相关的信息，或者调用相关软件才能正确联网。（微信开发者服务提供类似的服务*http://mp.weixin.qq.com/wiki/2/55f1e301f4558846d2bf0dd51543e252.html#.E9.A1.BE.E5.AE.A2.E8.BF.9E.E7.BD.91.E8.BF.87.E7.A8.8B*）

&emsp;&emsp;&emsp;&emsp;3. 认证通过之后给予网络连接

###背后的技术

**硬件要求**

1. 路由器（需要为ddwrt或者openwrt固件的路由器，或者手动刷固件，使其能够支持wifidog）

2. 服务器（主要是用于相关的认证和提供认证的页面）

**wifi热点的安装流程**

&emsp;现在基于wifi运营的相关公司比较多，所以wifi热点认证技术也相对比较火。而这个过程当中一般采用的都是开源的wifidog来实现相关的功能。WiFiDog是用来做无线WiFi热点认证管理的一套开源工具。

首先简单的介绍一下相关的wifidog的工作流程:

![wifidog认证原理](https://bytebucket.org/zhouyelihua/markdownphoto/raw/7f5a6df0d92c07d81c9e4edb645ab5ec0d9c1821/wifidog.png?token=51a293c50a781469f1743906cb882850673885ee)

1. 首先客服端发起相关的网络请求

2. 安装wifidog的路由器将网络请求定向到设置的认证服务器页面

3. 进行相关的服务认证（wifidog认证服务器主要需要实现以下几个页面[login,auth,portal,gw_message,ping] ）

4. 连接上网

##方案

1. 在指定地点放置配置好wifidog的路由器

2. 用户靠近时候，连接wifi（手机自动连接无密码的wifi），发起网页请求

   2.1  用户有安装app，调起app登陆，连接上网（类似微信认证）

   2.2  用户没有安装app

        2.2.1 给出自动下载连接？（wifidog防火墙配置方形相关网页请求）

        2.2.2 直接网页登陆，登陆之后跳转相关下载页面（会给人一种不安全的感觉，因为app账号就是淘宝账号）

3. 服务器端进行认证连接

##具体的实现

###路由器的设置

1.本人采用的是小米的mini路由器，首先需要对路由器进行刷openwrt的操作
本人参考的是一下网址(http://tieba.baidu.com/p/3618514879)

2.需要对刷完openwrt的路由器进行刷wifidog
   2.1 首先利用电脑先连接上路由器
   2.2 利用ssh连接上路由器。一般是ssh root@192.168.1.1 初始的密码是admin
   2.3 设置路由器的源。可以直接登录网页添加以下源
```
src/gz r2_base http://downloads.openwrt.org.cn/PandoraBox/ralink/packages/base
src/gz r2_management http://downloads.openwrt.org.cn/PandoraBox/ralink/packages/management
src/gz r2_oldpackages http://downloads.openwrt.org.cn/PandoraBox/ralink/packages/oldpackages
src/gz r2_packages http://downloads.openwrt.org.cn/PandoraBox/ralink/packages/packages
src/gz r2_routing http://downloads.openwrt.org.cn/PandoraBox/ralink/packages/routing
src/gz r2_telephony http://downloads.openwrt.org.cn/PandoraBox/ralink/packages/telephony
```
或者采用命令的方式
```
   dest root /
dest ram /tmp
lists_dir ext /var/opkg-lists
option overlay_root /overlay
src/gz r2_base http://downloads.openwrt.org.cn/PandoraBox/ralink/packages/base
src/gz r2_management http://downloads.openwrt.org.cn/PandoraBox/ralink/packages/management
src/gz r2_oldpackages http://downloads.openwrt.org.cn/PandoraBox/ralink/packages/oldpackages
src/gz r2_packages http://downloads.openwrt.org.cn/PandoraBox/ralink/packages/packages
src/gz r2_routing http://downloads.openwrt.org.cn/PandoraBox/ralink/packages/routing
src/gz r2_telephony http://downloads.openwrt.org.cn/PandoraBox/ralink/packages/telephony
```
    2.4     安装wifidog
    ```
    [root@PandoraBox:/root]#opkg update
[root@PandoraBox:/root]#opkg install wifidog
[root@PandoraBox:/root]#/etc/init.d/wifidog enable
[root@PandoraBox:/root]#/etc/init.d/wifidog start
    ```
    2.5  配置wifidog
        输入命令
        ```vim /etc/wifidog.conf```
```
 AuthServer {
Hostname 192.168.1.25#此处是你的服务器设置的地址
HTTPPort 8080
Path /wifidog/index.php/wifidog/
LoginScriptPathFragment         login/?
PortalScriptPathFragment        portal/?
MsgScriptPathFragment           gw_message.php?
PingScriptPathFragment          ping/?
AuthScriptPathFragment          auth/?
}
```

    2.6启动wifidog
```
/etc/init.d/wifidog enable
/etc/init.d/wifidog start
```



3.设置服务器
此处采用的是基于web.py实现的。安装了pip的同学，可以直接输入命令 ：pip install web.py既可。

我们的python服务器的实现如下

```
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
            <title>金猪酒店de</title>
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
```
4. app端的实现，其实很简单我们把连接网络和断开网络的两个函数贴出来

```objective-c
-(void)requestData{
    // 1 创建URL对象
    NSString*  uu=[NSString stringWithFormat:@"http://192.168.1.1:2060/wifidog/auth?token=%ld",(long)self.token];
    NSURL *url = [NSURL URLWithString:uu];
    
    // 2 创建请求对象
    NSMutableURLRequest *request = [NSMutableURLRequest requestWithURL:url];
    
    // 2.1 创建请求方式 (默认是get这一步可以不写)
    [request setHTTPMethod:@"get"];
    
    // 3 创建响应对象(有时会出错)
    NSURLResponse *response= nil;
    
    // 4 创建连接对象(同步)
    NSError *error;
    NSData *data = [NSURLConnection sendSynchronousRequest:request returningResponse:&response error:&error];
  //  NSDictionary *dict = [NSJSONSerialization JSONObjectWithData:data options:NSJSONReadingAllowFragments error:nil];
    NSLog(@"");
    NSLog(@"");
}
-(void)disconnect{
    // 1 创建URL对象
    NSString*  uu=[NSString stringWithFormat:@"http://192.168.1.1:2060/wifidog/auth?logout=1&token=%ld",(long)self.token];
    NSURL *url = [NSURL URLWithString:uu];
    
    // 2 创建请求对象
    NSMutableURLRequest *request = [NSMutableURLRequest requestWithURL:url];
    
    // 2.1 创建请求方式 (默认是get这一步可以不写)
    [request setHTTPMethod:@"get"];
    
    // 3 创建响应对象(有时会出错)
    NSURLResponse *response= nil;
    
    // 4 创建连接对象(同步)
    NSError *error;
    NSData *data = [NSURLConnection sendSynchronousRequest:request returningResponse:&response error:&error];
    //  NSDictionary *dict = [NSJSONSerialization JSONObjectWithData:data options:NSJSONReadingAllowFragments error:nil];
    NSLog(@"");
    NSLog(@"");
}
```


