# 识别Web服务器 (OTG-INFO-002)

### 综述
对于渗透测试人员来说，识别Web服务器是一项十分关键的任务。了解正在运行的服务器类型和版本能让测试者更好去测试已知漏洞和大概的利用方法。


今天市场上存在着许多不同开发商不同版本的Web服务器。明确被测试的服务器类型能够有效帮助测试过程和决定测试的流程。这些信息可以通过发送给web服务器测定命令，分析输出结果来推断出，因为不同版本的web服务器软件可能对这些命令有着不同的响应。通过了解不同服务器对于不同命令的响应，并把这些信息保存在指纹数据库中，测试者可以发送请求，分析响应，并与数据库中的已知签名相对比。请注意，由于不同版本的服务器对于同一个请求可能有同样的响应，所以可能需要多个命令请求才能准确识别web服务器。十分罕见的，也有不同版本的服务器响应的请求毫无差别。因此，通过发送不同的命令请求，测试者能增加猜测的准确度。


### 测试目标
发现运行的服务器的版本和类型，来决定已知漏洞和利用方式。


### 如何测试

#### 黑盒测试
最简单也是最基本的方法来鉴别web服务器就是查看HTTP响应头中的"Server"字段。下面实验中我们使用Netcat：


考虑如下HTTP请求响应对：
```
$ nc 202.41.76.251 80
HEAD / HTTP/1.0

HTTP/1.1 200 OK
Date: Mon, 16 Jun 2003 02:53:29 GMT
Server: Apache/1.3.3 (Unix)  (Red Hat/Linux)
Last-Modified: Wed, 07 Oct 1998 11:18:14 GMT
ETag: "1813-49b-361b4df6"
Accept-Ranges: bytes
Content-Length: 1179
Connection: close
Content-Type: text/html
```


从*Server*字段，我们可以发现服务器可能是Apache，版本1.3.3，运行在Linux系统上。

下面展示了4个其他服务器响应的例子。

**Apache 1.3.23** 服务器：
```
HTTP/1.1 200 OK
Date: Sun, 15 Jun 2003 17:10: 49 GMT
Server: Apache/1.3.23
Last-Modified: Thu, 27 Feb 2003 03:48: 19 GMT
ETag: 32417-c4-3e5d8a83
Accept-Ranges: bytes
Content-Length: 196
Connection: close
Content-Type: text/HTML
```

**Microsoft IIS 5.0** 服务器：
```
HTTP/1.1 200 OK
Server: Microsoft-IIS/5.0
Expires: Yours, 17 Jun 2003 01:41: 33 GMT
Date: Mon, 16 Jun 2003 01:41: 33 GMT
Content-Type: text/HTML
Accept-Ranges: bytes
Last-Modified: Wed, 28 May 2003 15:32: 21 GMT
ETag: b0aac0542e25c31: 89d
Content-Length: 7369
```

**Netscape Enterprise 4.1** 服务器：
```
HTTP/1.1 200 OK
Server: Netscape-Enterprise/4.1
Date: Mon, 16 Jun 2003 06:19: 04 GMT
Content-type: text/HTML
Last-modified: Wed, 31 Jul 2002 15:37: 56 GMT
Content-length: 57
Accept-ranges: bytes
Connection: close
```

**SunONE 6.1** 服务器：
```
HTTP/1.1 200 OK
Server: Sun-ONE-Web-Server/6.1
Date: Tue, 16 Jan 2007 14:53:45 GMT
Content-length: 1186
Content-type: text/html
Date: Tue, 16 Jan 2007 14:50:31 GMT
Last-Modified: Wed, 10 Jan 2007 09:58:26 GMT
Accept-Ranges: bytes
Connection: close
```


但是，这种测试方法有时候并不准确。网站有多种方法混淆或者改变服务器的标识字段。例如我们可能得到如下结果：
```
403 HTTP/1.1 Forbidden
Date: Mon, 16 Jun 2003 02:41: 27 GMT
Server: Unknown-Webserver/1.0
Connection: close
Content-Type: text/HTML; charset=iso-8859-1
```


在这个例子中，Server字段已经被混淆，测试者并不能从中得到服务器的信息。


#### 协议行为推断
更好的方法是从web服务器的不同特征上入手。下面是一些推断web服务器类型的方法：

**HTTP头字段顺序**

第一个方法通过观察响应头的组织顺序。每个服务器都有一个内部的HTTP头排序方法，考虑如下例子：

**Apache 1.3.23** 响应
```
$ nc apache.example.com 80
HEAD / HTTP/1.0

HTTP/1.1 200 OK
Date: Sun, 15 Jun 2003 17:10: 49 GMT
Server: Apache/1.3.23
Last-Modified: Thu, 27 Feb 2003 03:48: 19 GMT
ETag: 32417-c4-3e5d8a83
Accept-Ranges: bytes
Content-Length: 196
Connection: close
Content-Type: text/HTML
```
**IIS 5.0** 响应
```
$ nc iis.example.com 80
HEAD / HTTP/1.0

HTTP/1.1 200 OK
Server: Microsoft-IIS/5.0
Content-Location: http://iis.example.com/Default.htm
Date: Fri, 01 Jan 1999 20:13: 52 GMT
Content-Type: text/HTML
Accept-Ranges: bytes
Last-Modified: Fri, 01 Jan 1999 20:13: 52 GMT
ETag: W/e0d362a4c335be1: ae1
Content-Length: 133
```
**Netscape Enterprise 4.1** 响应
```
$ nc netscape.example.com 80
HEAD / HTTP/1.0

HTTP/1.1 200 OK
Server: Netscape-Enterprise/4.1
Date: Mon, 16 Jun 2003 06:01: 40 GMT
Content-type: text/HTML
Last-modified: Wed, 31 Jul 2002 15:37: 56 GMT
Content-length: 57
Accept-ranges: bytes
Connection: close
```
**SunONE 6.1** 响应
```
$ nc sunone.example.com 80
HEAD / HTTP/1.0

HTTP/1.1 200 OK
Server: Sun-ONE-Web-Server/6.1
Date: Tue, 16 Jan 2007 15:23:37 GMT
Content-length: 0
Content-type: text/html
Date: Tue, 16 Jan 2007 15:20:26 GMT
Last-Modified: Wed, 10 Jan 2007 09:58:26 GMT
Connection: close
```

我们注意到*Date*和*Server*字段在Apache、Netscape Enterprise和IIS中有所区别。


**畸形的请求测试**

另一个有用测试是发送畸形的请求或者不存在的页面请求，考虑如下HTTP响应：
Consider the following HTTP responses.

**Apache 1.3.23**
```
$ nc apache.example.com 80
GET / HTTP/3.0

HTTP/1.1 400 Bad Request
Date: Sun, 15 Jun 2003 17:12: 37 GMT
Server: Apache/1.3.23
Connection: close
Transfer: chunked
Content-Type: text/HTML; charset=iso-8859-1
```
**IIS 5.0**
```
$ nc iis.example.com 80
GET / HTTP/3.0

HTTP/1.1 200 OK
Server: Microsoft-IIS/5.0
Content-Location: http://iis.example.com/Default.htm
Date: Fri, 01 Jan 1999 20:14: 02 GMT
Content-Type: text/HTML
Accept-Ranges: bytes
Last-Modified: Fri, 01 Jan 1999 20:14: 02 GMT
ETag: W/e0d362a4c335be1: ae1
Content-Length: 133
```
**Netscape Enterprise 4.1**
```
$ nc netscape.example.com 80
GET / HTTP/3.0

HTTP/1.1 505 HTTP Version Not Supported
Server: Netscape-Enterprise/4.1
Date: Mon, 16 Jun 2003 06:04: 04 GMT
Content-length: 140
Content-type: text/HTML
Connection: close
```
**SunONE 6.1**
```
$ nc sunone.example.com 80
GET / HTTP/3.0

HTTP/1.1 400 Bad request
Server: Sun-ONE-Web-Server/6.1
Date: Tue, 16 Jan 2007 15:25:00 GMT
Content-length: 0
Content-type: text/html
Connection: close
```


我们发现每个服务器都有不同的应答方式，而且不同版本也有所不同响应。类似的结果也能通过构造不存在的HTTP方法/谓词来获得。考虑如下例子：

**Apache 1.3.23**
```
$ nc apache.example.com 80
GET / JUNK/1.0

HTTP/1.1 200 OK
Date: Sun, 15 Jun 2003 17:17: 47 GMT
Server: Apache/1.3.23
Last-Modified: Thu, 27 Feb 2003 03:48: 19 GMT
ETag: 32417-c4-3e5d8a83
Accept-Ranges: bytes
Content-Length: 196
Connection: close
Content-Type: text/HTML
```
**IIS 5.0**
```
$ nc iis.example.com 80
GET / JUNK/1.0

HTTP/1.1 400 Bad Request
Server: Microsoft-IIS/5.0
Date: Fri, 01 Jan 1999 20:14: 34 GMT
Content-Type: text/HTML
Content-Length: 87
```
**Netscape Enterprise 4.1**
```
$ nc netscape.example.com 80
GET / JUNK/1.0

<HTML><HEAD><TITLE>Bad request</TITLE></HEAD>
<BODY><H1>Bad request</H1>
Your browser sent to query this server could not understand.
</BODY></HTML>
```
**SunONE 6.1**
```
$ nc sunone.example.com 80
GET / JUNK/1.0

<HTML><HEAD><TITLE>Bad request</TITLE></HEAD>
<BODY><H1>Bad request</H1>
Your browser sent a query this server could not understand.
</BODY></HTML>
```


### 测试工具
* httprint - http://net-square.com/httprint.html
* httprecon - http://www.computec.ch/projekte/httprecon/
* Netcraft - http://www.netcraft.com
* Desenmascarame - http://desenmascara.me


#### 自动化测试工具
与其手动抓取旗标和分析web服务器头，测试者也可以使用自动化工具来得到同样的结果。有许多用于准确识别web服务器的测试例子。幸运的是，也有许多工具可以自动化这些测试过程。"*httprint*"就是其中一款工具。他使用签名字典来辨认web服务器的类型和版本。

下图是一个例子：

![Image:httprint.jpg](https://www.owasp.org/images/2/24/Httprint.jpg)


#### 在线测试工具
测试者想要更加隐蔽，不直接连接目标网站可以使用在线测试工具。[Netcraft](http://www.netcraft.com)是获得目标web服务器多种信息的一个在线工具的例子。通过这个工具我们可以获得目标的操作系统信息、web服务器信息、服务器上线时长信息、拥有者信息以及历史修改信息等等。
如下图中所示：

![Image:netcraft2.png](https://www.owasp.org/images/7/76/Netcraft2.png)


[OWASP Unmaskme Project](https://www.owasp.org/index.php/OWASP_Unmaskme_Project)致力于成为另一个识别网站的在线工具，他通过提取 [Web-metadata](https://www.owasp.org/index.php/Web-metadata) 信息来实现。这个项目背后的想法是任何网站管理人员都能从安全的视角来审查网站的元数据。

这个项目仍在开发之中，你可以尝试一下[这个想法的证明的一个西班牙语网站](http://desenmascara.me/)。


### 参考资料
**白皮书**<br>
* Saumil Shah: "An Introduction to HTTP fingerprinting" - http://www.net-square.com/httprint_paper.html
* Anant Shrivastava : "Web Application Finger Printing" - http://anantshri.info/articles/web_app_finger_printing.html


### 整改措施

使用加强的反向代理服务器来保护Web服务器的展示层。

混淆Web服务器展示层的头信息。
* Apache
* IIS

