# 测试应用平台配置 (OTG-CONFIG-002)

### 综述
为了防止可能攻破整个架构安全的错误，正确配置每个组成架构的元素是非常重要的。


配置审查和测试在创建和维护架构中是一项关键任务。这是因为不同的系统通常在安装时提供了通用的配置，这些配置不一定适合特点网站任务要求。


典型的web应用和服务器安装过程可能包含一系列的功能（比如应用例子，文档，测试页面等），这些不必须的功能应该在部署前移除来避免被恶意利用。

### 如何测试
#### 黑盒测试

##### 样本和已知文件/目录
许多web服务器和应用在默认安装过程中提供样本应用和文件来帮助开发者测试服务器是否正常安装工作。然而一些web服务器默认应用被发现存在漏洞。例如，CVE-1999-0449 （Exair样本站点的拒绝服务漏洞）, CAN-2002-1744 （IIS5.0 CodeBrws.asp 目录便利漏洞）， CAN-2002-1630 （Oracle9iAS sendmail.jsp利用），或 CAN-2003-1172 （Apache Cocoon 查看源代码样本中的目录遍历漏洞）。


CGI扫描器包含一些许多不同web或应用服务器提供的样本文件和目录详细列表，可能是一个快速发现这些文件的方法。然而，真正确保这些文件的唯一方法是对web服务器和应用服务器的内容进行全面审查来决定是否与应用相关。


##### 注释审查
通常很常见，甚至是推荐程序员在源代码中包含详细注释，来帮助其他程序员理解相关函数功能。程序员通常在开发大型web应用中加入注释。然而，包含在HTML源代码中的注释往往能揭露出不应该让攻击者获得信息。有时候有些不需要的功能在源代码中注释了，但是这些注释却通过HTML页面意外返回给用户。


注释应该被审查来确定没有信息泄露。这个审查只能通过完全分析web服务器静态和动态和文件搜索完成。使用自动化或基于向导浏览网站，存储所有获得的内容是十分有用的。这些内容可以用于查询分析任何代码中的注释。


#### 灰盒测试

##### 配置审查

web服务器或应用配置在保护文件内容中扮演一个重要角色，他们必须被仔细审查来发现常见的配置错误。显而易见，推荐配置根据站点策略和服务器软件提供的功能不同而不同。在大多数情况下配置指南（生产商提供或外部机构提供）应该被遵循来确定服务器是否正确安全配置。


虽然不可能通用地说明一个服务器应该如何配置，但是有些常用的指南应该被考虑进去：

* 只开启那些应用需要的服务器模块（IIS的例子中是ISAPI扩展）。由于模块被禁用，服务器大小和复杂度被减小，减少了攻击面。这也能防止那些被禁用模块的漏洞。
* 使用自定义的页面来替代默认web错误页面来处理服务器错误（40x或50x）。特别确保没有任何应用错误返回给终端用户，没有代码通过这些错误泄露给攻击者提供信息。事实上这种情况很常见，开发者可能会忘了这点，因为生产前环境需要这些信息。
* 确保服务器软件在操作系统中以最低权限允许。这防止了由于服务器软件的错误直接攻破整个系统的情况，虽然攻击者还可能通过在web服务器中运行代码进行提权。
* 确保服务器软件日志正确记录了合法访问和错误。
* 确保服务器被配置为正确处理超载情况，防止拒绝服务攻击。确保服务器正确进行了性能调试。
* 不要授予非管理主体（除了NT SERVICE\WMSvc外）访问 applicationHost.config，redirection.config，和administration.config （无论读或写权限）。这包括Network Service，IIS_IUSRS，IUSR或者其他IIS应用池中的自定义主体。IIS worker 进程不意味着能直接访问这些文件。
* 不要在网络上共享applicationHost.config，redirection.config，和administration.config 。当使用共享配置，倾向于导出 applicationHost.config 到其他位置（见“共享配置权限设置”章节）。
* 记住所有用户默认都能读取 .NET 框架的 machine.config 和根目录的 web.config 文件。不要在这些文件中存放只允许管理员查看的敏感信息。
* 加密敏感信息，是这些信息只能通过IIS worker进程访问，不能被机器上的其他用户读取。
* 不要授予写权限给主体来访问共享的 applicationHost.config 。这些主体应该只有读权限。
* 使用单独的主体来发布共享的 applicationHost.config 。不要使用这个主体来配置共享配置的权限。
* 使用强密码来导出共享配置使用的加密密钥。
* 保持受限访问那些包含共享配置的密钥的共享目录。如果共享目录被攻破了，攻击者能够读写服务器上的任何IIS配置，将你网站流量重定向到恶意站点，有些情况下甚至能通过向IIS worker进程注入任意代码来获得web服务器控制。
* 考虑通过防火墙规则和IPsec策略只允许web服务器成员连接来保护共享目录。


##### 日志记录

日志记录是应用架构安全非常重要的一环，因为他能够检测应用中的缺陷（如用户持续尝试获取一个不存在的文件）和证实恶意用户的攻击行为。日志通常被web或其他服务器软件正确生成。通常没有发现应用正确记录应用行为和发生时间，因为应用日志的主要目的是产生调试信息以便程序员分析特点错误。


在这两个情况下（服务器和应用程序日志记录），通过日志内容，有一些问题应该被测试和分析：

1. 日志包含敏感信息么？
2. 日志存储在专属服务器中么？
3. 日志使用可能产生拒绝服务的情况么？
4. 他们是如何迭代的？日志是否保存足够长的时间？
5. 日志是如何被审查的？管理员能否通过审查出发现攻击行为？
6. 日志备份如何保存？
7. 日志记录数据前是否进行验证（最小最大长度，字符等）？


***日志中的敏感信息***

有些应用可能，例如，使用GET请求来转发表单数据，这些请求能在服务日志中发现。这意味着服务器日志可能包含敏感信息（如用户名和密码，或者银行帐户详情）。这些敏感信息可能被获得日志的攻击者利用，例如，通过管理接口或者已知服务器漏洞或错误配置（比如Apache服务器知名的 *server-status* 错误配置）获得日志。


事件日志通常包含对攻击者有用的数据（信息泄露）或能被直接利用：

* 调试信息
* 堆栈追踪数据
* 用户名
* 系统组件名称
* 内部IP地址
* 敏感信息（如电子邮件地址，邮编地址和电话号码）
* 业务数据


同时，在一些司法管辖区域，在日志中存储敏感信息如个人数据，可能需要强制公司遵循数据保护法规，因为他们也可能记录他们的后台数据库到日志文件。如果没有做到这点，甚至是不知道的情况下，也可能受到这些数据保护法规的惩罚。


一个广范围的敏感信息列表包括：

* 应用程序源代码
* 会话鉴别值
* 访问令牌
* 敏感个人数据和一些个人鉴别信息（PII）
* 认证密码
* 数据库连接字符串
* 加密密钥
* 银行帐户或支付卡信息
* 高于日志系统能记录的高级别数据
* 商业敏感信息
* 在相关司法管辖区域属于非法收集的资料
* 用户不同意收集的信息，如使用不追踪（DNT）或同意收集的时限已经过期


##### 日志位置

通常服务器产生本地日志记录应用行为和错误，使用运行系统的服务器的磁盘空间。然而如果服务器被攻破，他的日志可能被入侵者清空来掩盖所有攻击和其手段。如果发生了这种情况，系统管理员就不清楚攻击是如何发生的以及攻击源位于何处。事实上大多数攻击工具包包含一个 *记录消除器* 来提供清除访问痕迹日志（如攻击者的IP地址）。这些会在攻击者植入的系统级别的工具包中定期运行。


因此，将日志保存在单独的地方，而不是服务本身是明智的选择。这也使得从相同应用程序的多个不同源来汇聚日志变得容易（比如那些web服务器群），以及更有利于记录分析工作（可能是CPU密集型）而不影响服务器本身。


##### 日志存储

如果日志没有正确的存储，那么他可能引入拒绝服务攻击条件。拥有大量资源的攻击者可能通过产生大量的请求来填满日志文件空间，如果这些日志没有特定防护措施。然而如果服务器没有正确配置，日志会存在操作系统软件或应用本身相同磁盘分区中。这意味着如果磁盘空间被填满，那么操作系统或应用可能不正常工作因为无法进行磁盘写操作。


在UNIX系统中日志通常保存在/var目录下（尽管有些服务器安装在/opt或/usr/local下），确保这些日志目录在独立分区下。有些情况下，为了保护系统日志不被影响，特定服务器软件本身的日志目录（如Apache服务器的/var/log/apache目录）也应该存储在独立分区中。


这不是说日志应该被允许填满整个文件系统。系统日志增长应该被监控以防成为攻击者的攻击目标。


在生产环境中测试这些条件是简单又危险的，因为产生大量请求来发现这些请求被记录并有可能填满整个日志分区。有些环境中，查询字符串也被记录进日志，无论是通过GET或POST请求产生的，长请求可以更快填满日志。通常单个请求可能仅仅记录小部分的数据，如日期时间、源IP地址、URI请求和服务结果。


##### 日志轮转迭代

大多数服务器（除了少数自定义应用）会轮转迭代日志文件来防止充满文件系统空间。迭代的假设是日志中的信息只需要存在一定有限的时间。


这个功能应该被测试来确保：

* 日志应该保存安全策略中定义的时间，不多也不少。
* 日志轮转后应该被压缩（这只是为了方便，节约磁盘空间记录更多日志）。
* 轮转的日志文件权限应该与日志文件本身一样（或更加严格）。例如，web服务器需要写日志，却不需要向轮转后的日志写，这意味着文件权限可以在轮转后改变来防止web服务器进程修改他们


有些服务器可能在日志文件达到制定大小轮转日志。在这种情况下，确保攻击者不能强制日志轮转来隐藏他们的痕迹。


##### 日志访问控制

事件日志信息不应该被终端用户访问。甚至web管理员也不应该查看这些日志，因为这会破坏独立职责管理。确保有访问控制措施保护日志和任何应用提供查看和搜索日志能力不应该被其他应用用户角色访问。任何日志数据也不应该被未认证用户查看。


##### 日志审查

日志审查不仅仅是提取服务器的文件使用数据统计信息（典型日志数据应用软件关注点），也应该确定web服务器上发生的攻击行为。


为了分析服务器攻击行为，错误日志应该被分析，审查应该关注：

* 40x（未找到）错误消息。来自同一个源头的大量错误可能表明存在一个CGI扫描工具。
* 50x （服务器错误）消息。这可能表明攻击者可能滥用应用程序，并产生了为处理异常。例如开始阶段的SQL注入攻击可能产生这些错误信息，当SQL查询没有正确编写以及后台执行失败的信息。 


日志统计和分析数据不应该产生或存储在产生日志的服务器上。否则攻击者可能通过服务器漏洞或错误配置文件获取访问他们的权限，并获得与日志文件本身类似的信息泄露。


### 参考资料

* Apache
    - Apache Security, by Ivan Ristic, O’reilly, March 2005.
	- Apache Security Secrets: Revealed (Again), Mark Cox, November 2003 - http://www.awe.com/mark/apcon2003/
	- Apache Security Secrets: Revealed, ApacheCon 2002, Las Vegas,  Mark J Cox, October 2002 - http://www.awe.com/mark/apcon2002
	- Performance Tuning - http://httpd.apache.org/docs/misc/perf-tuning.html
* Lotus Domino
	- Lotus Security Handbook, William Tworek et al., April 2004, available in the IBM Redbooks collection
	- Lotus Domino Security, an X-force white-paper, Internet Security Systems, December 2002
	- Hackproofing Lotus Domino Web Server, David Litchfield, October 2001,
	- NGSSoftware Insight Security Research, available at http://www.nextgenss.com
* Microsoft IIS
	- IIS 6.0 Security, by Rohyt Belani, Michael Muckin, - http://www.securityfocus.com/print/infocus/1765
	- IIS 7.0 Securing Configuration -http://technet.microsoft.com/en-us/library/dd163536.aspx
	- Securing Your Web Server (Patterns and Practices), Microsoft Corporation, January 2004
	- IIS Security and Programming Countermeasures, by Jason Coombs
	- From Blueprint to Fortress: A Guide to Securing IIS 5.0, by John Davis, Microsoft Corporation, June 2001
	- Secure Internet Information Services 5 Checklist, by Michael Howard, Microsoft Corporation, June 2000
	- “INFO: Using URLScan on IIS” - http://support.microsoft.com/default.aspx?scid=307608
* Red Hat’s (formerly Netscape’s) iPlanet
	- Guide to the Secure Configuration and Administration of iPlanet Web Server, Enterprise Edition 4.1, by James M Hayes, The Network Applications Team of the Systems and Network Attack Center (SNAC), NSA, January 2001
* WebSphere
	- IBM WebSphere V5.0 Security, WebSphere Handbook Series, by Peter Kovari et al., IBM, December 2002.
	- IBM WebSphere V4.0 Advanced Edition Security, by Peter Kovari et al., IBM, March 2002.
* 通用
	- [Logging Cheat Sheet](https://www.owasp.org/index.php/Logging_Cheat_Sheet), OWASP
	- [SP 800-92](http://csrc.nist.gov/publications/nistpubs/800-92/SP800-92.pdf)  Guide to Computer Security Log Management, NIST
	- [PCI DSS v2.0](https://www.pcisecuritystandards.org/security_standards/documents.php)  Requirement 10 and PA-DSS v2.0 Requirement 4, PCI Security Standards Council

* 其他
	- CERT Security Improvement Modules: Securing Public Web Servers - http://www.cert.org/security-improvement/
	- Apache Security Configuration Document, InterSect Alliance - http://www.intersectalliance.com/projects/ApacheConfig/index.html
	- “How To: Use IISLockdown.exe” - http://msdn.microsoft.com/library/en-us/secmod/html/secmod113.asp
