# 审查网页注释和元数据发现信息泄露 (OTG-INFO-005)


### 综述

在源代码中加入详细的注释和元数据非常常见，甚至是推荐行为。但是包含在HTML代码中的这些注释往往会揭露一些内部信息，这些信息本来不应该被潜在攻击者所查阅到。注释和元数据应该被审核来确定是否有信息泄露。


### 测试目标

审核页面注释和元数据来更了解应用情况和发现信息泄露。


### 如何测试

HTML注释常用于开发者进行应用调试。有时候他们忘了了注释这件事，并将他们留到了发布环境中。测试者应该查看以`<!--`开始,以`-->`结束的HTML注释。


#### 黑盒测试

检查HTML源代码中的注释获得敏感信息能更好的帮助攻击者加深对应用的理解。这些信息可能是SQL语句，用户名和密码，内部IP地址或者调试信息。

```
...

<div class="table2">
  <div class="col1">1</div><div class="col2">Mary</div>
  <div class="col1">2</div><div class="col2">Peter</div>
  <div class="col1">3</div><div class="col2">Joe</div>

<!-- Query: SELECT id, name FROM app.users WHERE active='1' -->

</div>
...
```


测试者甚至能发现下面这些信息：
```
<!-- Use the DB administrator password for testing:  f@keP@a$$w0rD -->
```


检查HTML版本信息来发现合法版本信息和数据类型定义（DTD）链接
```
 <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
```

* "strict.dtd" -- 默认严格的 DTD
* "loose.dtd" -- 宽松的 DTD
* "frameset.dtd" -- 框架页面的 DTD


有些元标签不能提供主动的攻击向量，但是允许攻击者获得档案信息
```
 <META name="Author" content="Andrew Muller">
```

有些元标签改变了HTTP回应头，比如 http-equiv 设置了基于页面属性的HTTP响应头，如下所示：
```
 <META http-equiv="Expires" content="Fri, 21 Dec 2012 12:34:56 GMT">
```

这会导致 HTTP 头加入如下信息：
```
 Expires: Fri, 21 Dec 2012 12:34:56 GMT
```

又如：
```
 <META http-equiv="Cache-Control" content="no-cache">
```

会产生下面结果：
```
 Cache-Control: no-cache
```

当测试页面是否执行注入漏洞时（比如CRLF攻击），这些元标签也能通过浏览器缓存来帮助决定信息泄露程度。

一个常见（但不是Web内容无障碍指南（WCAG）兼容版本）元标签就是刷新：
```
 <META http-equiv="Refresh" content="15;URL=https://www.owasp.org/index.html">
```

另一个常见元标签的使用是指定关键字给搜索引擎提高搜索结果的质量：
```
 <META name="keywords" lang="en-us" content="OWASP, security, sunshine, lollipops">
```

尽管大多数web服务器通过robots.txt来管理搜索引擎索引范围，但是也能通过元标签管理。这些标签会建议机器人不要索引和跟踪页面链接：
```
 <META name="robots" content="none">
```

因特网内容选择平台 （Platform for Internet Content Selection PICS） 和 网站描述资源协议（Protocol for Web Description Resources POWDER） 提供元数据如何关联因特网页面内容的基础内容。


#### 灰盒测试
不适用。


### 测试工具

* Wget
* Browser "view source" function
* Eyeballs
* Curl


### 参考资料
**白皮书**

[1] http://www.w3.org/TR/1999/REC-html401-19991224 HTML version 4.01

[2] http://www.w3.org/TR/2010/REC-xhtml-basic-20101123/ XHTML (for small devices)

[3] http://www.w3.org/TR/html5/ HTML version 5
