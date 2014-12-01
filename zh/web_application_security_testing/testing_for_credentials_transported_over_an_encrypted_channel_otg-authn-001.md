# 加密信道传输凭证测试 (OTG-AUTHN-001)


### 综述
凭证传输测试意味着验证用户的认证数据是通过加密信道传输的，避免被恶意用户截获。测试分析着重于试着弄清楚数据是否未加密从浏览器传输到服务器或web应用是否已经采取了恰当的安全措施如使用HTTPS协议。HTTPS协议是建立在TLS/SSL之上，加密传输数据确保数据发送于用户期望的目的站点。

明显的，数据流量被加密不代表他们是完全安全的。安全也依赖于使用的加密算法和应用程序使用的密钥的健壮性，但这个主题不是本章的重点。

对于TLS/SSL通道的安全性更加详细的讨论请参考[弱SSL/TLS测试](https://www.owasp.org/index.php/Testing_for_Weak_SSL/TSL_Ciphers,_Insufficient_Transport_Layer_Protection_%28OWASP-EN-002%29)章节。在这里，测试者仅仅试着理解用户在web表单中填写的，为了登录站点的数据是否通过安全的协议传输来保护他们远离攻击者。

现在关于这个主题最常见的例子是web应用程序的登录页面。测试者应该验证用户登录凭证是通过加密信道传输的。为了登录网站，用户通常需要填写一个简单的表单，通过POST方法提交给web应用程序。一个不明显的情况就是，数据可能通过HTTP协议发送，这导致了一个不安全的、明文的信息被传输；也可能通过HTTPS协议，这加密了传输数据。对于某些更加复杂的情况，有可能网站使用HTTP展示登录页面（让我们相信传输是不安全的），但是真正发送数据的时候又是使用HTTPS的。完成这个测试来确保攻击者不能够通过使用嗅探工具简单嗅探网络来获取敏感信息。

### 如何测试
#### 黑盒测试
在下面的例子中，我们将使用WebScarab来捕获数据包头，并分析他们。你可以使用任何你喜欢的web代理。


##### 例1：通过HTTP使用POST方法发送数据

假设登录页面是一个用户字段、密码字段和提交按钮组成的表单。如果我们检查发送的请求的数据头，我们会发现像下面这样的信息：

```
POST http://www.example.com/AuthenticationServlet HTTP/1.1
Host: www.example.com
User-Agent: Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.14) Gecko/20080404
Accept: text/xml,application/xml,application/xhtml+xml
Accept-Language: it-it,it;q=0.8,en-us;q=0.5,en;q=0.3
Accept-Encoding: gzip,deflate
Accept-Charset: ISO-8859-1,utf-8;q=0.7,*;q=0.7
Keep-Alive: 300
Connection: keep-alive
Referer: http://www.example.com/index.jsp
Cookie: JSESSIONID=LVrRRQQXgwyWpW7QMnS49vtW1yBdqn98CGlkP4jTvVCGdyPkmn3S!
Content-Type: application/x-www-form-urlencoded
Content-length: 64

delegated_service=218&User=test&Pass=test&Submit=SUBMIT
```

从这个例子测试者可以明白POST请求通过HTTP向页面*www.example.com/AuthenticationServlet* 发送了数据。所以数据是未被加密的，恶意用户可能通过使用像Wireshark之类的工具简单嗅探网络来截获用户名和密码。


##### 例2：通过HTTPS使用POST方法发送数据

假设我们的web应用程序使用HTTPS协议加密我们发送的数据（或至少加密传输敏感信息如登录凭证）。在这个例子中，我们登录的POST请求可能类似：

```
POST https://www.example.com:443/cgi-bin/login.cgi HTTP/1.1
Host: www.example.com
User-Agent: Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.14) Gecko/20080404
Accept: text/xml,application/xml,application/xhtml+xml,text/html
Accept-Language: it-it,it;q=0.8,en-us;q=0.5,en;q=0.3
Accept-Encoding: gzip,deflate
Accept-Charset: ISO-8859-1,utf-8;q=0.7,*;q=0.7
Keep-Alive: 300
Connection: keep-alive
Referer: https://www.example.com/cgi-bin/login.cgi
Cookie: language=English;
Content-Type: application/x-www-form-urlencoded
Content-length: 50

Command=Login&User=test&Pass=test
```

我们可以发现请求目的地址是*www.example.com:443/cgi-bin/login.cgi* ，使用了HTTPS协议，他确保了我们的凭证信息通过加密信道传输，不能够被恶意用户使用嗅探软件读取。


##### 例3：在一个HTTP页面上通过HTTPS POST方法发送数据

现在，想象一下我们在一个可以HTTP访问的页面，但他仅通过HTTPS发送认证表单的数据。这个情况可能发生，例如，我们处于一个大公司的登录入口，这个公司对外公开提供多种信息和服务。同时这个公司也提供用户登录之后的私人访问页面。所以当我们尝试登录时候，我们的请求头部会类似如下：

```
POST https://www.example.com:443/login.do HTTP/1.1
Host: www.example.com
User-Agent: Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.14) Gecko/20080404
Accept: text/xml,application/xml,application/xhtml+xml,text/html
Accept-Language: it-it,it;q=0.8,en-us;q=0.5,en;q=0.3
Accept-Encoding: gzip,deflate
Accept-Charset: ISO-8859-1,utf-8;q=0.7,*;q=0.7
Keep-Alive: 300
Connection: keep-alive
Referer: http://www.example.com/homepage.do
Cookie: SERVTIMSESSIONID=s2JyLkvDJ9ZhX3yr5BJ3DFLkdphH0QNSJ3VQB6pLhjkW6F
Content-Type: application/x-www-form-urlencoded
Content-length: 45

User=test&Pass=test&portal=ExamplePortal
```

我们可以发现请求通过HTTPS被发送到*www.example.com:443/login.do* 。但是如果我们仔细观察Referer-header（来自哪里的页面），可以发现正是 *www.example.com/homepage.do* ，可以通过简单HTTP访问。尽管我们通过HTTPS发送请求，这种部署方式可能允许[SSLStrip](http://www.thoughtcrime.org/software/sslstrip/)攻击（一种[Man-in-the-middle](http://en.wikipedia.org/wiki/Man-in-the-middle_attack)中间人攻击）。


##### 例4：通过HTTPS使用GET方法发送数据

在最后一个例子中，假设应用程序通过GET方法发送数据。这种方法不应该用于传输敏感信息如用户名和密码，因为数据在URL中明文显示，并会引起一系列的安全问题。例如，请求的URL可以简单从服务器日志或浏览器历史记录中获得，这将导致你的敏感信息可能被未认证的用户获得。所以这个例子只是纯粹展示作用，在现实中，强烈推荐使用POST方法来替代。

```
GET https://www.example.com/success.html?user=test&pass=test HTTP/1.1
Host: www.example.com
User-Agent: Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.14) Gecko/20080404
Accept: text/xml,application/xml,application/xhtml+xml,text/html
Accept-Language: it-it,it;q=0.8,en-us;q=0.5,en;q=0.3
Accept-Encoding: gzip,deflate
Accept-Charset: ISO-8859-1,utf-8;q=0.7,*;q=0.7
Keep-Alive: 300
Connection: keep-alive
Referer: https://www.example.com/form.html
If-Modified-Since: Mon, 30 Jun 2008 07:55:11 GMT
If-None-Match: "43a01-5b-4868915f"
```

我们可以发现数据在URL中明文传输，并不是像之前一样的在请求主体之中。但是我们必须考虑SSL/TLS是一个第五层的协议，比HTTP低一层，所以整个HTTP数据包仍然是加密的，URL是无法被恶意用户使用嗅探工具读取的。但正如之前所说的，使用GET方法来向web应用程序传输敏感数据不是一个好的实践方法，因为这些URL信息可能被存储在许多地方比如代理和web服务的日志中。


#### 灰盒测试
与web应用开发者交流，试着弄清楚他们是否注意到了HTTP和HTTPS协议的区别，他们是否明白应该使用HTTPS来传输敏感信息。然后和他们一起检查是否在每一处存在敏感信息的地方都使用了HTTPS，比如登录页面，来防止未授权用户截获数据。


### 测试工具
* [WebScarab](https://www.owasp.org/index.php/OWASP_WebScarab_Project)
* [OWASP Zed Attack Proxy (ZAP)](https://www.owasp.org/index.php/OWASP_Zed_Attack_Proxy_Project)


### 参考资料
**白皮书**
* HTTP/1.1: Security Considerations - http://www.w3.org/Protocols/rfc2616/rfc2616-sec15.html
* [SSL is not about encryption](http://www.troyhunt.com/2011/01/ssl-is-not-about-encryption.html) <br>
