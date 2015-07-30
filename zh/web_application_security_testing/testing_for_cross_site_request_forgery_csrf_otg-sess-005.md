# 跨站点请求伪造(CSRF)测试 (OTG-SESS-005)

### 综述

[CSRF](https://www.owasp.org/index.php/CSRF) 是一种强制最终用户在web应用认证的情况下执行操作的攻击。通过一些社会工程学技巧的帮助（比如通过电子邮件或聊天工具发送链接），攻击者能够让用户执行攻击者想要的操作。当面向普通用户时，一次成功的CSRF利用可以获取用户的数据。如果面向的用户时管理员账户的话，CSRF攻击能够攻破整个web应用系统。

CSRF依赖于下面条件：

1. Web浏览器支持会话相关的功能（如cookies和http认证信息）；
2. 攻击者知道合法的web应用url；
3. 应用程序进行会话管理所需要的信息，浏览器已经获得；
4. 直接进行HTTP/HTTPS资源访问的HTML标签，（如图像标签， *img* ）。

上述条件1、2、3必须满足才能导致漏洞存在，条件4时在实际利用过程中需要的附加条件，并不一定需要。

* 条件点 1) 浏览器自动发送鉴别用户会话的信息。假设 *site* 是一个web应用程序的站点，用户 *victim* 刚刚向 *site* 认证了自己。在响应中，*site* 给 *victim* 分配了标示认证会话的cookie。通常，一旦浏览器接受了 *site* 设置的cookie，就会自动在之后的所有指向 *site* 请求中发送该cookie。

* 条件点 2) 如果应用程序不在URL中加入会话相关的信息，那么意味着该应用URL，参数和其合法值可以识别出来（通过代码分析，或者通过访问，记录HTML/javascript中的表单和URL连接请求获得）。

* 条件点 3) “浏览器已知”指如cookie信息或基于http的认证信息（如http基础认证，不是表单形式的认证）已经存储在浏览器中，并在随后的请求中会进行再次发送的情况。下面所讨论的漏洞需要依赖这种仅通过这些已知信息就能的鉴别用户会话的情况。

为了化简情况，我们假设使用使用GET请求的URL（这些讨论情况也适用于POST请求情形）。如果 *victim* 已经进行认证，之后的请求就会自动带上认证的cookie（如图）。

![Image: session_riding.GIF](https://www.owasp.org/images/f/f3/Session_riding.GIF)


GET请求可以通过多种方法触发：

* 通过用户真实使用该web应用；
* 通过用户直接在浏览器上输入URL；
* 通过用户跟随URL链接（在应用程序之外）。

这些调用方法不能被应用程序识别。特别的，第三方的程序可能十分危险。有多种技巧（和漏洞）来区分链接的真实属性。链接可能嵌入电子邮件信息中，或者在引诱用户的恶意站点中（即链接出现在其他主机之中（其他web站点，HTML电子邮件信息等等））。如果用户点击了这些链接，因为该用户已经在 *site* 中认证过，浏览器会向改应用发出GET请求，伴随认证信息（会话cookie）。这可能导致在应用程序中执行了一个用户不希望的合法请求。比如在web银行中进行转账的恶意链接。

通过使用 *img* 标签，如同条件点4中描述的，甚至可能不需要用户去访问特定的链接。假设攻击者给用户发送了一封访问某个页面的电子邮件，下面是（简化后）的HTML文件：

```
<html><body>

...

<img src=”https://www.company.example/action” width=”0” height=”0”>

...

</body></html>
```

浏览器会展示该页面，并尝试显示特定的0宽度（即隐藏）图片。这导致一个自动发送给web应用的链接。图像URL是否是真的图片并不重要，img标签存在就会触发 *src* 中的特定请求。这意味着浏览器不会阻止图片下载，在默认配置中如果禁用图片功能会导致绝大多数的应用程序无法使用。

这个问题是下面一系列过程的结果：

* 网页结果中存在HTML标签自动执行了HTTP请求操作（ *img* 标签是其中之一）；
* 浏览器无法分辨出 *img* 标签请求的资源是否是真实图片，也无法分辨出其是否合法；
* 图片加载过程不考虑位置，即图片和表单自身不需要位于相同的主机之中，甚至不需要在同一个域名之下。虽然这是一个很有用的功能，但是他使得区分应用变的十分困难。

事实上，与web应用无关的HTML内容可能指向应用中的一些其他组件，浏览器也会自动向应用发有效请求，这导致了这种攻击产生。由于现在没有相关标准的制定，导致无法禁止这种行为，除非使攻击者无法辨认出有效应用URL。这意味着有效URL必须包含用户会话相关信息，不可能被攻击者预先知道，也就无法识别出这种URL。

情况可能更加糟糕，因为在整合了的邮件/浏览器环境下，简单展示包含图片的电子邮件消息就会导致通过相关cookie发起的应用程序请求。

问题可能通过混淆来更进一步，如通过指向看似合法图片URL的情况：
```
 <img src=”https://[attacker]/picture.gif” width=”0” height=”0”>
```
其中 [attacker] 是一个攻击者控制的站点，然后通过利用重定向的机制来指向第三方应用。
```
 http://[attacker]/picture.gif 重定向到 http://[thirdparty]/action.
```

利用cookie不是这种漏洞采用的唯一方法。只要能完全通过浏览器提供的会话信息进行操作的web应用就存在漏洞。这包括那些仅依赖于HTTP认证机制的应用，因为浏览器获得认证信息之后就会自动在每个请求中加入该信息。这 **不包括** 哪些基于表单的认证，这些认证只发生一次，并产生了一些会话相关信息（当然，在这个例子中，这样的信息简单通过cookie传递，也能够转化为之前的案例）。

**案例场景**

我们假设受害者登录了防火墙的web管理应用。为了进行登录，用户必须进行认证，会话信息保存在cookie中。

再假设防火墙web管理应用存在一个允许认证用户通过编号删除部分规则或者通过输入‘*’删除所有规则的功能（非常危险的功能，但是这让这个案例变得更加有趣）。下面展示了删除的页面URL。我们为了简化情况，假设通过GET请求进行操作：
```
 https://[target]/fwmgt/delete?rule=1
```
（来删除指定规则）
```
 https://[target]/fwmgt/delete?rule=*
```
（来删除所有规则）

这个例子非常简单，但是也展示了CSRF漏洞的危险之处。

![Image: Session Riding Firewall Management.gif](https://www.owasp.org/images/c/ca/Session_Riding_Firewall_Management.gif)

因此，如果我们输入‘*’，并点击删除按钮，将会发起下列请求。
```
 https://www.company.example/fwmgt/delete?rule=*
```
这将删除所有的防火墙规则（导致不正常的情况发生）。

![Image: Session Riding Firewall Management 2.gif](https://www.owasp.org/images/f/f8/Session_Riding_Firewall_Management_2.gif)

这不是唯一的场景，用户可能通过提交URL请求来得到同样的结果：
```
 https://[target]/fwmgt/delete?rule=*
```

或者点击相关的链接，直接或者通过跳转到上述URL地址。再或者通过嵌入指向相同链接的 *img* 标签也可以。

在所有的情况中，如果用户当前已登录防火墙管理应用，那么这些请求将正常执行，并成功修改了防火墙的配置。可以想象将攻击目标置于敏感的应用程序上，进行自动化的下单、资金转账、订单操作、关键组件配置修改等等情况。

有意思的是，这些漏洞可以在防火墙里面进行，即这些攻击链接受害者有权访问即可（不能直接被攻击者访问）。特别的，可以是任何内部web服务器；例如上文提及的防火墙管理站点就可能没有暴露在互联网中。想象一个针对核反应堆监视应用的CSRF攻击。想得太多了？也许，但是也不是不可能的情况。

那些自身包含漏洞的应用，即同时作为攻击向量和目标的应用（如web邮件应用），使得情况更加糟糕。如果应用程序存在漏洞，用户必定在登录后读取包含CSRF攻击的消息，该攻击致力于web邮件应用本身，执行如删除消息、作为该用户发送消息等操作。


### 如何测试

#### 黑盒测试

在黑盒测试中，攻击者必须知道在限制（认证）区域的URL地址。如果测试人员拥有有效登录信息，那么可以扮演双重角色－攻击者和受害者。在这种情况下，测试人员可以通过浏览应用获得相关URL地址。

相对的，如果测试人员没有有效登录凭证，就不得不组织一次真实的攻击，劝诱一个合法的登录后的用户来访问大致的链接。这需要一系列的社会工程学的技巧。

无论哪种方法，测试用例可以根据如下情况来设计：

* 将 *u* 作为测试URL，如，｀u = http://www.example.com/action`
* 建立一个包含请求URL u的html页面（特别是所有相关的参数；在HTTP GET请求的情况下很自然，如果通过POST请求则需要使用一系列的Javascript脚本）；
* 确保合法用户已经登录应用；
* 引诱合法用户访问测试URL（如果无法进行模仿，可能需要社会工程学技巧）；
* 观察结果，如检查web服务器是否执行了相关请求。


#### 灰盒测试

对应用程序进行审计检查其会话管理过程是否存在漏洞。如果会话管理只依赖客户端的数据（浏览器可获得的信息），那么应用程序就是存在漏洞的。“客户端数据”意味着cookie或HTTP认证凭证（基本认证和其他形式的HTTP认证；非基于表单的认证，这是一个应用层的认证）。如果应用程序不存在漏洞，该应用必须在URL中包含会话相关的信息，无法被用户辨别或预测出。（[3] 使用了术语 *秘密* 来表示这种信息）。

能通过HTTP GET请求访问的资源很容易存在漏洞，POST请求也能通过Javascript自动化提交产生漏洞；因此，通过单独使用POST请求不足以消除CSRF漏洞。


### 测试工具

* WebScarab Spider http://www.owasp.org/index.php/Category:OWASP_WebScarab_Project
* CSRF Tester http://www.owasp.org/index.php/Category:OWASP_CSRFTester_Project
* Cross Site Requester http://yehg.net/lab/pr0js/pentest/cross_site_request_forgery.php (via img)
* Cross Frame Loader http://yehg.net/lab/pr0js/pentest/cross_site_framing.php (via iframe)
* Pinata-csrf-tool http://code.google.com/p/pinata-csrf-tool/


### 参考资料

**白皮书**

* Peter W: "Cross-Site Request Forgeries" - http://www.tux.org/~peterw/csrf.txt
* Thomas Schreiber: "Session Riding" - http://www.securenet.de/papers/Session_Riding.pdf
* Oldest known post - http://www.zope.org/Members/jim/ZopeSecurity/ClientSideTrojan
* Cross-site Request Forgery FAQ - http://www.cgisecurity.com/articles/csrf-faq.shtml
* A Most-Neglected Fact About Cross Site Request Forgery (CSRF) - [http://yehg.net/lab/pr0js/view.php/A_Most-Neglected_Fact_About_CSRF.pdf ](http://yehg.net/lab/pr0js/view.php/A_Most-Neglected_Fact_About_CSRF.pdf)

### 整改措施

下面的对抗措施分为用户和开发者两部分。

**用户**

由于CSRF漏洞被广泛报告，推荐根据下面的实践过程来减少风险。一些可能的措施有：

* 在完成操作后立即登出系统。
* 不允许浏览器保存用户名/密码，也不允许站点“记住”登录情况。
* 不使用同一个浏览器访问敏感应用和随意浏览互联网；如果需要在同一台机器中同时进行，使用不同的浏览器来浏览。

整合HTML页面功能的邮件浏览器，新闻组浏览器增加了更多的风险，通过简单访问邮件消息和新闻消息可能导致攻击发生。


**开发者**

在URL中加入会话相关的信息。导致攻击发生的关键在于cookie中的唯一会话标示会随着请求一同发送。通过URL层面产生的其他会话相关信息可以使攻击者更加难以了解URL的结构。

下面是一些其他对抗措施，可能不能解决所有问题，但是可以使漏洞利用变的更加困难：

* 使用POST替代GET请求。虽然POST也能通过Javascript方式模拟发送，他将提高攻击的复杂度。
* 使用确认页面也一样（如“你确定要进行这项操作？”等等）。他们也可能被攻击者绕过，也会提高攻击复杂度。因此不要完全依赖这些手段来保护应用程序。
* 自动登出机制一定程度能缓解此类漏洞，但是最终还是取决于环境（用户可能需要一整天来进行有漏洞的web银行应用操作，这往往比偶尔使用这功能的用户有更多的风险）。


### 相关安全活动

#### CSRF漏洞描述

参见OWASP文章 [CSRF](https://www.owasp.org/index.php/CSRF) 。

#### 如何避免CSRF漏洞

参见 [OWASP 开发指南](https://www.owasp.org/index.php/Category:OWASP_Guide_Project) 中如何避免CSRF漏洞部分。

#### 如何审查代码中的CSRF漏洞

参见 [OWASP 代码评估指南](https://www.owasp.org/index.php/Category:OWASP_Code_Review_Project)  中关于如何[审查代码查询CSRF](https://www.owasp.org/index.php/Reviewing_code_for_Cross-Site_Request_Forgery_issues) 部分。

#### 如何防御CSRF漏洞

参见 [OWASP CSRF 防护速查表](http://www.owasp.org/index.php/Cross-Site_Request_Forgery_%28CSRF%29_Prevention_Cheat_Sheet)。
