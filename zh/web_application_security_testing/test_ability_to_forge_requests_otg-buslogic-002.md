# 伪造请求能力测试 (OTG-BUSLOGIC-002)

### 综述

伪造请求是一种攻击者用来绕过前端应用程序限制，直接向后端处理程序提交信息的方法。攻击者的目的在于通过中间代理发送带有在业务逻辑之外的非支持的、受保护的或者预期意外数据的HTTP POST/GET请求。伪造请求的例子包括利用可猜测的或可预测的参数和一些“隐藏”特性功能（如调试功能、特殊开发界面）来得到额外信息或者绕过业务逻辑。

伪造请求相关漏洞在不同应用及其业务逻辑数据验证方式中各不相同。着重于打破业务逻辑工作流。

应用程序必须有逻辑检查机制来对抗伪造请求，以防攻击者有机会利用伪造请求来破坏应用程序业务逻辑或者工作流程。伪造请求并不是新的技术手段；攻击者通过使用劫持代理来发送HTTP请求。通过伪造该请求中发现的、可预测的参数来绕过业务逻辑，错使应用程序以为任务或过程已经发生或没有发生。

此外，伪造请求可能会颠覆程序或者业务逻辑流，比如通过调用“隐藏”特性或功能（如调试模式、开发者模式、系统”彩蛋“）。”彩蛋“是一种故意的内部玩笑、隐藏消息或者特性，比如一段程序、影片、文章或者谜语。根据游戏设计者 Warren Robinett，这个名词是在 Atari 公司创造，某人被提示在 Robinett的广泛发行的游戏Adventure中隐藏的一段秘密消息。这个名字据称是传统的寻找复活节彩蛋的活动引发的想法。（http://en.wikipedia.org/wiki/Easter_egg_(media)）。


### 测试案例

#### 案例 1

假设一个电子影院允许用户选择电影票，并允许一次性的10%额外折扣。如果攻击者能够通过代理发现应用程序存在一个隐藏表单域（1或0）来确定折扣是否已经使用。攻击者通过递交’1‘来表明没有应用折扣从而进行多次折扣获得利益。

#### 案例 2

假设在线视频游戏中心在每次游戏关卡完成后将获得的积分转化为游戏券，这些游戏券可以兑换奖品。此外，每关游戏有等同于该关卡级别的分数累乘器。如果攻击者通过代理发现应用程序使用隐藏表单域来进入开发测试模式，就能快速跳到最高级别游戏关卡来快速累积游戏分数。

同时，如果攻击者能够通过调试的隐藏功能获得其他在线玩家的数据或者自身关卡数据，那么就能迅速完成关卡获得游戏分数。


### 如何测试

#### 通用测试方法

* 通览项目文档寻找可猜测、可预测或者隐藏的功能区域。
* 一旦发现这样的地方，尝试插入逻辑有效的数据，允许用户绕过正常业务逻辑工作流来使用系统。


#### 特定测试方法 1

* 使用劫持代理来观察HTTP GET/POST 请求，寻找容易猜测的数据或者以特定频率递增的数据。
* 如果找到这样的参数，试着改变其数值获得预期以外的结果。


#### 特定测试方法 2

* 使用劫持代理来观察HTTP GET/POST 请求，寻找暗示隐藏特性如调制开关的地方。
* 如果找到这样的地方，试着猜测并改变其数值来获得不同应用程序响应和行为。


### 相关测试用例

* [ 会话变量暴露测试 (OTG-SESS-004)](https://www.owasp.org/index.php/Testing_for_Exposed_Session_Variables_%28OTG-SESS-004%29)
* [ CSRF测试 (OTG-SESS-005)](https://www.owasp.org/index.php/Testing_for_CSRF_%28OTG-SESS-005%29)
* [ 账户枚举测试 (OTG-IDENT-004) ](https://www.owasp.org/index.php/Testing_for_Account_Enumeration_and_Guessable_User_Account_%28OTG-IDENT-004%29)


### 测试工具

* *OWASP Zed Attack Proxy (ZAP)* - https://www.owasp.org/index.php/OWASP_Zed_Attack_Proxy_Project

ZAP是一个非常容易使用的web应用程序渗透测试整合工具。他被设计为符合不同安全经验的人员使用，特别是新接触渗透测试的开发人员和功能测试人员的理想工具。ZAP在提供一系列的用于手工漏洞检测的工具的同时也提供了自动化扫描器。


### 参考资料

* Cross Site Request Forgery - Legitimizing Forged Requests - http://fragilesecurity.blogspot.com/2012/11/cross-site-request-forgery-legitimazing.html
* Debugging features which remain present in the final game - http://glitchcity.info/wiki/index.php/List_of_video_games_with_debugging_features#Debugging_features_which_remain_present_in_the_final_game
* Easter egg - http://en.wikipedia.org/wiki/Easter_egg_(media)
* Top 10 Software Easter Eggs - http://lifehacker.com/371083/top-10-software-easter-eggs


### 整改措施

应用程序应该设计的足够健壮来阻止攻击者预测和操纵可能颠覆业务逻辑的参数，或者如调试模式等利用隐藏/未公开的功能。
