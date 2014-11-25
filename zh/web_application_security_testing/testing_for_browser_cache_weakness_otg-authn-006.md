# 测试浏览器缓存脆弱点 (OTG-AUTHN-006)


### 综述
在这个阶段，测试者检查应用程序是否正确指导浏览器不记住敏感数据。


浏览器可能为了缓存机制和历史记录存储某些信息。缓存机制被用于提高性能，通过这个机制，上一次访问的信息可以不再需要下载一边。历史记录机制提供用户便捷功能，用户可以清楚看见他们下载的资源情况。如果有敏感信息被展示给用户（如地址信息、信用卡详细资料、社会安全码或用户名等等），那么这些信息有可能出于缓存或历史记录的目录被存储，如此也就能够通过简单使用“后退”按钮检查浏览器缓存获得。

### 如何测试

**浏览器历史记录**

从技术上来说，“后退”按钮原理是历史记录，而不是缓存（参见http://www.w3.org/Protocols/rfc2616/rfc2616-sec13.html#sec13.13）。缓存和历史记录是两样不同的东西。然后他们拥有共同的脆弱性，都能呈现上一个展示的敏感信息。


最先和最简单的测试包括向应用输入敏感信息，并登出。然后测试这点击“后退”按钮来检查浏览器是否能够访问了之前的敏感信息（在未认证状态）。


如果通过“后退”按钮，测试者能访问之前的页面，而不是新的页面，那么这就不是一个认证过程的问题，而是浏览器历史记录的问题。如果这些页面包含敏感数据，那么意味着应用不能禁止浏览器存储他们。


在这个测试中，通常不需要认证过程。例如，当用户输入他们的邮件地址来注册一个新邮件列表，这些信息不过没有正确处理，很有可能被离线获取。


“后退”按钮可以通过下面方法停在展示敏感数据：
* 通过HTTPS发布页面。
* 在HTTP响应头中设置 Cache-Control: must-re-validate


**浏览器缓存**

测试者在这里检测应用程序没有在浏览器缓存中泄露敏感数据。为了达到测试目的，测试者使用一个代理工具（比如WebScarab），然后搜索属于这个会话的服务器响应，检测每个可能包含敏感信息的页面，服务器是否指导浏览器不要缓存任何数据。如此的指示标记可以在HTTP响应头中发现：
* Cache-Control: no-cache, no-store
* Expires: 0
* Pragma: no-cache


这些指示符通常足够健壮，虽然一些额外的Cache-Control头标志可能会加入用来更好防止在文件系统中存储链接的文件。这些包括：
* Cache-Control: must-revalidate, pre-check=0, post-check=0, max-age=0, s-maxage=0

```
HTTP/1.1:
Cache-Control: no-cache
```

```
HTTP/1.0:
Pragma: no-cache
Expires: <past date or illegal value (e.g., 0)>
```


例如，假设测试者正测试一个电子金融应用系统，他们应该查看所有包含信用卡号码或其他金融信息的页面，并检查这些页面是否强制加入了 no-cache 指示符。如果找到的这些包含关键信息的页面并没有指导浏览器不缓存内容的信息，那么测试者就能了解这些敏感信息会被存储到磁盘上，他们就能简单从浏览器缓存中搜寻相关的页面来确认。


这些信息存储的确切地点依赖于客户端操作系统和他们使用的浏览器。这里有一些例子：

* Mozilla Firefox:
    - Unix/Linux: ~/.mozilla/firefox/<profile-id>/Cache/
    - Windows: C:\Documents and Settings\<user_name>\Local Settings\Application Data\Mozilla\Firefox\Profiles\<profile-id>\Cache

* Internet Explorer:
    - C:\Documents and Settings\<user_name>\Local Settings\Temporary Internet Files


### 灰盒测试
这个测试的方法与黑盒测试相同，在两种测试环境下，测试这都需要完全访问服务器响应头和HTML代码。然而，对于灰盒测试，测试者可能需要账户凭证来允许他们测试某些只有认证用户才能访问的敏感页面。

### 测试工具
* [OWASP Zed Attack Proxy](https://www.owasp.org/index.php/OWASP_Zed_Attack_Proxy_Project)
* Firefox 插件 [CacheViewer2](https://addons.mozilla.org/en-US/firefox/addon/cacheviewer2/?src=api)

### 参考资料
**白皮书**

* [Caching in HTTP](http://www.w3.org/Protocols/rfc2616/rfc2616-sec13.html)

