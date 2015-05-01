# 测试功能使用次数限制 (OTG-BUSLOGIC-005)


### 综述

应用程序需要解决的许多问题需要限制功能的使用次数或者操作的执行次数。应用程序必须“足够聪明”来限制用户使用超过他们的限额。因为在许多情况下，用户每使用一次某功能就能获得某种形式的利益，并需要支付合适的报酬。举例来说，一个电子金融站点可能只允许用户在一笔交易中使用一次折扣政策，或者有些应用程序可能有一种订阅计划，只允许用户每月下载三个完整的文档。

功能限制的相关漏洞可能与应用本身关系密切，设计误用用例必须符合当前应用/功能/动作的允许次数。

攻击者可能可以绕过业务逻辑，执行比“允许”次数更多的功能来利用应用程序获得利益。

### 例子

假设一个电子商务站点允许用户在他们的购物总价上应用许多折扣中一种，接着再进行结算和交易。万一攻击者在完成一次“允许”的折扣之后返回折扣页面后，能否再次利用其他的折扣？或是能否多次利用相同的折扣？

### 如何测试

* 评估项目文档，搜寻此类在系统或应用程序的工作流中不应该被执行一次或指定次数以上的功能。
* 对于每一个这样的功能，开发出误用/滥用测试用例来测试超出允许的使用次数的情况。例如，在只能执行一次功能的地方使用导航来回访问多次？或者用户能否添加删除购物车内容来使用额外的折扣？


### 相关测试用例

[ 测试账户枚举和可猜测用户账户 (OTG-IDENT-004) ](https://www.owasp.org/index.php/Testing_for_cookies_attributes_%28OTG-SESS-002%29)

[ 测试弱账户锁定机制 (OTG-AUTHN-003)](https://www.owasp.org/index.php/Test_Session_Timeout_%28OTG-SESS-007%29)


### 参考资料

InfoPath Forms Services business logic exceeded the maximum limit of operations Rule - http://mpwiki.viacode.com/default.aspx?g=posts&t=115678

Gold Trading Was Temporarily Halted On The CME This Morning -
http://www.businessinsider.com/gold-halted-on-cme-for-stop-logic-event-2013-10


### 整改措施

应用程序应该存在检查功能来确保业务逻辑正确执行，如果有功能或动作只能执行指定次数，那么当限制次数达到后，用户应该不能再使用该功能。为了防止用户超出功能使用限制，应用程序应该使用cookie等机制来计数或贯穿会话中不允许用户访问额外的功能。

