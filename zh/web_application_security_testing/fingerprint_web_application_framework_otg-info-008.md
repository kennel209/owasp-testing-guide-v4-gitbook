# 识别Web应用框架(OTG-INFO-008)


### 综述
Web框架[*]识别是信息收集过程简单重要的子任务。知道一个已知类型的框架而且被渗透测试过，这自然而然是一个巨大的优势。除了发现在未打补丁版本中的已知漏洞，还有了解在框架中特定的错误配置和已知文件目录框架使这一识别过程变得非常重要。


一些不同开发商不同版本的web框架被广泛使用。了解框架的信息对测试过程有极大帮助，也能帮助改进测试方案。这些信息可以从一些常见的地方仔细分析推断出来。大多数的web框架有几处特定的标记，能帮助攻击者识别他们。这也是基本上所有自动化工具做的事情，他们在定义好的位置搜寻标记，与数据库已知签名做比较。通常使用多个标记来增强准确程度。


[*] 请注意，这篇文章不区别Web应用框架（WAF）和内容管理系统（CMS）。这方便在同一章节中来识别他们。更进一步说，上述两个类别都被认为是web框架。


### 测试目标
定义使用的web框架来获得对安全测试方法论更好的理解。


### 如何测试

#### 黑盒测试
有好几个常见的地方来寻找当前框架：
* HTTP 头
* Cookies
* HTML 源代码
* 特别的文件和目录


##### HTTP 头
最基本识别web框架的方式是查看HTTP响应头中的*X-Powered-By*字段。许多工具可以用来识别目标，最简单一个是netcat。

考虑如下HTTP请求响应对：
```
$ nc 127.0.0.1 80
HEAD / HTTP/1.0

HTTP/1.1 200 OK
Server: nginx/1.0.14
Date: Sat, 07 Sep 2013 08:19:15 GMT
Content-Type: text/html;charset=ISO-8859-1
Connection: close
Vary: Accept-Encoding
X-Powered-By: Mono
```

从*X-Powered-By*字段中，我们能发现web应用框架很可能是Mono。尽管这个方法简单迅速，但是不会再100%的案例中有效。很有可能，*X-Powered-By*头被正确的配置禁用了。还有一些技巧使网站混淆HTTP头（参见下文整改措施章节的例子）。


所以在同样的例子中，测试者可能错过*X-Powered-By*头，或者得到其他消息，如下所示：
```
HTTP/1.1 200 OK
Server: nginx/1.0.14
Date: Sat, 07 Sep 2013 08:19:15 GMT
Content-Type: text/html;charset=ISO-8859-1
Connection: close
Vary: Accept-Encoding
X-Powered-By: Blood, sweat and tears
```


有时候有更多的HTTP头指向某个确定的web框架。在下面的例子中，根据HTTP响应的头，我们能发现*X-Powered-By*头包含PHP版本。然而*X-Generator*头指出使用的实际框架是Swiftlet，这能帮助渗透测试人员扩充他的攻击向量。在实施识别的过程中，总是应该仔细调查每一个HTTP头来寻找类似信息。
```
HTTP/1.1 200 OK
Server: nginx/1.4.1
Date: Sat, 07 Sep 2013 09:22:52 GMT
Content-Type: text/html
Connection: keep-alive
Vary: Accept-Encoding
X-Powered-By: PHP/5.4.16-1~dotdeb.1
Expires: Thu, 19 Nov 1981 08:52:00 GMT
Cache-Control: no-store, no-cache, must-revalidate, post-check=0, pre-check=0
Pragma: no-cache
X-Generator: Swiftlet
```


##### Cookies
另一个类似的，有时候更加可靠来决定当前web框架的是与其相关的框架特定cookies。

考虑如下HTTP请求：

![Image:Cakephp_cookie.png](https://www.owasp.org/images/4/49/Cakephp_cookie.png)


cookie *CAKEPHP* 被自动设置了，提示了我们使用的框架信息。常见cookies名字列表在下文常见框架章节中列出。限制条件与前者相同，可能cookie名字被改变。例如所标示的 *CakePHP*框架能通过下面配置改变（摘自core.php）。

```
/**
* The name of CakePHP's session cookie.
*
* Note the guidelines for Session names states: "The session name references
* the session id in cookies and URLs. It should contain only alphanumeric
* characters."
* @link http://php.net/session_name
*/
Configure::write('Session.cookie', 'CAKEPHP');
```


然而cookies不像*X-Powered-By*头那样可能变化，所以这个方法被认为更加可靠


##### HTML 源代码
这个技巧基于在HTML页面源代码中找到某一模板。我们常常能找到许多信息来帮助测试者辨认出一个特定web框架。一个通常的标志是HTML注释常常导致框架暴露。更常见的是某一框架相关的路径被发现，比如框架相关的css链接，js脚本目录。最后特定脚本变量也可能揭露特定框架。


从下面的截图我们可以通过上文提到的标记轻松发现使用的框架和他的版本。注释、特殊路径和脚本变量都能帮助攻击者迅速发现这是一个ZK框架的实例。

![Image:Zk_html_source.png](https://www.owasp.org/images/6/60/Zk_html_source.png)


这些信息很大可能存在于 `<head></head>` 标签之间，在 `<meta>` 标签内或者页面最后。无论如何，推荐检查整个文档，因为这也能有益于其他目的，比如寻找其他有用注释和隐藏表单字段。有时候，web开发者并不关心隐藏关于框架的信息。所以有时候你可能在页面底下发现如下信息：

![Image:banshee_bottom_page.png](https://www.owasp.org/images/9/9d/Banshee_bottom_page.png)


### 常见框架
#### Cookies

| 框架 | Cookie 名称     |
|-----------|-----------------|
| Zope      | zope3           |
| CakePHP   | cakephp         |
| Kohana    | kohanasession   |
| Laravel   | laravel_session |

#### HTML 源代码
##### 通用标记

| %framework_name% |
|------------------|
| powered by       |
| built upon       |
| running          |


##### 特定标志

| 框架         | 关键字                   |
|-------------------|---------------------------|
| Adobe ColdFusion  | `<!-- START headerTags.cfm` |
| Microsoft ASP.NET | `__VIEWSTATE`               |
| ZK                | `<!-- ZK`                   |
| Business Catalyst | `<!-- BC_OBNW -->`          |
| Indexhibit        | `ndxz-studio`               |


#### 特定文件和目录
每个特定框架都有不同特定文件和目录。推荐在渗透测试过程中自己搭建安装相关框架以便于更好理解框架的基础结构和明确服务器上的遗留文件。一些有用的文件类表已经存在，比如FuzzDB的预测文件和文件夹的字典（http://code.google.com/p/fuzzdb/ ）。


### 测试工具
下面展示了一系列通用和知名的测试工具列表。出了框架识别外他们还有许多其他功能。


#### WhatWeb
网站:  http://www.morningstarsecurity.com/research/whatweb <br>
现在市场上最好的识别工具之一。默认包括在[Kali Linux]之中。
语言: Ruby
使用下面技巧匹配指纹库：
* 字符串 （大小写敏感）
* 正则表达式
* Google Hack数据库查询（有限关键字组）
* MD5哈希值
* URL 识别
* HTML 标签模式
* 自定义ruby代码，被动和主动操作.


下面的截屏展现一个输出样例：

![Image:whatweb-sample.png](https://www.owasp.org/images/8/8e/Whatweb-sample.png)



#### BlindElephant
网站: https://community.qualys.com/community/blindelephant <br>
这个优秀的工具工作原理是基于不同版本的静态文件校验和，他提供了一个非常高质量的识别指纹库。T
语言: Python

一个成功识别的输出样例：
```
pentester$ python BlindElephant.py http://my_target drupal
Loaded /Library/Python/2.7/site-packages/blindelephant/dbs/drupal.pkl with 145 versions, 478 differentiating paths, and 434 version groups.
Starting BlindElephant fingerprint for version of drupal at http://my_target

Hit http://my_target/CHANGELOG.txt
File produced no match. Error: Retrieved file doesn't match known fingerprint. 527b085a3717bd691d47713dff74acf4

Hit http://my_target/INSTALL.txt
File produced no match. Error: Retrieved file doesn't match known fingerprint. 14dfc133e4101be6f0ef5c64566da4a4

Hit http://my_target/misc/drupal.js
Possible versions based on result: 7.12, 7.13, 7.14

Hit http://my_target/MAINTAINERS.txt
File produced no match. Error: Retrieved file doesn't match known fingerprint. 36b740941a19912f3fdbfcca7caa08ca

Hit http://my_target/themes/garland/style.css
Possible versions based on result: 7.2, 7.3, 7.4, 7.5, 7.6, 7.7, 7.8, 7.9, 7.10, 7.11, 7.12, 7.13, 7.14

...

Fingerprinting resulted in:
7.14


Best Guess: 7.14
```


#### Wappalyzer
网站: http://wappalyzer.com <br>
Wapplyzer是一个Firefox和Chrome插件。他只依赖于正则表达式，只需要一个浏览器上载入的页面就能工作。在浏览器层面工作并用图表形式给出结果。尽管有时候他会误报，但是在浏览一个网页后立刻能组织出目标站点使用技术信息也非常有用。


下面截图展示了一个输出样例：

![Image:Owasp-wappalyzer.png](https://www.owasp.org/images/a/a7/Owasp-wappalyzer.png)


### 参考资料
**白皮书**<br>
* Saumil Shah: "An Introduction to HTTP fingerprinting" - http://www.net-square.com/httprint_paper.html
* Anant Shrivastava : "Web Application Finger Printing" - http://anantshri.info/articles/web_app_finger_printing.html


### 整改措施
通用的建议是使用上面描述的工具并查看日志理解攻击者如何暴露web框架。通过多次扫描修改隐藏框架操作，达到一个较好的安全等级和保证框架不会被自动化扫描检测出来。下面是一些关于框架标志位置的特定建议和一些额外的有趣的方法。


#### HTTP 头
检查配置和禁止或者混淆所有会暴露信息的HTTP头。这里有一篇有趣的文章关于使用NetScaler混淆HTTP头的文章：
http://grahamhosking.blogspot.ru/2013/07/obfuscating-http-header-using-netscaler.html


#### Cookies
推荐通过修改相关配置文件来改变cookie名称。


#### HTML 源代码
手动检查HTML代码内容，移除所有明显指向框架的内容。

通用指南:
* 确保没有暴露框架可视标记；
* 移除不需要的注释（版权，bug信息，特定框架注释）；
* 移除生成的元标签；
* 使用公司自己的css和js脚本文件，不要存放在框架相关的目录；
* 不要使用页面默认的脚本，如果必须使用，混淆他们。


#### 特定文件和目录
通用指南：
* 在服务器上移除所有不需要的和无用的文件。这意味着也包括会暴露版本信息的文本文件和安装文件。
* 使用404错误响应来限制从外部访问其他文件。例如这可以通过修改htaccess文件，加入重写规则 RewriteCond 和 RewriteRuleRestrict。例如，限制两个常见的WordPress文件夹的例子如下：
```
RewriteCond %{REQUEST_URI} /wp-login\.php$ [OR]
RewriteCond %{REQUEST_URI} /wp-admin/$
RewriteRule $ /http://your_website [R=404,L]
```


当然，这不是唯一限制访问的方法，有相关特定框架的插件存在来自动化这个过程。一个WordPress的例子是StealthLogin (http://wordpress.org/plugins/stealth-login-page)。


#### 其他措施
通用指南：
* 校验和管理
    - 这个措施的目的是打败基于校验和的扫描器以及不让他们通过哈希值暴露文件。通常有两个方法进行校验和管理：
    - 改变这些文件存在的位置（就是将他们移动到另一个文件夹，或者重命名文件夹）
    - 修改文件内容 - 甚至细微的修改就能导致完全不同的哈希值，所以在文件末尾添加单个字节应该不是一个大问题。
* 制造混乱
    - 有个有趣且有效的方法需要从添加其他框架的伪装文件来愚弄工具盒混乱攻击者。但需要注意不要覆盖存在的文件和目录破坏现有框架。
