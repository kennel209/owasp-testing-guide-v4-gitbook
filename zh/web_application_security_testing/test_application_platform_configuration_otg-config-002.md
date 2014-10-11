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

web服务器或应用配置
The web server or application server configuration takes an important role in protecting the contents of the site and it must be carefully reviewed in order to spot common configuration mistakes. Obviously, the recommended configuration varies depending on the site policy, and the functionality that should be provided by the server software. In most cases, however, configuration guidelines (either provided by the software vendor or external parties) should be followed to determine if the server has been properly secured.


It is impossible to generically say how a server should be configured, however, some common guidelines should be taken into account:

* Only enable server modules (ISAPI extensions in the case of IIS) that are needed for the application. This reduces the attack surface since the server is reduced in size and complexity as software modules are disabled. It also prevents vulnerabilities that might appear in the vendor software from affecting the site if they are only present in modules that have been already disabled.
* Handle server errors (40x or 50x) with custom-made pages instead of with the default web server pages. Specifically make sure that any application errors will not be returned to the end-user and that no code is leaked through these errors since it will help an attacker. It is actually very common to forget this point since developers do need this information in pre-production environments.
* Make sure that the server software runs with minimized privileges in the operating system. This prevents an error in the server software from directly compromising the whole system, although an attacker could elevate privileges once running code as the web server.
* Make sure the server software properly logs both legitimate access and errors.
* Make sure that the server is configured to properly handle overloads and prevent Denial of Service attacks. Ensure that the server has been performance-tuned properly.
* Never grant non-administrative identities (with the exception of NT SERVICE\WMSvc) access to applicationHost.config, redirection.config, and administration.config (either Read or Write access). This includes Network Service, IIS_IUSRS, IUSR, or any custom identity used by IIS application pools. IIS worker processes are not meant to access any of these files directly.
* Never share out applicationHost.config, redirection.config, and administration.config on the network. When using Shared Configuration, prefer to export applicationHost.config to another location (see the section titled "Setting Permissions for Shared Configuration).
*Keep in mind that all users can read .NET Framework machine.config and root web.config files by default. Do not store sensitive information in these files if it should be for administrator eyes only.
* Encrypt sensitive information that should be read by the IIS worker processes only and not by other users on the machine.
* Do not grant Write access to the identity that the Web server uses to access the shared applicationHost.config. This identity should have only Read access.
* Use a separate identity to publish applicationHost.config to the share. Do not use this identity for configuring access to the shared configuration on the Web servers.
* Use a strong password when exporting the encryption keys for use with shared -configuration.
* Maintain restricted access to the share containing the shared configuration and encryption keys. If this share is compromised, an attacker will be able to read and write any IIS configuration for your Web servers, redirect traffic from your Web site to malicious sources, and in some cases gain control of all web servers by loading arbitrary code into IIS worker processes.
* Consider protecting this share with firewall rules and IPsec policies to allow only the member web servers to connect.


##### Logging

Logging is an important asset of the security of an application architecture, since it can be used to detect flaws in applications (users constantly trying to retrieve a file that does not really exist) as well as sustained attacks from rogue users. Logs are typically properly generated by web and other server software. It is not common to find applications that properly log their actions to a log and, when they do, the main intention of the application logs is to produce debugging output that could be used by the programmer to analyze a particular error.


In both cases (server and application logs) several issues should be tested and analysed based on the log contents:

1. Do the logs contain sensitive information?
2. Are the logs stored in a dedicated server?
3. Can log usage generate a Denial of Service condition?
4. How are they rotated? Are logs kept for the sufficient time?
5. How are logs reviewed? Can administrators use these reviews to detect targeted attacks?
6. How are log backups preserved?
7. Is the data being logged data validated (min/max length, chars etc) prior to being logged?


***Sensitive information in logs***

Some applications might, for example, use GET requests to forward form data which will be seen in the server logs. This means that server logs might contain sensitive information (such as usernames as passwords, or bank account details). This sensitive information can be misused by an attacker if they obtained the logs, for example, through administrative interfaces or known web server vulnerabilities or misconfiguration (like the well-known *server-status *misconfiguration in Apache-based HTTP servers ).


Event logs will often contain data that is useful to an attacker (information leakage) or can be used directly in exploits:

* Debug information
* Stack traces
* Usernames
* System component names
* Internal IP addresses
* Less sensitive personal data (e.g. email addresses, postal addresses and telephone numbers associated with named individuals)
* Business data


Also, in some jurisdictions, storing some sensitive information in log files, such as personal data, might oblige the enterprise to apply the data protection laws that they would apply to their back-end databases to log files too. And failure to do so, even unknowingly, might carry penalties under the data protection laws that apply.


A wider list of sensitive information is:

* Application source code
* Session identification values
* Access tokens
* Sensitive personal data and some forms of personally identifiable information (PII)
* Authentication passwords
* Database connection strings
* Encryption keys
* Bank account or payment card holder data
* Data of a higher security classification than the logging system is allowed to store
* Commercially-sensitive information
* Information it is illegal to collect in the relevant jurisdiction
* Information a user has opted out of collection, or not consented to e.g. use of do not track, or where consent to collect has expired


##### Log location

Typically servers will generate local logs of their actions and errors, consuming the disk of the system the server is running on. However, if the server is compromised its logs can be wiped out by the intruder to clean up all the traces of its attack and methods. If this were to happen the system administrator would have no knowledge of how the attack occurred or where the attack source was located. Actually, most attacker tool kits include a *log zapper* that is capable of cleaning up any logs that hold given information (like the IP address of the attacker) and are routinely used in attacker’s system-level root kits.


Consequently, it is wiser to keep logs in a separate location and not in the web server itself. This also makes it easier to aggregate logs from different sources that refer to the same application (such as those of a web server farm) and it also makes
it easier to do log analysis (which can be CPU intensive) without affecting the server itself.


##### Log storage

Logs can introduce a Denial of Service condition if they are not properly stored. Any attacker with sufficient resources could be able to produce a sufficient number of requests that would fill up the allocated space to log files, if they are not specifically prevented from doing so. However, if the server is not properly configured, the log files will be stored in the same disk partition as the one used for the operating system software or the application itself. This means that if the disk were to be filled up the operating system or the application might fail because it is unable to write on disk.


Typically in UNIX systems logs will be located in /var (although some server installations might reside in /opt or /usr/local) and it is important to make sure that the directories in which logs are stored are in a separate partition. In some cases, and in order to prevent the system logs from being affected, the log directory of the server software itself (such as /var/log/apache in the Apache web server) should be stored in a dedicated partition.


This is not to say that logs should be allowed to grow to fill up the file system they reside in. Growth of server logs should be monitored in order to detect this condition since it may be indicative of an attack.


Testing this condition is as easy, and as dangerous in production environments, as firing off a sufficient and sustained number of requests to see if these requests are logged and  if there is a possibility to fill up the log partition through these requests. In some environments where QUERY_STRING parameters are also logged regardless of whether they are produced through GET or POST requests, big queries can be simulated that will fill up the logs faster since, typically, a single request will cause only a small amount of data to be logged, such as date and time, source IP address, URI request, and server result.


##### Log rotation

Most servers (but few custom applications) will rotate logs in order to prevent them from filling up the file system they reside on. The assumption when rotating logs is that the information in them is only necessary for a limited amount of time.


This feature should be tested in order to ensure that:

* Logs are kept for the time defined in the security policy, not more and not less.
* Logs are compressed once rotated (this is a convenience, since it will mean that more logs will be stored for the same available disk space).
* File system permission of rotated log files are the same (or stricter) that those of the log files itself. For example, web servers will need to write to the logs they use but they don’t actually need to write to rotated logs, which means that the permissions of the files can be changed upon rotation to prevent the web server process from modifying these.


Some servers might rotate logs when they reach a given size. If this happens, it must be ensured that an attacker cannot force logs to rotate in order to hide his tracks.


##### Log Access Control

Event log information should never be visible to end users. Even web administrators should not be able to see such logs since it breaks separation of duty controls. Ensure that any access control schema that is used to protect access to raw logs and any applications providing capabilities to view or search the logs is not linked with access control schemas for other application user roles. Neither should any log data be viewable by unauthenticated users.


##### Log review

Review of logs can be used for more than extraction of usage statistics of files in the web servers (which is typically what most log-based application will focus on), but also to determine if attacks take place at the web server.


In order to analyze web server attacks the error log files of the server need to be analyzed. Review should concentrate on:

* 40x (not found) error messages. A large amount of these from the same source might be indicative of a CGI scanner tool being used against the web server
* 50x (server error) messages. These can be an indication of an attacker abusing parts of the application which fail unexpectedly. For example, the first phases of a SQL injection attack will produce these error message when the SQL query is not properly constructed and its execution fails on the back end database.


Log statistics or analysis should not be generated, nor stored, in the same server that produces the logs. Otherwise, an attacker might, through a web server vulnerability or improper configuration, gain access to them and retrieve similar information as would be disclosed by log files themselves.


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
