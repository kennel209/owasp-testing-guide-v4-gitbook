# 测试会话变量泄露 (OTG-SESS-004)


### 综述

会话令牌（cookie，会话ID，隐藏域），如果泄露，可能允许攻击者模仿受害者并非法访问系统。重要的是这些令牌应该无时无刻被保护，防止窃听，特别是在传输过程中。

这里的信息关注于对敏感的会话ID数据的传输安全更胜于通常的数据，可能在缓存和传输策略上更加严格。

使用个人代理，就有可能确认每个请求与响应：
* 使用的协议（如HTTP与HTTPS）
* HTTP头
* 消息主题（如POST或页面内容）

每当会话ID在客户端与服务器中传递的时候，协议、缓存、隐私指示符、和消息主体都应该检查。传输安全这里指的是通过GET或POST请求、消息主体或其他方法在合法的HTTP请求中传输会话ID。


### 如何测试

**测试会话令牌的加密和复用漏:**

防止窃听的的方法通常是提供SSL加密，但是可能无法和其他隧道或加密一起使用。应当注意的是加密或其他密码学散列算法处理会话ID应该考虑与传输加密分开，正如应该保护的是会话ID本身，而不是其中的数据。

如果会话ID能够被攻击者直接获得访问权限，那么他必须在传输中被保护来减轻风险。因此当会话ID传递时，应该确保加密措施在任何请求和响应中都是默认和强制执行的，无论是使用何种机制（如隐藏域）。简单的检查是https://用http://替代，同时修改表单来确定在安全和不安全的站点中是否有足够的隔离措施。

注意，如果站点存在用户使用会话ID追踪的一个元素，然而没有安全措施（如注册用户可下载的公开文件），有必要使用一个不同的会话ID。会话ID应该在客户端切换安全与非安全的元素时候被监控，来确保使用的不同的ID。


**期待结果:**

每次成功进行认证之后，用户应该期待能获取：
* 一个不同的会话令牌
* 发起HTTP请求时，令牌通过加密信道传输


**测试代理和缓存漏洞:**

在评估应用程序安全时，必须将代理考虑进去。在许多情况下，客户端可能通过公司、ISP、或其他代理或协议分析网关（如防火墙）访问应用程序。HTTP协议提供了控制下游代理行为的指示符，应该评估这些指示符被正确实现。

通常，会话ID不应该通过未加密信道发送，也不应该被缓存。应用程序必须检查并确保加密通信在传输任何会话ID时是默认和强制。更进一步，无论何时会话ID被传输，指示符也应该一同传输来防止中间缓存甚至本地缓存。

应用程序也应该被配置为确保在HTTP 1.0 和HTTP 1.1（RFC 2616）同样确保缓存数据安全。 HTTP 1.1 提供一系列的缓存控制措施。Cache-Control: no-cache 指示代理必须不复用任何数据。而 Cache-Control: Private 看上去是一个更加合适的指示符，允许不共享的代理缓存数据。在网吧或其他共享系统的情况中，显然这是一个风险点。甚至单用户工作机缓存的会话ID也可能通过文件系统或网络存储暴露给其他人。HTTP 1.0缓存无法识别Cache-Control: no-cache 指示符。

**期待结果:**

“Expires: 0” 和 Cache-Control: max-age=0 指示符应该被使用来进一步确保缓存不泄露数据。

每一个传输会话ID的请求/响应都应该检查是否含有正确的缓存指示符。

**测试GET和POST漏洞:**

通常，不应该使用GET请求，因为会话ID可能在代理或防火墙日志中泄露。而且与其他类型的传输相比，也更加非常容易操纵，尽管任何机制都可以在客户端用合适的工具来操纵。进一步来说，[跨站脚本 (XSS)](https://www.owasp.org/index.php/Cross-site_Scripting_%28XSS%29) 攻击最容易通过该方式发送构造的GET请求链接给受害者来利用。通过使用POST发送数据更加不容易发生。


**期待结果:**

所有服务器端使用POST接受数据的代码都应该被测试确保不能使用GET传输。

例如，考虑如下登陆页面的POST请求。

```
POST http://owaspapp.com/login.asp HTTP/1.1
Host: owaspapp.com
User-Agent: Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.0.2) Gecko/20030208 Netscape/7.02 Paros/3.0.2b
Accept: */*
Accept-Language: en-us, en
Accept-Charset: ISO-8859-1, utf-8;q=0.66, *;q=0.66
Keep-Alive: 300
Cookie: ASPSESSIONIDABCDEFG=ASKLJDLKJRELKHJG
Cache-Control: max-age=0
Content-Type: application/x-www-form-urlencoded
Content-Length: 34

Login=Username&password=Password&SessionID=12345678
```

如果login.asp没有很好实现，可能能通过如下URL进行登陆：

```
http://owaspapp.com/login.asp?Login=Username&password=Password&SessionID=12345678
```

能通过检查每一个POST请求来识别潜在的不完全服务器端脚本。

**测试传输漏洞:**

所有客户端和应用程序的交互至少要按以下标准进行测试：
* 会话ID是如何传输的？如，GET，POST，表单（包括隐藏域）
* 会话ID总是默认通过加密传输的么？
* 是否可能操纵应用程序不加密传输会话ID？如，通过将HTTPS改为HTTP？
* 在传输会话ID的请求/响应中使用了什么缓存控制指示符？
* 这些指示符总是存在么？如果不是，哪里有特例？
* 会话ID使用了GET请求了么？
* 如果使用POST，是否可以使用GET替代？


### 参考资料

**白皮书**

* RFCs 2109 & 2965 – HTTP State Management Mechanism [D. Kristol, L. Montulli] - http://www.ietf.org/rfc/rfc2965.txt, http://www.ietf.org/rfc/rfc2109.txt
* RFC 2616 – Hypertext Transfer Protocol -- HTTP/1.1 - http://www.ietf.org/rfc/rfc2616.txt

