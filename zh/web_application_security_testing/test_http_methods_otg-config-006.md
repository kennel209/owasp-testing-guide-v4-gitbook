# 测试HTTP方法 (OTG-CONFIG-006)


### 综述
HTTP 提供了一系列的方法来与服务器交互。许多被设计来用作辅助开发者进行部署可测试HTTP应用。这些HTTP方法可能被用于邪恶的目的，如果web服务器被错误配置。此外跨站点追踪（Cross Site Tracing，XST），一种跨站脚本的形式使用了服务器的HTTP TRACE方法。

虽然GET和POST是目前被用于访问web服务器提供的信息的常用方法，但超文本传输协议（Hypertext Transfer Protocol，HTTP）也允许一些其他方法（不那么知名）。RFC 2616（现在的标准，描述了HTTP 版本1.1）定义了下面8个方法：

* HEAD
* GET
* POST
* PUT
* DELETE
* TRACE
* OPTIONS
* CONNECT


上述的一些方法可能潜在造成web应用的安全风险，因为他们允许攻击者修改存储在web服务器上的文件，以及在一些场景中，可以盗取合法用户的凭证。特别是如下这些方法应该被禁止使用：

* PUT: 这个方法允许客户端向web服务器上传新的文件。攻击者可以利用他来上传恶意文件（比如一个asp文件通过调用cmd.exe来执行命令），或者简单使用受害者服务器作为文件仓库。
* DELETE: 这个方法允许客户端删除web服务器上的一个文件。攻击者能利用他简单直接破坏网站或者实施拒绝服务攻击。
* CONNECT: 这个方法允许客户端使用web服务器作为代理。
* TRACE: 这个方法简单返回客户端发送给服务器的所有信息，主要用于调试目的。这个方法最初被认为没有危害，被Jermiah Grossman发现能被用于实施XST（见最下面链接）。


如果应用需要一个或多个上述方法，比如REST Web 服务（可能需要PUT或DELETE），检查他们被正确限于可信用户和安全条件下使用。


#### 任意HTTP方法

Arshan Dabirsiaghi（参见链接）发现许多web应用框架也允许自选的或者任意的HTTP方法来绕过环境级别的访问控制检查：

* 许多框架和语言处理 "HEAD" 就如同 "GET" 一样，虽然可能响应中不带有任何信息。但是如果 "GET" 中设置了安全约束条件只允许认证用户访问特定容器或资源，那么这些约束可能被 "HEAD" 版本绕过。

* 一些框架允许任意HTTP方法如 "JEFF" 或 "CATS"，没有任何使用限制，如果他们如同 "GET" 请求一样处理，那么他们可能不被基于角色的权限控制机制检查，再一次绕过了GET请求，获得特权。


在很多例子中，显示检查 "GET" 和 "POST" 的代码风格才能更加安全。


### 如何测试

**发现支持的方法** <br>
测试者需要找出web服务器支持的HTTP方法。OPTIONS HTTP方法能提供测试者最直接的和便捷的方法。RFC 2616中这么写道：“OPTIONS方法代表一个请求，请求关于请求URI中用于请求/响应链的可用的通信选项的信息。


这个测试很容易，我们只需要使用netcat（或telnet）：
```
$ nc www.victim.com 80
OPTIONS / HTTP/1.1
Host: www.victim.com

HTTP/1.1 200 OK
Server: Microsoft-IIS/5.0
Date: Tue, 31 Oct 2006 08:00:29 GMT
Connection: close
Allow: GET, HEAD, POST, TRACE, OPTIONS
Content-Length: 0

```


如例子中所示，OPTIONS 提供了web服务器支持的HTTP方法列表，在这个例子中，我们发现服务器启用了TRACE方法。关于这个方法的危害将在后面章节中描述。

**测试潜在的XST**<br>
注意： 为了理解这个攻击的逻辑和目标，攻击者必须熟悉 [跨站脚本攻击（XSS）](https://www.owasp.org/index.php/XSS)。


TRACE方法，看上去没有危害，但能在某些场景下成功被利用并盗取合法用户的凭证。这个攻击技巧被Jeremiah Grossman在2003年发现，一次企图绕过 [HTTPOnly](https://www.owasp.org/index.php/HTTPOnly) 标签，以及微软引进IE6 SP1来保护cookies被JavaScript访问。事实上，XSS上最常见的攻击模式是获取document.cookie，并将它 As a matter of fact, one of the most recurring attack patterns in Cross Site Scripting is to access the document.cookie object and send it to a web server controlled by the attacker so that he or she can hijack the victim's session. Tagging a cookie as httpOnly forbids JavaScript from accessing it, protecting it from being sent to a third party. However, the TRACE method can be used to bypass this protection and access the cookie even in this scenario.


As mentioned before, TRACE simply returns any string that is sent to the web server. In order to verify its presence (or to double-check the results of the OPTIONS request shown above), the tester can proceed as shown in the following example:
```
$ nc www.victim.com 80
TRACE / HTTP/1.1
Host: www.victim.com

HTTP/1.1 200 OK
Server: Microsoft-IIS/5.0
Date: Tue, 31 Oct 2006 08:01:48 GMT
Connection: close
Content-Type: message/http
Content-Length: 39

TRACE / HTTP/1.1
Host: www.victim.com
```


The response body is exactly a copy of our original request, meaning that the target allows this method. Now, where is the danger lurking? If the tester instructs a browser to issue a TRACE request to the web server, and this browser has a cookie for that domain, the cookie will be automatically included in the request headers, and will therefore be echoed back in the resulting response. At that point, the cookie string will be accessible by JavaScript and it will be finally possible to send it to a third party even when the cookie is tagged as httpOnly.


There are multiple ways to make a browser issue a TRACE request, such as the XMLHTTP ActiveX control in Internet Explorer and XMLDOM in Mozilla and Netscape. However, for security reasons the browser is allowed to start a connection only to the domain where the hostile script resides. This is a mitigating factor, as the attacker needs to combine the TRACE method with another vulnerability in order to mount the attack.


An attacker has two ways to successfully launch a Cross Site Tracing attack:
* Leveraging another server-side vulnerability: the attacker injects the hostile JavaScript snippet that contains the TRACE request in the vulnerable application, as in a normal Cross Site Scripting attack
* Leveraging a client-side vulnerability: the attacker creates a malicious website that contains the hostile JavaScript snippet and exploits some cross-domain vulnerability of the browser of the victim, in order to make the JavaScript code successfully perform a connection to the site that supports the TRACE method and that originated the cookie that the attacker is trying to steal.


More detailed information, together with code samples, can be found in the original whitepaper written by Jeremiah Grossman.<br>


#### Testing for arbitrary HTTP methods

Find a page to visit that has a security constraint such that it would normally force a 302 redirect to a log in page or forces a log in directly. The test URL in this example works like this, as do many web applications. However, if a tester obtains a "200" response that is not a log in page, it is possible to bypass authentication and thus authorization.

```
$ nc www.example.com 80
JEFF / HTTP/1.1
Host: www.example.com

HTTP/1.1 200 OK
Date: Mon, 18 Aug 2008 22:38:40 GMT
Server: Apache
Set-Cookie: PHPSESSID=K53QW...
```


If the framework or firewall or application does not support the "JEFF" method, it should issue an error page (or preferably a 405 Not Allowed or 501 Not implemented error page). If it services the request, it is vulnerable to this issue.


If the tester feels that the system is vulnerable to this issue, they should issue CSRF-like attacks to exploit the issue more fully:

* FOOBAR /admin/createUser.php?member=myAdmin
* JEFF /admin/changePw.php?member=myAdmin&passwd=foo123&confirm=foo123
* CATS /admin/groupEdit.php?group=Admins&member=myAdmin&action=add


With some luck, using the above three commands - modified to suit the application under test and testing requirements - a new user would be created, a password assigned, and made an administrator.


#### Testing for HEAD access control bypass

Find a page to visit that has a security constraint such that it would normally force a 302 redirect to a log in page or forces a log in directly. The test URL in this example works like this, as do many web applications. However, if the tester obtains a "200" response that is not a login page, it is possible to bypass authentication and thus authorization.

```
$ nc www.example.com 80
HEAD /admin HTTP/1.1
Host: www.example.com

HTTP/1.1 200 OK
Date: Mon, 18 Aug 2008 22:44:11 GMT
Server: Apache
Set-Cookie: PHPSESSID=pKi...; path=/; HttpOnly
Expires: Thu, 19 Nov 1981 08:52:00 GMT
Cache-Control: no-store, no-cache, must-revalidate, post-check=0, pre-check=0
Pragma: no-cache
Set-Cookie: adminOnlyCookie1=...; expires=Tue, 18-Aug-2009 22:44:31 GMT; domain=www.example.com
Set-Cookie: adminOnlyCookie2=...; expires=Mon, 18-Aug-2008 22:54:31 GMT; domain=www.example.com
Set-Cookie: adminOnlyCookie3=...; expires=Sun, 19-Aug-2007 22:44:30 GMT; domain=www.example.com
Content-Language: EN
Connection: close
Content-Type: text/html; charset=ISO-8859-1
```


If the tester gets a "405 Method not allowed" or "501 Method Unimplemented", the target (application/framework/language/system/firewall) is working correctly. If a "200" response code comes back, and the response contains no body, it's likely that the application has processed the request without authentication or authorization and further testing is warranted.

If the tester thinks that the system is vulnerable to this issue, they should issue CSRF-like attacks to exploit the issue more fully:

* HEAD /admin/createUser.php?member=myAdmin
* HEAD /admin/changePw.php?member=myAdmin&passwd=foo123&confirm=foo123
* HEAD /admin/groupEdit.php?group=Admins&member=myAdmin&action=add


With some luck, using the above three commands - modified to suit the application under test and testing requirements - a new user would be created, a password assigned, and made an administrator, all using blind request submission.


### Tools
* NetCat - http://nc110.sourceforge.net
* cURL - http://curl.haxx.se/


### References
**Whitepapers**<br>
* RFC 2616: "Hypertext Transfer Protocol -- HTTP/1.1"
* RFC 2109 and RFC 2965: "HTTP State Management Mechanism"
* Jeremiah Grossman: "Cross Site Tracing (XST)" - http://www.cgisecurity.com/whitehat-mirror/WH-WhitePaper_XST_ebook.pdf<br>
* Amit Klein: "XS(T) attack variants which can, in some cases, eliminate the need for TRACE" - http://www.securityfocus.com/archive/107/308433
* Arshan Dabirsiaghi: "Bypassing VBAAC with HTTP Verb Tampering" - http://static.swpag.info/download/Bypassing_VBAAC_with_HTTP_Verb_Tampering.pdf
