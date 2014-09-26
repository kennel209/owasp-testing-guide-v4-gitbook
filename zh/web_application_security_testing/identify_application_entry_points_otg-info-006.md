# 鉴别应用入口点 (OTG-INFO-006)


### 综述
枚举应用和他的攻击面是一个关键的前期准备工作，应该在完全测试开展前进行，他为测试者识别了可能的弱点范围。这部分目标是一旦完成枚举映射工作，帮助识别和筹划应用中应该被详细调查的区域。


### 测试目标

理解请求是如何组织的，和典型的应用响应。


### 如何测试

在任何测试开始前，测试者总是应该对应用程序有足够的理解，明白用户和浏览器是如何与应用通信的。随着测试者在应用中遨游，他应当特别关注于所有的HTTP请求（GET和POST方法，也叫做谓词）以及每个传递给应用的参数和表单。此外也应该注意在传参数给应用时，什么时候使用的是GET请求，什么时候又使用了POST请求。通常情况下大多数使用GET请求，但是当传送敏感信息时，往往包含在POST请求的主体中。


注意为了查看POST请求中参数，测试这可能需要使用数据劫持代理工具（比如OWASP的[Zed Attack Proxy (ZAP)](https://www.owasp.org/index.php/OWASP_Zed_Attack_Proxy_Project)）或者一些浏览器插件。在POST请求中，测试者应当特别注意传递给应用的任何表单隐藏域，往往他们包含一些敏感信息，这些信息可能是开发者不希望你看见或者修改的，如信息状态、物品数量、物品价格信息等等。


根据作者的经验，在这个阶段使用一个数据劫持代理和电子表格是非常有用的。代理工具能记录和追踪每一个测试者和应用之间的请求和响应。此外，测试者通常能捕获每一个请求和响应，能够清楚看到每一个发出的和返回的头、参数等等信息。这些可能有时十分乏味特别是大型交互网站（想一想银行应用）。但是经验积累会告诉你该看什么，这个过程将极大地减轻。


当测试者在漫游应用的时候，也应当注意在URL中、自定义HTTP头中或请求响应中的有趣的参数，并在电子表格中记录下来。表格中应当包含被请求的页面（或许加入代理中的请求序号来做引用会更好），有趣的参数，请求类型（POST/GET），访问是否需要认证，是否使用SSL，以及其他相关备注（如果有多个过程）。一旦每一个应用区域都被映射完成，测试者应该测试每一个他们识别出来的地方，记录是否如预期一样工作。指南剩下的部分会指导如何测试这些有趣的区域，但是这章的工作必须在任何测试正式开始前完成。


下面是通用的请求和响应中有意思的点，在请求部分，关注GET和POST方法，他往往是请求的主要部分。注意其他方法如PUT和DELETE也可能被使用。这些更加罕见的请求如果被接受，经常会产生漏洞。在指南中有特别的一个章节描述如何测试HTTP方法。


**请求:**
* 识别GET请求和POST请求使用的地方。
* 识别所有使用在POST请求中的参数（这些参数在请求主体中）。
* 在POST请求中，特别注意隐藏参数。POST请求会在HTTP消息的主体中发送所有的表单域（包括隐藏参数）给应用。这些往往不可见，除非使用代理或者查看页面源代码。此外，隐藏属性 的值可能导致不同的后续页面、数据和访问级别。
* 识别所有GET请求中的参数（如URL），特别是查询字符串（一般跟着`?`标记后）。
* 识别查询字符串中的所有参数。这些参数往往成对出现，如foo=bar。注意一下，许多参数也能在一个查询字符串中，用`&, ~, :`或者其他特殊字符或编码分割。
* 注意如果在查询字符串或POST请求中存在多个参数，需要识别执行攻击中真正需要的一些或所有参数。测试者需要识别所有参数（甚至编码过或加密过的），识别出哪些是被应用程序处理的。指南后面章节会指导你如何测试这些参数，在这里，我们只需要确认识别出每一个参数即可。
* 注意有些附加或自定义的头不是正常情况能发现的（比如debug=False）。


**响应:**
* 识别在哪里新cookies被设置（Set-Cookie头），修改或新增。
* 识别出在正常访问过程中（未修改正常请求）。重定向跳转发生的地方（3xx HTTP 状态码），400 状态码，特别是403 禁止访问，和500 内部服务器错误。
* 也注意有些有趣的HTTP头。比如, "Server: BIG-IP" 表明这个站点被负载均衡。因此，如果一个站点是负载均衡的，而且有一个服务器没有被正确配置，那么测试者需要请求多次来访问有漏洞的服务器，取决于使用了何种负载均衡设备。


#### 黑盒测试
**测试应用入口点** <br>
下面是如何测试应用入口点的两个例子。


##### 例1
这个例子展现一个从在线商店购买东西的GET请求。
```
 GET https://x.x.x.x/shoppingApp/buyme.asp?CUSTOMERID=100&ITEM=z101a&PRICE=62.50&IP=x.x.x.x
 Host: x.x.x.x
 Cookie: SESSIONID=Z29vZCBqb2IgcGFkYXdhIG15IHVzZXJuYW1lIGlzIGZvbyBhbmQgcGFzc3dvcmQgaXMgYmFy
```

**期望结果：**

这里测试者可能注意到了所有在请求中的参数如CUSTOMERID，ITEM，PRICE，IP和Cookie（用于会话状态，经过编码的参数）。


##### 例2
这个例子展现了登陆一个应用的POST请求。
```
 POST https://x.x.x.x/KevinNotSoGoodApp/authenticate.asp?service=login
 Host: x.x.x.x
 Cookie: SESSIONID=dGhpcyBpcyBhIGJhZCBhcHAgdGhhdCBzZXRzIHByZWRpY3RhYmxlIGNvb2tpZXMgYW5kIG1pbmUgaXMgMTIzNA
 CustomCookie=00my00trusted00ip00is00x.x.x.x00
```

POST请求消息主体：
```
 user=admin&pass=pass123&debug=true&fromtrustIP=true
```

**期望结果：**

在这个例子中测试者应该注意之前注意过的参数，但是请注意参数在消息的主体中传递，而不是URL中。此外，注意我们使用了一个自定义的cookie。


#### 灰盒测试

通过灰盒方法来测试应用入口点包括我们已经识别出来的上文部分，再加上另外一点。在从外部数据源获取数据并处理的情况中（如SNMP捕获，syslog消息，SMTP或其他服务器的SOAP信息）。与应用开发者进行一次会谈，来识别处理功能函数，用户输入期望和输入格式。例如，开发者能帮助理解如何编写一个应用接受的正确的SOAP请求，这些web服务或其他功能可能是我们没在黑盒测试中考虑到和识别出来的。


### 测试工具

**劫持代理:**<br>

* OWASP: [Zed Attack Proxy (ZAP)](https://www.owasp.org/index.php/OWASP_Zed_Attack_Proxy_Project)
* OWASP: [WebScarab](https://www.owasp.org/index.php/OWASP_WebScarab_Project)
* [Burp Suite](http://www.portswigger.net/burp/)
* [CAT](http://www.contextis.com/research/tools/cat/)


**浏览器插件:**<br>

* [TamperIE for Internet Explorer](http://www.bayden.com/TamperIE/)
* [Tamper Data for Firefox](https://addons.mozilla.org/en-US/firefox/addon/966)


### 参考资料

**白皮书**<br>

* RFC 2616 – Hypertext Transfer Protocol – HTTP 1.1 -
http://tools.ietf.org/html/rfc2616
