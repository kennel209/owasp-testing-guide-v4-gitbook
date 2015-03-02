# 测试Cookies属性 (OTG-SESS-002)

### 综述
Cookie通常是恶意用户的重点攻击向量，应用程序需要尽力保护cookie。本章节注重于应用程序如何在分配cookie时采取必需的保护措施，以及如何测试这些属性被正确配置。

安全使用Cookie的重要性常常不被理解，特别是在动态应用程序中，往往需要在如HTTP之类的无状态协议中维持一定的状态。为了理解cookie的重要性，首先必须理解他们的主要用途是什么。这些主要功能通常包括会话授权和认证令牌或者临时的数据容器。因此，如果攻击者获得了一个会话令牌（比如，通过跨站脚本漏洞或在未加密会话中嗅探），那么他们就能使用这些cookie劫持一个合法的会话。

此外，cookie也用于在多个请求中维持状态。由于HTTP是无状态的，服务器在缺少某种鉴别标识时不能确定一个请求是当前会话的一部分或者是其他新的会话的开始。这些标识符通常就是cookie，其他方法也有可能。许多不同类型的应用程序需要在多个请求中维持会话状态。在线商店就是其中一种应用。用户添加多个商品进入购物车，这些数据必须在之后的请求中也使用到。cookie在这个场景下通常被采用，通过应用程序使用Set-Cookie指示符来设定，通常是 名字=内容 的形式（如果启用了cookie，并被支持，通常被所有的现代浏览器支持）。一旦应用程序告诉浏览器使用特定的cookie，浏览器就会在随后的请求中都带上该cookie。cookie能包含的数据可能是在线购物车的商品、价格、数量、个人信息、用户ID等等。

取决于cookie的敏感属性，他们通常被编码或加密来包含其中的数据。通常多个cookie会在请求中设置（通过分号分隔）。比如在在线商店的例子中，当用户添加多个商品到购物车时候，一个新的cookie可能被设置。此外，通常当用户登录时也有一个cookie用于认证（比如前文的会话令牌），以及多个其他的cookie用于鉴别用户希望购买的商品和他们的辅助信息（如价格、数量）。

一旦测试这理解cookie如何被设置，何时被设置，其用途是什么，为什么使用，以及其重要程度，那么测试者应该查看这些cookie设置了什么属性，以及如何测试他们的安全性。下面是一系列每个cookie能够被设置的属性以及其意义。下一章节会关注如何测试每个属性。

* secure - 这个属性告诉浏览器该cookie只能通过安全的信道传输，如HTTPS。这将有助于防止从未加密信道进行请求传输。如果应用程序可以通过HTTP和HTTPS访问，那么cookie可能被明文发送。

* HttpOnly - 这个属性被用于防止跨站脚本等攻击，因为他不允许通过客户端脚本如JavaScript获取Cookie。值得注意，不是所有的浏览器支持这项功能。

* domain -  这个属性用于比较服务器请求的URL域名。如果该域名符合设置的domain或者是其子域，那么再检查path属性。

    注意只有特定域名的主机才能设置cookie的domain属性。domain属性也不能是顶级域名（如.gov或.com）来防止为其他域设置任意属性。如果domain属性没有设置，那么产生cookie的服务器域名被用于作为默认domain属性。

    举例说明，如果cookie在app.mydomain.com中设置，并且没有domian属性，那么cookie会在所有接下来的app.mydomain.com以及其子域（如hacker.app.mydomain.com）中提交，但不会在ptherapp.mydomain.com中出现。如果开发者希望宽松限制，那么他们应该将该domain属性设置为mydomain.com。在这个例子中，cookie能被发送到app.mydomain.com和其子域名，如hacker.app.mydomain.com，甚至是bank.mydomain.com。如果一个在子域上的漏洞服务器（如otherapp.mydomain.com），且domian属性过于宽松（如mydomain.com），那么漏洞服务器可以用来获取cookie（比如会话令牌）。


* path - domain属性的额外部分，判断特定路径的合法URL。如果域名和路径都符合，请求中会附上该cookie。如同domain属性一样，如果path属性也过于宽松，可能导致相同服务器的其他应用程序获取该cookie的漏洞。比如，如果path属性被设置为服务器根目录 “/”，那么应用程序cookie可以在相同域名下的所有路径中发送。

* expires - 这个属性用于设置持久性的cookie，cookie在设置日期前不会过期。持久化的cookie被用于浏览器会话和随后的会话，直到过期为止。一旦过期，浏览器会删除这个cookie。相对的，如果这个属性没有被设置，那么这个cookie仅仅在当前浏览器会话生命周期内才有效，当会话结束后将被删除。

### 如何测试

#### 黑盒测试
**如何测试cookie属性漏洞:** 

通过使用中间代理软件或流量劫持插件，捕获所有设置cookie的浏览器响应（使用Set-cookie指示符），检查下面的属性：

* Secure 属性 - 当cookie包含敏感信息，或者是一个会话令牌的时候，他必须总是通过加密信道进行传输。例如，在应用程序登陆后，通过cookie设置了一个会话令牌，接着验证是否标记了“;secure”标志。如果没有这个标志，浏览器会将他通过不加密的信道，如HTTP，进行传输，可能导致攻击者获得用户提交的cookie。

* HttpOnly 属性 - 这个属性应该总是存在，即使不是所有浏览器都支持。他阻止cookie被客户端脚本获得，虽然不能消除跨站脚本风险但可以消除一些攻击向量。检查是否存在“;HttpOnly”标识。

* Domain 属性 - 验证domain属性没有被设置过分宽松。正如上面提到的，应该仅仅设置为服务器需要接收cookie的域名。比如，app.mysite.com应该设置为"; domain=app.mysite.com" 而不是 "; domain=.mysite.com" ，因为这会允许潜在漏洞服务器获得cookie。

* Path 属性 - 验证path属性也没有设置过分宽松，如domain属性一样。甚至如果Domain属性被设置非常严格，path属性却是"/"根目录，那么可能被服务器上部分低安全的应用程序发现漏洞。例如，应用程序部署在"/myapp/"，验证path被设置为"; path=/myapp/" 而不是 "; path=/" 或者 "; path=/myapp"。注意，尾斜杠"/"必须使用，否则，浏览器会将cookie发送给任何匹配"myapp"，比如"myapp-exploited"。

* Expires 属性 - 如果这个属性被设置为未来的时刻，验证cookie是否包含任何敏感信息。例如，如果cookie设置为"; expires=Sun, 31-Jul-2016 13:45:29 GMT"而现在是2014年7月31日，那么测试者应该检查这个cookie。如果cookie是会话令牌，并存储在用户磁盘中，攻击者或者是本地用户（比如管理员）就能读取这个cookie，并在过期日期使用这个令牌来访问应用系统。


### 测试工具

**代理工具:**

* **[OWASP Zed Attack Proxy Project](https://www.owasp.org/index.php/OWASP_Zed_Attack_Proxy_Project)**

**浏览器插件:**

* "TamperIE" for Internet Explorer -
http://www.bayden.com/TamperIE/

* Adam Judson: "Tamper Data" for Firefox -
https://addons.mozilla.org/en-US/firefox/addon/966


### 参考资料
**白皮书**

* RFC 2965 - HTTP State Management Mechanism - http://tools.ietf.org/html/rfc2965

* RFC 2616 – Hypertext Transfer Protocol – HTTP 1.1 - http://tools.ietf.org/html/rfc2616

* The important "expires" attribute of Set-Cookie http://seckb.yehg.net/2012/02/important-expires-attribute-of-set.html

* HttpOnly Session ID in URL and Page Body http://seckb.yehg.net/2012/06/httponly-session-id-in-url-and-page.html

