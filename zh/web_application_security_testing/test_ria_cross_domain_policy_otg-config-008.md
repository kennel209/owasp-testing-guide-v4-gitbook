# 应用程序跨域策略测试 (OTG-CONFIG-008)


### 综述
富因特网应用程序（Rich Internet Applications, RIA）应该遵循Adobe的 crossdomian.xml 策略来控制跨域访问数据和使用服务，例如Oracle Java，Siverlight和Adobe Flash。因此，一个域名授予另一个不同域名远程访问自己的服务的能力。但是，这些策略文件中描述的访问控制被糟糕配置。糟糕的策略配置会导致跨站点伪造请求攻击（CSRF），也可能允许第三方机构访问只属于用户的敏感信息。


#### 什么是跨域策略文件？
一个跨域策略文件规定了一个web客户端如Java，Adobe Flash，Adobe Reader等访问不同域名站点数据的权限文件。对于Silverlight来说，微软采取接纳一部分crossdomain.xml配置，也额外创建了自己的跨域策略文件：clientaccesspolicy.xml文件。


当一个web客户端发现一个资源需要从另一个站点请求获得，他先查看目标站点的策略文件来决定是否进行跨域请求，包括http头和允许的基于socket的连接。


主策略文件位于域名的根目录下。一个客户端可能被指示读取一个不同的策略文件，但他总会先检查主策略文件来确保主策略文件允许读取请求的我策略文件。


##### Crossdomain.xml vs. Clientaccesspolicy.xml
许多应用程序支持 crossdomian.xml 文件。但是在Silverlight的例子中，他只接受被配置为允许任何域名站点访问的 crossdomain.xml 。为了更加精细控制Silverlight，必须使用 clientaccesspolicy.xml 文件。


策略文件可以授予如下几种控制权限：
* 可接受的策略文件（主策略文件可以禁止或限制特定策略文件）
* Sockets权限
* HTTP头权限
* HTTP/HTTPS 访问权限
* 基于密码学凭证，来允许访问


一个过度（滥用）的权限控制策略文件例子：
```
<?xml version="1.0"?>
<!DOCTYPE cross-domain-policy SYSTEM
"http://www.adobe.com/xml/dtds/cross-domain-policy.dtd">
<cross-domain-policy>
   <site-control permitted-cross-domain-policies="all"/>
   <allow-access-from domain="*" secure="false"/>
   <allow-http-request-headers-from domain="*" headers="*" secure="false"/>
</cross-domain-policy>
```


#### 跨域策略文件如何被滥用？
* 过度的跨域权限策略。
* 产生的服务器应答可能被当作跨域策略文件。
* 使用文件上传功能上传的文件可能被当作跨域策略文件。


#### 滥用跨域访问的影响
* 破坏CSRF防护措施。
* 读取限制的或被跨源（cross-origin）策略保护的数据。


### 如何测试
**测试应用策略文件弱点：**

为了测试RIA策略文件弱点，测试需要从应用程序根目录获得 crossdomain.xml 和 clientaccesspolicy.xml 策略文件，以及从每一个能够发现的目录。

举例说明，如果一个应用的URL是 http://www.owasp.org ，测试应该尝试下载 http://www.owasp.org/crossdomain.xml 和 http://www.owasp.org/clientaccesspolicy.xml 。 

在获取所有的策略文件之后，每个权限都应该检查是否遵循最低权限原则。请求应该从域名、端口或协议来做限制，过度的权限策略应该避免。存在“*”的策略应该被特别仔细检查。

例子：
```
<cross-domain-policy>
 <allow-access-from domain="*" />
</cross-domain-policy>
```


**期望结果：**<br>
* 一系列策略文件被发现。
* 策略中发现脆弱设置。


### 测试工具
* Nikto
* OWASP Zed Attack Proxy Project
* W3af


### 参考资料
**白皮书**<br>
* UCSD: "Analyzing the Crossdomain Policies of Flash Applications" - http://cseweb.ucsd.edu/~hovav/dist/crossdomain.pdf
* Adobe: "Cross-domain policy file specification" - http://www.adobe.com/devnet/articles/crossdomain_policy_file_spec.html
* Adobe: "Cross-domain policy file usage recommendations for Flash Player" - http://www.adobe.com/devnet/flashplayer/articles/cross_domain_policy.html
* Oracle: "Cross-Domain XML Support" - http://www.oracle.com/technetwork/java/javase/plugin2-142482.html#CROSSDOMAINXML
* MSDN: "Making a Service Available Across Domain Boundaries" - http://msdn.microsoft.com/en-us/library/cc197955(v=vs.95).aspx
* MSDN: "Network Security Access Restrictions in Silverlight" - http://msdn.microsoft.com/en-us/library/cc645032(v=vs.95).aspx
* Stefan Esser: "Poking new holes with Flash Crossdomain Policy Files" http://www.hardened-php.net/library/poking_new_holes_with_flash_crossdomain_policy_files.html
* Jeremiah Grossman: "Crossdomain.xml Invites Cross-site Mayhem" http://jeremiahgrossman.blogspot.com/2008/05/crossdomainxml-invites-cross-site.html
* Google Doctype: "Introduction to Flash security " - http://code.google.com/p/doctype-mirror/wiki/ArticleFlashSecurity
