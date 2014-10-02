# HTTP严格传输安全测试 (OTG-CONFIG-007)


### 综述
HTTP严格传输安全（HTTP Strict Transport Security, HSTS）头是一项机制：在特定域名下，网站和浏览器之间通信必须都通过https传输。这有助于保护信息从非加密请求中泄露。


考虑这个安全措施的重要意义，测试的关键在于验证网站是否使用这个HTTP头，来确保所有数据都是从浏览器加密传输到服务器端的。


HTTP严格传输安全特征使得web应用能够通过使用特别的响应头告诉浏览器不要使用HTTP与特定服务器建立连接。相对的，所有访问请求都应该自动通过HTTPS建立连接。


HSTS头使用两个指令：
* max-age: 来指示浏览器应该自动转换所有HTTP请求为HTTPS的时间（秒）。
* includeSubDomains:  来指明所有web应用的子域名也必须使用HTTPS。


下面是一个HSTS头实现的例子：
```
 Strict-Transport-Security: max-age=60000; includeSubDomains
```

使用HSTS头的应用必须检查如下几个可能产生的问题：
* 攻击者可能嗅探网络浏览来访问未加密的信道获得信息。
* 攻击者利用中间人攻击手段，因为证书可能不可信任。
* 用户错误输入HTTP地址来替换HTTPS，或者用户点击了web应用中的错误使用HTTP协议的链接。


### 如何测试
可以使用劫持代理或者curl来测试HSTS头是否存在与服务器应答中，如下所示：
```
    $ curl -s -D- https://domain.com/ | grep Strict
```

期望结果：
```
    Strict-Transport-Security: max-age=...
```

### 参考资料
* OWASP HTTP Strict Transport Security - https://www.owasp.org/index.php/HTTP_Strict_Transport_Security
* OWASP Appsec Tutorial Series - Episode 4: Strict Transport Security - http://www.youtube.com/watch?v=zEV3HOuM_Vw
* HSTS Specification: http://tools.ietf.org/html/rfc6797
