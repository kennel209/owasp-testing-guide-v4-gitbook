# 枚举Web服务器上的应用 (OTG-INFO-004)


### 综述
测试Web应用漏洞的一个重要步骤是寻找出运行在服务器上的流行应用程序。许多应用程序存在已知漏洞或者已知的攻击手段来获取控制权限或者数据。此外，许多应用往往被错误配置，而且没有更新。他们被认为是“内部”使用，所以没有威胁存在。

随着虚拟web服务的大量使用，传统一个IP地址与一个服务器一一对应的传统形式已经失去了最初的重要意义。多个网站或应用解析到同一个IP地址并不少见。这样的场景不局限于主机托管环境，也应用在平常的合作环境。

安全专家有时候被给与了一系列IP地址作为测试目标。可能会有争议，这个场景更接近渗透测试类型的任务，但是无论何种情况，类似的任务都希望测试目标地址中所有可以访问到的应用。问题是所给IP地址在80端口运行了一个HTTP服务，但是测试者通过指定IP地址（仅有的信息）访问却得到“没有web服务器被配置”或类似的消息。当访问不相关的域名（DNS）时，系统可能拒绝访问。显而易见，一定程度的分析工作极大影响测试任务，不然只能仅仅测试他们所意识到的系统。

有时候，测试目标的描述会更加丰富。测试者给予一系列IP地址以及相关的域名。当然，这个列表可能只传递了部分信息，例如它可能忽略部分域名，客户也可能根本没意识到这个问题（这在大型组织中往往很常见）。

其他影响测试范围的问题还表现在Web应用程序发布了不明显的URL，例如（http://www.example.com/some-strange-URL） ，哪儿都访问不到这个地址。出现这样的地址可能由于偶然错误，比如错误配置，也可能是故意而为，比如不公开的管理接口。

为了发现这些问题，我们需要实施web应用发现。


### 测试目标

枚举web服务器上存在的应用程序。


### 如何测试

#### 黑盒测试
Web应用发现是一个在给定基础条件情况下鉴别Web应用程序的过程。一定基础条件往往是一系列IP地址(可能是一个网段)，也可能是一系列DNS解析名称，也可能是两者混合。
这些信息往往是项目开始之前中最先给出的内容，无论在一个典型渗透测试或者是应用评估任务中。在这两种案例中，除非是合约条款中明确指出（例如，仅测试指定应用URL http://www.example.com/），否则测试应该力求最复杂的范围，比如应该识别出目标的所有应用访问入口。下面的例子展示了一些达成这个目标的技巧。


**注意:** 一些技巧是应用于互联网Web服务器、DNS服务器、反向IP搜索服务以及搜索引擎。文中例子所使用的私有ip地址（如*192.168.1.100*)仅仅是为了匿名需要指代表示 *通用* IP地址。


应用的数量与所给的域名或IP的关系受到三个因素的影响：

**1. 不同的基本 URL** <br>
一个web应用明显的入口是 *www.example.com*, 也就是说，这个缩写表明我们认为这个Web应用最初的入口在http://www.example.com/ （HTTPS也一样）。然而即使这是常见情况，但是也没任何强制的措施要求应用程序一定要从“/”开始。


例如，下面这些相同域名下的链接可能表示了三个不同的应用：
```
http://www.example.com/url1
http://www.example.com/url2
http://www.example.com/url3
```

在这个例子中，URL地址 http://www.example.com/ 并没有分配到一个有意义的页面，有三个应用被“隐藏”了，除非测试者明确清楚如何访问他们，就是说需要明确知道*url1*, *url2* 和 *url3*。往往不会像这样发布web应用，除非拥有者不希望他们被正常访问，只将特定的地址通知特定的用户。这不意味着这些地址是秘密的，只是他们存在的确切地址没有被明确公布而已。


**2. 非标准端口**<br>
Web应用常常使用80端口（http）和443端口（https），但是这些端口号没有什么特殊之处。事实上，web应用可以关联任意TCP端口，能通过如下方式为http[s]:www.wxample.com:port/指定端口。比如，http://www.example.com:20000/。


**3. 虚拟主机**<br>
DNS允许单个IP地址被关联多个域名。例如，IP地址 *192.168.1.100* 可能关联 *www.example.com, helpdesk.example.com, webmail.example.com* 等域名。没有必要所有名字都属于相同的DNS域名。这个一对多的关系来提供不同的网页内容的技术叫做虚拟主机。识别虚拟主机的信息涵在HTTP 1.1标准的 *Host:* 头中[1]。


一个人可能不会意识到除了明显的*www.example.com* 之外还存在其他web应用，除非他们知道 *helpdesk.example.com* 和 *webmail.example.com*。


**对抗因素1 - 非标准URL地址**<br>
没有完全确定非标准命名的URL的web应用的方法。因为不是标准化，没有固定的规范来指导命名规则，但是有一些技巧能帮助测试者获取额外的信息。


首先如果web服务器被错误配置成允许目录浏览，，可以通过这点来发现其他应用。漏洞扫描器可以在这里提供帮助。


其次，这些应用可能被其他web页面引用，就有机会被蜘蛛机器人和搜素引擎收录。如果测试者怀疑有隐藏的应用存在在*www.example.com*中，可以使用 *site* 操作符来搜索结果，“site: www.example.com”。在返回结果中可以能存在指向这些不明显的应用。


另一个发现未发布的应用的方法是提供一个候选列表。例如，一个web邮件应用前端往往能通过类似 https://www.example.com/webmail, https://webmail.example.com/, 或 https://mail.example.com/ 之类的URL进行访问。这种方法也能应用于管理界面，它也可能作为隐藏页面发布（比如Tomcat管理接口），没有被其他地方链接。所以使用一些基于字典的查找方法（或“聪明的猜测”）能获得一些结果。漏洞扫描器也能在这方面提供帮助。


**对抗因素2 - 非标准端口**<br>
发现非标准端口上的应用是非常简单的。一个端口扫描器，比如namp[2]就能通过-sV选项胜任这项服务识别工作，它也能识别任意端口上的http[s]服务。这可能需要完整扫描64k的TCP端口地址空间。


下面例子中的命令会使用TCP连接扫描技术寻找IP *192.168.1.100* 的所有TCP端口，并识别这些端口上的服务。（nmap有着许多选项，我们只列出了*必需*的选择，其他内容超出了本章范围。）
```
nmap –PN –sT –sV –p0-65535 192.168.1.100
```

检查输出寻找http或者潜在的SSL包装服务（这些往往能被确认为https）就十分足够了。下面是上一个命令输出的例子：
```
Interesting ports on 192.168.1.100:
(The 65527 ports scanned but not shown below are in state: closed)
PORT      STATE SERVICE     VERSION
22/tcp    open  ssh         OpenSSH 3.5p1 (protocol 1.99)
80/tcp    open  http        Apache httpd 2.0.40 ((Red Hat Linux))
443/tcp   open  ssl         OpenSSL
901/tcp   open  http        Samba SWAT administration server
1241/tcp  open  ssl         Nessus security scanner
3690/tcp  open  unknown
8000/tcp  open  http-alt?
8080/tcp  open  http        Apache Tomcat/Coyote JSP engine 1.1
```

从这个例子中我们发现：
* 80端口运行这Apache Http服务器；
* 443端口可能运行Https服务（但是无法确定，可以通过浏览器访问https://192.168.1.100 验证)；
* 901端口运行着Samva SWAT web界面；
* 1241端口运行的不是Https服务，而是SSL包装下的Nessus守护进程；The service on port 1241 is not https, but is the SSL-wrapped Nessus daemon.
* 3690显示一个未知的服务（nmap给出了它的指纹情况，在这里为了显示清晰，我们忽略了这项内容。通过文档指导，可以将这些内容提交去合并入nmap的指纹数据库，来查找到底运行着什么服务）。
* 8000上显示另一个未知的服务，他有可能是Http服务，因为在这个端口上Http服务很常见。下面让我们来仔细查看这个：

```
$ telnet 192.168.10.100 8000
Trying 192.168.1.100...
Connected to 192.168.1.100.
Escape character is '^]'.
GET / HTTP/1.0

HTTP/1.0 200 OK
pragma: no-cache
Content-Type: text/html
Server: MX4J-HTTPD/1.0
expires: now
Cache-Control: no-cache

<html>
...
```

可以确定它是一个HTTP服务器。此外，测试这也能使用web浏览器或者使用Perl命令来模仿HTTP交互情况发送上面的GET或HEAD请求（注意HEAD请求可能不被所有浏览器支持）。
* 8080端口运行着Apache Tomcat服务。


漏洞扫描器也能完成同样的工作，但是扫描器的第一选择是识别非标准端口上是否运行http[s]服务。例如，Nessus[3]能鉴别任意端口上的服务（设定扫描所有端口的任务），与nmap相比，还能提供一系列服务器已知漏洞，包括https服务的SSL配置问题。就如前面提到的，Nessus也能发现没有提到的流行的应用程序和web入口，比如Tomcat管理接口。


**对抗因素3 - 虚拟主机**<br>
有一系列的技巧来识别给定IP *x.y.z.t* 下的DNS域名。


*DNS 区域传输*<br>
这个技巧在现在已经被限制，DNS服务器很可能拒绝区域传输。但是仍然值得一试。首先，测试者需要确定*x.y.z.t*的域名服务器（name server）。如果这个IP的一个域名已经已知（比如*www.example.com*)，那么可以使用*nslookup*，*host*或者*dig*工具来查询DNS的NS记录来确定域名服务器。


如果不知道任何*x.y.z.t*的相关域名，但是测试目标定义中存在至少一个域名，测试者仍应尝试通过相同的办法来查询域名服务器（希望*x.y.t.z*也是被同一个域名服务器提供）。例如测试目标包括IP地址*x.y.z.t*和一个域名*mail.example.com*，可以考虑查询域名*example.com*的域名服务器。


下面的例子展示了如何使用host命令查询www.owasp.org的域名服务器：
```
$ host -t ns www.owasp.org
www.owasp.org is an alias for owasp.org.
owasp.org name server ns1.secure.net.
owasp.org name server ns2.secure.net.
```


区域传送可以通过向*example.com*的域名服务器发出请求完成。如果足够幸运，测试者能得到该域名的一系列DNS条目。这里面会包含明显的*www.example.com*和不明显的*helpdesk.example.com*与*webmail.example.com*（还包括其他域名）。检查所有得到的域名，并对需要评估的目标进行分析。

试着对owasp.org的一个域名服务器请求区域传输：
```
$ host -l www.owasp.org ns1.secure.net
Using domain server:
Name: ns1.secure.net
Address: 192.220.124.10#53
Aliases:

Host www.owasp.org not found: 5(REFUSED)
; 请求失败了
```


*DNS 反向查询*<br>
过程和前面类似，只不过依赖于反向（PTR）DNS记录。区别与区域传输，将记录类型设置成PTR，为IP地址发送请求。幸运的话，我们可以得到一系列DNS域名的记录。这个技巧需要服务器存在IP到域名的映射，有时无法保证这一点。


*基于web的DNS搜索DNS*<br>
这种搜索更类似于DNS区域传输，但是是依赖于提供DNS查询的Web服务。比如像*Netcraft Search DNS*的服务，地址在 http://searchdns.netcraft.com/?host 。测试者能提交一系列域名查询请求，如*example.com*，会返回一系列他们获得的相关目标域名。


*反向IP查询服务*<br>
反向IP查询服务类似DNS反向查询，不同之处在于测试者向web应用查询，而不是DNS服务器。有许多这样的服务网站存在，由于他们一般都返回部分结果（通常都不同），所以使用不同的服务查询会得到一个更加完善的结果。


*Domain tools reverse IP*: http://www.domaintools.com/reverse-ip/
(需要注册)


*MSN search*: http://search.msn.com
用法： "ip:x.x.x.x"


*Webhosting info*: http://whois.webhosting.info/
用法： http://whois.webhosting.info/x.x.x.x


*DNSstuff*: http://www.dnsstuff.com/
(存在多个服务)

http://www.net-square.com/mspawn.html
(多种服务，需要安装)


*tomDNS*: http://www.tomdns.net/index.php
(部分服务未公开)


*SEOlogs.com*: http://www.seologs.com/ip-domains.html
(反向IP/DNS查询)


下面例子展示了关于216.48.3.18的反向IP查找结果，这个IP是www.owasp.org的地址。例子中揭示了其他三个该IP地址下的不明显的域名。

<center>
![Image:Owasp-Info.jpg](https://www.owasp.org/images/3/3e/Owasp-Info.jpg)
</center>


*Googling*<br>
通过之前的信息收集的技巧介绍，测试者可以通过搜索引擎精炼和加强他们的结果分析。比如证明其他目标的其他域名存在或者可以通过隐藏URL访问应用。


举例说明，考虑上一个*www.owasp.org*的例子，测试者可以使用google或者其他搜索引擎获得相关信息（DNS域名）从而发现 *webgoat.org*，*webscarab.com*和*webscarab.net*。


Googling技巧请参阅 [Testing: Spiders, Robots, and Crawlers](https://www.owasp.org/index.php/Testing:_Spiders,_Robots,_and_Crawlers_%28OWASP-IG-001%29)。


#### 灰盒测试
不适用。无论从哪里开始，基本方法和黑盒测试相同。


### 测试工具
* DNS查询工具如 *nslookup*, *dig* 等等；
* 搜索引擎 (Google, Bing 和其他主要搜索引擎)；
* 定制化的DNS相关web搜索服务：见上文；
* Nmap - http://www.insecure.org
* Nessus Vulnerability Scanner - http://www.nessus.org
* Nikto - http://www.cirt.net/nikto2


### 参考资料
**白皮书**
[1] RFC 2616 – Hypertext Transfer Protocol – HTTP 1.1

