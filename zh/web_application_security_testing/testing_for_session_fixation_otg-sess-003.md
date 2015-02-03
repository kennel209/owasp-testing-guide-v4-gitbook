# 测试会话固定 (OTG-SESS-003)


### 综述
当应用程序在用户成功登陆之后不更新他们的会话cookie时候，那么有可能存在会话固定的漏洞，使得攻击者可以偷取用户会话（会话劫持）。

会话固定漏洞在下面情况下会发生：
* 应用程序在没有销毁已经存在的会话ID的情况下进行用户认证，因此可以继续使用该会话ID。
* 攻击者可以强制用户使用一个已知的会话ID，一旦用户通过验证，攻击者就可以访问这个已知的认证后的会话。

会话固定漏洞通常的利用过程是，攻击者在web应用程序上创建新的会话，并记录相关的会话ID。然后诱使受害者使用该会话ID进行再次认证，借此来获得能够访问用户账户的合法会话。

更进一步来说，那些在HTTP上赋予会话ID，并重定向到HTTPS登录表单中的过程中也可能存在这问题。如果会话ID不在用户认证过程中重新生成，攻击者仍然能够监听并盗取该会话ID，进而劫持该会话。

### 如何测试
#### 黑盒测试

**测试会话固定漏洞：**

第一步是向被测站点发出请求（如www.example.com）。假设测试者发起如下请求：
```
 GET www.example.com
```
可能获得如下响应：
```
HTTP/1.1 200 OK
Date: Wed, 14 Aug 2008 08:45:11 GMT
Server: IBM_HTTP_Server
Set-Cookie: JSESSIONID=0000d8eyYq3L0z2fgq10m4v-rt4:-1; Path=/; secure
Cache-Control: no-cache="set-cookie,set-cookie2"
Expires: Thu, 01 Dec 1994 16:00:00 GMT
Keep-Alive: timeout=5, max=100
Connection: Keep-Alive
Content-Type: text/html;charset=Cp1254
Content-Language: en-US
```

应用程序设置了一个新的会话标识`JSESSIONID=0000d8eyYq3L0z2fgq10m4v-rt4:-1`。

接着，如果测试者能通过如下HTTPS POST请求获取认证：
```
POST https://www.example.com/authentication.php HTTP/1.1
Host: www.example.com
User-Agent: Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.16) Gecko/20080702 Firefox/2.0.0.16
Accept: text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5
Accept-Language: it-it,it;q=0.8,en-us;q=0.5,en;q=0.3
Accept-Encoding: gzip,deflate
Accept-Charset: ISO-8859-1,utf-8;q=0.7,*;q=0.7
Keep-Alive: 300
Connection: keep-alive
Referer: http://www.example.com
Cookie: JSESSIONID=0000d8eyYq3L0z2fgq10m4v-rt4:-1
Content-Type: application/x-www-form-urlencoded
Content-length: 57

Name=Meucci&wpPassword=secret!&wpLoginattempt=Log+in
```
可以观察到如下响应：
```
HTTP/1.1 200 OK
Date: Thu, 14 Aug 2008 14:52:58 GMT
Server: Apache/2.2.2 (Fedora)
X-Powered-By: PHP/5.1.6
Content-language: en
Cache-Control: private, must-revalidate, max-age=0
X-Content-Encoding: gzip
Content-length: 4090
Connection: close
Content-Type: text/html; charset=UTF-8
...
HTML data
...
```

在成功认证之后并没有新的cookie产生，那么测试者就可能实施会话劫持。

**期望结果:**

测试者能够向用户发送合法的会话标识（可能使用一些社会工程学技巧），并等待用户进行登录认证，接着验证cookie是否被分配到了相应权限。

#### 灰盒测试

与开发者进行讨论，并弄明白他们是否实现了用户成功登录后会话令牌更新机制。

**期待结果:**

应用程序首先应该在进行用户认证之前销毁已经存在的会话ID，然后在用户成功认证之后提供新的会话ID。


### 测试工具
* JHijack - a numeric session hijacking tool - http://yehg.net/lab/pr0js/files.php/jhijackv0.2beta.zip
* OWASP WebScarab: [OWASP_WebScarab_Project](https://www.owasp.org/index.php/OWASP_WebScarab_Project)


### 参考资料
**白皮书**

* [Session Fixation](https://www.owasp.org/index.php/Session_Fixation)
* ACROS Security: http://www.acrossecurity.com/papers/session_fixation.pdf
* Chris Shiflett: http://shiflett.org/articles/session-fixation

