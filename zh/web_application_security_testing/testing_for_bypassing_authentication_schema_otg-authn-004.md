# 绕过认证模式测试 (OTG-AUTHN-004)


### 综述

尽管大多数应用程序需要认证来获得访问私有数据的权限或执行人物，但是不是每一个认证方法都能够提供适当的安全性。忽视、无视或低估安全威胁往往导致认证机制可以被轻易绕过，如通过简单跳过登录页面直接访问本需要登录后才能访问内部页面的行为。

此外，通常也可能通过更改请求，欺骗应用程序，使他认为用户已经被认证来绕过认证机制。这可以通过修改URL参数、操纵表单或伪造会话来达到目的。

有关认证模式的问题可以在软件开发生命周期（SDLC）的各个阶段中发现，比如设计阶段、开发阶段和部署阶段：
* 在设计阶段，发生的问题可以包括错误的应用区域保护定义、未选择强加密协议来保证凭证传输安全等等。
* 在开发阶段，发生的问题可以包括错误的输入验证功能实现或未遵循相关语言的安全开发最佳实践。
* 在应用部署阶段，可能在应用设置过程中（安装和配置）中发生问题，缺乏必须的技巧技能或缺乏良好的帮助文档。


### 如何测试
#### 黑盒测试

有一些绕过web应用中的认证模式的：
* 直接页面请求 ([forced browsing](https://www.owasp.org/index.php/Forced_browsing))
* 修改参数
* 会话ID预测
* SQL注入

##### 直接页面请求

如果web应用程序只在登录页面实现了访问控制，那么这种认证模式可以被绕过。例如，如果用户通过强制浏览技巧直接请求访问不同的页面，这个页面可能不会检查访问凭证。尝试在浏览器地址栏输入地址直接访问受保护的页面来测试这个绕过方法。

<center>![Image:basm-directreq.jpg](https://www.owasp.org/images/7/7f/Basm-directreq.jpg)</center>

##### 修改参数

另一个关于认证设计的问题是应用程序被设计为通过一个固定的参数来验证登录是否成功的情形。用户可以修改这些参数来获取访问保护区域的权限但不提供有效凭证。在下面的例子中"authenticated"参数被改为了"yes"，这使用户获得的权限。在这个例子中，参数是包含在URL中的，但是使用代理也可以修改参数，特别是当这些参数被放在表单中使用POST请求发送或存储在cookie时。

```
http://www.site.com/page.asp?authenticated=no
```

```
raven@blackbox /home $nc www.site.com 80
GET /page.asp?authenticated=yes HTTP/1.0

HTTP/1.1 200 OK
Date: Sat, 11 Nov 2006 10:22:44 GMT
Server: Apache
Connection: close
Content-Type: text/html; charset=iso-8859-1

<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<HTML><HEAD>
</HEAD><BODY>
<H1>You Are Authenticated</H1>
</BODY></HTML>
```

<center>![Image:basm-parammod.jpg](https://www.owasp.org/images/8/8c/Basm-parammod.jpg)</center>


##### 会话ID预测

许多web应用通过会话标识（session ID）来管理认证。因此，如果会话ID的生成是可以预测的话，恶意用户就可以找到一个合法的会话ID来获取非授权的访问，模仿先前的一个已经认证过的用户。

在下面的图示中，cookie中的数值是线性增长的，所以攻击者很容易就可以猜测出一个有效的会话ID。

<center>![Image:basm-sessid.jpg](https://www.owasp.org/images/8/83/Basm-sessid.jpg)</center>

在下面的图示中，cookie中的数值只有局部发生变化，可以通过有限的暴力攻击来猜测。

<center>![Image:basm-sessid2.jpg](https://www.owasp.org/images/f/f4/Basm-sessid2.jpg)</center>

##### SQL注入（HTML表单认证）

SQL注入是一个著名的攻击技巧。在这个章节不会详细描述这个技巧，指南中的一些章节将解释注入攻击技巧，作用范围不仅仅限于本章节内容。

<center>![Image:basm-sqlinj.jpg](https://www.owasp.org/images/4/46/Basm-sqlinj.jpg)</center>

下面的图示展示了一个简单的SQL注入攻击，有时可以用来绕过认证表单。

<center>![Image:basm-sqlinj2.gif](https://www.owasp.org/images/d/d1/Basm-sqlinj2.gif)</center>

#### 灰盒测试

如果攻击者已经能够获得应用程序源代码，通过之前发现的漏洞（如目录遍历），或通过web仓库（开源软件），那么就有可能对认证过程的实现进行精细的攻击。

在下面的例子中（PHPBB 2.0.13 - 认证绕过漏洞），在第5行，unserialize()函数解析用户提供的cookie，并设置$row数组中。在第10行，用户储存于后台数据库的MD5密码哈希与提供的进行比较。

```
1.  if ( isset($HTTP_COOKIE_VARS[$cookiename . '_sid']) ||
2.  {
3.  $sessiondata = isset( $HTTP_COOKIE_VARS[$cookiename . '_data'] ) ?
4.
5.  unserialize(stripslashes($HTTP_COOKIE_VARS[$cookiename . '_data'])) : array();
6.
7.  $sessionmethod = SESSION_METHOD_COOKIE;
8.  }
9.
10. if( md5($password) == $row['user_password'] && $row['user_active'] )
11.
12. {
13. $autologin = ( isset($HTTP_POST_VARS['autologin']) ) ? TRUE : 0;
14. }
```

在PHP中，布尔变量（1 - 真）和字符串值进行比较结果总是为真，所以通过向unserialize()函数提供下面字符串（重点是"b:1"部分），就可能绕过认证控制：
```
 a:2:{s:11:"autologinid";b:1;s:6:"userid";s:1:"2";}
```

### 测试工具
* [WebScarab](https://www.owasp.org/index.php/OWASP_WebScarab_Project)
* [WebGoat](https://www.owasp.org/index.php/OWASP_WebGoat_Project)
* [OWASP Zed Attack Proxy (ZAP)](https://www.owasp.org/index.php/OWASP_Zed_Attack_Proxy_Project)


### 参考资料
**白皮书**

* Mark Roxberry: "PHPBB 2.0.13 vulnerability"
* David Endler: "Session ID Brute Force Exploitation and Prediction" - http://www.cgisecurity.com/lib/SessionIDs.pdf
