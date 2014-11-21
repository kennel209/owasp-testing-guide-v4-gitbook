# 测试权限提升 (OTG-AUTHZ-003)

### 综述
这部分描述权限提升问题。在这个阶段中，测试者应该验证用户是否可以修改自己在应用系统中的权限或角色来达成权限提升攻击。

权限提升问题发生在当用户去的访问超出自己正常允许访问的资源或功能时候，而这种权限提升或改变的情况本应该被应用程序阻止。通常原因是应用程序存在漏洞。带来的后果是应用程序执行了更高权限的任务，而这些任务通常是给开发者或者系统管理员使用的。


权限提升的程度取决于攻击者被授权了何种特权和什么特权能够被成功利用。例如，一个程序错误允许成功认证后的用户获得额外的权限，这个情况限制了权限提升程度，因为用户已经被授予了某些权限。类似的，一个远程攻击者不需要任何认证措施就能获得超级用户的权利表明了一个非常大的权限提升程度的例子。


通常，我们把取得更高权限账户资源的情况（如取得应用程序的管理员特权）认为是 *垂直权限提升*，把取得类似配置账户的资源的情况（如在在线银行应用程序中访问不同用户的信息）认为是 *水平权限提升* 。


### 如何测试
**测试角色/权限操纵**

在应用程序的每一个用户可以向数据库创建信息（如，创建支付环节、添加通讯录或发送信息等等），能获取信息（账户状态，订单详情等等）或删除信息（删除用户、消息等等）的部分，都应该记录相关函数功能是否正常。测试者应该以其他用户的身份来尝试访问这些功能来验证是否可以访问这些被用户角色/权限限制的内容（可能被其他用户允许）。


例如：

下面的HTTP POST请求允许属于grp001的用户访问订单 #0001 ：
```
 POST /user/viewOrder.jsp HTTP/1.1
 Host: www.example.com
 ...

 groupID=grp001&orderID=0001
```

验证不属于grp001的用户是否可以修改‘groupID’和‘orderID’参数来取得数据访问权限。


又例如：

下面服务器应答表明返回用户成功认证后的HTML中的隐藏表单。
```
 HTTP/1.1 200 OK
 Server: Netscape-Enterprise/6.0
 Date: Wed, 1 Apr 2006 13:51:20 GMT
 Set-Cookie: USER=aW78ryrGrTWs4MnOd32Fs51yDqp; path=/; domain=www.example.com
 Set-Cookie: SESSION=k+KmKeHXTgDi1J5fT7Zz; path=/; domain= www.example.com
 Cache-Control: no-cache
 Pragma: No-cache
 Content-length: 247
 Content-Type: text/html
 Expires: Thu, 01 Jan 1970 00:00:00 GMT
 Connection: close

 <form  name="autoriz" method="POST" action = "visual.jsp">
 <input type="hidden" name="profile" value="SysAdmin">
 <body onload="document.forms.autoriz.submit()">
 </td>
 </tr>
```

如果测试者修改自己'profile'参数的值为'SysAdmin'会发生什么？是否可能成为管理员？


例如：

在一个情形下，服务器发送错误消息在参数中包含了一系列应答代码的值，如下所示：
```
 @0`1`3`3``0`UC`1`Status`OK`SEC`5`1`0`ResultSet`0`PVValid`-1`0`0` Notifications`0`0`3`Command  Manager`0`0`0` StateToolsBar`0`0`0`
 StateExecToolBar`0`0`0`FlagsToolBar`0
```

服务器盲目信任用户。他认为用户将会用上面的消息来应答来结束会话。


在这个情形下，验证是否可以通过修改参数值来提升权限。在这个特别的例子中，通过修改 `PVValid`的值从 '-1' 到 '0'（没有错误条件），就能被服务器认证为管理员用户。

### 参考资料
**白皮书**

* Wikipedia - Privilege Escalation: http://en.wikipedia.org/wiki/Privilege_escalation<br>


### Tools
* OWASP WebScarab: [OWASP WebScarab Project](https://www.owasp.org/index.php/OWASP_WebScarab_Project)
* [OWASP Zed Attack Proxy (ZAP)](https://www.owasp.org/index.php/OWASP_Zed_Attack_Proxy_Project)

