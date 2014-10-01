# Fingerprint Web Application (OTG-INFO-009)

### Summary

There is nothing new under the sun, and nearly every web application that one may think of developing has already been developed. With the vast number of free and open source software projects that are actively developed and deployed around the world, it is very likely that an application security test will face a target site that is entirely or partly dependent on these well known applications (e.g. Wordpress, phpBB, Mediawiki, etc). Knowing the web application components that are being tested significantly helps in the testing process and will also drastically reduce the effort required during the test. These well known web applications have known HTML headers, cookies, and directory structures that can be enumerated to identify the application.


### Test Objectives

Identify the web application and version to determine known vulnerabilities and the appropriate exploits to use during testing.


### How to Test

#### Cookies
A relatively reliable way to identify a web application is by the application-specific cookies.

Consider the following HTTP-request:

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

The cookie *CAKEPHP* has automatically been set, which gives information about the framework being used. List of common cookies names is presented in Cpmmon Application Identifiers section. However, it is possible to change the name of the cookie.


#### HTML source code
This technique is based on finding certain patterns in the HTML page source code. Often one can find a lot of information which helps a tester to recognize a specific web application. One of the common markers are HTML comments that directly lead to application disclosure. More often certain application-specific paths can be found, i.e. links to application-specific css and/or js folders. Finally, specific script variables might also point to a certain application.

From the meta tag below, one can easily learn the application used by a website and its version. The comment, specific paths and script variables can all help an attacker to quickly determine an instance of an application.

```
<meta name="generator" content="WordPress 3.9.2" />
```

More frequently such information is placed between `<head></head>` tags, in `<meta>` tags or at the end of the page. Nevertheless, it is recommended to check the whole document since it can be useful for other purposes such as inspection of other useful comments and hidden fields.

#### Specific files and folders
Apart from information gathered from HTML sources, there is another approach which greatly helps an attacker to determine the application with high accuracy. Every application has its own specific file and folder structure on the server. It has been pointed out that one can see the specific path from the HTML page source but sometimes they are not explicitly presented there and still reside on the server.

In order to uncover them a technique known as dirbusting is used. Dirbusting is brute forcing a target with predictable folder and file names and monitoring HTTP-responses to emumerate server contents. This information can be used both for finding default files and attacking them, and for fingerprinting the web application. Dirbusting can be done in several ways, the example below shows a successful dirbusting attack against a WordPress-powered target with the help of defined list and intruder functionality of Burp Suite.

![Image:Wordpress_dirbusting.png](https://www.owasp.org/images/3/35/Wordpress_dirbusting.png)

We can see that for some WordPress-specific folders (for instance, /wp-includes/, /wp-admin/ and /wp-content/) HTTP-reponses are 403 (Forbidden), 302 (Found, redirection to wp-login.php) and 200 (OK) respectively. This is a good indicator that the target is WordPress-powered. The same way it is possible to dirbust different application plugin folders and their versions. On the screenshot below one can see a typical CHANGELOG file of a Drupal plugin, which provides information on the application being used and discloses a vulnerable plugin version.

![Image:Drupal_botcha_disclosure.png](https://www.owasp.org/images/c/c9/Drupal_botcha_disclosure.png)

Tip: before starting dirbusting, it is recommended to check the robots.txt file first. Sometimes application specific folders and other sensitive information can be found there as well. An example of such a robots.txt file is presented on a screenshot below.

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
