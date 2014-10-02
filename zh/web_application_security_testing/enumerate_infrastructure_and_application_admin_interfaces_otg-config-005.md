# 枚举基础设施和应用程序管理接口测试 (OTG-CONFIG-005)


### 综述

管理员接口可能存在与应用程序上或者应用服务器上来允许特定用户对网站进行权限操作行为。测试者应该试图去发现特权功能是否可以或者如何被非授权用户和普通用户使用。


一个应用可能需要管理接口来允许特权用户来访问那些会改变站点行为的功能。这样的行为可能包括：

* 用户帐号操作
* 网站设计和布局操作
* 数据操作
* 配置改变


在很多例子中，这些接口并没有针对非授权使用作出有效的控制措施。这个测试目标是发现这些管理接口并使用这些为特权用户准备的功能。


### 如何测试
#### 黑盒测试
接下来的章节描述了一些用于测试管理接口的测试向量。这些技巧可能也能用于测试其他问题，包括权限提升，在指南的其他地方会更详细介绍（比如 [认证绕过测试 (OTG-AUTHZ-002)](https://www.owasp.org/index.php/Testing_for_Bypassing_Authorization_Schema_%28OTG-AUTHZ-002%29) 和 [不安全直接对象引用测试 (OTG-AUTHZ-004)](https://www.owasp.org/index.php/Testing_for_Insecure_Direct_Object_References_%28OTG-AUTHZ-004%29)）。


* 目录和文件枚举。一个管理接口可能存在，但对测试者不可见。尝试猜测管理接口路径可能会很简单不如请求： */admin 或者 /administrator 等* 或者在一下场景可以通过使用[Google dorks](http://www.exploit-db.com/google-dorks)在几秒中内发现。
* 有许多工具可以暴力浏览服务器内容，参见下面测试工具章节。
* 测试人员可能不得不识别管理页面的文件名，强制访问这些识别出来的页面能访问管理接口。
* 在源代码里的注释和链接。许多站点使用通用的页面提供给所有网站用户。通过检查所有源代码，通向管理功能的链接可能被发现，值得调查。
* 审阅服务器和应用软件文档。如果应用或应用服务器是通过默认配置部署的，那么通过配置或帮助文档中描述的信息就能访问到管理接口。如果管理接口需要凭证，应该考虑默认密码。
* 公开可用信息。许多应用比如wordpress存在默认的管理接口。
* 可选的服务端口。管理接口还可能在另一个不同的端口被发现。例如，Apache Tomcat的管理接口常见于8080端口。
* 参数伪造。GET或POST请求参数或特殊cookie变量可能被需要来开启管理功能。这些线索可能来自于隐藏字段，如：
    ```
    <input type="hidden" name="admin" value="no">
    ```
    或者cookie：
    ```
    Cookie: session_cookie; useradmin=0
    ```

一旦管理接口被发现，上面这些技巧的结合可能用于绕过认证。如果都失败了，测试人员可能试图使用暴力破解。在这样的例子中，测试人员应当注意管理帐号的锁定情况，如果存在这样的机制的话。


#### 灰盒测试
应该采取更加详细地对服务器和应用组件的检查来确保加固措施（也就是管理页面应该通过IP过滤或其他控制措施来保证不被其他任何人访问）。如果还是对外可用，那么应该验证所有组件没有使用默认凭证或者默认配置文件。

源代码应该被审查来确保认证和授权模型明确了站点管理员和普通用户的权限责任区分。被普通用户的管理员用户共享的用户功能接口应该被审查来保证无法从这些接口中获得信息泄漏。
<br>


### 测试工具
* [Dirbuster](https://www.owasp.org/index.php/Category:OWASP_DirBuster_Project)  这个当前未被积极开发的OWSAP项目依旧是一个用来暴力浏览服务器上的目录和文件的优秀工具。
* [THC-HYDRA](https://www.thc.org/thc-hydra/)  是一个用于暴力访问许多接口的工具，功能支持基于表单的HTTP认证机制。
* 在拥有好的字典的情况下，暴力破解工具能工作地更有效，一个好例子就是 [netsparker](https://www.netsparker.com/blog/web-security/svn-digger-better-lists-for-forced-browsing/) 字典。


### 参考资料
* 默认字典列表：http://www.governmentsecurity.org/articles/DefaultLoginsandPasswordsforNetworkedDevices.php
* 默认字典列表：http://www.cirt.net/passwords
