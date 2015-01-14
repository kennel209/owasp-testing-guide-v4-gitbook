# 测试未加密通道中的敏感信息 (OTG-CRYPST-003)

### 综述
敏感信息在通过网络传输中必须被保护。如果数据是通过HTTPS或其他加密机制传输的，必须保证没有漏洞或这限制，如在文章 [测试弱SSL/TLS加密算法，不充分的传输层保护(OTG-CRYPST-001)](https://www.owasp.org/index.php?title=Testing_for_Weak_SSL/TLS_Ciphers,_Insufficient_Transport_Layer_Protection_%28OTG-CRYPST-001%29)[1] 和其他OWASP文档中的描述的问题[2], [3], [4], [5]。

通常根据经验来看，如果数据在存储时必须被保护，那么在传输中也应该如此。下面是一些敏感信息的例子：
* 用于认证的信息（如登陆凭证，PIN码，会话标识，令牌，Cookies等等）
* 被法律、规定或组织相关策略保护的信息（如信用卡号码、客户数据）

如果应用程序通过未加密的通道（如HTTP）传输这些信息，这需要被认为是一个安全风险。比如一些通过HTTP发送明文凭证的基本认证措施，通过HTTP发送表单认证方法以及明文传输那些被规范、法律、组织策略或是应用程序业务逻辑中被认定的敏感信息。

### 如何测试

许多类型的信息应该被保护，但是会应用程序以明文方式传输。可以通过使用HTTP代替HTTPS来进行传输来检查这个问题，或者使用弱的加密算法。参考 [Top 10 2013-A6-Sensitive Data Exposure](https://www.owasp.org/index.php/Top_10_2013-A6-Sensitive_Data_Exposure) [3] 来发现更多的不安全的凭证传输的信息，以及 [ insufficient transport layer protection in general [Top 10 2010-A9-Insufficient Transport Layer Protection](https://www.owasp.org/index.php/Top_10_2010-A9-Insufficient_Transport_Layer_Protection) [2] 中关于更多的不安全的传输层保护的信息。


#### 例1: 通过HTTP的基本认证
一个典型的例子是通过HTTP进行基本认证。当使用基本认证时，用户凭证是被编码而不是加密，并通过HTTP头进行发送。在下面的例子中，测试者使用curl[5]来测试这个问题。注意应用程序是如何进行基本认证的，以及使用的HTTP而不是HTTPS。

```
$ curl -kis http://example.com/restricted/
HTTP/1.1 401 Authorization Required
Date: Fri, 01 Aug 2013 00:00:00 GMT
WWW-Authenticate: Basic realm="Restricted Area"
Accept-Ranges: bytes Vary:
Accept-Encoding Content-Length: 162
Content-Type: text/html

<html><head><title>401 Authorization Required</title></head>
<body bgcolor=white> <h1>401 Authorization Required</h1>  Invalid login credentials!  </body></html>
```


#### 例2: 通过HTTP传输基于表单的认证操作
另一个典型的例子是通过HTTP传输用户认证信息的认证表单。在下面的例子中，我们可以看到HTTP在表单的"action" 属性中被使用，就有可能通过代理劫持的方式查看HTTP数据流来发现这个问题。

```
<form action="http://example.com/login">
	<label for="username">User:</label> <input type="text" id="username" name="username" value=""/><br />
	<label for="password">Password:</label> <input type="password" id="password" name="password" value=""/>
	<input type="submit" value="Login"/>
</form>
```


#### 例3: 通过HTTP发送包含会话ID的Cookie信息
包含会话ID的Cookie信息必须通过受保护的信道进行传输。如果Cookie没有设置secure标志[6]，这允许应用程序不加密传输他们。注意下面这些没有设置Secure标志的Cookie，所有的过程记录都是在HTTP中完成，而不是HTTPS。

```
https://secure.example.com/login

POST /login HTTP/1.1
Host: secure.example.com
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:25.0) Gecko/20100101 Firefox/25.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: https://secure.example.com/
Content-Type: application/x-www-form-urlencoded
Content-Length: 188

HTTP/1.1 302 Found
Date: Tue, 03 Dec 2013 21:18:55 GMT
Server: Apache
Cache-Control: no-store, no-cache, must-revalidate, max-age=0
Expires: Thu, 01 Jan 1970 00:00:00 GMT
Pragma: no-cache
Set-Cookie: JSESSIONID=BD99F321233AF69593EDF52B123B5BDA; expires=Fri, 01-Jan-2014 00:00:00 GMT; path=/; domain=example.com; httponly
Location: private/
X-Content-Type-Options: nosniff
X-XSS-Protection: 1; mode=block
X-Frame-Options: SAMEORIGIN
Content-Length: 0
Keep-Alive: timeout=1, max=100
Connection: Keep-Alive
Content-Type: text/html

----------------------------------------------------------
http://example.com/private

GET /private HTTP/1.1
Host: example.com
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:25.0) Gecko/20100101 Firefox/25.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: https://secure.example.com/login
Cookie: JSESSIONID=BD99F321233AF69593EDF52B123B5BDA;
Connection: keep-alive

HTTP/1.1 200 OK
Cache-Control: no-store
Pragma: no-cache
Expires: 0
Content-Type: text/html;charset=UTF-8
Content-Length: 730
Date: Tue, 25 Dec 2013 00:00:00 GMT
----------------------------------------------------------
```


### 测试工具
* [5] [curl](http://curl.haxx.se/) 可以被用于手动检查页面

### 参考资料
**OWASP 资料**
* [1] [OWASP Testing Guide - Testing for Weak SSL/TLS Ciphers, Insufficient Transport Layer Protection (OTG-CRYPST-001)](https://www.owasp.org/index.php/Testing_for_Weak_SSL/TLS_Ciphers,_Insufficient_Transport_Layer_Protection_%28OTG-CRYPST-001%29)
* [2] [OWASP TOP 10 2010 - Insufficient Transport Layer Protection](https://www.owasp.org/index.php/Top_10_2010-A9-Insufficient_Transport_Layer_Protection)
* [3] [OWASP TOP 10 2013 - Sensitive Data Exposure](https://www.owasp.org/index.php/Top_10_2013-A6-Sensitive_Data_Exposure)
* [4] [OWASP  ASVS v1.1 - V10 Communication Security Verification Requirements](https://code.google.com/p/owasp-asvs/wiki/Verification_V10)
* [6] [OWASP Testing Guide - Testing for Cookies attributes (OTG-SESS-002)](https://www.owasp.org/index.php/Testing_for_cookies_attributes_%28OTG-SESS-002%29)
