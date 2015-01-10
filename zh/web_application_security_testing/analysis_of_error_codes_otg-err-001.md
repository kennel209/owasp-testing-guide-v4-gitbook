# 错误码分析 (OTG-ERR-001)


### 综述

通常在Web应用的渗透测试中，我们会遇到许多应用服务器产生的错误返回码。通过使用工具和手工特殊构造的特定请求，我们可以触发这些错误。这些错误码可能对于测试者非常有用，因为他们会揭示许多数据库的信息、漏洞信息或者其他应用程序使用的相关组件信息。

这章节分析这些常用的返回码（和错误消息）并关注他们对应用的关系。在这个分析活动中，最关键的部分是将注意力着眼于产生的错误上面，将这些错误视为一系列帮助我们进行下一步分析的信息。一个好的信息集合能降低实施测试的时间，从而提升漏洞评估的效率。

攻击者有时候使用搜索引擎来找出暴露信息的错误位置。搜索随机受害站点的错误信息，或使用搜索引擎过滤工具来查找指定站点的错误信息，参见[搜索引擎发现和信息泄漏侦查 (OTG-INFO-001)](https://www.owasp.org/index.php/Conduct_search_engine_discovery/reconnaissance_for_information_leakage_%28OTG-INFO-001%29)。


#### Web服务错误

在测试中我们常见的错误是HTTP 404 页面不存在。通常，这个错误码提供了关于目标web服务器和相关组件的有用细节。比如：

```
Not Found
The requested URL /page.html was not found on this server.
Apache/2.2.3 (Unix) mod_ssl/2.2.3 OpenSSL/0.9.7g  DAV/2 PHP/5.1.2 Server at localhost Port 80
```

这个错误消息可以通过请求一个不存在的URL来生成。除了页面不存在的常见消息，还伴随着一下关于web服务器版本、操作系统、模块组件和其他用到的产品的信息。这些信息从鉴别操作系统和应用类型的角度来看是非常重要的。

其他HTTP响应码比如400 错误请求、405 方法不允许、501 方法未实现、408 请求超时和505 HTTP 版本不支持也能被攻击者强制触发。当收到特定构造的请求时，web服务器会基于其HTTP实现来响应相关请求。

测试web服务器错误码信息暴露在[识别Web服务器 (OTG-INFO-002)](https://www.owasp.org/index.php/Fingerprint_Web_Server_%28OTG-INFO-002%29)的相关HTTP头信息暴露章节中也有描述。

#### 应用程序错误

应用程序错误通常由应用程序本身返回，而不是web服务器。这些错误可能是来自代码框架（ASP，JSP等等）的错误消息或者应用程序代码烦恼会的特定错误。这些详细的应用程序错误通常提供关于服务器路径、安装软件情况和应用程序版本信息。

#### 数据库错误

数据库错误通常在数据库查询或连接时发生问题，由数据库系统返回。每个数据库系统比如MySQL，Oracle或MSSQL，都有着自己的错误代码。这些错误可能提供敏感信息比如数据库服务器IP信息、数据库表、列信息和登陆细节。

此外，许多SQL注入利用技巧也使用了数据库返回的消息错误消息，参见[测试SQL注入 (OTG-INPVAL-005)](https://www.owasp.org/index.php/Testing_for_SQL_Injection_%28OTG-INPVAL-005%29)章节来进一步了解相关信息。

在安全分析中，Web服务器错误不是唯一的有用的输出。考虑下面这个错误消息例子：

```
Microsoft OLE DB Provider for ODBC Drivers (0x80004005)
[DBNETLIB][ConnectionOpen(Connect())] - SQL server does not exist or access denied
```

发生了什么情况？我们下面将一步一步为你分析。

在这个例子中，80004005是一个通用的ISS返回错误码，他表明无法与相关数据库建立连接。在许多情况下，错误消息会详细说明数据库类型。这通常也能关联揭示底层的操作系统信息。通过这些信息，渗透测试人员可以做出安全测试的大致策略。

通过操纵数据库连接字符串的值，我们可以获取更详细的错误信息。

```
Microsoft OLE DB Provider for ODBC Drivers error '80004005'
[Microsoft][ODBC Access 97 ODBC driver Driver]General error Unable to open registry key 'DriverId'
```

在这个例子中，我们发现同样的通用错误信息揭示相关数据库类型和版本，以及一个需要的Windows注册表项。

现在我们将通过一个实际的安全测试例子，这个例子的对象是一个无法连接数据库服务器并处理异常的控制行为的web应用程序。这可能由于数据库名称无法进行解析，或处理非预期的变量和其他网络问题引起。

考虑这样一个场景，我们已经拥有了一个数据库管理web入口，这样我们可以通过前端图形界面来进行数据库查询、创建新表和修改数据库。在POST登陆过程中出现了下面的消息。这些消息指明了MySQL数据库的存在：

```
Microsoft OLE DB Provider for ODBC Drivers (0x80004005)
[MySQL][ODBC 3.51 Driver]Unknown MySQL server host
```

如果我们查看登陆HTML页面的源代码，我们可以发一个含有数据库IP地址的 **隐藏域** 我们可以尝试更改这个IP为渗透测试者控制的数据库服务器来尝试迷惑应用程序，使他认为登陆是成功的。

另一个例子：已知后台的数据库服务器类型，我们可以利用这个信息来对该数据库进行SQL注入攻击或存储式XSS测试。


### 如何测试

下面是一些测试详细错误消息的例子。每一个例子都展示了操作系统和应用程序版本等等信息。

**测试: 404 Not Found**
```
telnet <host target> 80
GET /<wrong page> HTTP/1.1
host: <host target>
<CRLF><CRLF>
```
**结果:**
```
HTTP/1.1 404 Not Found
Date: Sat, 04 Nov 2006 15:26:48 GMT
Server: Apache/2.2.3 (Unix) mod_ssl/2.2.3 OpenSSL/0.9.7g
Content-Length: 310
Connection: close
Content-Type: text/html; charset=iso-8859-1
...
<title>404 Not Found</title>
...
<address>Apache/2.2.3 (Unix) mod_ssl/2.2.3 OpenSSL/0.9.7g at <host target> Port 80</address>
...
```


**测试:**
```
导致无法连接数据库服务器的网络问题
```
**结果:**
```
Microsoft OLE DB Provider for ODBC Drivers (0x80004005) '
[MySQL][ODBC 3.51 Driver]Unknown MySQL server host
```


**测试:**
```
缺乏登陆凭证导致认证失败
```
**结果:**

用于认证的防火墙版本信息：
```
Error 407
FW-1 at <firewall>: Unauthorized to access the document.
•  Authorization is needed for FW-1.
•  The authentication required by FW-1 is: unknown.
•  Reason for failure of last attempt: no user
```


**测试: 400 Bad Request**
```
telnet <host target> 80
GET / HTTP/1.1
<CRLF><CRLF>
```
**结果:**
```
HTTP/1.1 400 Bad Request
Date: Fri, 06 Dec 2013 23:57:53 GMT
Server: Apache/2.2.22 (Ubuntu) PHP/5.3.10-1ubuntu3.9 with Suhosin-Patch
Vary: Accept-Encoding
Content-Length: 301
Connection: close
Content-Type: text/html; charset=iso-8859-1
...
<title>400 Bad Request</title>
...
<address>Apache/2.2.22 (Ubuntu) PHP/5.3.10-1ubuntu3.9 with Suhosin-Patch at 127.0.1.1 Port 80</address>
...
```


**测试: 405 Method Not Allowed**
```
telnet <host target> 80
PUT /index.html HTTP/1.1
Host: <host target>
<CRLF><CRLF>
```
**结果:**
```
HTTP/1.1 405 Method Not Allowed
Date: Fri, 07 Dec 2013 00:48:57 GMT
Server: Apache/2.2.22 (Ubuntu) PHP/5.3.10-1ubuntu3.9 with Suhosin-Patch
Allow: GET, HEAD, POST, OPTIONS
Vary: Accept-Encoding
Content-Length: 315
Connection: close
Content-Type: text/html; charset=iso-8859-1
...
<title>405 Method Not Allowed</title>
...
<address>Apache/2.2.22 (Ubuntu) PHP/5.3.10-1ubuntu3.9 with Suhosin-Patch at <host target> Port 80</address>
...
```


**测试: 408 Request Time-out**
```
telnet <host target> 80
GET / HTTP/1.1
-   等待X秒钟（取决于目标服务器，Apache服务器默认为21秒）
```
**结果:**
```
HTTP/1.1 408 Request Time-out
Date: Fri, 07 Dec 2013 00:58:33 GMT
Server: Apache/2.2.22 (Ubuntu) PHP/5.3.10-1ubuntu3.9 with Suhosin-Patch
Vary: Accept-Encoding
Content-Length: 298
Connection: close
Content-Type: text/html; charset=iso-8859-1
...
<title>408 Request Time-out</title>
...
<address>Apache/2.2.22 (Ubuntu) PHP/5.3.10-1ubuntu3.9 with Suhosin-Patch at <host target> Port 80</address>
...
```



**测试: 501 Method Not Implemented**
```
telnet <host target> 80
RENAME /index.html HTTP/1.1
Host: <host target>
<CRLF><CRLF>
```
**结果:**
```
HTTP/1.1 501 Method Not Implemented
Date: Fri, 08 Dec 2013 09:59:32 GMT
Server: Apache/2.2.22 (Ubuntu) PHP/5.3.10-1ubuntu3.9 with Suhosin-Patch
Allow: GET, HEAD, POST, OPTIONS
Vary: Accept-Encoding
Content-Length: 299
Connection: close
Content-Type: text/html; charset=iso-8859-1
...
<title>501 Method Not Implemented</title>
...
<address>Apache/2.2.22 (Ubuntu) PHP/5.3.10-1ubuntu3.9 with Suhosin-Patch at <host target> Port 80</address>
...
```

**测试:**
```
通过拒绝访问错误信息枚举目录：

http://<host>/<dir>
```
**结果:**
```
Directory Listing Denied
This Virtual Directory does not allow contents to be listed.
```
```
Forbidden
You don't have permission to access /<dir> on this server.
```


### 测试工具
* [1] ErrorMint - http://sourceforge.net/projects/errormint/ <br>
* [2] ZAP Proxy - https://www.owasp.org/index.php/OWASP_Zed_Attack_Proxy_Project <br>

### 参考资料

* [1] [[RFC2616](http://www.ietf.org/rfc/rfc2616.txt?number=2616)] Hypertext Transfer Protocol -- HTTP/1.1
* [2] [[ErrorDocument](http://httpd.apache.org/docs/2.2/mod/core.html#errordocument)] Apache ErrorDocument Directive
* [3] [[AllowOverride](http://httpd.apache.org/docs/2.2/mod/core.html#allowoverride)] Apache AllowOverride Directive
* [4] [[ServerTokens](http://httpd.apache.org/docs/2.2/mod/core.html#servertokens)] Apache ServerTokens Directive
* [5] [[ServerSignature](http://httpd.apache.org/docs/2.2/mod/core.html#serversignature)] Apache ServerSignature Directive

### 整改措施

#### IIS和ASP.net中的错误处理

ASP.net是来自微软的常用web应用框架。IIS是一个常用的web服务器。所有应用程序都会发生错误，开发者尝试捕获大部分的错误，但几乎不可能覆盖所有异常（但是可能配置web服务器来向用户隐藏这些详细的错误信息）。

IIS使用一系列自定义的错误页面，通常能在c:\winnt\help\iishelp\common目录下找到，比如“404 页面无法访问”。这些默认页面可以更改，自定义的错误也能在IIS服务器中配置。当IIS服务器接收一个aspx页面请求时，这个请求将被传递给.NET框架。

在.NET框架中有许多不同处理错误的方法，在ASP.net中，有如下三个地方可以处理错误：

1. 在 Web.config 的 customErrors 节中
2. 在 global.asax 的 Application_Error 子过程中
3. 在 aspx中或Page_Error子过程中相关的代码处理页面中


**使用web.config处理错误**
```
<customErrors defaultRedirect="myerrorpagedefault.aspx" mode="On|Off|RemoteOnly">
   <error statusCode="404" redirect="myerrorpagefor404.aspx"/>
   <error statusCode="500" redirect="myerrorpagefor500.aspx"/>
</customErrors>
```

mode="On" 将开启自定义错误消息。 mode=RemoteOnly 将对远程应用程序用户显示自定义错误消息。本地访问用户会得到完整的堆栈情况的信息，而不是自定义的错误页面。

所有错误，除了显示指定的，都会跳转到defaultRedirect指定的页面。如myerrorpagedefault.aspx。所有状态码为404的页面将会跳转为myerrorpagefor404。


**在Global.asax中处理错误**

当错误发生时候，Application_Error子过程被调用。开发者可以在这个子过程中为错误处理/页面编写代码。

```
Private Sub Application_Error (ByVal sender As Object, ByVal e As System.EventArgs)
     Handles MyBase.Error
End Sub
```


**在Page_Error子过程中处理错误**

类似应用程序错误。

```
Private Sub Page_Error (ByVal sender As Object, ByVal e As System.EventArgs)
     Handles MyBase.Error
End Sub
```


**ASP.net中错误处理顺序**

Page_Error子过程将被最先处理，接着是global.asax中的Application_Error子过程，最后是web.config文件中的customErrors节中定义的内容。

服务器端的web应用程序信息收集非常困难，但是在这里发现的信息非常有利于正确的漏洞利用（比如，SQL注入或者XSS攻击），同时也能减少误报。


**如何测试ASP.net和IIS中的错误处理**

打开你的浏览器，并输入随机名字页面:

```
http:\\www.mywebserver.com\anyrandomname.asp
```

如果页面返回下面信息:

```
The page cannot be found

Internet Information Services
```

这意味着IIS自定义错误页面没有开启。请注意.asp扩展。

同时也测试.net自定义错误页面。输入aspx后缀的随机页面名字:

```
http:\\www.mywebserver.com\anyrandomname.aspx
```

如果服务器返回：

```
Server Error in '/' Application.
--------------------------------------------------------------------------------

The resource cannot be found.
Description: HTTP 404. The resource you are looking for (or one of its dependencies) could have been removed, had its name changed, or is temporarily unavailable. Please review the following URL and make sure that it is spelled correctly.
```

那么.net的自定义页面没有开启。

#### Apache服务器中的错误处理

Apache是一个常见的处理HTML和PHP网页的HTTP服务器。默认情况下，Apache服务器会在HTTP错误响应中显示服务器版本、已安装产品和操作系统信息。

这些错误响应可以在全局环境中配置和自定义，在apache2.conf下的每个站点或每个目录中使用ErrorDocument指示符来配置[2]:

```
ErrorDocument 404 “Customized Not Found error message”
ErrorDocument 403 /myerrorpagefor403.html
ErrorDocument 501 http://www.externaldomain.com/errorpagefor501.html
```

如果在apache2.conf [3]中全局指示符AllowOverride被正确配置，那么站点管理员可以使用.htaccess文件来定义自己的错误页面。

HTTP错误显示的信息可以通过配置apache2.conf配置文件中的ServerTokens指示符[4]和ServerSignature指示符[5]来控制。“ServerSignature Off” （默认开启）能在错误响应消息中除去服务器信息，而ServerTokens [ProductOnly|Major|Minor|Minimal|OS|Full] （默认Full）定义了错误页面中将展示什么信息。


#### Tomcat服务器中的错误处理

Tomcat服务器是一个处理JSP和Java Servlet应用程序的HTTP服务器。默认情况下Tomcat服务器在HTTP错误响应消息中现实服务器版本信息。

可以在web.xml配置文件中自定义错误响应。

```
<error-page>
    <error-code>404</error-code>
    <location>/myerrorpagefor404.html</location>
</error-page>
```

