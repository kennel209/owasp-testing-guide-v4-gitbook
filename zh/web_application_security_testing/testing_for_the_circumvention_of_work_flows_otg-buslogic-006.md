# 测试绕过工作流 (OTG-BUSLOGIC-006)

### 综述

工作流漏洞指任意类型的允许攻击者误用应用/系统功能来绕过（不依从）设计好的工作流。

“工作流由一系列无缝组合的步骤组成。他是一系列操作的描述，人员或组织员工或者更简单和复杂机制的工作的声明。工作流被视作是真实工作的抽象。” (https://en.wikipedia.org/wiki/Workflow)

应用程序业务逻辑必须要求用户以正确/特定顺序完成指定步骤，如果工作流没有正确完成而终止，所有的操作和操作带来的后续反应都应该“回滚”或者取消。绕过工作流或者正确业务逻辑的漏洞独特在于他是应用程序相关的，必须小心设计手工误用测试用例来进行测试。

应用业务流程必须检查来确保用户的行为/事务以正确/可接受的顺序进行处理。如果一个事务触发了一系列操作，那么万一事务没有成功完成，这些操作必须可以“回滚”或移除。


### 测试案例

#### 案例 1

许多人收到过杂货店和加油站专用返金券。假设用户能够发起一个事务来向他们的账户进行购买以增加反利点数，但在最后阶段取消商品购买。在这种情况下，系统应该将回馈点回滚到原先的情况。如果不是这样，攻击者可以通过循环此类操作增加自己的反利点，而不用购买任何东西。


#### 案例 2

BBS系统可能被设计成确保初始帖子不能带有禁止用语。如果一个词语在“黑名单”中发现，用户的帖子就不能提交。但是一旦提交，帖子主可以访问、编辑、改变其中内容，包括黑名单的违禁词。系统不会再次审核。通过这种办法，攻击者可能通过发布空白初始帖子，然后从更新中进行操作。


### 如何测试

#### 通用测试方法

* 通览项目文档寻找可以跳过或者能够以非预期顺利进行操作的步骤的业务逻辑流。
* 对于每一个找到的方法，设计一个误用测试用例，尝试绕过或实施不可接受的操作来测试业务逻辑工作流。


#### 特定测试方法 1

* 发起一个事务来改变用户账户的额度/点数。
* 取消这个事务来观察点数是否减少来确保点数被正确记录。


#### 特定测试方法 2

* 在内容管理系统或者bbs系统中输入合法的内容或数值。
* 尝试追加、编辑、移除数据来让整个过程含有非法的数值或者成为非法的状态，确保用户不允许保存这种不正确的信息。“非法”信息可能包括违禁词或者不适当的主题（如宗教）。



### 相关测试用例

* [ 测试目录遍历/文件包含 (OTG-AUTHZ-001)](https://www.owasp.org/index.php/Testing_Directory_traversal/file_include_%28OTG-AUTHZ-001%29)
* [ 测试授权绕过 (OTG-AUTHZ-002)](https://www.owasp.org/index.php/Testing_for_Bypassing_Authorization_Schema_%28OTG-AUTHZ-002%29)
* [ 测试会话管理绕过 (OTG-SESS-001)](https://www.owasp.org/index.php/Testing_for_Session_Management_Schema_%28OTG-SESS-001%29)
* [ 测试业务逻辑数据验证 (OTG-BUSLOGIC-001)](https://www.owasp.org/index.php/Test_business_logic_data_validation_%28OTG-BUSLOGIC-001%29)
* [ 测试请求伪造能力 (OTG-BUSLOGIC-002)](https://www.owasp.org/index.php/Test_Ability_to_forge_requests_%28OTG-BUSLOGIC-002%29)
* [ 测试数据完整性 (OTG-BUSLOGIC-003)](https://www.owasp.org/index.php/Test_integrity_checks_%28OTG-BUSLOGIC-003%29)
* [ 测试处理时长 (OTG-BUSLOGIC-004)](https://www.owasp.org/index.php/Test_for_Process_Timing_%28OTG-BUSLOGIC-004%29)
* [ 测试功能使用限制 (OTG-BUSLOGIC-005)](https://www.owasp.org/index.php/Test_number_of_times_a_function_can_be_used_limits_%28OTG-BUSLOGIC-005%29)
* [ 测试应用程序误用防护 (OTG-BUSLOGIC-007)](https://www.owasp.org/index.php/Test_defenses_against_application_mis-use_%28OTG-BUSLOGIC-007%29)
* [ 测试非预期文件类型上传 (OTG-BUSLOGIC-008)](https://www.owasp.org/index.php/Test_Upload_of_Unexpected_File_Types_%28OTG-BUSLOGIC-008%29)
* [ 测试恶意文件上传 (OTG-BUSLOGIC-009)](https://www.owasp.org/index.php/Test_Upload_of_Malicious_Files_%28OTG-BUSLOGIC-009%29)


### 参考资料

* OWASP Detail Misuse Cases - https://www.owasp.org/index.php/Detail_misuse_cases
* Real-Life Example of a 'Business Logic Defect - http://h30501.www3.hp.com/t5/Following-the-White-Rabbit-A/Real-Life-Example-of-a-Business-Logic-Defect-Screen-Shots/ba-p/22581
* Top 10 Business Logic Attack Vectors Attacking and Exploiting Business Application
* Assets and Flaws – Vulnerability Detection to Fix - http://www.ntobjectives.com/go/business-logic-attack-vectors-white-paper/ and http://www.ntobjectives.com/files/Business_Logic_White_Paper.pdf
* CWE-840: Business Logic Errors - http://cwe.mitre.org/data/definitions/840.html


### 整改建议

应用程序必须有自我察觉机制，对用户完成工作流的每一步进行检查，确保正确顺序，防护攻击者绕过/跳过/重复任何流程。测试工作流漏洞需要设计业务逻辑滥用/误用测试用例，这些用例主要是不通过正确的步骤或程序来成功完成整个业务逻辑。
