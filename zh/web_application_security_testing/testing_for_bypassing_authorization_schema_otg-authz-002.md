# 测试授权绕过 (OTG-AUTHZ-002)


### 综述
这类测试注重于验证每个角色或访问限制文件的特权的授权模式是否良好实现。


对于评估中测试者拥有的每个不同角色，每个功能函数和应用在完成认证环节后的请求，都需要被验证：
* 未认证用户是否可以访问资源？
* 登出后是否可以访问资源？
* 不同角色或权限的用户是否可以访问功能函数和资源？


尝试用管理员用户来访问应用并追踪记录所有的管理功能。
* 普通权限用户是否可以访问管理功能？
* 那些拥有不同权限的用户是否可以使用管理功能（没有该权限）？


### 如何测试
**测试访问管理功能**

例如，假设'AddUser.jsp'功能是应用管理功能的一部分，而且他可以通过请求下列URL来访问：
```
  https://www.example.com/admin/addUser.jsp
```

然后，下列HTTP请求在调用AddUser功能函数时候被生产：
```
POST /admin/addUser.jsp HTTP/1.1
Host: www.example.com
[other HTTP headers]

userID=fakeuser&role=3&group=grp001
```

如果一个非管理员用户尝试执行这个请求会发生什么事情？新用户能被创建么？如果能，新用户能否使用管理员特权？


**测试访问不同角色的资源**

例如，应用程序使用一个共享目录来为不同的用户存储临时的PDF文件。假设documentABC.pdf应该仅能够被roleA角色的用户test1访问，验证如果角色roleB的用户test2能否访问这个资源。
<br><br>

### 测试工具
* OWASP WebScarab: [OWASP WebScarab Project](https://www.owasp.org/index.php/OWASP_WebScarab_Project)<br>
* [OWASP Zed Attack Proxy (ZAP)](https://www.owasp.org/index.php/OWASP_Zed_Attack_Proxy_Project)

