# 测试上传恶意文件 (OTG-BUSLOGIC-009)


### 综述

许多应用程序允许用户上传数据信息。我们通常验证文本的安全性和合法性，但是接受文件上传可能引入更多的风险。为了减轻风险，我们可能只接受特定扩展名的文件，但是攻击者可能在将恶意代码嵌入文件中。测试恶意文件确保应用程序/系统能够正确阻止攻击者上传恶意文件。

恶意文件上传的相关漏洞独特之处在于“恶意”文件能够轻易在在业务逻辑层被拒绝，在上传过程阶段进行文件扫描，拒绝那些扫描结果为恶意的文件。此外，不同于上传非预期文件的是，上传的文件类型是合法，可以接受的的，但其内容可能对系统存在恶意影响。

最后，“恶意”对于不同的系统可能存在不同的解释，例如，利用SQL服务器漏洞的恶意文件可能在静态文件框架环境下不认为是“恶意”的。

应用程序可能允许上传包含漏洞利用程序或shellcode的恶意文件，并且不会对他们进行文件扫描。恶意文件也可能在应用程序架构的不同地方被检测出来，如IPS/IDS，服务器反病毒软件或者自动化过程的反病毒扫描程序。


### 案例

假设一个图片分享应用允许用户上传.gif或.jpg图形文件。万一攻击者能够上传一个PHP shell或者exe文件或者病毒会如何？攻击者上传的文件可能存储在系统某处，病毒可能通过自身或远程执行扩散，或者shell代码被执行。


### 如何测试

#### 通用测试方法

* 审查项目文档，探索应用/系统来发现形成“恶意”文件的原因。
* 设计或者获取一个已知的“恶意”文件。
* 尝试上传该恶意文件，确认是否被拒绝。
* 如果一次可以上传多个文件，确认每一个文件被正确处理。


#### 特定测试方法1

* 使用Metasploit荷载生成功能，利用“msfpayload”命令生成含有shellcode的windows可执行文件。
* 上传该文件检查是否被拒绝。


#### 特定测试方法2

* 设计或创建一个可能破坏应用程序恶意探测过程的文件。互联网上有许多这样的文件，如ducklin.htm或dcklin-html.htm。
* 上传该文件检查是否被拒绝。


#### 特定测试方法3

* 建立代理来捕获“合法”的文件上传请求。
* 发送“非法”请求，查看该请求是否被拒绝。


### 相关测试用例

* [ 测试敏感信息的文件扩展处理 (OTG-CONFIG-003) ](https://www.owasp.org/index.php/Test_File_Extensions_Handling_for_Sensitive_Information_%28OTG-CONFIG-003%29)

* [ 测试上传非预期类型文件 (OTG-BUSLOGIC-008)](https://www.owasp.org/index.php/Test_Upload_of_Malicious_Files_%28OTG-BUSLOGIC-009%29)


### 测试工具

* Metasploit相关荷载生成功能
* 劫持代理


### 参考资料

* OWASP - Unrestricted File Upload - https://www.owasp.org/index.php/Unrestricted_File_Upload
* Why File Upload Forms are a Major Security Threat - http://www.acunetix.com/websitesecurity/upload-forms-threat/
* File upload security best practices: Block a malicious file upload - http://www.computerweekly.com/answer/File-upload-security-best-practices-Block-a-malicious-file-upload
* Overview of Malicious File Upload Attacks - http://securitymecca.com/article/overview-of-malicious-file-upload-attacks/
* Stop people uploading malicious PHP files via forms - http://stackoverflow.com/questions/602539/stop-people-uploading-malicious-php-files-via-forms
* How to Tell if a File is Malicious - http://www.techsupportalert.com/content/how-tell-if-file-malicious.htm
* CWE-434: Unrestricted Upload of File with Dangerous Type - http://cwe.mitre.org/data/definitions/434.html
* Implementing Secure File Upload - http://infosecauditor.wordpress.com/tag/malicious-file-upload/
* Watchful File Upload - http://palizine.plynt.com/issues/2011Apr/file-upload/
* Matasploit Generating Payloads - http://www.offensive-security.com/metasploit-unleashed/Generating_Payloads
* Project Shellcode – Shellcode Tutorial 9: Generating Shellcode Using Metasploit http://www.projectshellcode.com/?q=node/29
* Anti-Malware Test file - http://www.eicar.org/86-0-Intended-use.html


### 整改措施

除了使用黑白名单的防护措施，使用“Content-Type”头，或使用文件类型识别程序可能不总是足以对抗这类漏洞。每个从用户接受文件的应用程序必须含有验证上传文件是否含有恶意代码的机制。上传文件不应该存储在用户或者攻击者能够直接访问的位置。
