# 业务逻辑数据验证测试 (OTG-BUSLOGIC-001)

### 综述

应用程序必须确保只有逻辑合法的数据才能在前端输入和直接传输到服务器端。只对数据进行本地验证可能是应用层序在服务器端遭到攻击，比如通过代理或传输途中的其他系统。这不同于进行简单的边界数据分析（BVA），验证更加困难，大多数情况下不能简单在输入端进行验证，通常需要其他系统进行检查。

举例说明：应用程序可能需要你的社会安全号码（SSN）。在BAV中，应用程序应该在数据输入时候检查文件形式和语法（在这里是9位数字，非负数，不全为0）。但是也必须考虑一些逻辑上的约束。SSN号码是有组织分类的。是否在死亡名单中？是否是来自某特定地区？

业务逻辑数据验证相关漏洞独特在是应用程序相关的，不同于伪造请求相关漏洞的地方在于他们更加关心数据逻辑，而不是简单破坏业务逻辑工作流。

应用程序的前后两端都应该进行数据验证和有效性验证，来确保传递的数据时逻辑有效的。甚至当用户提交的有效数据时，业务逻辑也可能因为该数据或此时状态表现出不同的处理行为。


### 测试案例

#### 案例 1

假设我们正在维护一个多层的电子商务站点，这个站点主要业务是卖地毯。用户选择他们喜欢的地毯，输入尺寸，进行交易，应用程序前端对输入信息进行验证，保证制作颜色和尺寸信息是正确的，合同信息时有效的。但是在后端的业务逻辑有两条路径，如果地毯有库存，就直接从仓库发货，但是如果缺货，就会联系合作伙伴的系统，检查他们是否有库存，如果有从合作伙伴的仓库发货，并支付报酬。如果攻击者能进行一个有库存的交易，但是仍将他作为缺货发送给合作伙伴，这种情况如果发生会如何？又如果攻击者能够作为中间人发送消息给合作伙伴仓库而不进行支付又会如何？

#### 案例 2

许多信用卡系统在晚上核实账户资金情况，所以用户可能在某种程度上获取更多的支付额度。反过来也一样。如果在早上花完了我的信用卡额度，可能就不能在傍晚进行可用支付。另一个例子是在多个地点同时进行信用卡支付，可能会超出限额，如果系统是通过昨晚的数据进行限额配置的话。


### 如何测试

#### 通用测试方法

* 通览项目文档寻找数据输入点或者数据传递点。
* 一旦找到了，试着插入逻辑无效的数据。

#### 特定测试方法

* 对前端系统数据进行有效性测试，确保他们只接受“有效”的数据。
* 使用劫持代理来观察HTTP POST/GET请求情况，寻找数据传递的请求（如花费、数量）。特别的，寻找数据在应用系统相互传递过程中，可能的注入或者数据篡改点。
* 一旦逻辑无效的数据被系统审查（如不存在的SSN或特别id标示，或者其他不适合业务逻辑的数据）。该行为验证了服务端系统工作正常，不接受逻辑无效的数据。


### 相关测试用例

* 所有 [输入验证测试](https://www.owasp.org/index.php/Testing_for_Input_Validation) 测试用例
* [账户枚举测试 (OTG-IDENT-004)](https://www.owasp.org/index.php/Testing_for_Account_Enumeration_and_Guessable_User_Account_%28OTG-IDENT-004%29)
* [会话管理控制绕过测试 (OTG-SESS-001)](https://www.owasp.org/index.php/Testing_for_Session_Management_Schema_%28OTG-SESS-001%29)
* [会话变量暴露测试 (OTG-SESS-004)](https://www.owasp.org/index.php/Testing_for_Exposed_Session_Variables_%28OTG-SESS-004%29)


### 测试工具

* *OWASP Zed Attack Proxy (ZAP)* - https://www.owasp.org/index.php/OWASP_Zed_Attack_Proxy_Project

ZAP是一个非常容易使用的web应用程序渗透测试整合工具。他被设计为符合不同安全经验的人员使用，特别是新接触渗透测试的开发人员和功能测试人员的理想工具。ZAP在提供一系列的用于手工漏洞检测的工具的同时也提供了自动化扫描器。


### 参考资料

Beginning Microsoft Visual Studio LightSwitch Development - http://books.google.com/books?id=x76L_kaTgdEC&pg=PA280&lpg=PA280&dq=business+logic+example+valid+data+example&source=bl&ots=GOfQ-7f4Hu&sig=4jOejZVligZOrvjBFRAT4-jy8DI&hl=en&sa=X&ei=mydYUt6qEOX54APu7IDgCQ&ved=0CFIQ6AEwBDgK#v=onepage&q=business%20logic%20example%20valid%20data%20example&f=false


### 整改措施

应用程序/系统必须确保只有“逻辑有效“的数据才可被应用程序输入点和数据传递点接受，数据不能在进入系统的时候就被简单信任处理。
