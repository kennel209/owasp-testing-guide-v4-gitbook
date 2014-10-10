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


TRACE方法，看上去没有危害，但能在某些场景下成功被利用并盗取合法用户的凭证。这个攻击技巧被Jeremiah Grossman在2003年发现，一次企图绕过 [HTTPOnly](https://www.owasp.org/index.php/HTTPOnly) 标签，以及微软引进IE6 SP1来保护cookies被JavaScript访问。事实上，XSS上最常见的攻击模式是获取document.cookie，并将它发到攻击者控制的服务器，以便于攻击者能够劫持受害者的会话。标记为httponly的cookie禁止JavaScript访问，被保护无法发送给第三方。然而TRACE方法能用于绕过这层防护已经在上述场景里访问cookie。


正如先前提到的，TRACE简单返回任何发送给服务器的字符串。为了证明方法可行（或使用OPTIONS请求），测试者像如下例子中操作：
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


响应主体正好是我们原始请求的拷贝，意味着目标允许这个方法。现在哪里潜伏危机？如果测试者指示浏览器向web服务器发起TRACE请求，并且浏览器存在该域名的cookie，这个cookie会自动包含在请求头中，如此会在响应结果中回显。此时，cookie能被JavaScript访问并最后可能发送给第三方即使这个cookie是标记为httpOnly的。


有多种方式使浏览器发送TRACE请求，比如IE中的XMLHTTP ActiveX控件，Mozilla和Nescape的XMLDOM。然而，由于安全原因，浏览器只允许从恶意脚本存在的域名发起这样连接。这是一个缓解因素，因为攻击者需要结合其他漏洞和TRACE方法来完成攻击。


一个攻击者有两种成功实施XST攻击的方法：
* 利用其他服务器端漏洞：攻击者向漏洞应用注入包含TRACE请求的恶意JavaScript代码就像正常XSS攻击那样。
* 利用客户端漏洞：攻击者创建一个恶意站点包含恶意JS代码和浏览器的跨域漏洞利用程序，使JS代码能成功发起支持TRACE方法和目标cookie的请求。


更多的信息和代码例子能从Jeremah Grossman的白皮书中找到。


#### 测试任意HTTP方法

找到一个页面含有安全约束控制使通常访问强制返回302跳转到登陆页面或强制登陆。这个测试URL在下面例子中是这么工作的，如同许多web应用那样。然后，如果测试者获得一个200响应却又不是登陆页面，那么他可能绕过了认证和授权过程。

```
$ nc www.example.com 80
JEFF / HTTP/1.1
Host: www.example.com

HTTP/1.1 200 OK
Date: Mon, 18 Aug 2008 22:38:40 GMT
Server: Apache
Set-Cookie: PHPSESSID=K53QW...
```


如果框架或者防火墙或应用不支持"JEFF"方法，那么他应该指向一个错误页面（更好的是返回405响应不允许，或者501响应未实现错误页面）。如果服务器产生正常应答，那么这可能是一个漏洞。


如果测试者觉得系统存在这个漏洞，他们应该发起一些像CSRF一样的攻击来利用这个问题，比如：

* FOOBAR /admin/createUser.php?member=myAdmin
* JEFF /admin/changePw.php?member=myAdmin&passwd=foo123&confirm=foo123
* CATS /admin/groupEdit.php?group=Admins&member=myAdmin&action=add


如果足够幸运，使用上面三个命令 - 修改符合适合测试情况的需求 - 一个新的管理员用户将被建立，并分配了密码。


#### 测试HEAD访问控制绕过

找到一个页面含有安全约束控制使通常访问强制返回302跳转到登陆页面或强制登陆。这个测试URL在下面例子中是这么工作的，如同许多web应用那样。然后，如果测试者获得一个200响应却又不是登陆页面，那么他可能绕过了认证和授权过程。

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


如果攻击者得到 “405 方法不允许” 或 “501 方法未实现”，那么目标（应用/框架/语言/系统/防火墙）是正确工作的。如果返回200响应，而且不存在响应主体，那么很可能应用在没有认证和授权的情况下处理了请求，需要进一步测试。

如果测试者觉得系统存在这个漏洞，他们应该发起一些像CSRF一样的攻击来利用这个问题，比如：

* HEAD /admin/createUser.php?member=myAdmin
* HEAD /admin/changePw.php?member=myAdmin&passwd=foo123&confirm=foo123
* HEAD /admin/groupEdit.php?group=Admins&member=myAdmin&action=add


如果足够幸运，使用上面三个命令 - 修改符合适合测试情况的需求 - 一个新的管理员用户将被建立，并分配了密码，所有过程使用了盲请求提交。


### 测试工具
* NetCat - http://nc110.sourceforge.net
* cURL - http://curl.haxx.se/


### 参考资料
**白皮书**<br>
* RFC 2616: "Hypertext Transfer Protocol -- HTTP/1.1"
* RFC 2109 and RFC 2965: "HTTP State Management Mechanism"
* Jeremiah Grossman: "Cross Site Tracing (XST)" - http://www.cgisecurity.com/whitehat-mirror/WH-WhitePaper_XST_ebook.pdf<br>
* Amit Klein: "XS(T) attack variants which can, in some cases, eliminate the need for TRACE" - http://www.securityfocus.com/archive/107/308433
* Arshan Dabirsiaghi: "Bypassing VBAAC with HTTP Verb Tampering" - http://static.swpag.info/download/Bypassing_VBAAC_with_HTTP_Verb_Tampering.pdf
