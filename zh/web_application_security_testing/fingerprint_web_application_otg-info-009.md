# 识别Web应用程序 (OTG-INFO-009)

### 综述

其实没有什么新鲜的事，几乎每个想开发的web应用基本都已经被开发过了。在世界上存在着巨大数量的免费和开源软件项目正在被积极开发和部署，很有可能一个应用安全测试将面对一个目标站点是完全或者部分依赖这些知名的应用程序（如Wedpress，phpBB，Mediawiki等等）。了解即将被测试的web应用组件将极大帮助测试过程，也会减少测试开销。这些知名的web应用程序拥有已知的HTML头，cookies，和目录结构可以被枚举来鉴别这些应用。


### 测试目标

鉴别Web应用程序和其版本来确定已知漏洞和可能的利用方式。


### 如何测试

#### Cookies
一个相当可靠的方法来测试web应用是检查应用特定的cookies。

考虑如下HTTP请求：

```
GET / HTTP/1.1
User-Agent: Mozilla/5.0 (Windows NT 6.2; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
**Cookie: wp-settings-time-1=1406093286; wp-settings-time-2=1405988284**
DNT: 1
Connection: keep-alive
Host: blog.owasp.org
```

cookie *CAKEPHP* 被自动设置，指明了我们框架信息。在常见应用识别章节我们会列举一系列常见的cookies名称。不过，cookie名称还是有可能被改变的。


#### HTML 源代码
这个技巧基于在HTLM页面源代码中搜寻特征模式。通常我们能找到许多能帮助测试者识别特定web应用的信息。一个常见的地方是HTML注释直接暴露了应用信息。更常见的是应用相关的路径信息，比如链接特定应用css或者js目录。最后，特定的脚本变量也能指明特定的应用信息。

从下面的元标签，我们能轻易发现网站使用的应用程序和其版本。注释、特定路径和脚本变量都能帮助攻击者快速确定应用实例。

```
<meta name="generator" content="WordPress 3.9.2" />
```

更常见的是这些信息往往能在`<head></head>`标签，`<meta>`标签或页面底部发现。无论如何，推荐检查整个文档因为这也有助于检查有用的注释和隐藏字段。

#### 特定文件和路径
除了从HTML源代码里面收集到的信息，还有个方法能极大帮助攻击者确定应用程序。每个应用都有自己特定的文件和目录结构。事实表明我们能从HTML页面源代码中找到特定的路径信息，有时候他们并没有在代码中明显出现，但是仍然遗留在服务器上。

为了发现他们，一个叫dirbusting的技巧被使用。Dirbusting是通过预测目录和文件名称并监视HTTP相应来暴力破解一个目标枚举服务内容。这些信息也可以用在发现默认文件和攻击系统以及识别web应用之中。Dirbusting可以通过很多方法实现，下面的例子展示了一个成功的攻击，通过Burp Suite的intruder功能和预先定义的列表来攻击一个基于WordPress的站点。

![Image:Wordpress_dirbusting.png](https://www.owasp.org/images/3/35/Wordpress_dirbusting.png)

我们能发现一些WordPress特定的目录（比如，/wp-includes/，/wp-admin/和/wp-content/）的HTTP响应是403（禁止访问），302（找到，并重定向到wp-login.php）和200（OK）。这很好指明了站点是基于WordPress开发的。同样的方法我们能暴力列举不同的应用插件目录和他们的版本信息。在下面的截图中，我们能发现一个典型的Drupal插件的CHANGELOG文件，这提供了应用程序的信息，并暴露了一个漏洞插件版本。

![Image:Drupal_botcha_disclosure.png](https://www.owasp.org/images/c/c9/Drupal_botcha_disclosure.png)

小提示：在开始暴力枚举前，推荐先检查robots.txt文件。有时候应用特定的目录和其他敏感信息也能在这里发现。下面是这样的一个例子截图：

![Image:Robots_info_disclosure.png](https://www.owasp.org/index.php?title=Special:Upload&wpDestFile=Robots_info_disclosure.png)

每个特定框架都有不同特定文件和目录。推荐在渗透测试过程中自己搭建安装相关框架以便于更好理解框架的基础结构和明确服务器上的遗留文件。一些有用的文件类表已经存在，比如FuzzDB的预测文件和文件夹的字典（http://code.google.com/p/fuzzdb/ ）。

### 常见应用识别
#### Cookies

| 框架    | Cookie 名称                       |
|--------------|-----------------------------------|
| phpBB        | phpbb3_                           |
| Wordpress    | wp-settings                       |
| 1C-Bitrix    | BITRIX_                           |
| AMPcms       | AMP                               |
| Django CMS   | django                            |
| DotNetNuke   | DotNetNukeAnonymous               |
| e107         | e107_tz                           |
| EPiServer    | EPiTrace, EPiServer               |
| Graffiti CMS | graffitibot                       |
| Hotaru CMS   | hotaru_mobile                     |
| ImpressCMS   | ICMSession                        |
| Indico       | MAKACSESSION                      |
| InstantCMS   | InstantCMS[logdate]               |
| Kentico CMS  | CMSPreferredCulture               |
| MODx         | SN4[12symb]                       |
| TYPO3        | fe_typo_user                      |
| Dynamicweb   | Dynamicweb                        |
| LEPTON       | lep[some_numeric_value]+sessionid |
| Wix          | Domain=.wix.com                   |
| VIVVO        | VivvoSessionId                    |


#### HTML 源代码

| 应用 | 关键字                                                                      |
|-------------|------------------------------------------------------------------------------|
| Wordpress   | `<meta name="generator" content="WordPress 3.9.2" />`                          |
| phpBB       | `<body id="phpbb"   `                                                          |
| Mediawiki   | `<meta name="generator" content="MediaWiki 1.21.9" />`                         |
| Joomla      | `<meta name="generator" content="Joomla! - Open Source Content Management" />` |
| Drupal      | `<meta name="Generator" content="Drupal 7 (http://drupal.org)" />`             |
| DotNetNuke  | DNN Platform - http://www.dnnsoftware.com                                    |



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
