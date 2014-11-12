# 审查旧文件、备份文件和未引用的文件中的敏感信息 (OTG-CONFIG-004)


### 综述
虽然大多数web服务器的文件被服务器自己处理，但是能找到未引用的或这遗忘的文件，这些文件可能会有助于获得基础设施的重要信息或有效登陆凭证。


大多数场景包括重命名后的就版本修改文件，不同语言文件可以被当作源代码文件下载，或者自动或手动备份压缩文件。备份文件也可能由于文件系统的特性被自动生成，比如“文件快照”。


所有这些文件给予了测试者访问内部网络、后门、管理接口甚至登陆凭证来连接管理接口或数据库服务器。

漏洞的重要来源在于这些文件，他们可能和应用程序本身无关，但是在编辑应用文件过程中产生或临时备份文件中产生，又或是遗留的旧文件或未引用文件。在生产服务器上实施在线修改或其他管理行为可能无意中留下备份的文件拷贝，或是自动被编辑器在编辑的过程产生，或被管理员存放在压缩备份文件中。


这些文件很容易被遗忘，并导致严重的安全威胁。这是由于备份文件的文件扩展名可能区别于原始文件。我们生成了 *.tar，.zip 或.gz* 归档文件（被遗忘），显然是不同的扩展名，编辑器自动备份的也一样（比如emacs生成的临时文件 *file* 命名为 *file~* ）。手动备份也可能有这个问题（考虑复制 *file* 到 *file.old* 的情况）。应用的文件系统也可能在你不知道的时候为你的应用创建不同的时间点的 *快照* ，这些可能也能通过web访问到，对应用程序产生一个类似于备份文件但不同的威胁。


总之，这些行为产生应用程序不需要的文件，可能会被web服务器不同方式处理。例如，如果我们复制 *login.asp* 为 *login.asp.old*，那么我们就允许用户下载 *login.asp* 的源代码。因为 *login.asp.old* 由于他的扩展名可能当作文本文件被处理，而不是被执行。换而言之，访问 *login.asp* 会引起服务器端执行 *login.asp* 的代码，然而访问 *login.asp.old* 导致 *login.asp.old* 的内容（事实上是服务器端代码）被当作文本返回给用户，并在浏览器中显示。这可能是安全风险，因为敏感信息被泄露了。


通常来说暴露服务器端代码是一个坏主意。不仅仅暴露了不必须的业务逻辑，同时也揭露了应用相关的信息（路径名称、数据结构等等），可能会给攻击者提供帮助。更不要说很多脚本直接内嵌明文的用户名和密码（这是一个粗心的非常危险的编码实践）。


其他引起未引用文件的情况取决于设计或这配置选择，当允许不同种类的应用相关文件，如数据文件、配置文件、日志文件存储在web服务器能够访问的文件系统目录时就会发生。正常情况下，这些文件没有放在能通过web访问的文件系统中的理由，因为他们只被应用层访问，只被应用程序本身使用（不是使用浏览器的不同用户）。


#### 威胁

备份文件和未引用文件可能对web应用程序的安全造成多种威胁：

* 未引用的文件可能暴露敏感信息有助于攻击行为；比如引用文件包含数据库凭证信息，配置文件包含其他隐藏的信息，比如绝对路径等等。
* 未引用的页面可能能够包含攻击应用程序的强大功能函数；比如管理页面不应该从公开页面内容中获得，但是能够被已知路径的用户访问。
* 旧文件和备份文件可能包含在近期版本中已经修复的漏洞；比如 *viewdoc.old.jsp* 可能包含目录遍历漏洞，而 *viewdoc.jsp* 中已经修复，但是这个漏洞仍然可能被发现旧版本的恶意人员利用。
* 备份文件可能暴露页面源代码；比如请求 *viewdoc.bak* 可能返回 *viewdoc.jsp* 的源代码，通过评审源代码可能发现那些很难从盲目的请求中发现的漏洞。
* 备份压缩文件可能包含web目录下的所有文件（甚至web根目录之外的文件）。这允许攻击者能快速枚举整个应用，包括未引用的页面、源代码和包含文件等等。例如如果你遗忘了一个名为 *myservlets.jar.old* 的文件，它包含了一个你实现 servlet类的备份，那么许多敏感信息可能被反编译和逆向工程中获得。
* 在一些例子中，复制或编辑文件不修改文件扩展名，但是修改文件名。例如在windows环境下可能发生这个问题，当文件被复制时候，操作系统自动给文件加上本地语言化的“复制”字符。由于文件扩展名没有改变，可执行文件不会被服务器以明文方式返回，所以这种情况下不会暴露源代码。然而，这些文件也可能十分有害，因为他们可能已经被废弃或包含错误的逻辑，当被调用时候，可能引发应用程序错误，这些诊断信息或许能给攻击者带来有用的信息。
* 日志文件可能包含关于用户的敏感信息，例如URL参数中传递敏感数据，会话ID，已访问URL（可能暴露一些未引用内容）等等。其他日志文件（如FTP日志）可能包含系统管理员维护系统情况的敏感信息。
* 文件系统快照也可能包含那些已经修复的存在漏洞的代码拷贝。例如 */.snapshot/monthly.1/view.php* 可能包含已经修复的存在目录遍历楼的的 */view.php* 文件，这个漏洞能被任何能够访问就版本文件的人利用。


### 如何测试
#### 黑盒测试

测试未引用的文件包括自动化和手动技巧，通常需要以下一系列技巧的组合：

##### 从发布的公开内容中推断文件命名模式

枚举所有应用程序页面和功能。这能通过使用浏览器手动完成，或使用应用爬虫工具。许多应用使用可以识别的命名模式，或者使用可识别的词语来组织文件目录和资源。从已经发布的内容的命名模式，很有可能推断出未引用的页面的名称和目录。例如找到一个名字为 *viewuser.asp* ，那么可以试着找找 *edituser.asp*、*adduser.asp*和*deleteuser.asp*。如果找到一个 */app/user* 目录，可以试着找找 */app/admin* 和 */app/manager* 。


##### 已发布的内容中的其他线索

许多web应用会在已发布的内容中留下通往隐藏页面和隐藏功能的线索。这些线索往往能在JavaScript文件和HTML源代码中发现。所有已经发布的内容中的源代码都应该被手动评审来鉴别关于其他页面和功能的线索。例如：

程序员的注释和注释掉的源代码部分可能指向隐藏内容：

```
<!-- <A HREF="uploadfile.jsp">Upload a document to the server</A> -->
<!-- Link removed while bugs in uploadfile.jsp are fixed          -->
```


JavaScript可能包含特定情况下的用户页面链接：

```
var adminUser=false;
:
if (adminUser) menu.add (new menuItem ("Maintain users", "/admin/useradmin.jsp"));
```


HTML页面可能包含禁用SUBMIT元素的隐藏表单：

```
<FORM action="forgotPassword.jsp" method="post">
    <INPUT type="hidden" name="userID" value="123">
    <!-- <INPUT type="submit" value="Forgot Password"> -->
</FORM>
```


另一个包含未引用的目录的线索在*/robots.txt*文件之中，可能提供如下信息：

```
User-agent: *
Disallow: /Admin
Disallow: /uploads
Disallow: /backup
Disallow: /~jbloggs
Disallow: /include
```


##### 盲目猜测

在最简单的一种方式就是通过请求一系列的常用文件名字来尝试猜测服务器上存在的文件和目录。下面包含netcat的包装脚本可以读取一个字典列表，并实施基本的猜测攻击：

```
#!/bin/bash

server=www.targetapp.com
port=80

while read url
do
echo -ne "$url\t"
echo -e "GET /$url HTTP/1.0\nHost: $server\n" | netcat $server $port | head -1
done | tee outputfile

```


视服务器情况而定，GET请求可能用HEAD请求替代来加速攻击。输出文件可以通过grep过滤来获得有趣的响应。200响应码（OK）通常表明一个合法的自由被发现（假设服务器没有提供一个自定义的“未发现”200响应页面）。同时也查找301响应（Moved）、302响应（Found）、401响应（Unauthorized）、403响应（Forrbidden）和500响应（Internal error），这些响应也表明目录或自由值得深入调查。


基本的猜测攻击应该在web根目录中和其他被鉴别出来的（通过其他枚举手段）中运行。更多高级/有效的猜测攻击如下：

* 通过应用程序已知区域来鉴别扩展名（如jsp，aspx，html），使用基本字典加上这些扩展名（或使用更多的扩展名字典，如果条件允许）。
* 对于每一个从其他枚举技巧中发现的文件，创建一个从这些文件衍生出的自定义的字典。使用一系列常见的文件修饰扩展（包括~，bak，txt，src，dev，old，inc，orig，copy，tmp等等），在实际文件名的前面、后面加入这些扩展，或直接替代文件名。


注意：在windows环境下，当文件被复制时候，操作系统自动给文件加上本地语言化的“复制”字符。由于文件扩展名没有改变，这种情况下不会暴露源代码。然而，这些文件可能引发应用程序错误，能给攻击者带来有用的信息。


##### 从服务器漏洞和错误配置中获得的信息

最显而易见在错误配置的服务器中暴露未引用页面的方法是通过目录列举浏览。请求枚举获得的目录来鉴别那些目录提供目录列举功能。

大多在个人web服务器中发现的漏洞能允许攻击者枚举未引用的内容，例如：

* Apache ?M=D 目录列举漏洞
* 不同的IIS脚本源代码暴露漏洞
* IIS WebDAV 目录列举漏洞


##### Use of publicly available information

Pages and functionality in Internet-facing web applications that are not referenced from within the application itself may be referenced from other public domain sources. There are various sources of these references:
* Pages that used to be referenced may still appear in the archives of Internet search engines. For example, *1998results.asp* may no longer be linked from a company’s website, but may remain on the server and in search engine databases. This old script may contain vulnerabilities that could be used to compromise the entire site. The *site:* Google search operator may be used to run a query only against the domain of choice, such as in: *site:www.example.com*. Using search engines in this way has lead to a broad array of techniques which you may find useful and that are described in the *Google Hacking* section of this Guide. Check it to hone your testing skills via Google. Backup files are not likely to be referenced by any other files and therefore may have not been indexed by Google, but if they lie in browsable directories the search engine might know about them.
* In addition, Google and Yahoo keep cached versions of pages found by their robots. Even if *1998results.asp* has been removed from the target server, a version of its output may still be stored by these search engines. The cached version may contain references to, or clues about, additional hidden content that still remains on the server.
* Content that is not referenced from within a target application may be linked to by third-party websites. For example, an application which processes online payments on behalf of third-party traders may contain a variety of bespoke functionality which can (normally) only be found by following links within the web sites of its customers.


##### File name filter bypass

Because blacklist filters are based on regular expressions, one can sometimes take advantage of obscure OS file name expansion features in which work in ways the developer didn't expect. The tester can sometimes exploit differences in ways that file names are parsed by the application, web server, and underlying  OS and it's file name conventions.


Example: Windows 8.3 filename expansion
"c:\program files" becomes "C:\PROGRA~1"
```
– Remove incompatible characters
– Convert spaces to underscores
- Take the first six characters of the basename
– Add “~<digit>” which is used to distinguish files with names using the same six initial characters
- This convention changes after the first 3 cname ollisions
– Truncate  file extension to three characters
- Make all the characters uppercase
```


#### 灰盒测试

Performing gray box testing against old and backup files requires examining the files contained in the directories belonging to the set of web directories served by the web server(s) of the web application infrastructure. Theoretically the examination should be performed by hand to be thorough. However, since in most cases copies of files or backup files tend to be created by using the same naming conventions, the search can be easily scripted. For example, editors leave behind backup copies by naming them with a recognizable extension or ending and humans tend to leave behind files with a “.old” or similar predictable extensions. A good strategy is that of periodically scheduling a background job checking for files with extensions likely to identify them as copy or backup files, and performing manual checks as well on a longer time basis.


### 测试工具

* Vulnerability assessment tools tend to include checks to spot web directories having standard names (such as “admin”, “test”, “backup”, etc.), and to report any web directory which allows indexing. If you can’t get any directory listing, you should try to check for likely backup extensions. Check for example Nessus (http://www.nessus.org), Nikto2(http://www.cirt.net/code/nikto.shtml) or its new derivative Wikto (http://www.sensepost.com/research/wikto/), which also supports Google hacking based strategies.
* Web spider tools: wget (http://www.gnu.org/software/wget/,   http://www.interlog.com/~tcharron/wgetwin.html); Sam Spade (http://www.samspade.org); Spike proxy includes a web site crawler function (http://www.immunitysec.com/spikeproxy.html); Xenu (http://home.snafu.de/tilman/xenulink.html); curl (http://curl.haxx.se). Some of them are also included in standard Linux distributions.
* Web development tools usually include facilities to identify broken links and unreferenced files.


### 整改措施
To guarantee an effective protection strategy, testing should be compounded by a security policy which clearly forbids dangerous practices, such as:


* Editing files in-place on the web server or application server file systems. This is a particular bad habit, since it is likely to unwillingly generate backup files by the editors. It is amazing to see how often this is done, even in large organizations. If you absolutely need to edit files on a production system, do ensure that you don’t leave behind anything which is not explicitly intended, and consider that you are doing it at your own risk.
* Check carefully any other activity performed on file systems exposed by the web server, such as spot administration activities. For example, if you occasionally need to take a snapshot of a couple of directories (which you should not do on a production system), you may be tempted to zip them first. Be careful not to forget behind those archive files.
* Appropriate configuration management policies should help not to leave around obsolete and unreferenced files.
* Applications should be designed not to create (or rely on) files stored under the web directory trees served by the web server. Data files, log files, configuration files, etc. should be stored in directories not accessible by the web server, to counter the possibility of information disclosure (not to mention data modification if web directory permissions allow writing).
* File system snapshots should not be accessible via the web if the document root is on a file system using this technology. Configure your web server to deny access to such directories, for example under apache a location directive such this should be used:
```
<Location ~ ".snapshot">
    Order deny,allow
    Deny from all
</Location>
```
