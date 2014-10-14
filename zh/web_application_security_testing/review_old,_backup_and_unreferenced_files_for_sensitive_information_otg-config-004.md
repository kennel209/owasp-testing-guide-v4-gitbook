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

* Unreferenced files may disclose sensitive information that can facilitate a focused attack against the application; for example include files containing database credentials, configuration files containing references to other hidden content, absolute file paths, etc.
* Unreferenced pages may contain powerful functionality that can be used to attack the application; for example an administration page that is not linked from published content but can be accessed by any user who knows where to find it.
* Old and backup files may contain vulnerabilities that have been fixed in more recent versions; for example *viewdoc.old.jsp* may contain a directory traversal vulnerability that has been fixed in *viewdoc.jsp* but can still be exploited by anyone who finds the old version.
* Backup files may disclose the source code for pages designed to execute on the server; for example requesting *viewdoc.bak* may return the source code for *viewdoc.jsp*, which can be reviewed for vulnerabilities that may be difficult to find by making blind requests to the executable page. While this threat obviously applies to scripted languages, such as Perl, PHP, ASP, shell scripts, JSP, etc., it is not limited to them, as shown in the example provided in the next bullet.
* Backup archives may contain copies of all files within (or even outside) the webroot. This allows an attacker to quickly enumerate the entire application, including unreferenced pages, source code, include files, etc. For example, if you forget a file named *myservlets.jar.old* file containing (a backup copy of) your servlet implementation classes, you are exposing a lot of sensitive information which is susceptible to decompilation and reverse engineering.
* In some cases copying or editing a file does not modify the file extension, but modifies the file name. This happens for example in Windows environments, where file copying operations generate file names prefixed with “Copy of “ or localized versions of this string. Since the file extension is left unchanged, this is not a case where an executable file is returned as plain text by the web server, and therefore not a case of source code disclosure. However, these files too are dangerous because there is a chance that they include obsolete and incorrect logic that, when invoked, could trigger application errors, which might yield valuable information to an attacker, if diagnostic message display is enabled.
* Log files may contain sensitive information about the activities of application users, for example sensitive data passed in URL parameters, session IDs, URLs visited (which may disclose additional unreferenced content), etc. Other log files (e.g. ftp logs) may contain sensitive information about the maintenance of the application by system administrators.
* File system snapshots may contain copies of the code that contain vulnerabilities that have been fixed in more recent versions. For example */.snapshot/monthly.1/view.php* may contain a directory traversal vulnerability that has been fixed in */view.php* but can still be exploited by anyone who finds the old version.


### 如何测试
#### 黑盒测试

Testing for unreferenced files uses both automated and manual techniques, and typically involves a combination of the following:

##### Inference from the naming scheme used for published content

Enumerate all of the application’s pages and functionality. This can be done manually using a browser, or using an application spidering tool. Most applications use a recognizable naming scheme, and organize resources into pages and directories using words that describe their function. From the naming scheme used for published content, it is often possible to infer the name and location of unreferenced pages. For example, if a page *viewuser.asp* is found, then look also for *edituser.asp*, *adduser.asp* and *deleteuser.asp*. If a directory */app/user* is found, then look also for */app/admin* and */app/manager*.


##### Other clues in published content

Many web applications leave clues in published content that can lead to the discovery of hidden pages and functionality. These clues often appear in the source code of HTML and JavaScript files. The source code for all published content should be manually reviewed to identify clues about other pages and functionality. For example:

Programmers’ comments and commented-out sections of source code may refer to hidden content:

```
<!-- <A HREF="uploadfile.jsp">Upload a document to the server</A> -->
<!-- Link removed while bugs in uploadfile.jsp are fixed          -->
```


JavaScript may contain page links that are only rendered within the user’s GUI under certain circumstances:

```
var adminUser=false;
:
if (adminUser) menu.add (new menuItem ("Maintain users", "/admin/useradmin.jsp"));
```


HTML pages may contain FORMs that have been hidden by disabling the SUBMIT element:

```
<FORM action="forgotPassword.jsp" method="post">
    <INPUT type="hidden" name="userID" value="123">
    <!-- <INPUT type="submit" value="Forgot Password"> -->
</FORM>
```


Another source of clues about unreferenced directories is the */robots.txt* file used to provide instructions to web robots:

```
User-agent: *
Disallow: /Admin
Disallow: /uploads
Disallow: /backup
Disallow: /~jbloggs
Disallow: /include
```


##### Blind guessing

In its simplest form, this involves running a list of common file names through a request engine in an attempt to guess files and directories that exist on the server. The following netcat wrapper script will read a wordlist from stdin and perform a basic guessing attack:

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


Depending upon the server, GET may be replaced with HEAD for faster results. The output file specified can be grepped for “interesting” response codes. The response code 200 (OK) usually indicates that a valid resource has been found (provided the server does not deliver a custom “not found” page using the 200 code). But also look out for 301 (Moved), 302 (Found), 401 (Unauthorized), 403 (Forbidden) and 500 (Internal error), which may also indicate resources or directories that are worthy of further investigation.


The basic guessing attack should be run against the webroot, and also against all directories that have been identified through other enumeration techniques. More advanced/effective guessing attacks can be performed as follows:

* Identify the file extensions in use within known areas of the application (e.g. jsp, aspx, html), and use a basic wordlist appended with each of these extensions (or use a longer list of common extensions if resources permit).
* For each file identified through other enumeration techniques, create a custom wordlist derived from that filename. Get a list of common file extensions (including ~, bak, txt, src, dev, old, inc, orig, copy, tmp, etc.) and use each extension before, after, and instead of, the extension of the actual file name.


Note: Windows file copying operations generate file names prefixed with “Copy of “ or localized versions of this string, hence they do not change file extensions. While “Copy of ” files typically do not disclose source code when accessed, they might yield valuable information in case they cause errors when invoked.


##### Information obtained through server vulnerabilities and misconfiguration

The most obvious way in which a misconfigured server may disclose unreferenced pages is through directory listing. Request all enumerated directories to identify any which provide a directory listing.

Numerous vulnerabilities have been found in individual web servers which allow an attacker to enumerate unreferenced content, for example:

* Apache ?M=D directory listing vulnerability.
* Various IIS script source disclosure vulnerabilities.
* IIS WebDAV directory listing vulnerabilities.


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
