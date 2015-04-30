# 业务逻辑测试

### 综述

在多功能的动态web应用程序中测试业务逻辑漏洞需要用非常规手段来思考。如果应用认证机制原先以1、2、3的步骤依次执行的验证身份目的来开发，万一用户从步骤1直接跳到步骤3会发生什么？用更加简单的例子来说，在打开失败、权限拒绝或仅仅500的错误的情况下，应用程序是否依然能够提供访问权限？

可以举出许多例子，但是不变的思想是“跳出常规思维”。这种类型的漏洞无法被漏洞扫描工具探测到，依赖于渗透测试人员的技巧和创造性。此外，这种类型的漏洞往往是最难探测的漏洞之一，而且通常是特定应用程序相关的，但是同样的，如果被利用，也是对应用程序最有害的。

尽管在现实生活中，这种业务漏洞的利用常常发生，有许多应用漏洞的研究者调查他们，业务逻辑缺陷的分类还在研究之中。web应用程序是其中的焦点。社区的争论在于这些问题是展示了新概念还是仅仅是已知问题的变种。

测试这些业务逻辑缺陷类似功能测试人员测试逻辑或有限状态测试。这些类型的测试需要安全专家多一些不同的思考，开发误用和滥用测试用例，以及许多功能测试人员使用的技巧。自动化的业务逻辑滥用测试用例几乎不可能，这仍然是需要依赖测试者的技巧和知识来完成业务过程和利用其中的规则的手工艺术。

### 业务限制

考虑应用程序提过的业务功能的规则。有没有对用户行为的限制？然后思考应用程序是否强制执行了这些规则。如果测试人员非常熟悉业务，那么通常非常容易识别出测试和分析用例来验证应用程序的规则。如果测试人员是第三方的测试者，需要使用自己的常识和询问有关人员关于业务过程，以及应用系统是否允许不同的操作。

有时，在一些非常复杂的应用系统中，测试者可能不会一开始就弄清楚应用程序的每一方面。在这些情况下，最好是在开始测试之前，客户可以陪同测试人员熟悉整个应用，以便于测试人员更好理解应用程序的限制和开发意图。此外，如果可能，在测试过程中，如果发生有关应用程序功能的问题，能够与开发人员直接交流可能会带来极大帮助。


### 问题描述

自动化工具很难理解上下文，因此只有人工才能实施此类测试。下面两个例子会展示如何理解应用程序功能、开发者意图、以及一些创造性“跳出盒子”的想法来打破应用程序逻辑。第一个例子从最简单的参数操纵开始，第二个例子是真实世界中多步骤处理缺陷导致完全颠覆应用程序。


**例1**:

假设一个电子金融站点允许用户选择购买的物品，查看金额合计页面以及付款。如果攻击者能够退回到合计页面，维持有效的会话，并将物品价格修改为较低的价格并完成支付过程？

**例2**:

保持/锁住资源，使其他人无法购买该物品可能导致攻击者通过一个较低的价格获得商品。对抗方法是实现超时和确保只有正确的价格可以支付的机制。

**例3**:

万一用户可以从他们俱乐部/组织账户发起交易事务，随后将节点指向自己账户并取消交易？是否交易点券/额度会加入他们自己的账户？


### 业务逻辑测试用例

每一个应用程序存在不同的业务处理流程，应用程序相关的逻辑可以通过无限中方法进行组合。这部分主要提供一些场景的业务逻辑问题的例子，并没有罗列出所有可能的问题。


**业务逻辑漏洞利用方法可以分解为如下类别**:

* [业务逻辑数据验证测试 (OTG-BUSLOGIC-001)](./test_business_logic_data_validation_otg-buslogic-001.html)

在业务逻辑数据验证测试中，我们验证应用程序不允许用户向系统/应用程序插入“未验证”的数据。这是非常重要的，因为如果没有这层防护措施，攻击者可能向应用程序/系统插入“未验证”的数据/信息，而且使系统认为这些数据是“好的”并且已经在“入口”点进行验证，并且让系统相信“入口”点已经实施过了数据验证，因为这是业务逻辑工作流的一环。


* [请求伪造能力测试 (OTG-BUSLOGIC-002)](./test_ability_to_forge_requests_otg-buslogic-002.html)

在伪造和参数预测测试中，我们验证应用程序不允许用户向系统任何不应该有权限访问的或者需要特定时间特定方法访问的组件中提交或改变数据。这非常重要，因为缺少这层防护措施，攻击者可能通过“愚弄/忽悠”应用系统允许他们进入本不能进入的区域，绕过了应用业务逻辑工作流。


* [完整性测试 (OTG-BUSLOGIC-003)](./test_integrity_checks_otg-buslogic-003.html)

在完整性检查和篡改证据测试中，我们验证应用程序不允许用户破坏系统任何部分或数据的完整性。这非常重要，因为缺少这层防护措施，攻击者能打破业务逻辑工作流，并改变已经被攻破的应用/系统数据或者通过改变日志文件中的信息掩盖某种行为。


* [过程时长测试 (OTG-BUSLOGIC-004)](./test_for_process_timing_otg-buslogic-004.html)

在过程时长测试中，我们验证应用程序不允许用户通过输入/输出时长来操作系统或者预测系统行为。这非常重要，因为缺少这层防护，攻击者可能能监视处理时间和确定基于时间的输出内容或通过时间差异不完成某事务或某动作来绕过应用程序业务逻辑。


* [功能使用次数限制测试 (OTG-BUSLOGIC-005)](./test_number_of_times_a_function_can_be_used_limits_otg-buslogic-005.html)

在功能限制测试中，我们验证应用程序不允许用户使用超出应用程序的份额或业务工作流需要的功能次数。这非常重要，因为缺少这层防护，攻击者可能能超出业务使用次数许可地使用应用程序功能或者份额来获取额外的利益。


* [工作流程绕过测试 (OTG-BUSLOGIC-006)](./testing_for_the_circumvention_of_work_flows_otg-buslogic-006.html)

在绕过工作流的测试中，我们验证应用系统不允许用户实施在业务处理流程“支持/需要”之外的动作。这非常重要，因为缺少这层防护，攻击者可能能绕过工作流和某些检查，允许他们提前进入或跳过某些必须的区域。应用系统潜在允许动作/事务在不完成完整的业务流程下完成，使整个系统处在不完整的信息追踪回溯的环境中。


* [应用误用防护测试 (OTG-BUSLOGIC-007)](./test_defenses_against_application_mis-use_otg-buslogic-007.html)

在应用程序误用测试中，我们验证系统不允许用户以不预期的方式使用应用程序。


* [非预期文件类型上传测试 (OTG-BUSLOGIC-008)](./test_upload_of_unexpected_file_types_otg-buslogic-008.html)

在非预期文件上传测试中，我们验证应用程序不允许用户上传系统期待或业务逻辑允许以外的文件类型的文件。这非常重要因为缺少这层防护，攻击者可能提交非预期的文件如.exe或.php，这些文件可能被保存在系统之中，并被系统或应用程序执行。


* [恶意文件上传测试 (OTG-BUSLOGIC-009)](./test_upload_of_malicious_files_otg-buslogic-009.html)

在恶意文件上传测试中，我们验证应用系统不允许用户向系统上传能破坏系统安全的恶意或潜在恶意文件。这非常重要因为缺少这层防护措施，攻击者就能够向系统上传恶意文件来传播病毒、恶意软件甚至利用程序如执行shellcode。


### 测试工具

虽然这里有许多测试工具能够验证业务流程在合法情况下是否工作正常，但是这些工具无法探测逻辑漏洞。举例来说，工具不能探测用户是否能通过编辑参数、预测资源名称或提升权限够绕过业务处理缺陷来访问受限资源，也没有有效机制来帮助测试人员来质疑事务状态。

下面是一下常见的可能有助于发现业务逻辑问题的工具。

**HP 业务流程测试软件**

* http://www8.hp.com/us/en/software-solutions/software.html?compURI=1174789#.UObjK3ca7aE


**数据劫持代理 - 来观察HTTP流量中的请求与响应**

* Webscarab - https://www.owasp.org/index.php/Category:OWASP_WebScarab_Project

* Burp Proxy - http://portswigger.net/burp/proxy.html

* Paros Proxy - http://www.parosproxy.org/


**Web 浏览器插件 - 来查看和修改HTTP/HTTPS头、post参数和观察浏览器的DOM结构**

* Tamper Data (for Internet Explorer) - https://addons.mozilla.org/en-us/firefox/addon/tamper-data/

* TamperIE (for Internet Explorer) - http://www.bayden.com/tamperie/

* Firebug (for Internet Explorer) - https://addons.mozilla.org/en-us/firefox/addon/firebug/ and http://getfirebug.com/


**其他测试工具**

* Web Developer toolbar - https://chrome.google.com/webstore/detail/bfbameneiokkgbdmiekhjnmfkcnldhhm
    - Web开发者工具扩展为浏览器提供许多web开发者工具。这是Firefox官方扩展插件。

* HTTP Request Maker - https://chrome.google.com/webstore/detail/kajfghlhfkcocafkcjlajldicbikpgnp?hl=en-US
    - Request Maker是一个渗透测试工具，你可以使用他轻易捕捉web页面请求，修改URL、http头和POST数据。当然你也能创造新的请求。

* Cookie Editor - https://chrome.google.com/webstore/detail/fngmhnnpilhplaeedifhccceomclgfbg?hl=en-US
    - 一个Cookie管理器，可以用来添加、删除、修改、搜索、保护、阻隔Cookies。

* Session Manager - https://chrome.google.com/webstore/detail/bbcnbpafconjjigibnhbfmmgdbbkcjfi
    - 通过Session Manager你可以快速存储和读取你当前浏览器状态。你能够管理多个会话，重命名或异常会话数据库。每个会话都有独立的状态，比如打开的标签和窗口信息。一旦打开会话，浏览器就能恢复原来的状态。

* Cookie Swap - https://chrome.google.com/webstore/detail/dffhipnliikkblkhpjapbecpmoilcama?hl=en-US
    - 一个会话管理器，用来管理cookies，让你能使用不同账号登陆网站。你可以使用你所有的账户登陆Gmail、yahoo、hotmail和任何其他网站；使用这个工具切换其他账户。

* HTTP Response Browser - https://chrome.google.com/webstore/detail/mgekankhbggjkjpcbhacjgflbacnpljm?hl=en-US
    - 从浏览器发起HTTP请求，浏览响应（HTTP头和源代码）。使用XMLHttpRequest发送HTTP请求、HTTP头、消息主体，并能查看HTTP状态、头和源代码。在HTTP头或主体中点击链接来发起新的请求。这个插件对XML响应使用了[Syntax Highlighter](http://alexgorbatchev.com/)进行了格式化。

* Firebug lite for Chrome - https://chrome.google.com/webstore/detail/bmagokdooijbeehmkpknfglimnifench
    - Firebug Lite不是Firebug或Chrome开发者工具的替代品。他是一个整合这些工具的工具，他提供丰富的HTML元素、DOM元素、投影模型等可视化功能，他也能提供即时查看HTML元素、在线编辑CSS属性功能。

### 参考资料

**白皮书**

* Business Logic Vulnerabilities in Web Applications - http://www.google.com/url?sa=t&rct=j&q=BusinessLogicVulnerabilities.pdf&source=web&cd=1&cad=rja&ved=0CDIQFjAA&url=http%3A%2F%2Faccorute.googlecode.com%2Ffiles%2FBusinessLogicVulnerabilities.pdf&ei=2Xj9UJO5LYaB0QHakwE&usg=AFQjCNGlAcjK2uz2U87bTjTHjJ-T0T3THg&bvm=bv.41248874,d.dmg

* The Common Misuse Scoring System (CMSS): Metrics for Software Feature Misuse Vulnerabilities - NISTIR 7864 - http://csrc.nist.gov/publications/nistir/ir7864/nistir-7864.pdf

* Designing a Framework Method for Secure Business Application Logic Integrity in e-Commerce Systems, Faisal Nabi - http://ijns.femto.com.tw/contents/ijns-v12-n1/ijns-2011-v12-n1-p29-41.pdf

* Finite State testing of Graphical User Interfaces, Fevzi Belli - http://www.slideshare.net/Softwarecentral/finitestate-testing-of-graphical-user-interfaces

* Principles and Methods of Testing Finite State Machines - A Survey, David Lee, Mihalis Yannakakis - http://www.cse.ohio-state.edu/~lee/english/pdf/ieee-proceeding-survey.pdf

* Security Issues in Online Games, Jianxin Jeff Yan and Hyun-Jin Choi -   http://homepages.cs.ncl.ac.uk/jeff.yan/TEL.pdf

* Securing Virtual Worlds Against Real Attack, Dr. Igor Muttik, McAfee - https://www.info-point-security.com/open_downloads/2008/McAfee_wp_online_gaming_0808.pdf

* Seven Business Logic Flaws That Put Your Website At Risk – Jeremiah Grossman Founder and CTO, WhiteHat Security - https://www.whitehatsec.com/resource/whitepapers/business_logic_flaws.html

* Toward Automated Detection of Logic Vulnerabilities in Web Applications - Viktoria Felmetsger Ludovico Cavedon Christopher Kruegel Giovanni Vigna - https://www.usenix.org/legacy/event/sec10/tech/full_papers/Felmetsger.pdf

* 2012 Web Session Intelligence & Security Report: Business Logic Abuse, Dr. Ponemon - http://www.emc.com/collateral/rsa/silvertail/rsa-silver-tail-ponemon-ar.pdf

* 2012 Web Session Intelligence & Security Report: Business Logic Abuse (UK) Edition, Dr. Ponemon - http://buzz.silvertailsystems.com/Ponemon_UK.htm


**OWASP 相关**

* Business Logic Attacks – Bots and Bats, Eldad Chai - http://www.imperva.com/resources/adc/pdfs/AppSecEU09_BusinessLogicAttacks_EldadChai.pdf

* OWASP Detail Misuse Cases - https://www.owasp.org/index.php/Detail_misuse_cases

* How to Prevent Business Flaws Vulnerabilities in Web Applications, Marco Morana -  http://www.slideshare.net/marco_morana/issa-louisville-2010morana


**常用站点**

* Abuse of Functionality - http://projects.webappsec.org/w/page/13246913/Abuse-of-Functionality

* Business logic - http://en.wikipedia.org/wiki/Business_logic

* Business Logic Flaws and Yahoo Games -  http://jeremiahgrossman.blogspot.com/2006/12/business-logic-flaws.html

* CWE-840: Business Logic Errors - http://cwe.mitre.org/data/definitions/840.html

* Defying Logic: Theory, Design, and Implementation of Complex Systems for Testing Application Logic - http://www.slideshare.net/RafalLos/defying-logic-business-logic-testing-with-automation

* Prevent application logic attacks with sound app security practices - http://searchappsecurity.techtarget.com/qna/0,289202,sid92_gci1213424,00.html?bucket=NEWS&topic=302570

* Real-Life Example of a 'Business Logic Defect - http://h30501.www3.hp.com/t5/Following-the-White-Rabbit-A/Real-Life-Example-of-a-Business-Logic-Defect-Screen-Shots/ba-p/22581

* Software Testing Lifecycle - http://softwaretestingfundamentals.com/software-testing-life-cycle/

* Top 10 Business Logic Attack Vectors Attacking and Exploiting Business Application Assets and Flaws – Vulnerability Detection to Fix - http://www.ntobjectives.com/go/business-logic-attack-vectors-white-paper/ and http://www.ntobjectives.com/files/Business_Logic_White_Paper.pdf


**书籍**

* The Decision Model: A Business Logic Framework Linking Business and Technology, By Barbara Von Halle, Larry Goldberg, Published by CRC Press, ISBN1420082817 (2010)

