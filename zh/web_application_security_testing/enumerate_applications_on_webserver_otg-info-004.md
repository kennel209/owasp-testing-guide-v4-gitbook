# 枚举Web服务器上的应用 (OTG-INFO-004)


### 综述
测试Web应用漏洞的一个重要步骤是寻找出运行在服务器上的流行应用程序。许多应用程序存在已知漏洞或者已知的攻击手段来获取控制权限或者数据。此外，许多应用往往被错误配置，而且没有更新。他们被认为是“内部”使用，所以没有威胁存在。

随着虚拟web服务的大量使用，传统一个IP地址与一个服务器一一对应的传统形式已经失去了最初的重要意义。多个网站或应用解析到同一个IP地址并不少见。这样的场景不局限于主机托管环境，也应用在平常的合作环境。

安全专家有时候被给与了一系列IP地址作为测试目标。可能会有争议，这个场景更接近渗透测试类型的任务，但是无论何种情况，类似的任务都希望测试目标地址中所有可以访问到的应用。问题是所给IP地址在80端口运行了一个HTTP服务，但是测试者通过指定IP地址（仅有的信息）访问却得到“没有web服务器被配置”或类似的消息。当访问不相关的域名（DNS）时，系统可能拒绝访问。显而易见，一定程度的分析工作极大影响测试任务，不然只能仅仅测试他们所意识到的系统。

有时候，测试目标的描述会更加丰富。测试者给予一系列IP地址以及相关的域名。当然，这个列表可能只传递了部分信息，例如它可能忽略部分域名，客户也可能根本没意识到这个问题（这在大型组织中往往很常见）。

其他影响测试范围的问题还表现在Web应用程序发布了不明显的URL，例如（http://www.example.com/some-strange-URL），哪儿都访问不到这个地址。出现这样的地址可能由于偶然错误，比如错误配置，也可能是故意而为，比如不公开的管理接口。

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


**2. Non-standard ports**<br>
While web applications usually live on port 80 (http) and 443 (https), there is nothing magic about these port numbers. In fact, web applications may be associated with arbitrary TCP ports, and can be referenced by specifying the port number as follows: http[s]://www.example.com:port/. For example, http://www.example.com:20000/.


**3. Virtual hosts**<br>
DNS allows a single IP address to be associated with one or more symbolic names. For example, the IP address *192.168.1.100* might be associated to DNS names *www.example.com, helpdesk.example.com, webmail.example.com*. It is not necessary that all the names belong to the same DNS domain. This 1-to-N relationship may be reflected to serve different content by using so called virtual hosts. The information specifying the virtual host we are referring to is embedded in the HTTP 1.1 *Host:* header [1].


One would not suspect the existence of other web applications in addition to the obvious *www.example.com*, unless they know of *helpdesk.example.com* and *webmail.example.com*.


**Approaches to address issue 1 - non-standard URLs**<br>
There is no way to fully ascertain the existence of non-standard-named web applications. Being non-standard, there is no fixed criteria governing the naming convention, however there are a number of techniques that the tester can use to gain some additional insight.


First, if the web server is mis-configured and allows directory browsing, it may be possible to spot these applications. Vulnerability scanners may help in this respect.


Second, these applications may be referenced by other web pages and there is a chance that they have been spidered and indexed by web search engines. If testers suspect the existence of such “hidden” applications on *www.example.com* they could search using the *site* operator and examining the result of a query for “site: www.example.com”. Among the returned URLs there could be one pointing to such a non-obvious application.


Another option is to probe for URLs which might be likely candidates for non-published applications. For example, a web mail front end might be accessible from URLs such as https://www.example.com/webmail, https://webmail.example.com/, or https://mail.example.com/. The same holds for administrative interfaces, which may be published at hidden URLs (for example, a Tomcat administrative interface), and yet not referenced anywhere. So doing a bit of dictionary-style searching (or “intelligent guessing”) could yield some results. Vulnerability scanners may help in this respect.


**Approaches to address issue 2 - non-standard ports**<br>
It is easy to check for the existence of web applications on non-standard ports. A port scanner such as nmap [2] is capable of performing service recognition by means of the -sV option, and will identify http[s] services on arbitrary ports. What is required is a full scan of the whole 64k TCP port address space.


For example, the following command will look up, with a TCP connect scan, all open ports on IP *192.168.1.100* and will try to determine what services are bound to them (only *essential* switches are shown – nmap features a broad set of options, whose discussion is out of scope):
```
nmap –PN –sT –sV –p0-65535 192.168.1.100
```

It is sufficient to examine the output and look for http or the indication of SSL-wrapped services (which should be probed to confirm that they are https). For example, the output of the previous command could look like:
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

From this example, one see that:
* There is an Apache http server running on port 80.
* It looks like there is an https server on port 443 (but this needs to be confirmed, for example, by visiting https://192.168.1.100 with a browser).
* On port 901 there is a Samba SWAT web interface.
* The service on port 1241 is not https, but is the SSL-wrapped Nessus daemon.
* Port 3690 features an unspecified service (nmap gives back its *fingerprint* - here omitted for clarity - together with instructions to submit it for incorporation in the nmap fingerprint database, provided you know which service it represents).
* Another unspecified service on port 8000; this might possibly be http, since it is not uncommon to find http servers on this port. Let's examine this issue:

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

This confirms that in fact it is an HTTP server. Alternatively, testers could have visited the URL with a web browser; or used the GET or HEAD Perl commands, which mimic HTTP interactions such as the one given above (however HEAD requests may not be honored by all servers).
* Apache Tomcat running on port 8080.


The same task may be performed by vulnerability scanners, but first check that the scanner of choice is able to identify http[s] services running on non-standard ports. For example, Nessus [3] is capable of identifying them on arbitrary ports (provided it is instructed to scan all the ports), and will provide, with respect to nmap, a number of tests on known web server vulnerabilities, as well as on the SSL configuration of https services. As hinted before, Nessus is also able to spot popular applications or web interfaces which could otherwise go unnoticed (for example, a Tomcat administrative interface).


**Approaches to address issue 3 - virtual hosts**<br>
There are a number of techniques which may be used to identify DNS names associated to a given IP address *x.y.z.t*.


*DNS zone transfers*<br>
This technique has limited use nowadays, given the fact that zone transfers are largely not honored by DNS servers. However, it may be worth a try. First of all, testers must determine the name servers serving *x.y.z.t*. If a symbolic name is known for *x.y.z.t* (let it be *www.example.com*), its name servers can be determined by means of tools such as *nslookup*, *host*, or *dig*, by requesting DNS NS records.


If no symbolic names are known for *x.y.z.t*, but the target definition contains at least a symbolic name, testers may try to apply the same process and query the name server of that name (hoping that *x.y.z.t* will be served as well by that name server). For example, if the target consists of the IP address *x.y.z.t* and the name *mail.example.com*, determine the name servers for domain *example.com*.


The following example shows how to identify the name servers for www.owasp.org by using the host command:
```
$ host -t ns www.owasp.org
www.owasp.org is an alias for owasp.org.
owasp.org name server ns1.secure.net.
owasp.org name server ns2.secure.net.
```


A zone transfer may now be requested to the name servers for domain *example.com*. If the tester is lucky, they will get back a list of the DNS entries for this domain. This will include the obvious *www.example.com* and the not-so-obvious *helpdesk.example.com* and *webmail.example.com* (and possibly others). Check all names returned by the zone transfer and consider all of those which are related to the target being evaluated. <br>

Trying to request a zone transfer for owasp.org from one of its name servers:
```
$ host -l www.owasp.org ns1.secure.net
Using domain server:
Name: ns1.secure.net
Address: 192.220.124.10#53
Aliases:

Host www.owasp.org not found: 5(REFUSED)
; Transfer failed.
```


*DNS inverse queries*<br>
This process is similar to the previous one, but relies on inverse (PTR) DNS records. Rather than requesting a zone transfer, try setting the record type to PTR and issue a query on the given IP address. If the testers are lucky, they may get back a DNS name entry. This technique relies on the existence of IP-to-symbolic name maps, which is not guaranteed.


*Web-based DNS searches*<br>
This kind of search is akin to DNS zone transfer, but relies on web-based services that enable name-based searches on DNS. One such service is the *Netcraft Search DNS* service, available at http://searchdns.netcraft.com/?host. The tester may query for a list of names belonging to your domain of choice, such as *example.com*. Then they will check whether the names they obtained are pertinent to the target they are examining.


*Reverse-IP services*<br>
Reverse-IP services are similar to DNS inverse queries, with the difference that the testers query a web-based application instead of a name server. There are a number of such services available. Since they tend to return partial (and often different) results, it is better to use multiple services to obtain a more comprehensive analysis.


*Domain tools reverse IP*: http://www.domaintools.com/reverse-ip/
(requires free membership)


*MSN search*: http://search.msn.com
syntax: "ip:x.x.x.x" (without the quotes)


*Webhosting info*: http://whois.webhosting.info/
syntax: http://whois.webhosting.info/x.x.x.x


*DNSstuff*: http://www.dnsstuff.com/
(multiple services available)

http://www.net-square.com/mspawn.html
(multiple queries on domains and IP addresses, requires installation)


*tomDNS*: http://www.tomdns.net/index.php
(some services are still private at the time of writing)


*SEOlogs.com*: http://www.seologs.com/ip-domains.html
(reverse-IP/domain lookup)


The following example shows the result of a query to one of the above reverse-IP services to 216.48.3.18, the IP address of www.owasp.org. Three additional non-obvious symbolic names mapping to the same address have been revealed.

<center>
![Image:Owasp-Info.jpg](https://www.owasp.org/images/3/3e/Owasp-Info.jpg)
</center>


*Googling*<br>
Following information gathering from the previous techniques, testers can rely on search engines to possibly refine and increment their analysis. This may yield evidence of additional symbolic names belonging to the target, or applications accessible via non-obvious URLs.


For instance, considering the previous example regarding *www.owasp.org*, the tester could query Google and other search engines looking for information (hence, DNS names) related to the newly discovered domains of *webgoat.org*, *webscarab.com*, and *webscarab.net*.


Googling techniques are explained in [Testing: Spiders, Robots, and Crawlers](https://www.owasp.org/index.php/Testing:_Spiders,_Robots,_and_Crawlers_%28OWASP-IG-001%29).


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

