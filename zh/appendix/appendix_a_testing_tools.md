# 附录 A： 测试工具

### 开源黑盒测试工具

#### 通用测试工具

* **[OWASP ZAP](https://www.owasp.org/index.php/OWASP_Zed_Attack_Proxy_Project)**

    - Zed攻击代理(ZAP)是一款非常容易使用的整合型渗透测试工具，主要功能是发现web应用漏洞。他设计时候的使用对象是面向拥有不同安全测试经验的人员，很适合开发者和初学的渗透测试人员。
    - ZAP提供自动化扫描工具，同时也提供一系列手动发现漏洞的工具。

* **[OWASP WebScarab](https://www.owasp.org/index.php/OWASP_WebScarab_Project)**

    - WebScarab是一款用于分析HTTP和HTTPS协议通信的框架工具。他使用JAVA编写，具有高移植性，一些操作模式由扩展插件支持。

* **[OWASP CAL9000](https://www.owasp.org/index.php/OWASP_CAL9000_Project)**
	- CAL9000是一款基于浏览器的测试工具的集合，能够提高手工测试效率。 is a collection of browser-based tools that enable more effective and efficient manual testing efforts.
	- 包含XSS攻击工具，字符编码/解码工具，HTTP请求/响应生成工具，测试清单列表，自动攻击编辑器以及其他更多工具。
* **[OWASP Pantera Web Assessment Studio Project](https://www.owasp.org/index.php/Category:OWASP_Pantera_Web_Assessment_Studio_Project)**
	- Pantera使用SpikeProxy的加强版本来提供更加强大的web应用分析引擎。Pantera主要目标是结合手工测试和自动化测试来达到更好的测试结果。
* **[OWASP Mantra - Security Framework](https://www.owasp.org/index.php/OWASP_Mantra_-_Security_Framework)**
    - Mantra是基于浏览器构建的一个web应用测试框架。他支持Windows, Linux(包括32和64位)和苹果系统。此外，他也能方便地与其他代理工具如ZAP等有效结合。Mantra支持9种语言：阿拉伯语、繁体中文、简体中文、英语、法语、葡萄牙语、俄语、西班牙语和土耳其语。
* **SPIKE** - http://www.immunitysec.com/resources-freesoftware.shtml
	- SPIKE被设计用来分析信息的网络协议，目的是发现缓冲区溢出之类的类似漏洞。他的使用对象需要有较强的C语言知识，仅支持Linux系统。
* **Burp Proxy** - http://www.portswigger.net/Burp/
	- Burp代理是一款数据劫持代理工具。通过劫持和修改双向的HTTP(S)流量来进行web应用测试，他也支持自定义SSL证书和在不支持代理的客户端中工作。
* **Odysseus Proxy** - http://www.wastelands.gen.nz/odysseus/
	- Odysseus是一个代理服务器，在HTTP会话中扮演中间人角色。一个典型的HTTP代理能够转发客户端浏览器和服务器的数据包。他能够劫持任意方向的HTTP会话数据。
* **Webstretch Proxy** - http://sourceforge.net/projects/webstretch
	- Webstretch代理允许用户查看和改变通信数据流。他也能被用于开发调试。
*  **WATOBO** - http://sourceforge.net/apps/mediawiki/watobo/index.php?title=Main_Page
	- WATOBO能像一个本地代理一样工作，与Webscarab, ZAP 和BurpSuite类似，提供主动和被动测试功能。
* **Firefox LiveHTTPHeaders** - https://addons.mozilla.org/en-US/firefox/addon/live-http-headers/
	- 提供查看HTTP头内容功能。
* **Firefox Tamper Data** - https://addons.mozilla.org/en-US/firefox/addon/tamper-data/
	- 使用tamperdata能查看和修改HTTP/HTTPS头参数和POST参数。
* **Firefox Web Developer Tools** - https://addons.mozilla.org/en-US/firefox/addon/web-developer/
	- web开发者扩展为浏览器加入了许多的开发者工具。
* **DOM Inspector** - https://developer.mozilla.org/en/docs/DOM_Inspector
	-  DOM Inspector用于视察、浏览和编辑DOM。
* **Firefox Firebug** - http://getfirebug.com/
	- Firebug为Firefox整合了编辑、调试、监视CSS、HTML和JavaScript功能。
* **Grendel-Scan** - http://securitytube-tools.net/index.php?title=Grendel_Scan
	- Grendel-Scan是一款自动化web应用安全测试工具，它也支持手工渗透测试。
*  **OWASP SWFIntruder** - http://www.mindedsecurity.com/swfintruder.html
	- SWFIntruder (读作 Swiff Intruder)是第一个专门用于实时分析和测试Flash应用的工具。
* **SWFScan** - http://h30499.www3.hp.com/t5/Following-the-Wh1t3-Rabbit/SWFScan-FREE-Flash-decompiler/ba-p/5440167
	- Flash反编译器。
*  **Wikto** - http://www.sensepost.com/labs/tools/pentest/wikto
	- Wikto具有模糊测试逻辑错误功能、后台挖掘功能、google辅助目录挖掘功能和实时HTTP请求/响应监视功能。
* **w3af** - http://w3af.org
	- w3af是一个web应用攻击和审计框架，这个项目分目标是发现和利用web应用漏洞。
* **skipfish** - http://code.google.com/p/skipfish/
	- Skipfish是一个主动式web应用侦查工具。
* **Web Developer toolbar** - https://chrome.google.com/webstore/detail/bfbameneiokkgbdmiekhjnmfkcnldhhm
	- Web开发者工具扩展为浏览器提供许多web开发者工具。这是Firefox官方扩展插件。
* **HTTP Request Maker** - https://chrome.google.com/webstore/detail/kajfghlhfkcocafkcjlajldicbikpgnp?hl=en-US
	- Request Maker是一个渗透测试工具，你可以使用他轻易捕捉web页面请求，修改URL、http头和POST数据。当然你也能创造新的请求。
* **Cookie Editor** - https://chrome.google.com/webstore/detail/fngmhnnpilhplaeedifhccceomclgfbg?hl=en-US
	- 一个Cookie管理器，可以用来添加、删除、修改、搜索、保护、阻隔Cookies。
* **Cookie swap** - https://chrome.google.com/webstore/detail/dffhipnliikkblkhpjapbecpmoilcama?hl=en-US
	- 一个会话管理器，用来管理cookies，让你能使用不同账号登陆网站。
* **Firebug lite for Chrome** -  https://chrome.google.com/webstore/detail/bmagokdooijbeehmkpknfglimnifench
    - Firebug Lite不是Firebug或Chrome开发者工具的替代品。他是一个整合这些工具的工具，他提供丰富的HTML元素、DOM元素、投影模型等可视化功能，他也能提供即时查看HTML元素、在线编辑CSS属性功能。
* **Session Manager** -  https://chrome.google.com/webstore/detail/bbcnbpafconjjigibnhbfmmgdbbkcjfi
    - 通过Session Manager你可以快速存储和读取你当前浏览器状态。你能够管理多个会话，重命名或异常会话数据库。每个会话都有独立的状态，比如打开的标签和窗口信息。
* **Subgraph Vega** - http://www.subgraph.com/products.html
    - Vega是一个免费开源的web应用扫描器和测试平台。他能帮你找到并验证SQL注入漏洞，XSS漏洞，敏感信息泄露以及其他漏洞，使用Java编写而成，拥有GUI界面，可以运行在Linux系统，OS X和windows系统。


#### 特定漏洞测试工具

##### DOM XSS测试工具
* DOMinator Pro - https://dominator.mindedsecurity.com


##### AJAX测试工具
* **[OWASP Sprajax Project](https://www.owasp.org/index.php/Category:OWASP_Sprajax_Project)**


##### SQL注入测试工具
* **[OWASP SQLiX](https://www.owasp.org/index.php/Category:OWASP_SQLiX_Project)**
* Sqlninja: 一个SQL Server注入工具 - http://sqlninja.sourceforge.net
* Bernardo Damele A. G.: sqlmap, 自动化SQL注入工具 - http://sqlmap.org/
* Absinthe 1.1 (过去叫做 SQLSqueal) - http://sourceforge.net/projects/absinthe/
* SQLInjector - 使用推荐技巧提取数据和确定后台数据库工具 - http://www.databasesecurity.com/sql-injector.htm
* Bsqlbf-v2: 盲注提取数据perl脚本 - http://code.google.com/p/bsqlbf-v2/
* Pangolin: 自动化SQL注入工具 - http://www.darknet.org.uk/2009/05/pangolin-automatic-sql-injection-tool/
* Antonio Parata: MySql推断备份工具 - SqlDumper - http://www.ruizata.com/
* 多系统SQL注入工具 - SQL Power Injector - http://www.sqlpowerinjector.com/
* MySql盲注暴破工具, Reversing.org - sqlbftools - http://packetstormsecurity.org/files/43795/sqlbftools-1.2.tar.gz.html


##### Oracle测试工具
* TNS Listener tool (Perl) - http://www.jammed.com/%7Ejwa/hacks/security/tnscmd/tnscmd-doc.html
* Toad for Oracle - http://www.quest.com/toad


##### SSL测试工具
* Foundstone SSL Digger - http://www.mcafee.com/us/downloads/free-tools/ssldigger.aspx


##### 暴力破解密码工具
* THC Hydra - http://www.thc.org/thc-hydra/
* John the Ripper - http://www.openwall.com/john/
* Brutus - http://www.hoobie.net/brutus/
* Medusa - http://www.foofus.net/~jmk/medusa/medusa.html
* Ncat - http://nmap.org/ncat/


##### 缓冲区溢出测试工具
*  OllyDbg - http://www.ollydbg.de
	- 一个windows下分析缓冲区溢出攻击的调试工具。
* Spike - http://www.immunitysec.com/downloads/SPIKE2.9.tgz
	- 一个用来发现漏洞的模糊测试框架
* Brute Force Binary Tester (BFB) - http://bfbtester.sourceforge.net
	- 一个主动型的二进制检查器
* Metasploit - http://www.metasploit.com/
	- 一个漏洞利用工具的快速开发和测试框架


##### 模糊测试工具
* **[OWASP WSFuzzer](https://www.owasp.org/index.php/Category:OWASP_WSFuzzer_Project)**
* Wfuzz - http://www.darknet.org.uk/2007/07/wfuzz-a-tool-for-bruteforcingfuzzing-web-applications/


##### googling搜索引擎测试工具
* Stach & Liu's Google Hacking Diggity Project - http://www.stachliu.com/resources/tools/google-hacking-diggity-project/
* Foundstone Sitedigger (Google cached fault-finding) - http://www.mcafee.com/us/downloads/free-tools/sitedigger.aspx


### 商业黑盒测试工具
* NGS Typhon III - http://www.nccgroup.com/en/our-services/security-testing-audit-compliance/information-security-software/ngs-typhon-iii/
* NGSSQuirreL - http://www.nccgroup.com/en/our-services/security-testing-audit-compliance/information-security-software/ngs-squirrel-vulnerability-scanners/
* IBM AppScan - http://www-01.ibm.com/software/awdtools/appscan/
* Cenzic Hailstorm - http://www.cenzic.com/products_services/cenzic_hailstorm.php
* Burp Intruder - http://www.portswigger.net/burp/intruder.html
* Acunetix Web Vulnerability Scanner - http://www.acunetix.com
* Sleuth - http://www.sandsprite.com
* NT Objectives NTOSpider - http://www.ntobjectives.com/products/ntospider.php
* MaxPatrol Security Scanner - http://www.maxpatrol.com
* Ecyware GreenBlue Inspector - http://www.ecyware.com
* Parasoft SOAtest (more QA-type tool)- http://www.parasoft.com/jsp/products/soatest.jsp?itemId=101
* MatriXay - http://www.dbappsecurity.com/webscan.html
* N-Stalker Web Application Security Scanner - http://www.nstalker.com
* HP WebInspect - http://www.hpenterprisesecurity.com/products/hp-fortify-software-security-center/hp-webinspect
* SoapUI (Web Service security testing) - http://www.soapui.org/Security/getting-started.html
* Netsparker - http://www.mavitunasecurity.com/netsparker/
* SAINT - http://www.saintcorporation.com/
* QualysGuard WAS - http://www.qualys.com/enterprises/qualysguard/web-application-scanning/
* Retina Web - http://www.eeye.com/Products/Retina/Web-Security-Scanner.aspx
* Cenzic Hailstorm - http://www.cenzic.com/downloads/datasheets/Cenzic-datasheet-Hailstorm-Technology.pdf


### 源代码分析工具

#### 开源/免费工具
* **[Owasp Orizon](https://www.owasp.org/index.php/Category:OWASP_Orizon_Project)**
* **[OWASP LAPSE](https://www.owasp.org/index.php/Category:OWASP_LAPSE_Project)**
* **[OWASP O2 Platform](https://www.owasp.org/index.php/OWASP_O2_Platform)**
* Google CodeSearchDiggity - http://www.stachliu.com/resources/tools/google-hacking-diggity-project/attack-tools/
* PMD - http://pmd.sourceforge.net/
* FlawFinder - http://www.dwheeler.com/flawfinder
* Microsoft’s [FxCop](https://www.owasp.org/index.php/FxCop)
* Splint - http://splint.org
* Boon - http://www.cs.berkeley.edu/~daw/boon
* FindBugs - http://findbugs.sourceforge.net
* Find Security Bugs - http://h3xstream.github.io/find-sec-bugs/
* Oedipus - http://www.darknet.org.uk/2006/06/oedipus-open-source-web-application-security-analysis/
* W3af - http://w3af.sourceforge.net/
* phpcs-security-audit - https://github.com/Pheromone/phpcs-security-audit


#### 商业软件

* Armorize CodeSecure - http://www.armorize.com/index.php?link_id=codesecure
* Parasoft C/C++ test - http://www.parasoft.com/jsp/products/cpptest.jsp/index.htm
* Checkmarx CxSuite  - http://www.checkmarx.com
* HP Fortify - http://www.hpenterprisesecurity.com/products/hp-fortify-software-security-center/hp-fortify-static-code-analyzer
* GrammaTech - http://www.grammatech.com
* ITS4 - http://seclab.cs.ucdavis.edu/projects/testing/tools/its4.html
* Appscan - http://www-01.ibm.com/software/rational/products/appscan/source/
* ParaSoft - http://www.parasoft.com
* Virtual Forge CodeProfiler for ABAP - http://www.virtualforge.de
* Veracode - http://www.veracode.com
* Armorize CodeSecure - http://www.armorize.com/codesecure/


### 验收测试工具
验收测试工具用来验证web应用的功能性完整。通过一系列程序方法和单元测试框架来组织测试套件和测试用例来进行测试。这些测试能够大部分覆盖安全相关测试和功能性测试


#### 其他开源工具

* WATIR - http://wtr.rubyforge.org
	- 一个基于RUby的web测试框架，提供IE接口。
	- 仅支持windows
* HtmlUnit - http://htmlunit.sourceforge.net
	- 一个基于Java、JUnit和Apache HttpClient的测试框架。
	- 非常健壮和可定制化，被一些其他工具作为测试引擎。
* jWebUnit - http://jwebunit.sourceforge.net
	- 一个基于Java的元测试框架，使用htmlunit或selenium作为测试引擎。
* Canoo Webtest - http://webtest.canoo.com
	- 一个基于XML测试工具，作为htmlunit的前端。
	- 不需要编写代码，完全由XML定义测试。
	- XML无法完成任务时，可以使用Groovy编写脚本。
	- 更新很积极。
* HttpUnit - http://httpunit.sourceforge.net
	- 最早的web测试框架，使用原生JDK提供HTTP传输，存在局限性。
* Watij - http://watij.com
	- WATIR的一个Java实现.
	- 由于使用IE进行测试，仅支持windows（Mozilla整合功能正在开发中）
* Solex - http://solex.sourceforge.net
	- 一个提供图形化界面来记录HTTP会话，并基于结果进行断言的Eclipse插件。
* Selenium - http://seleniumhq.org/
	- 基于JavaScript的测试框架，跨平台，提供GUI界面创建测试案例。
	- 非常成熟和流行的工具，但是使用JavaScript可能不利于部分安全测试。


### 其他工具

#### 实时(Runtime)分析工具

* Rational PurifyPlus - http://www-01.ibm.com/software/awdtools/purify/
* Seeker by Quotium - http://www.quotium.com/prod/security.php


#### 二进制文件分析工具

* BugScam IDC Package - http://sourceforge.net/projects/bugscam
* Veracode - http://www.veracode.com


#### 需求管理工具

* Rational Requisite Pro - http://www-306.ibm.com/software/awdtools/reqpro


#### 站点镜像工具
* wget - http://www.gnu.org/software/wget, http://www.interlog.com/~tcharron/wgetwin.html
* curl - http://curl.haxx.se
* Sam Spade - http://www.samspade.org
* Xenu's Link Sleuth - http://home.snafu.de/tilman/xenulink.html
