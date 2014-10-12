# 测试用户注册过程 (OTG-IDENT-002)


### 综述

有些站点提供用户注册过程来自动化（半自动化）授予用户访问系统的权限。整个鉴别过程从没有鉴别到主动鉴别根据系统不同而不同，依赖于系统的安全需求。许多公开应用完全自动化注册过程和授予用户权限过程因为用户基数导致不能手动管理。然而，许多公司的应用会手动验证用户，这些测试案例不能应用在上面。


### 测试目标

1. 验证用户注册的主体需求满足业务和安全要求。
2. 验证注册过程。


### 如何测试

验证用户注册的主体需求满足业务和安全要求：
1. 是否任何人都能进行注册？
2. 如果满足条件，注册是人工授予权限还是自动授予？
3. 相同的人或主体是否能多次注册？
4. 用户可以被注册成不同的角色和许可么？
5. 成功注册需要主体拿出什么证据？
6. 是否验证注册主体？

验证注册过程：
1. 主体信息是否可以轻易伪造？
2. 通过恶意操作是否可以在注册过程中改变主体信息？


#### 测试例子

在下面WordPress例子中，注册过程中唯一的鉴别要求是电子邮件地址。

![File:Wordpress_registration_page.jpg|700px](https://www.owasp.org/images/thumb/c/c7/Wordpress_registration_page.jpg/700px-Wordpress_registration_page.jpg)


相对的，在google例子中，下面的鉴别过程包括名字、生日、国家、移动电话号码、电子邮件地址和验证码。虽然只有两项被验证（电子邮件地址和电话号码），整个鉴别过程也比WordPress严格。

![File:Google_registration_page.jpg|700px](https://www.owasp.org/images/thumb/9/92/Google_registration_page.jpg/700px-Google_registration_page.jpg)


### 测试工具

HTTP代理是有有用的工具来测试这个过程。


### 参考资料

* [User Registration Design](http://mashable.com/2011/06/09/user-registration-design/)


### 整改措施

实现鉴定和验证满足相关保护凭证信息的安全需求。
