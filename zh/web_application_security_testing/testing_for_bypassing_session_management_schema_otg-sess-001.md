# 测试会话管理绕过 (OTG-SESS-001)


### 综述

为了避免在网站或者服务中每一个页面都要认证，web应用程序实现了不同的机制来保存和验证一定时间内的用户登陆凭证。这些机制被称做会话管理，他们在增强用户易用性和友好性上非常重要，同时也可能被渗透测试人员理由来获取账户权限。

在这个测试中，测试者想要检查cookie状态和其他用安全和不可预测方法产生的会话令牌。攻击者如果能预测和伪造一个弱的cookie，就能很容易劫持合法用户的会话。

Cookie被用于实现会话管理，并在RFC 2965中详细描述。简单来说，当一个用户访问了一个应用程序，这个应用程序需要在多个请求中跟踪记录用户身份和行为，服务器端产生cookie，发送给客户端。然后客户端将在cookie过期或被摧毁之前的每一个连接中发送该cookie回服务器。存储在cookie中的数据能提供给服务器大量关于用户身份的信息，以及到目前为止的行为和用户的偏好信息等等。因此为像HTTP一样的无状态协议提供一个状态。

一个典型的例子就在线商店购物车。在用户会话周期内，应用程序必须跟踪用户身份，个人资料和已经选择的产品、数量、单价、折扣等等。cookie是一个有效存储和传递这些信息的方法（其他方法是通过URL参数和隐藏域）。

取决于cookie中保存的数据的重要性，他们在应用系统安全中处于重要的地位。如果能伪造cookie可能导致合法用户的会话被劫持，或者获得更高的权限，或更加一般的影响是通过未授权途径访问应用。

在这个测试者，测试者必须检查客户端中保存的cookie是否能经受住一系列广范围的攻击，特别是目的是干涉合法用户和应用程序本身的攻击。总的来说，目的是能够通过伪造，使cookie被认为是合法的，并能通过他们获取一系列非授权的访问能力（会话劫持、权限提升等等）。

通常攻击的主要模式步骤有这么几种：
* **cookie 收集**: 收集大量的cookie样本；
* **cookie 逆向**: 分析cookie生成算法；
* **cookie 操纵**: 伪造合法cookie来实施攻击。最后一步可能需要大量的尝试，取决于cookie是如何被生成的（cookie暴力破解攻击）。

另一种攻击模式是cookie溢出。严格来说，这种攻击的本质是不同的，因为攻击者不是为了重建完美合法的cookie，相对的，他的目标是使内存区域溢出，来干涉应用程序的正确行动，可能能注入（和远程执行）恶意代码。

### 如何测试

#### 黑盒测试和相关例子

所有客户端和应用程序的交互应该根据下面几个准则进行测试：
* 所有Set-Cookie指示符中是否标记了Secure属性？
* 有任何cookie操作发生在非加密传输信道中么？
* cookie能强制在非加密信道中传输么？
* 如果是这样，应用程序如何保证安全？
* 有任何持久化的cookie么？
* 持久化的Cookie设置了什么过期时间，这些时间是否合理？
* 有没有临时cookie被设置成持久的？
* 有什么HTTP/1.1 Cache-Control 设置被用于保护cookie？
* 有什么HTTP/1.0 Cache-Control 设置被用于保护cookie？


##### Cookie 收集

操纵cookie的第一步是弄明白应用程序如何创建和管理cookie。在这个任务中，测试者必须试着回答下面问题：

* 应用程序使用了多少cookie？
    - 浏览应用，记录cookie何时被创建。制作一个收集的cookie列表，和设置cookie的页面（含有set-cookie指示符），和他们的有效域名、数值和特性。
* 应用程序的哪些部分生成或修改cookie？
    - 浏览应用，找出保持不变的cookie和被修改的cookie。找出是什么项目导致修改cookie？
* 应用程序的哪些部分需要cookie来访问和使用？
    - 找出那些需要cookie的部分。访问一个页面，然后尝试不使用cookie再次访问，或者修改cookie的数值。试着找出使用的cookie的对于关系。

使用电子表格来对应每个cookie和相关应用程序部分以及相关信息作为这阶段中有价值的输出成果。


##### 会话分析

会话令牌（cookie、会话ID、表单隐藏域）本身应该被检查，来确保他们从安全角度来看是好的。可以通过测试他们的随机性、独特性、抗统计和密码学分析能力以及信息泄露等标准来确定。

* 令牌结构和信息泄露

第一阶段是检查应用程序提供的会话ID的结构和内容。一个常见的错误是在令牌中包含特定的数据，而不是提供一个引用标识来索引真正存放在服务器端的数据。

如果会话ID是明文的，他的结构和数据就很容易观察到，如：
```
192.168.100.1:owaspuser:password:15:58
```

如果整个令牌都是被编码或哈希化的，应该通过一些不同的技巧来检查是否存在明显的混淆。比如`“192.168.100.1:owaspuser:password:15:58”`可以表示为十六进制编码、Base64编码和MD5散列：
```
Hex	3139322E3136382E3130302E313A6F77617370757365723A70617373776F72643A31353A3538
Base64	MTkyLjE2OC4xMDAuMTpvd2FzcHVzZXI6cGFzc3dvcmQ6MTU6NTg
MD5	01c2fc4f0a817afd8366689bd29dd40a
```

如果成功识别出混淆的形式，就有可能解码获得原始数据。但是在大多数情况下，不太现实。即使是这样，枚举消息编码的格式也是非常有用的。进一步说，如果令牌格式和混淆形式都能推断出来，那么自动化的暴力破解攻击就能够设计。

一些混合令牌可能包含ID地址和编码后的用户鉴别信息，比如如下形式：
```
owaspuser:192.168.100.1: a7656fafe94dae72b1e1487670148412
```

在分析完单个会话令牌后，就该检查典型样本。对令牌的简单分析应该能立即揭示明显的结构模式。比如，一个32位令牌可能包含16位静态数据和16位变量数据。这暗示前16位可能是表示用户的固定属性（如用户名或IP地址）。如果后16位数据块以常规频率递增，那么可能暗示是一个生产序列或就是时间序列元素。参见下面的例子。

如果能识别出令牌的静态元素，就需要收集更多的样本，一次改变一个潜在输入。比如，通过不同用户或不同IP地址的登陆尝试次数可能改变会话令牌的静态部分。

下面的问题应该在测试会话ID结构中考虑到：
* 会话ID哪个部分的静态的？
* 会话ID中存储了什么明文的凭证信息？（如用户名，UID，IP地址等）
* 还存储了什么可以轻易解码的凭证信息？
* 从会话ID的结构中能推断出什么信息？
* 会话ID的什么部分在同样的登陆条件下都是静态的？
* 在会话ID中有什么明显模式表示是一个整体的部分或个别的部分？


##### 会话ID的可预测性和随机性

分析会话ID的变量部分是接下来要做的事情，来建立任何已经识别出来的东西和预测的模式。这些分析可能需要手动实施，包括定制、统计和密码学分析来推断会话ID的内容模式。手动检查应该包括对比相同登陆情况下的会话ID，如同样的用户名、密码、IP地址等。

时间是一个重要的控制因素。需要在相同时间窗口内发出大量同步连接来收集样本，并维持变量不变。甚至50ms或更少的分割也可能过于粗糙，通过这个方法采集的样本可能会错过用来揭示基于时间的组件。

变量应该多次分析来决定他们是不是自然增长的。当他们是递增的，可以研究是否存在相对于绝对时间或流逝时间的模式。许多系统使用时间作为伪随机数发生器的种子。如果这些ID模式看上去是随机的，那么也可以把对时间或其他环境变量的单向哈希的情况列入考虑中。通常，密码哈希算法的结果是一个可以鉴别的十进制或十六进制的数字。

在分析会话序列时，模式或循环、静态元素和客户端依赖都应该被考虑有可能涉及令牌结构或其中的程序功能函数中。
* 会话ID能证明是完全随机的么？是否可以重现结果？
* 同样的输入条件和能产生同样的ID么？
* 会话ID能被证明能对抗统计或密码学分析么？
* 会话ID中的什么元素可能和时间相关？
* 会话ID中的什么部分是可预测的？
* 给定整个生成算法的所有信息和之前的ID能推断出下一个ID么？


##### Cookie 逆向

既然测试者可以枚举cookie，且知道他们是使用途径，是时候来更加仔细考察cookie有什么有趣的地方了。测试者对什么样的cookie更感兴趣呢？一个提供安全的会话管理的cookie，必须包含一系列特性，来保护不被其他攻击。

这些特性总结为如下几点：
1. 不可预测性: 一个cookie必须包含一下难以猜测的数据。越难以伪造合法cookie，就越不容易破坏合法用户的会话。如果一个攻击者能够猜测合法用户正使用的cookie，也就能全面模仿该用户（会话劫持）。为了是cookie不可预测，随机变量和密码学应该被使用。
2. 抗篡改: 一个cookie必须抵抗恶意的修改企图。如果测试者获得了一个像 IsAdmin=No 的cookie，明显可以通过这个字段他来获得管理权限，除非应用程序进行了多重的检查（比如，在cookie后增加了该数值的加密哈希作为验证）。
3. 有效期限: 一个重要的cookie必须只能在一定的时间内有效，必须在使用后从磁盘或内存中删除来避免重放攻击。这对于那些不太重要的数据不太适用，他们可能需要在不同会话之间传递（比如在网站外观偏好信息）。
4. “Secure” 标志: 一个对完整性要求的会话cookie应该带有这个标志，来保证他们只在加密信道中进行传输，防止被监听。

在这里使用到的方法是收集充分多的cookie实例，并从他们值中寻找出特点的模式。“充分”的确切意义需要具体情况具体分析，如果cookie生成模式很容易被破解，几条就够了，如果测试者需要进行数学分析（如，卡方检验chi-quares，吸引子attractors。更多信息见后文），那就需要数千条才行。

重点是特别要注意应用程序的工作流，因为会话状态可能会严重影响收集到的cookie。在进行认证前收集的cookie，和认证后去的的cookie可能大不相同。

另一个需要考虑的因素是时间。总是记录cookie取得时候的确切时间，因为很有可能时间在cookie中会扮演重要角色（服务器可能将时间戳作为cookie值的一部分）。时间记录可以是本地时间或是HTTP响应中的服务器上的时间戳（或两者都记录）。

当分析收集到的数值的时候，测试者应该找出所有可能影响cookie数值的变量，并试着一次一个地改变他们。将修改过的cookie发回服务器可能有利于理解应用程序是如何读取并处理cookie的方法。

在这个阶段，一些实施的检查例子包括：
* cookie中用到了哪些字符集？是数值型的？字母和数字？十六进制？如果测试者使用不在预期集合里面的字符会发生什么？
* cookie是由多个子部分组合而成的么？这些不同的部分如何分割的？通过分隔符么？

有些部分可能会经常变化，也有些可能是常量，还有些可能在一部分范围内进行选择。分解cookie的各个部分是分析的基础。

一个很容易就能了解的cookie结构的例子：

```
ID=5a0acfc7ffeb919:CR=1:TM=1120514521:LM=1120514521:S=j3am5KzC4v01ba3q
```

这个例子展示了5个变量，包含不同类型的数据：

```
ID – 十六进制
CR – 小整数
TM and LM – 大整数（有趣的是他们相同，可能值得修改其中之一）
S – 数字和字母
```

甚至有时没有分隔符，但是足够多的样本也能提供帮助。比如，下面的序列：

```
0123456789abcdef
```


##### 暴力破解攻击

暴力破解攻击不可避免涉及到了概率和随机性。会话ID的变化必须和应用程序会话持续长度和超时机制相互联系。如果会话ID的变化比较小，而且有效持久性比较长，那么暴力破解的成功概率就会更加大。

一个长的会话ID（或者每次变化很大的ID）和一个较短有效时间的间隔的ID可能难以使用暴力破解成功攻击。

* 暴力搜索所有可能的会话ID需要多久？
* 会话ID空间是否足够大来防止暴力破解？比如，密钥的长度在其有效生命周期内充分大。
* 不同会话ID的连接请求是否有延迟机制来减轻暴力攻击的风险？


#### 灰盒测试和相关例子

如果测试者能够接触到会话管理机制的实现部分，应该检查如下地方：
* 随机会话令牌
    - 客户端的会话ID或cookie应该不能轻易被预测（不要使用基于可预测变量的线性算法如客户端IP地址）。使用加密算法的密钥长度建议在256位（以AES为例）。
* 令牌长度
    - 会话ID长度应该至少50个字符。
* 会话超时
    - 会话令牌应该有一个预设的超时时间（依赖于应用程序数据的重要程度）。
* Cookie配置
    - non-persistent: 只存于RAM内存中
	- secure （只能用户HTTPS信道） `Set Cookie: cookie=data; path=/; domain=.aaa.it; secure`
	- [HTTPOnly](https://www.owasp.org/index.php/HTTPOnly) （无法被脚本读取）  `Set Cookie: cookie=data; path=/; domain=.aaa.it; HTTPOnly`

更多信息参见： [测试cookie属性](https://www.owasp.org/index.php/Testing_for_cookies_attributes_%28OWASP-SM-002%29)

### 测试工具

* OWASP Zed Attack Proxy Project (ZAP) - https://www.owasp.org/index.php/OWASP_Zed_Attack_Proxy_Project - features a session token analysis mechanism.
* Burp Sequencer - http://www.portswigger.net/suite/sequencer.html
* Foundstone CookieDigger - http://www.mcafee.com/us/downloads/free-tools/cookiedigger.aspx
* YEHG's JHijack - https://www.owasp.org/index.php/JHijack

### 参考资料

**白皮书**

* RFC 2965 “HTTP State Management Mechanism”
* RFC 1750 “Randomness Recommendations for Security”
* Michal Zalewski: "Strange Attractors and TCP/IP Sequence Number Analysis" (2001): http://lcamtuf.coredump.cx/oldtcp/tcpseq.html
* Michal Zalewski: "Strange Attractors and TCP/IP Sequence Number Analysis - One Year Later" (2002): http://lcamtuf.coredump.cx/newtcp/
* Correlation Coefficient: http://mathworld.wolfram.com/CorrelationCoefficient.html
* Darrin Barrall: "Automated Cookie Analysis" –  http://www.spidynamics.com/assets/documents/SPIcookies.pdf
* ENT: http://fourmilab.ch/random/
* http://seclists.org/lists/fulldisclosure/2005/Jun/0188.html
* Gunter Ollmann: "Web Based Session Management" - http://www.technicalinfo.net
* Matteo Meucci:"MMS Spoofing" - http://www.owasp.org/images/7/72/MMS_Spoofing.ppt

**视频资料**

* Session Hijacking in Webgoat Lesson - http://yehg.net/lab/pr0js/training/view/owasp/webgoat/WebGoat_SessionMan_SessionHijackingWithJHijack/


### 相关安全资料

#### 会话管理漏洞的描述

参见OWASP的关于 [会话管理漏洞](https://www.owasp.org/index.php/Category:Session_Management_Vulnerability) 的文章。


#### 会话管理对抗措施的描述

参见OWASP的关于 [会话管理对抗措施](https://www.owasp.org/index.php/Category:Session_Management) 的文章。


#### 如何避免会话管理漏洞

参见 [OWASP开发指南](https://www.owasp.org/index.php/Category:OWASP_Guide_Project) 中关于 [避免会话管理漏洞](https://www.owasp.org/index.php/Session_Management) 的文章。


#### 如何针对会话管理漏洞审查代码

参见 [OWASP 代码评估指南](https://www.owasp.org/index.php/Category:OWASP_Code_Review_Project) 中关于 [审查会话管理](https://www.owasp.org/index.php/Codereview-Session-Management) 的文章。

