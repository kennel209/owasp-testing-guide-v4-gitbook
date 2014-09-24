# 搜索引擎信息发现和侦察 (OTG-INFO-001)

### 综述
使用搜索引擎来侦察有直接和间接两种办法。直接的方法是直接查询索引和从缓存中发现相关内容。间接的方法是从论坛、新闻组和其他相关网站发现敏感信息和配置信息。


一旦搜索引擎机器人完成抓取工作，它会基于标签如*`<TITLE>`*或者属性来组织相关内容的索引[1]。如果robots.txt没有更新，或者也没有内联HTML标签要求不抓取，搜索引擎可能会检索到拥有者不希望包含的页面。网站管理员可以使用上面提到的robots.txt文件、HTLM元标签、认证措施或者搜索引擎提供的工具来移除这些内容。


### 测试目标

了解有多少应用/系统/组织的敏感设计和配置信息在网上公开，包括直接在组织网站公布和第三方网站间接公开。


### 如何测试

使用搜索引擎来查找：
* 网络拓扑和配置
* 获得管理员或者其他核心员工的发帖信息和邮件
* 登陆流程和用户名格式
* 用户名和密码
* 错误消息内容
* 开发、测试、验收和上线版本的网站


#### 搜索选项
使用高级的"site:"搜索选项，他可以帮助检索特定域名下的内容[2]。不要局限在一种所搜索引擎，不同的引擎抓取页面有不同的算法，可能会产生不同的结果。可以考虑使用下面这些搜索引擎：

* Baidu
* binsearch.info
* Bing
* Duck Duck Go
* ixquick/Startpage
* Google
* Shodan
* PunkSpider


Duck Duck Go 和 ixquick/Startpage 提供关于测试者简化的泄露信息。

Google提供另一个高级的搜索选项"cache:"[2]，它相当于在Google搜索结果页面里面点击"Cached"按钮。所以更加推荐先使用"site:"，在结果中在寻找缓存按钮。

Google SOAP 搜索 API 支持 "doGetCachedPage" 和相关的"doGetCachedPageResponse" SOAP消息[3] ，来帮助获取缓存页面。一个相关的实现正在开发中，请参考 [OWASP "Google Hacking" Project](https://www.owasp.org/index.php/Category:OWASP_Google_Hacking_Project)项目。

PunkSpider 是一个应用程序漏洞搜素引擎。他给渗透测试人员进行手工测试工作只能带来一点帮助，但是他可以作为证明脚本小子发现漏洞是如此容易的一个例子。


**例子**

比如一个典型搜索引擎发现owasp.org的网页内容的例子如下：
```
site:owasp.org
```
![Image:Google_site_Operator_Search_Results_Example_20121219.jpg||border](https://www.owasp.org/images/6/67/Google_site_Operator_Search_Results_Example_20121219.jpg)

展示owasp.org的index.html的缓存页面如下：
```
cache:owasp.org
```
![Image:Google_cache_Operator_Search_Results_Example_20121219.jpg||border](https://www.owasp.org/images/3/3f/Google_cache_Operator_Search_Results_Example_20121219.jpg)


#### Google Hacking 数据库

Google Hacking 数据库是一组十分有用的Google查询语句。查询被分为如下几个类别：
* 演示页面
* 包含文件名的文件
* 敏感目录
* Web服务器探测
* 漏洞文件
* 漏洞服务器
* 错误信息
* 包含有趣信息的文件
* 包含密码的文件
* 敏感在线购物信息


### 测试工具
* FoundStone SiteDigger - http://www.mcafee.com/uk/downloads/free-tools/sitedigger.aspx <br>
* Google Hacker - http://yehg.net/lab/pr0js/files.php/googlehacker.zip<br>
* Stach & Liu's Google Hacking Diggity Project - http://www.stachliu.com/resources/tools/google-hacking-diggity-project/ <br>
* PunkSPIDER - http://punkspider.hyperiongray.com/ <br>


### 参考资料
**Web**<br>
[1] "Google Basics: Learn how Google Discovers, Crawls, and Serves Web Pages" - https://support.google.com/webmasters/answer/70897 <br>
[2] "Operators and More Search Help" - https://support.google.com/websearch/answer/136861?hl=en <br>
[3] "Google Hacking Database" - http://www.exploit-db.com/google-dorks/ <br>


### 整改措施
在敏感设计资料和配置信息公布在网上时请再三考虑。

定期审查公开在网上的敏感设计资料和配置信息配置信息。

