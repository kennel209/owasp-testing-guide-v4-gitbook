# 测试HTML代码注入 (OTG-CLIENT-003)


### 综述

HTML注入是一种发生在用户可以控制输入点，并且向有漏洞的网页可以注入任意HTML代码的注入漏洞。这个漏洞能导致很多后果，比如用户会话ID暴露导致的身份模仿问题，或者，更加普通的，他允许攻击者修改用户看到的页面内容。

### 如何测试

当用户输入没有正确审查而输出没有被编码的情况下，漏洞就会发生。注入攻击使攻击者能够发送恶意HTML页面给受害者。目标浏览器无法分辨页面内容是否有恶意，后果就是解析并执行所有内容。

有大量的方法和属性可以用来渲染HTML内容。如果这些方法由不可信的输入提供，那么就有很大的几率导致XSS风险，特别是HTML注入。比如恶意的HTML代码可以通过innerHTML进行注入，这被用于渲染用户插入的HTML代码。如果字符串没有正确审查，这个问题就会导致基于HTML注入的XSS。另一个方法可能是document.write()。

当尝试进行此类问题的利用时候，考虑一些被不同浏览器不同对待的特殊字符。参见参考资料中的DOM XSS维基。

innerHTML属性设置了内部HTML元素。不正确使用这个特性，也就是对不可信输入缺少审查措施，而且对输出未进行编码，就允许攻击者注入恶意的HTML代码。

**漏洞代码例子：**

下面例子展示了一小段漏洞代码，允许未验证的输入在页面动态创建HTML：

```
var userposition=location.href.indexOf("user=");
var user=location.href.substring(userposition+5);
document.getElementById("Welcome").innerHTML=" Hello, "+user;
```

同样的，下面的例子展示了使用document.write()功能的漏洞代码：

```
var userposition=location.href.indexOf("user=");
var user=location.href.substring(userposition+5);
document.write("<h1>Hello, " + user +"</h1>");
```

在这两个例子中，使用如下输入：

```
 http://vulnerable.site/page.html?user=<img%20src='aaa'%20onerror=alert(1)>
```

就可以向HTML上下文中注入执行任意JavaScript代码的恶意图片标签。

#### 黑盒测试

HTML注入通常不进行黑盒测试，因为需要客户端执行注入的代码，而且源代码总是可以获得的。

#### 灰盒测试

**测试HTML注入漏洞：**

例如，在下面的URL例子中：

```
 http://www.domxss.com/domxss/01_Basics/06_jquery_old_html.html
```

HTML代码包括如下脚本：

```
<script src="../js/jquery-1.7.1.js"></script>
<script>
function setMessage(){
 var t=location.hash.slice(1);
 $("div[id="+t+"]").text("The DOM is now loaded and can be manipulated.");
}
$(document).ready(setMessage  );
$(window).bind("hashchange",setMessage)
</script>
<body><script src="../js/embed.js"></script>
<span><a href="#message" > Show Here</a><div id="message">Showing Message1</div></span>
<span><a href="#message1" > Show Here</a><div id="message1">Showing Message2</div>
<span><a href="#message2" > Show Here</a><div id="message2">Showing Message3</div>
</body>
```

这里就能够注入HTML代码。

### 参考资料

**OWASP 资源**

* [DOM based XSS Prevention Cheat Sheet](https://www.owasp.org/index.php/DOM_based_XSS_Prevention_Cheat_Sheet)
* DOMXSS.com - http://www.domxss.com

**白皮书**

* Browser location/document URI/URL Sources - https://code.google.com/p/domxsswiki/wiki/LocationSources
    - i.e., what is returned when the user asks the browser for things like document.URL, document.baseURI, location, location.href, etc.

