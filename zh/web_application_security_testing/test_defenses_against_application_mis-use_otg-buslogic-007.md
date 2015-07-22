# 测试对抗应用程序误用的防御措施 (OTG-BUSLOGIC-007)


### 综述

合法功能的误用和非法使用能够识别出企图枚举web应用程序、识别脆弱性和利用漏洞的攻击。应该通过测试确定是否存在应用层的防御机制来保护应用程序。

缺少主动防御机制允许攻击者不需要任何帮助就能寻找漏洞。应用程序拥有者也不会发现他们的程序正在被攻击。


### 案例

一个认证的用户可能采取（往往不会）下面行为：
1. 尝试访问他们所不允许下载的文件ID
2. 使用单引号(')替换文件ID数字
3. 改变使用GET来请求原来的POST请求
4. 添加额外的参数
5. 复制一个参数的名字/数值对

应用程序正在监视误用情况，并在第五项事件后充分相信该用户是一个攻击者。例如：
* 禁用了重要功能
* 对其他操作需要额外的认证过程
* 对请求作出延迟响应
* 开始记录该用户进行的交互行为的数据（如过滤处理过的HTTP请求头，主体和响应主体）

如果应用程序没有如此做出回应，攻击者可能继续滥用应用功能，向应用提交恶意内容。应用程序无法通过测试。在实践中，在案例中的这些离散的样例行为不太可能如此发生。更多的是使用模糊工具来识别出每一个参数的脆弱点。这也是一个安全测试人员会实施的。


### 如何测试

这个测试不同于其他测试，测试结果可以从其他测试行为中提取出来。当实施其他测试的时候，记录下可能暗示应用程序存在内建的自我防御行为：

* 改变了响应
* 阻挡了请求
* 强制登出账户或锁定账户的行为

可能这些防御是局部的，通常的局部（每个功能）防御措施有：

* 拒绝含有特定字符的输入
* 在一系列认证失败后临时锁定账户

局部的安全控制可能不足。通常没有对抗下列普通误用行为的防御措施：

* 强制浏览
* 绕过输入验证
* 多重访问控制错误
* 额外、重复、或缺少参数名称
* 多重输入验证或业务逻辑验证失效（非用户错误输入的结果）
* 错误的结构化数据（如，JSPN，XML）
* 明显的跨站脚本或SQL注入荷载
* 排除利用自动化工具以外的快速利用应用程序
* 用户地理位置的改变
* 用户代理（UA）的改变
* 通过错误顺序访问多阶段的业务处理过程
* 大量或者高频使用应用相关的功能（如优惠代码提交，失败的信用卡支付，文件上传，文件下载，登出等等）。

这些防御措施工作在应用认证部分最有效，虽然也有在公开的平台通过新建账户或者访问内容（来获取信息）的行为。

不是说上面提及的行为都需要被应用程序监视，但是如果一项也不涉及就会存在问题。通过上述的行为来测试应用程序，查看有没有对抗措施。如果没有，测试人员应该报告应用程序不存在应用层面的误用防御措施。注意有时候有可能攻击者能够觉察的请求已经被静默了（如日志记录行为的改变，监视的增强，向管理员的告警和请求代理），所以通过这个方法发现的问题不一定能确保肯定存在。在实际中，只有少数的应用程序（或者相关基础设施如web防火墙）会探测这种误用形式。


### 相关测试用例

适用其他所有的测试用例。


### 测试工具

测试人员可以使用其他测试中使用到的大量工具。


### 参考资料

* [Resilient Software](https://buildsecurityin.us-cert.gov/swa/resilient.html), Software Assurance, US Department Homeland Security
* [IR 7684](http://csrc.nist.gov/publications/nistir/ir7864/nistir-7864.pdf) Common Misuse Scoring System (CMSS), NIST
* [Common Attack Pattern Enumeration and Classification](http://capec.mitre.org/) (CAPEC), The Mitre Corporation
* [OWASP_AppSensor_Project](https://www.owasp.org/index.php/OWASP_AppSensor_Project)
* [ AppSensor Guide v2](https://www.owasp.org/index.php/File:Owasp-appensor-guide-v2.doc), OWASP
* Watson C, Coates M, Melton J and Groves G, [Creating Attack-Aware Software Applications with Real-Time Defenses](http://www.crosstalkonline.org/storage/issue-archives/2011/201109/201109-Watson.pdf), CrossTalk The Journal of Defense Software Engineering, Vol. 24, No. 5, Sep/Oct 2011


### 整改措施

建立对抗应用程序误用的主动防护措施。
