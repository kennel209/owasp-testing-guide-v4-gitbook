# 非预期类型文件上传测试 (OTG-BUSLOGIC-008)


### 综述

许多应用的业务逻辑允许通过文件上传数据或修改数据。但这个业务过程必须检查文件，并只允许特定的，“支持”的文件类型。业务逻辑到底“支持”哪些文件是应用程序/系统相关的。允许用户上传文件可能存在风险，攻击者可能上传未预期的文件类型的文件，而且这些文件可能能被执行，对应用程序造成不利的影响，如丑化站点，执行远程命令，浏览系统文件，浏览本地资源，攻击其他服务器，或利用本地漏洞进行攻击，等等。

上传非预期文件类型的文件的相关漏洞是独特的，因为这个过程本应该在不是特定类型的文件中拒绝上传。此外，区别于恶意文件上传，在大多数的错误文件类型可能本身没有“恶意”，但是保存的文件内容存在问题。举例来说，如果应用程序接受windows excel文件，如果相似的数据库文件被上传，可能这些数据也能被读取，但可能会提取到不正确的位置。

应用程序可能期待某个特定的文件类型被上传处理，如.cvs，.txt文件。应用程序可能不通过后缀（低可信的文件验证）或内容（高可信的文件验证）进行上传文件的验证。这可能导致非预期的系统或数据库结果，或给攻击者额外攻击系统/应用的渠道。


### 案例

假设一个图片分享应用允许用户上传.gif或.jpg图形文件。万一攻击者能够上传含有`<script>`标签的html文件或者php文件会如何？系统可能将这些文件从临时目录移动到最终目录，在这目录中，可能就能执行php代码。


### 如何测试

#### 通用测试方法

* 审阅项目文档，查找那些文件类型不应该被应用程序/系统支持。
* 尝试上传这些“不支持”的文件，验证是否被拒绝。
* 如果可以同时上传多个文件，测试是不是每个文件都被有效验证了。


#### 特定测试方法

*	学习应用程序的逻辑需求。
*	准备一系列的不被支持的文件用于上传，可能包括：jsp，exe，或htmlPrepare a library of files that are “not approved” for upload that may contain files such as: jsp, exe, or html files containing script.
*	In the application navigate to the file submission or upload mechanism.
*	Submit the “not approved” file for upload and verify that they are properly prevented from uploading


### 相关测试用例

[ Test File Extensions Handling for Sensitive Information (OTG-CONFIG-003) ](https://www.owasp.org/index.php/Test_File_Extensions_Handling_for_Sensitive_Information_%28OTG-CONFIG-003%29)

[ Test Upload of Malicious Files (OTG-BUSLOGIC-009)](https://www.owasp.org/index.php/Test_Upload_of_Malicious_Files_%28OTG-BUSLOGIC-009%29)


### 参考资料

* OWASP - Unrestricted File Upload - https://www.owasp.org/index.php/Unrestricted_File_Upload
* File upload security best practices: Block a malicious file upload - http://www.computerweekly.com/answer/File-upload-security-best-practices-Block-a-malicious-file-upload
* Stop people uploading malicious PHP files via forms - http://stackoverflow.com/questions/602539/stop-people-uploading-malicious-php-files-via-forms
* CWE-434: Unrestricted Upload of File with Dangerous Type - http://cwe.mitre.org/data/definitions/434.html
* Secure Programming Tips - Handling File Uploads - https://www.datasprings.com/resources/dnn-tutorials/artmid/535/articleid/65/secure-programming-tips-handling-file-uploads?AspxAutoDetectCookieSupport=1


### 整改措施

应用程序应该含有只允许“可接受”的文件机制，这些文件会被其他的应用程序使用或处理。一些特定的例子包括：文件类型黑白名单，在http头使用“Content-Type”，或使用文件类型识别程序。目标都是只允许特定类型的文件进入系统。

