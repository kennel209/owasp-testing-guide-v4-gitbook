# 测试JavaScript脚本执行 (OTG-CLIENT-002)


### 综述

JavaScript注入漏洞是跨站脚本（XSS）的一个子类，需要在受害者浏览器执行注入任意JavaScript代码的能力。这个漏洞可能产生许多问题，像是用户会话cookie暴露可以被用于模仿受害者，或者，更加普通的，他允许攻击者修改受害者能看到的页面内容或者应用程序行为。


### 如何测试

这样的漏洞发生在应用程序缺乏正确用户输入和输出验证。JavaScript用于动态更新web页面，这个注入发生在页面处理阶段，接着影响受害者。

当尝试利用这种问题，考虑一些被不同浏览器不同对待的特殊字符。参见参考资料中的DOM XSS维基。

下面的脚本没有对变量rr的验证过程，rr变量通过查询字符串来得到用户提供的输入，而且没有任何编码：

```
var rr = location.search.substring(1);
if(rr)
  window.location=decodeURIComponent(rr);
```

这表示攻击者能够通过如下查询字符串注入JavaScript：

```
www.victim.com/?javascript:alert(1)
```


#### 黑盒测试

JavaScript执行测试通常不进行黑盒测试，因为需要客户端执行注入的代码，而且源代码总是可以获得的。

#### 灰盒测试

**测试JavaScript脚本执行漏洞:**

例如，查看下面URL：

```
http://www.domxss.com/domxss/01_Basics/04_eval.html
```

这个页面包含下面的脚本：

```
<script>
function loadObj(){
 var cc=eval('('+aMess+')');
 document.getElementById('mess').textContent=cc.message;
}

if(window.location.hash.indexOf('message')==-1)
  var aMess="({\"message\":\"Hello User!\"})";
else
  var aMess=location.hash.substr(window.location.hash.indexOf('message=')+8);
</script>
```

上面的脚本包含 '`location.hash`' ，而且可以被攻击者控制，在 '`message`' 值注入 JavaScript 代码来控制用户浏览器。


### 参考资料

**OWASP 资源**

* [DOM based XSS Prevention Cheat Sheet](https://www.owasp.org/index.php/DOM_based_XSS_Prevention_Cheat_Sheet)
* DOMXSS.com - http://www.domxss.com

**白皮书**

* Browser location/document URI/URL Sources - https://code.google.com/p/domxsswiki/wiki/LocationSources
    - i.e., what is returned when the user asks the browser for things like document.URL, document.baseURI, location, location.href, etc.

