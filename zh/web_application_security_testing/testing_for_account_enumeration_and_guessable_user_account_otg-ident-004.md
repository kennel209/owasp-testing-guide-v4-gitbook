# 测试帐户枚举和可猜测的用户帐户 (OTG-IDENT-004)

### 综述
这个测试的范围是验证嫩条通过应用的认证机制交互来收集一系列的合法用户名。这个测试可能对暴力破解测试有帮助，在这个测试中发现合法的用户名来找到相应的密码。


通常web应用会显示用户名是否存在系统中，这个结果可能是策略决定或者错误配置的结果。举例说明，有时候，当我们提交错误的凭证信息，我们得到一个消息，告诉我们用户名存在在系统上，或提供的密码有误。这个信息可以被攻击者利用来获得一个系统上用户列表。这些信息可能用于攻击web应用，比如通过暴力破解，或默认用户名密码攻击系统。


测试这应该与认证机制交互来弄清楚发送特定请求是否会引起应用程序不同的方式应答。这个问题存在的原因是web应用或web服务器当用户提供合法的用户名返回的信息区别于用户提供非法的用户名的信息。


在一些例子中，获得消息可以揭示提供的凭证有错误是因为非法用户名或者非法密码。有时候测试这可以通过发送用户名和空密码来枚举存在的用户。


### 如何测试
在黑盒测试中，测试者不知道特定应用程序、用户名、应用逻辑、登陆错误信息或密码找回功能。如果应用程序存在漏洞，测试者获得的响应消息可以直接或间接揭示出有用的消息来枚举用户。


#### HTTP响应消息

**测试合法用户/正确密码**

记录和合法用户ID和合法密码的服务器应答。


**期望结果：**

使用WebScarab，注意成功认证收到的信息（HTTP 200 响应，响应长度）。


**测试合法用户，错误密码** 

现在，测试者应该尝试合法用户ID和错误密码，并记录应用生成的错误消息。


**期望结果：**

浏览器返回消息应该类似下图：

![Image:AuthenticationFailed.png](https://www.owasp.org/images/f/f8/AuthenticationFailed.png)

或者类似：

![Image:NoConfFound.jpg](https://www.owasp.org/images/4/43/NoConfFound.jpg)

相对的，任何消息揭示用户的存在，如类似下面信息：

```
 Login for User foo: invalid password
```

使用WebScarab，注意从这个不成功的认证企图中获得的消息（HTTP 200 响应，响应长度等）。


**测试一个不存在的用户名**

现在，测试者应该尝试不合法的用户ID和错误密码，记录服务器应答（测试者应该确认用户名不合法）。记录错误消息和服务器应答。


**期望结果：**

如果测试者输入不存在的用户ID，他们可能收到类似消息：

![Image:Userisnotactive.png](https://www.owasp.org/images/8/8d/Userisnotactive.png)

或者如下消息：

```
 Login failed for User foo: invalid Account
```

通常情况下，应用程序应该响应同样的错误页面和响应长度来应对不同的错误请求。如果响应不是相同的，测试者应该调查，并找出产生不同响应的关键之处。例如：
```
* Client request: Valid user/wrong password --> Server answer:'The password is not correct'
* Client request: Wrong user/wrong password --> Server answer:'User not recognized'
```

上面响应让客户端明白前一个请求他们拥有合法用户名，所以他们可以通过与应用程序交互请求来获得可能的用户ID。

观察第二个响应，测试者通过相同的方法明白他们不是合法的用户名。所以他们也能通过同样的方法创建出一系列合法的用户ID。


#### 其他枚举用户的方法

测试者可以通过集中不同的方法枚举用户，比如：


* ** 分析登陆页面获取的错误返回码**

一些应用程序返回特定的错误代码或消息，便于我们能够进行分析。


* ** 分析URL和重定向URL**

例如：
```
 http://www.foo.com/err.jsp?User=baduser&Error=0
 http://www.foo.com/err.jsp?User=gooduser&Error=2
```

如上所示，当测试者向web应用程序提供用户ID和密码，他们能看见在URL中指明错误是如何发生的消息。在第一个例子中是错误的用户ID和密码，后一个例子中，正确的ID和密码。如此能识别出合法用户ID。


* ** URI 探测**

有时候，web服务器对存在或这不存在的目录会返回不同响应。例如，有些个人入口分配目录给用户。如果测试者访问存在的目录，他们会得到web服务器错误消息。


通常从web服务器获得的消息是：
```
   403 Forbidden error code
```
以及：
```
   404 Not found error code
```

例子：
```
 http://www.foo.com/account1 - we receive from web server: 403 Forbidden
 http://www.foo.com/account2 - we receive from web server: 404 file Not Found
```

在第一个例子中用户存在，但是测试者无法查看网页，第二个例子中，用户“account2”不存在。通过这个方法收集信息来可以列举用户。


* ** 分析Web页面标题**

测试者可以通过web页面标题获得有用信息，比如获得特定的错误码或消息来揭示问题发生在用户名还是密码上。


例如，一个用户没有被认证会返回类似页面标题：
```
 Invalid user
 Invalid authentication
```

* ** 分析从恢复机制中获得的消息**

当我们使用恢复机制时候（如忘记密码功能），漏洞程序可能返回消息揭示用户名是否存在。

例如，类似下面的消息：
```
 Invalid username: e-mail address is not valid or the specified user was not found.
 Valid username: Your password has been successfully sent to the email address you registered with.
```


* ** 友善的404错误消息**

当我们通过目录请求不存在的用户时候，并不总是得到404错误。相对的，我们可能获得“200 ok”和图像，在这个例子中，我们能假定我们收到特定的图像时用户不存在。这个逻辑也能被应用在其他服务器响应中，其中的诀窍是对web服务器和web应用消息进行良好分析。


#### 猜测用户
在一些情况中，用户ID通过管理员或公司的特定策略创建。例如，我们可以观察到用户ID序列化生成：
```
		CN000100
		CN000101
		…. 
```

有时用户名通过域别名创建，跟着序列号：
```
		R1001 – user 001 for REALM1
		R2001 – user 001 for REALM2

```

在上面的例子中，我们可以创建简单的脚本来生成用户ID，通过工具提交请求，比如wget，来自动化web查询发现合法的用户ID。我们也可以使用Perl创建脚本结合Curl使用。


其他可能情况为：
* 用户ID与信用卡号码相关，或是通用数字模式。
* 用户ID与真实姓名相关，如Freddie Mercury 用户名为 "fmercury"，那么你可能会猜测 Roger Taylor 可能是 "rtaylor"。


此外，我们还可以通过从LDAP查询中猜测用户名，或从Google收集信息。比如，从特定域中收集。Google能帮助通过特定查询或简单的脚本或工具查找域用户。


**注意：** 通过枚举用户帐户，多次失败后可能有锁定帐户风险，取决于应用程序策略。有时候，你的IP地址也可能被应用防火墙或入侵防护系统的动态规则封禁。


#### 灰盒测试
**测试认证错误消息**

验证应用程序应答对每一个用户请求都相同，产出错误认证消息。在这个问题中，黑盒测试和灰盒测试拥有相同的概念，都是基于分析从web应用中获得的消息或者错误码。


**期望结果：**

应用程序应该对每一个错误的认证企图做出相同的应答。

例如：
```
Credentials submitted are not valid
```

### 测试工具
* WebScarab: [OWASP_WebScarab_Project](https://www.owasp.org/index.php/OWASP_WebScarab_Project)
* CURL: http://curl.haxx.se/
* PERL: http://www.perl.org
* Sun Java Access & Identity Manager users enumeration tool: http://www.aboutsecurity.net


### 参考资料
* Marco Mella, *Sun Java Access & Identity Manager Users enumeration: http://www.aboutsecurity.net<br>*
* *用户名枚举漏洞： http://www.gnucitizen.org/blog/username-enumeration-vulnerabilities<br>*


### 整改措施

确保应用在登陆过程中返回一致通用的错误消息来响应不合法用户名、密码和其他用户凭证。

确保默认系统帐户和测试帐户在系统发布到生产环境中（或暴露到不可信网络）前已经删除。
