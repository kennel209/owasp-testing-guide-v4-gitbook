# 测试帐户选项过程 (OTG-IDENT-003)


### 综述

帐户选项给攻击者呈现一个绕过正确鉴别和认证过程创建合法帐户的机会。


### 测试目标

验证什么帐户可以选择其人帐户选项和帐户类型。


### 如何测试

确定什么角色能改变其他用户的选项，和他们能改变何种类型的帐户。

* 有没有任何验证，审查和认证过程在用户选项请求中？
* 有没有任何验证，审查和认证过程在撤销用户选项请求中？
* 管理员是否能改变其他管理员的选项或者仅仅是用户的选项？
* 管理员和其他用户选项授予帐户能否给予自己更高的权限？
* 管理员或用户能否取消自己的帐户选项？
* 被取消用户选项的用户文件和资源如何被管理？被删除？或者权限被转移？


#### 测试例子

在WordPress中，仅需要用户名称和电子邮件地址就可以改变用户选项，就像下面展示的：

![File:Wordpress_useradd.png|800px](https://www.owasp.org/images/thumb/4/49/Wordpress_useradd.png/800px-Wordpress_useradd.png)


取消用户选项需要管理员选择该用户，从下拉列表中删除，并应用这个行为。管理员被提供一个对话框来询问对用户的文章做如何处理（删除或转移）。

![File:Wordpress_authandusers.png|800px](https://www.owasp.org/images/thumb/6/63/Wordpress_authandusers.png/800px-Wordpress_authandusers.png)


### 测试工具

虽然有许多完全和精准的方法手动完成这个测试，但是HTTP代理工具可能非常有用。
