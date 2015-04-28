# 测试脆弱的SSL/TLS加密算法，不充分的传输层保护 (OTG-CRYPST-001)


### 综述

敏感数据通过网络传输必须被保护。这样的数据包括用户凭证信息和信用卡号码。一般来说，如果数据在存储时候必须被保护，那么在传输过程中也必须被保护。

HTTP是一个明文的协议，他需要通过SSL/TLS隧道转换成HTTPS流量来保证安全。使用这些协议不仅仅保证秘密性，同时也是一个认证过程。服务器可以使用数字证书进行认证，也允许使用客户端证书进行双向认证。

甚至是现在使用的高级芯片，一些服务器端的错误配置可能被利用来强制使用一些弱的加密算法（甚至糟糕到没有加密），允许攻击者获得这个看上去安全的通信信道的访问能力。其他错误配置可能被用于发起拒绝服务攻击。

### 常见问题

一个常见的漏洞是使用HTTP协议发送敏感信息[2]（比如通过HTTP传输登陆口令[3]）。

当SSL/TLS服务正常工作时候，这是好事，但他也增加了攻击面，可能存在下列漏洞：
* SSL/TLS协议、加密算法、密钥和协商过程必须正确配置。
* 必须确保证书有效。

其他相关的注意点有：
* 必须更新可能存在已知漏洞的软件[4]。
* 为会话Cookies使用Secure标志[5]。
* 使用HTTP严格传输安全（HSTS）头[6]。
* 同时存在HTTP和HTTPS，可能能截获流量[7],[8]。
* 同一个页面混合HTTPS和HTTP内容，可能导致信息泄露。


#### 明文传输敏感信息

应用程序不应该通过非加密信道传输敏感信息。通常能找到那些基于HTTP的基本认证过程，通过HTTP传输密码或会话cookie，和一些规定、法律或组织策略要求的信息。


#### 弱SSL/TLS密码算法/协议/密钥

在历史上，美国政府曾经颁布限制条款只允许出口的密码系统最多使用40位加密密钥，这个密钥长度是严重不足的，允许通信被解密。从那以后，出口规定已经被放宽到最大加密密钥为128位。

检查SSL配置避免使用那些已经轻易能够破解的密码算法是非常重要的。为了达到这个目的，基于SSL的服务不应该提供选择弱加密算法套件的选项。一个密码套件是指加密协议（如DES，RC4，AES），加密密钥长度（如40，56，或者128位），以及一个用于完整性检查的哈希算法（如SHA，MD5）。

简单来说，密码套件选择的关键取决于下面这些内容：
1. 客户端发送给服务器ClientHello消息中（与其他信息一起）规定了协议信息和能够处理的密码套件信息。注意客户端通常是一个web浏览器（现在最常见的SSL客户端），但是这不是必须的，客户端可以是任何支持SSL的应用程序；服务器端也是如此，不一定是web服务器，虽然大部分情况是web服务器[9]。
2. 服务器通过ServerHello消息进行响应，包含已选择的协议和本次会话使用的密码套件（通常服务器选择客户端与服务端共同支持的强度最大的协议和密码套件）。能通过配置指示服务器支持的密码套组，通过这个方法可以控制是否与只支持40位加密的客户端进行通信。


#### SSL证书有效性 - 客户端和服务端

当通过HTTPS协议访问web应用程序时候，服务端和客户端建立起来一条安全的通信通道。通过数字证书的方法确认一端的身份（服务端）或双方的身份（服务端和客户端）。因此，一旦加密算法套件确定了，SSL握手过程接下来做的工作就是交换证书。
1. 服务器通过Certificate消息发送证书信息，如果需要验证客户端（双向认证），发送CertificateRequest消息给客户端。
2. 服务器发送ServerHelloDone消息，等待客户端响应。
3. 收到ServerHelloDone消息后，客户端验证服务端的数字证书的有效性。

为了使得通信能够建立，需要对这些证书进行一些检查。讨论SSL和基于数字证书的认证过程超出了本测试指南的范围，这里只注重于讨论确认证书有效性的主要评判条件：
* 检查CA是否是已知的（认为是可信任的）；
* 检查证书目前是否有效；
* 检查网站名称和证书中描述的名称是否一致。

让我们来更详细深入每项检查：

* 每一个浏览器都有一系列预置的信任CA，用来进行签名CA的判断（这个列表可以被自定义和任意扩展）。在与HTTPS服务器进行初始协商阶段，如果服务器证书是浏览器未知的CA相关签署的，通常浏览器会发出一个警告。这通常会发生在web应用程序依赖于一个自己设置的CA签名的证书的情况中。这可以涉及到多个方面。举例来说，这种情况发生可能在一个内网环境是正常的（比如HTTPS下的公司web邮件服务；在这里，显然所有用户能够将内部CA标记为可信CA）。当服务在互联网上向公众公开，显然（当确认我们交流的服务器的身份是非常重要的情况下），依赖于可信CA往往是必须的，这些CA应该被所有的用户识别出来（这里我们为了简化迷信，我们暂时不深入挖掘数字证书中的信任模型的实现情况）。

* 证书分配有有效时间段，因此他们会过期。同样，浏览器会对此发出警告。一个公开服务需要当前的有效证书；否则意味着虽然我们访问的服务器证书是被我们信任的某人签署，但是已经失效，需要更新。

* 万一证书的名字和服务器名字不匹配会发生什么？如果这种现象发生了，听上去好像是多虑了。由于一系列的原因下，其实这种情况不罕见。一个系统可能托管了许多基于名字的虚拟主机，他们共享同样的IP地址，并通过HTTP 1.1中的Host头的信息进行识别。在这种情况下，由于SSL握手对于服务器证书的检测是在在HTTP请求处理之前完成的，他不可能分配给不同虚拟主机的不同的证书。因此，如果站点的名称和证书上的名称不匹配，服务器可能会给我们一个标志告诉我们这一情况。为了避免这种现象，必须使用基于IP的虚拟服务器。[33]和[34]描述了处理这个问题的技巧以及如何允许基于名字的虚拟主机被正确指向问题。


#### 其他漏洞
由于新服务的存在，监听不同的tcp端口可能会引入漏洞，比如软件没有即使更新导致的基础设施漏洞[4]。此外，为了正确保护传输过程中的数据安全，会话cookie必须使用Secure标志[5]以及使用一些指示符来应该被设置来保证浏览器只接受安全的数据流（如HSTS[6]，CSP）。

同样的，也有一下通过截获通信数据流来发起的攻击，比如在web服务器同时在HTTP和HTTPS上同时提供服务[6],[7]或在同一个页面混合HTTP和HTTPS资源的情况下。


### 如何测试

#### 测试明文传输的敏感信息
不同类型的需要保护的敏感信息可能被明文方式传输。可以通过使用HTTP替换HTTPS协议来确认这个情况。参见下面具体的案例来了解细节，比如凭证[3]和其他数据[2]。


##### 例1： 通过HTTP的基本认证
一个典型的例子是在HTTP上使用基本认证（Basic Authentication）。因为基本认证系统中，在登陆后，登陆凭证是通过编码，而不是加密在HTTP头中发送。

```
$ curl -kis http://example.com/restricted/
HTTP/1.1 401 Authorization Required
Date: Fri, 01 Aug 2013 00:00:00 GMT
WWW-Authenticate: Basic realm="Restricted Area"
Accept-Ranges: bytes
Vary: Accept-Encoding
Content-Length: 162
Content-Type: text/html

<html><head><title>401 Authorization Required</title></head>
<body bgcolor=white>
<h1>401 Authorization Required</h1>

Invalid login credentials!

</body></html>
```


#### 测试弱SSL/TLS加密算法/协议/密钥漏洞
由于存在巨大数量的加密套件，快速的密码学分析使得测试SSL服务器成为较重要的人物。

在编写这片测试准则的时候，下面这些别认为是最小的检查列表：
* 弱加密算法不应该被使用（比如，密钥小于128比特[10]；不使用加密算法，因为没有使用任何加密；没有匿名DH，因为不能提供认证过程）。
* 必须禁止弱加密协议（如，SSLv2必须禁止，因为该协议设计上存在已知漏洞[11]）。
* 协商过程必须被正确配置（如，不安全的协商过程必须禁止，因为存在中间人攻击[12]以及由客户端开始的初始协商必须禁止，因为存在拒绝服务攻击漏洞[13]）。
* 不存在出口级的密码套件，因为他们很容易被破解[10]。
* X.509 证书密钥长度必须健壮（如，RSA或DSA使用的密钥至少1024比特）。
* X.509 证书必须只被安全的哈兮算法所签名（如，不要使用MD5算法，因为该算法存在已知的冲突攻击）。
* 密钥必须通过正确的熵中生成（如，Debian生成的弱密钥）[14]。

更加完整的检查列表包括：
* 应该开启安全的协商过程。
* 由于已知冲突攻击，MD5不应该被使用。[35]
* 由于密码学分析攻击，RC4不应该被使用。[15]
* 服务器应该防止BEAST攻击[16]。
* 服务器应该防止CRIME攻击，禁止TLS压缩[17]。
* 服务器应该支持前向安全性[18]。

下面标准可以作为部署SSL服务器的参考资料：
* PCI-DSS v2.0 在4.1中要求相关机构必须使用“健壮加密措施”，但是没有精确定义密钥长度和算法。通常的解释是，部分基于该标准的上一个版本，至少128位密钥长度，没有出口级的算法强度，以及不使用SSLv2 [19]。
* Qualys SSL 实验室的服务器评价指南[14]，部署最佳实践[10]和SSL威胁模型[20]被设计为标准化SSL服务器评估和配置标准。但是没有SSL服务器工具一样更新[21]。
* OWASP 也有许多关于SSL/TLS安全的自由[22]，[23]，[24]，[25]，[26]。

一些工具和扫描器有免费的（如SSLAudit[28]和SSLScan[29]），也有商业的（如Tenable的Nessus[27]），可以被用来评估SSL/TLS漏洞。但是由于这些漏洞是不断发展的，一个好办法是通过openssl[30]来手动检查，或使用工具的输出来作为人工评估的输入依据。

有时，SSL/TLS服务不能直接访问，测试人员只能通过使用HTTP代理中的CONNECT方法进行访问[36]。大多数工具会尝试希望的tcp端口来开始SSL/TLS握手。但这可能无法在HTTP代理中起作用。测试人员可以简单通过一下中转软件如socat[37]来绕过这种情况。


##### 例2：通过nmap发现SSL服务

第一步是识别被SSL/TLS包装服务的端口。通常通过SSL的web或邮件服务端口是 - 443（https），465（ssmtp），585（imap4-ssl），993（imaps），995（ssl-pop）。

在下面的例子中，我们通过使用nmap的“-sV”选项来搜寻SSL服务，这个选项用于识别服务，所以也能够识别出SSL服务[31]。这个例子中其他选项也进行了定制。通常在web应用渗透测试中的测试范围端口限定在80和443。

```
$ nmap -sV --reason -PN -n --top-ports 100 www.example.com
Starting Nmap 6.25 ( http://nmap.org ) at 2013-01-01 00:00 CEST
Nmap scan report for www.example.com (127.0.0.1)
Host is up, received user-set (0.20s latency).
Not shown: 89 filtered ports
Reason: 89 no-responses
PORT    STATE SERVICE  REASON  VERSION
21/tcp  open  ftp      syn-ack Pure-FTPd
22/tcp  open  ssh      syn-ack OpenSSH 5.3 (protocol 2.0)
25/tcp  open  smtp     syn-ack Exim smtpd 4.80
26/tcp  open  smtp     syn-ack Exim smtpd 4.80
80/tcp  open  http     syn-ack
110/tcp open  pop3     syn-ack Dovecot pop3d
143/tcp open  imap     syn-ack Dovecot imapd
443/tcp open  ssl/http syn-ack Apache
465/tcp open  ssl/smtp syn-ack Exim smtpd 4.80
993/tcp open  ssl/imap syn-ack Dovecot imapd
995/tcp open  ssl/pop3 syn-ack Dovecot pop3d
Service Info: Hosts: example.com
Service detection performed. Please report any incorrect results at http://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 131.38 seconds
```


##### 例3： 通过nmap检查证书信息，弱加密算法以及SSLv2

Nmap有两个相关脚本来检测证书信息和弱加密算法[31]。

```
$ nmap --script ssl-cert,ssl-enum-ciphers -p 443,465,993,995 www.example.com
Starting Nmap 6.25 ( http://nmap.org ) at 2013-01-01 00:00 CEST
Nmap scan report for www.example.com (127.0.0.1)
Host is up (0.090s latency).
rDNS record for 127.0.0.1: www.example.com
PORT    STATE SERVICE
443/tcp open  https
| ssl-cert: Subject: commonName=www.example.org
| Issuer: commonName=*******
| Public Key type: rsa
| Public Key bits: 1024
| Not valid before: 2010-01-23T00:00:00+00:00
| Not valid after:  2020-02-28T23:59:59+00:00
| MD5:   *******
|_SHA-1: *******
| ssl-enum-ciphers:
|   SSLv3:
|     ciphers:
|       TLS_RSA_WITH_CAMELLIA_128_CBC_SHA - strong
|       TLS_RSA_WITH_CAMELLIA_256_CBC_SHA - strong
|       TLS_RSA_WITH_RC4_128_SHA - strong
|     compressors:
|       NULL
|   TLSv1.0:
|     ciphers:
|       TLS_RSA_WITH_CAMELLIA_128_CBC_SHA - strong
|       TLS_RSA_WITH_CAMELLIA_256_CBC_SHA - strong
|       TLS_RSA_WITH_RC4_128_SHA - strong
|     compressors:
|       NULL
|_  least strength: strong
465/tcp open  smtps
| ssl-cert: Subject: commonName=*.exapmple.com
| Issuer: commonName=*******
| Public Key type: rsa
| Public Key bits: 2048
| Not valid before: 2010-01-23T00:00:00+00:00
| Not valid after:  2020-02-28T23:59:59+00:00
| MD5:   *******
|_SHA-1: *******
| ssl-enum-ciphers:
|   SSLv3:
|     ciphers:
|       TLS_RSA_WITH_CAMELLIA_128_CBC_SHA - strong
|       TLS_RSA_WITH_CAMELLIA_256_CBC_SHA - strong
|       TLS_RSA_WITH_RC4_128_SHA - strong
|     compressors:
|       NULL
|   TLSv1.0:
|     ciphers:
|       TLS_RSA_WITH_CAMELLIA_128_CBC_SHA - strong
|       TLS_RSA_WITH_CAMELLIA_256_CBC_SHA - strong
|       TLS_RSA_WITH_RC4_128_SHA - strong
|     compressors:
|       NULL
|_  least strength: strong
993/tcp open  imaps
| ssl-cert: Subject: commonName=*.exapmple.com
| Issuer: commonName=*******
| Public Key type: rsa
| Public Key bits: 2048
| Not valid before: 2010-01-23T00:00:00+00:00
| Not valid after:  2020-02-28T23:59:59+00:00
| MD5:   *******
|_SHA-1: *******
| ssl-enum-ciphers:
|   SSLv3:
|     ciphers:
|       TLS_RSA_WITH_CAMELLIA_128_CBC_SHA - strong
|       TLS_RSA_WITH_CAMELLIA_256_CBC_SHA - strong
|       TLS_RSA_WITH_RC4_128_SHA - strong
|     compressors:
|       NULL
|   TLSv1.0:
|     ciphers:
|       TLS_RSA_WITH_CAMELLIA_128_CBC_SHA - strong
|       TLS_RSA_WITH_CAMELLIA_256_CBC_SHA - strong
|       TLS_RSA_WITH_RC4_128_SHA - strong
|     compressors:
|       NULL
|_  least strength: strong
995/tcp open  pop3s
| ssl-cert: Subject: commonName=*.exapmple.com
| Issuer: commonName=*******
| Public Key type: rsa
| Public Key bits: 2048
| Not valid before: 2010-01-23T00:00:00+00:00
| Not valid after:  2020-02-28T23:59:59+00:00
| MD5:   *******
|_SHA-1: *******
| ssl-enum-ciphers:
|   SSLv3:
|     ciphers:
|       TLS_RSA_WITH_CAMELLIA_128_CBC_SHA - strong
|       TLS_RSA_WITH_CAMELLIA_256_CBC_SHA - strong
|       TLS_RSA_WITH_RC4_128_SHA - strong
|     compressors:
|       NULL
|   TLSv1.0:
|     ciphers:
|       TLS_RSA_WITH_CAMELLIA_128_CBC_SHA - strong
|       TLS_RSA_WITH_CAMELLIA_256_CBC_SHA - strong
|       TLS_RSA_WITH_RC4_128_SHA - strong
|     compressors:
|       NULL
|_  least strength: strong
Nmap done: 1 IP address (1 host up) scanned in 8.64 seconds
```


##### 例4： 通过openssl手动检查客户端发起的协商和安全协商过程

Openssl[30]可以用来人工测试SSL/TLS。在这个例子中，测试者尝试通过客户端初始化一个协商过程来连接服务器。然后写下HTTP请求第一行以及在新的一行写下“R”类型。接着等待协商以及HTTP请求的完成，从服务器的输出来检查是否支持安全协商过程。同时使用人工请求也能够检测是否开启了TLS压缩，检测CRIME[13]，以及一些其他的加密算法和漏洞。

```
$ openssl s_client -connect www2.example.com:443
CONNECTED(00000003)
depth=2 ******
verify error:num=20:unable to get local issuer certificate
verify return:0
---
Certificate chain
 0 s:******
   i:******
 1 s:******
   i:******
 2 s:******
   i:******
---
Server certificate
-----BEGIN CERTIFICATE-----
******
-----END CERTIFICATE-----
subject=******
issuer=******
---
No client certificate CA names sent
---
SSL handshake has read 3558 bytes and written 640 bytes
---
New, TLSv1/SSLv3, Cipher is DES-CBC3-SHA
Server public key is 2048 bit
Secure Renegotiation IS NOT supported
Compression: NONE
Expansion: NONE
SSL-Session:
    Protocol  : TLSv1
    Cipher    : DES-CBC3-SHA
    Session-ID: ******
    Session-ID-ctx:
    Master-Key: ******
    Key-Arg   : None
    PSK identity: None
    PSK identity hint: None
    SRP username: None
    Start Time: ******
    Timeout   : 300 (sec)
    Verify return code: 20 (unable to get local issuer certificate)
---
```

现在测试者可以写下HTTP请求，以及在新的一行写下R。
```
HEAD / HTTP/1.1
R
```

服务器正在协商中

```
RENEGOTIATING
depth=2 C******
verify error:num=20:unable to get local issuer certificate
verify return:0
```

测试者可以完成请求，检查响应

```
HEAD / HTTP/1.1

HTTP/1.1 403 Forbidden ( The server denies the specified Uniform Resource Locator (URL). Contact the server administrator.  )
Connection: close
Pragma: no-cache
Cache-Control: no-cache
Content-Type: text/html
Content-Length: 1792

read:errno=0
```

甚至当HEAD请求是不允许，客户端初始的协商仍是被允许的。


##### 例5： 通过TestSSLServer测试支持的加密套件，BEAST和CRIME攻击

TestSSLServer[32]是一个脚本，他使测试者可以检查加密套件和检测BEAST、CRIME攻击。BEAST（Browser Exploit Against SSL/TLS）利用TLS 1.0中CBC模式的漏洞。CRIME（Compression Ratio Info-leak Made Easy）利用TLS压缩中的漏洞，这个选项应该被禁用。有趣的是BEAST的第一个修复方案是使用RC4，但是RC4是不推荐的，因为存在密码分析攻击[15]。

一个在线检测工具是SSL Labs，但是只能用在面向互联网的服务器。同时要考虑目标站点数据可能会存在SSL Labs服务器中，也会有来自该服务器的链接[21]。

```
$ java -jar TestSSLServer.jar www3.example.com 443
Supported versions: SSLv3 TLSv1.0 TLSv1.1 TLSv1.2
Deflate compression: no
Supported cipher suites (ORDER IS NOT SIGNIFICANT):
  SSLv3
     RSA_WITH_RC4_128_SHA
     RSA_WITH_3DES_EDE_CBC_SHA
     DHE_RSA_WITH_3DES_EDE_CBC_SHA
     RSA_WITH_AES_128_CBC_SHA
     DHE_RSA_WITH_AES_128_CBC_SHA
     RSA_WITH_AES_256_CBC_SHA
     DHE_RSA_WITH_AES_256_CBC_SHA
     RSA_WITH_CAMELLIA_128_CBC_SHA
     DHE_RSA_WITH_CAMELLIA_128_CBC_SHA
     RSA_WITH_CAMELLIA_256_CBC_SHA
     DHE_RSA_WITH_CAMELLIA_256_CBC_SHA
     TLS_RSA_WITH_SEED_CBC_SHA
     TLS_DHE_RSA_WITH_SEED_CBC_SHA
  (TLSv1.0: idem)
  (TLSv1.1: idem)
  TLSv1.2
     RSA_WITH_RC4_128_SHA
     RSA_WITH_3DES_EDE_CBC_SHA
     DHE_RSA_WITH_3DES_EDE_CBC_SHA
     RSA_WITH_AES_128_CBC_SHA
     DHE_RSA_WITH_AES_128_CBC_SHA
     RSA_WITH_AES_256_CBC_SHA
     DHE_RSA_WITH_AES_256_CBC_SHA
     RSA_WITH_AES_128_CBC_SHA256
     RSA_WITH_AES_256_CBC_SHA256
     RSA_WITH_CAMELLIA_128_CBC_SHA
     DHE_RSA_WITH_CAMELLIA_128_CBC_SHA
     DHE_RSA_WITH_AES_128_CBC_SHA256
     DHE_RSA_WITH_AES_256_CBC_SHA256
     RSA_WITH_CAMELLIA_256_CBC_SHA
     DHE_RSA_WITH_CAMELLIA_256_CBC_SHA
     TLS_RSA_WITH_SEED_CBC_SHA
     TLS_DHE_RSA_WITH_SEED_CBC_SHA
     TLS_RSA_WITH_AES_128_GCM_SHA256
     TLS_RSA_WITH_AES_256_GCM_SHA384
     TLS_DHE_RSA_WITH_AES_128_GCM_SHA256
     TLS_DHE_RSA_WITH_AES_256_GCM_SHA384
----------------------
Server certificate(s):
  ******
----------------------
Minimal encryption strength:     strong encryption (96-bit or more)
Achievable encryption strength:  strong encryption (96-bit or more)
BEAST status: vulnerable
CRIME status: protected

```


##### 例6： 通过sslyze特使SSL/TLS漏洞

sslyze [33] 是一个python脚本用来进行大量测试和XML输出。下面例子展示了一个常规扫描。这是SSL/TLS测试较为完整和全面的工具之一。

```
./sslyze.py --regular example.com:443

 REGISTERING AVAILABLE PLUGINS
 -----------------------------

  PluginHSTS
  PluginSessionRenegotiation
  PluginCertInfo
  PluginSessionResumption
  PluginOpenSSLCipherSuites
  PluginCompression



 CHECKING HOST(S) AVAILABILITY
 -----------------------------

  example.com:443                      => 127.0.0.1:443



 SCAN RESULTS FOR EXAMPLE.COM:443 - 127.0.0.1:443
 ---------------------------------------------------

  * Compression :
        Compression Support:      Disabled

  * Session Renegotiation :
      Client-initiated Renegotiations:    Rejected
      Secure Renegotiation:               Supported

  * Certificate :
      Validation w/ Mozilla's CA Store:  Certificate is NOT Trusted: unable to get local issuer certificate
      Hostname Validation:               MISMATCH
      SHA1 Fingerprint:                  ******

      Common Name:                       www.example.com
      Issuer:                            ******
      Serial Number:                     ****
      Not Before:                        Sep 26 00:00:00 2010 GMT
      Not After:                         Sep 26 23:59:59 2020 GMT

      Signature Algorithm:               sha1WithRSAEncryption
      Key Size:                          1024 bit
      X509v3 Subject Alternative Name:   {'othername': ['<unsupported>'], 'DNS': ['www.example.com']}

  * OCSP Stapling :
      Server did not send back an OCSP response.

  * Session Resumption :
      With Session IDs:           Supported (5 successful, 0 failed, 0 errors, 5 total attempts).
      With TLS Session Tickets:   Supported

  * SSLV2 Cipher Suites :

      Rejected Cipher Suite(s): Hidden

      Preferred Cipher Suite: None

      Accepted Cipher Suite(s): None

      Undefined - An unexpected error happened: None

  * SSLV3 Cipher Suites :

      Rejected Cipher Suite(s): Hidden

      Preferred Cipher Suite:
        RC4-SHA                       128 bits      HTTP 200 OK

      Accepted Cipher Suite(s):
        CAMELLIA256-SHA               256 bits      HTTP 200 OK
        RC4-SHA                       128 bits      HTTP 200 OK
        CAMELLIA128-SHA               128 bits      HTTP 200 OK

      Undefined - An unexpected error happened: None

  * TLSV1_1 Cipher Suites :

      Rejected Cipher Suite(s): Hidden

      Preferred Cipher Suite: None

      Accepted Cipher Suite(s): None

      Undefined - An unexpected error happened:
        ECDH-RSA-AES256-SHA             socket.timeout - timed out
        ECDH-ECDSA-AES256-SHA           socket.timeout - timed out

  * TLSV1_2 Cipher Suites :

      Rejected Cipher Suite(s): Hidden

      Preferred Cipher Suite: None

      Accepted Cipher Suite(s): None

      Undefined - An unexpected error happened:
        ECDH-RSA-AES256-GCM-SHA384      socket.timeout - timed out
        ECDH-ECDSA-AES256-GCM-SHA384    socket.timeout - timed out

  * TLSV1 Cipher Suites :

      Rejected Cipher Suite(s): Hidden

      Preferred Cipher Suite:
        RC4-SHA                       128 bits      Timeout on HTTP GET

      Accepted Cipher Suite(s):
        CAMELLIA256-SHA               256 bits      HTTP 200 OK
        RC4-SHA                       128 bits      HTTP 200 OK
        CAMELLIA128-SHA               128 bits      HTTP 200 OK

      Undefined - An unexpected error happened:
        ADH-CAMELLIA256-SHA             socket.timeout - timed out



 SCAN COMPLETED IN 9.68 S
 ------------------------
```


##### 例7： 通过testssl.sh测试SSL/TLS

Testssl.sh [38] 是一个Linux shell脚本提供了清晰的输出来帮助做决策。他不仅可以检测web服务器而且可以其他端口的服务，支持STARTTLS，SNI，SPDY和一些HTTP头部检测。

这个工具很容易使用，下面是一些样本输出：

```
user@myhost: % testssl.sh owasp.org

#########################################################
testssl.sh v2.0rc3  (https://testssl.sh)
($Id: testssl.sh,v 1.97 2014/04/15 21:54:29 dirkw Exp $)

   This program is free software. Redistribution +
   modification under GPLv2 is permitted.
   USAGE w/o ANY WARRANTY. USE IT AT YOUR OWN RISK!

 Note you can only check the server against what is
 available (ciphers/protocols) locally on your machine
#########################################################

Using "OpenSSL 1.0.2-beta1 24 Feb 2014" on
      "myhost:/<mypath>/bin/openssl64"


Testing now (2014-04-17 15:06) ---> owasp.org:443 <---
("owasp.org" resolves to "192.237.166.62 / 2001:4801:7821:77:cd2c:d9de:ff10:170e")


--> Testing Protocols

 SSLv2     NOT offered (ok)
 SSLv3     offered
 TLSv1     offered (ok)
 TLSv1.1   offered (ok)
 TLSv1.2   offered (ok)

 SPDY/NPN  not offered

--> Testing standard cipher lists

 Null Cipher              NOT offered (ok)
 Anonymous NULL Cipher    NOT offered (ok)
 Anonymous DH Cipher      NOT offered (ok)
 40 Bit encryption        NOT offered (ok)
 56 Bit encryption        NOT offered (ok)
 Export Cipher (general)  NOT offered (ok)
 Low (<=64 Bit)           NOT offered (ok)
 DES Cipher               NOT offered (ok)
 Triple DES Cipher        offered
 Medium grade encryption  offered
 High grade encryption    offered (ok)

--> Testing server defaults (Server Hello)

 Negotiated protocol       TLSv1.2
 Negotiated cipher         AES128-GCM-SHA256

 Server key size           2048 bit
 TLS server extensions:    server name, renegotiation info, session ticket, heartbeat
 Session Tickets RFC 5077  300 seconds

--> Testing specific vulnerabilities

 Heartbleed (CVE-2014-0160), experimental  NOT vulnerable (ok)
 Renegotiation (CVE 2009-3555)             NOT vulnerable (ok)
 CRIME, TLS (CVE-2012-4929)                NOT vulnerable (ok)

--> Checking RC4 Ciphers

RC4 seems generally available. Now testing specific ciphers...

 Hexcode    Cipher Name                   KeyExch.  Encryption Bits
--------------------------------------------------------------------
 [0x05]     RC4-SHA                       RSA         RC4      128

RC4 is kind of broken, for e.g. IE6 consider 0x13 or 0x0a

--> Testing HTTP Header response

 HSTS        no
 Server      Apache
 Application (None)

--> Testing (Perfect) Forward Secrecy  (P)FS)

no PFS available

Done now (2014-04-17 15:07) ---> owasp.org:443 <---

user@myhost: %


```

STARTTLS 可以通过 `testssl.sh -t smtp.gmail.com:587  smtp` 来测试，`testssl -e <target>`来测试加密算法，`testssl -E <target>`来测试加密算法的每种协议。可以通过`testssl -V`查看本地openssl支持和安装的加密套件。

最有意思的是，测试者可以通过学习源代码来了解如何测试相关特性，参考例4。更有意思的是，他使用纯bash和/dev/tcp 套接字来完成heartbleed的整个握手过程。

此外，他也提供RFC加密套件到OpenSSL套件的映射（通过“testssl.sh -V”）。测试者可以参考同一目录下mapping-rfc.txt文件。


##### 例8： 通过SSL Breacher测试SSL/TLS

这个工具 [99] 组合了其他一些工具，并加入了一些额外的检测过程来完成最复杂的SSL测试。

他支持如下检测：

```
#HeartBleed
#ChangeCipherSpec Injection
#BREACH
#BEAST
#Forward Secrecy support
#RC4 support
#CRIME & TIME (If CRIME is detected, TIME will also be reported)
#Lucky13
#HSTS: Check for implementation of HSTS header
#HSTS: Reasonable duration of MAX-AGE
#HSTS: Check for SubDomains support
#Certificate expiration
#Insufficient public key-length
#Host-name mismatch
#Weak Insecure Hashing Algorithm (MD2, MD4, MD5)
#SSLv2 support
#Weak ciphers check
#Null Prefix in certificate
#HTTPS Stripping
#Surf Jacking
#Non-SSL elements/contents embedded in SSL page
#Cache-Control
```

```
pentester@r00ting: % breacher.sh https://localhost/login.php


Host Info:
#####
Host : localhost
Port : 443
Path : /login.php



Certificate Info:
#####
Type: Domain Validation Certificate (i.e. NON-Extended Validation Certificate)
Expiration Date: Sat Nov 09 07:48:47 SGT 2019
Signature Hash Algorithm: SHA1withRSA
Public key: Sun RSA public key, 1024 bits
  modulus: 135632964843555009910164098161004086259135236815846778903941582882908611097021488277565732851712895057227849656364886898196239901879569635659861770850920241178222686670162318147175328086853962427921575656093414000691131757099663322369656756090030190369923050306668778534926124693591013220754558036175189121517
  public exponent: 65537
Signed for: CN=localhost
Signed by: CN=localhost
Total certificate chain: 1

(Use -Djavax.net.debug=ssl:handshake:verbose for debugged output.)

#####

Certificate Validation:
#####
[!] Signed using Insufficient public key length 1024 bits
    (Refer to http://www.keylength.com/ for details)
[!] Certificate Signer: Self-signed/Untrusted CA  - verified with Firefox & Java ROOT CAs.

#####

Loading module: Hut3 Cardiac Arrest ...

Checking localhost:443 for Heartbleed bug (CVE-2014-0160) ...

[-] Connecting to 127.0.0.1:443 using SSLv3
[-] Sending ClientHello
[-] ServerHello received
[-] Sending Heartbeat
[Vulnerable] Heartbeat response was 16384 bytes instead of 3! 127.0.0.1:443 is vulnerable over SSLv3
[-] Displaying response (lines consisting entirely of null bytes are removed):

  0000: 02 FF FF 08 03 00 53 48 73 F0 7C CA C1 D9 02 04  ......SHs.|.....
  0010: F2 1D 2D 49 F5 12 BF 40 1B 94 D9 93 E4 C4 F4 F0  ..-I...@........
  0020: D0 42 CD 44 A2 59 00 02 96 00 00 00 01 00 02 00  .B.D.Y..........
  0060: 1B 00 1C 00 1D 00 1E 00 1F 00 20 00 21 00 22 00  .......... .!.".
  0070: 23 00 24 00 25 00 26 00 27 00 28 00 29 00 2A 00  #.$.%.&.'.(.).*.
  0080: 2B 00 2C 00 2D 00 2E 00 2F 00 30 00 31 00 32 00  +.,.-.../.0.1.2.
  0090: 33 00 34 00 35 00 36 00 37 00 38 00 39 00 3A 00  3.4.5.6.7.8.9.:.
  00a0: 3B 00 3C 00 3D 00 3E 00 3F 00 40 00 41 00 42 00  ;.<.=.>.?.@.A.B.
  00b0: 43 00 44 00 45 00 46 00 60 00 61 00 62 00 63 00  C.D.E.F.`.a.b.c.
  00c0: 64 00 65 00 66 00 67 00 68 00 69 00 6A 00 6B 00  d.e.f.g.h.i.j.k.
  00d0: 6C 00 6D 00 80 00 81 00 82 00 83 00 84 00 85 00  l.m.............
  01a0: 20 C0 21 C0 22 C0 23 C0 24 C0 25 C0 26 C0 27 C0   .!.".#.$.%.&.'.
  01b0: 28 C0 29 C0 2A C0 2B C0 2C C0 2D C0 2E C0 2F C0  (.).*.+.,.-.../.
  01c0: 30 C0 31 C0 32 C0 33 C0 34 C0 35 C0 36 C0 37 C0  0.1.2.3.4.5.6.7.
  01d0: 38 C0 39 C0 3A C0 3B C0 3C C0 3D C0 3E C0 3F C0  8.9.:.;.<.=.>.?.
  01e0: 40 C0 41 C0 42 C0 43 C0 44 C0 45 C0 46 C0 47 C0  @.A.B.C.D.E.F.G.
  01f0: 48 C0 49 C0 4A C0 4B C0 4C C0 4D C0 4E C0 4F C0  H.I.J.K.L.M.N.O.
  0200: 50 C0 51 C0 52 C0 53 C0 54 C0 55 C0 56 C0 57 C0  P.Q.R.S.T.U.V.W.
  0210: 58 C0 59 C0 5A C0 5B C0 5C C0 5D C0 5E C0 5F C0  X.Y.Z.[.\.].^._.
  0220: 60 C0 61 C0 62 C0 63 C0 64 C0 65 C0 66 C0 67 C0  `.a.b.c.d.e.f.g.
  0230: 68 C0 69 C0 6A C0 6B C0 6C C0 6D C0 6E C0 6F C0  h.i.j.k.l.m.n.o.
  0240: 70 C0 71 C0 72 C0 73 C0 74 C0 75 C0 76 C0 77 C0  p.q.r.s.t.u.v.w.
  0250: 78 C0 79 C0 7A C0 7B C0 7C C0 7D C0 7E C0 7F C0  x.y.z.{.|.}.~...
  02c0: 00 00 49 00 0B 00 04 03 00 01 02 00 0A 00 34 00  ..I...........4.
  02d0: 32 00 0E 00 0D 00 19 00 0B 00 0C 00 18 00 09 00  2...............
  0300: 10 00 11 00 23 00 00 00 0F 00 01 01 00 00 00 00  ....#...........
  0bd0: 00 00 00 00 00 00 00 00 00 12 7D 01 00 10 00 02  ..........}.....

[-] Closing connection

[-] Connecting to 127.0.0.1:443 using TLSv1.0
[-] Sending ClientHello
[-] ServerHello received
[-] Sending Heartbeat
[Vulnerable] Heartbeat response was 16384 bytes instead of 3! 127.0.0.1:443 is vulnerable over TLSv1.0
[-] Displaying response (lines consisting entirely of null bytes are removed):

  0000: 02 FF FF 08 03 01 53 48 73 F0 7C CA C1 D9 02 04  ......SHs.|.....
  0010: F2 1D 2D 49 F5 12 BF 40 1B 94 D9 93 E4 C4 F4 F0  ..-I...@........
  0020: D0 42 CD 44 A2 59 00 02 96 00 00 00 01 00 02 00  .B.D.Y..........
  0060: 1B 00 1C 00 1D 00 1E 00 1F 00 20 00 21 00 22 00  .......... .!.".
  0070: 23 00 24 00 25 00 26 00 27 00 28 00 29 00 2A 00  #.$.%.&.'.(.).*.
  0080: 2B 00 2C 00 2D 00 2E 00 2F 00 30 00 31 00 32 00  +.,.-.../.0.1.2.
  0090: 33 00 34 00 35 00 36 00 37 00 38 00 39 00 3A 00  3.4.5.6.7.8.9.:.
  00a0: 3B 00 3C 00 3D 00 3E 00 3F 00 40 00 41 00 42 00  ;.<.=.>.?.@.A.B.
  00b0: 43 00 44 00 45 00 46 00 60 00 61 00 62 00 63 00  C.D.E.F.`.a.b.c.
  00c0: 64 00 65 00 66 00 67 00 68 00 69 00 6A 00 6B 00  d.e.f.g.h.i.j.k.
  00d0: 6C 00 6D 00 80 00 81 00 82 00 83 00 84 00 85 00  l.m.............
  01a0: 20 C0 21 C0 22 C0 23 C0 24 C0 25 C0 26 C0 27 C0   .!.".#.$.%.&.'.
  01b0: 28 C0 29 C0 2A C0 2B C0 2C C0 2D C0 2E C0 2F C0  (.).*.+.,.-.../.
  01c0: 30 C0 31 C0 32 C0 33 C0 34 C0 35 C0 36 C0 37 C0  0.1.2.3.4.5.6.7.
  01d0: 38 C0 39 C0 3A C0 3B C0 3C C0 3D C0 3E C0 3F C0  8.9.:.;.<.=.>.?.
  01e0: 40 C0 41 C0 42 C0 43 C0 44 C0 45 C0 46 C0 47 C0  @.A.B.C.D.E.F.G.
  01f0: 48 C0 49 C0 4A C0 4B C0 4C C0 4D C0 4E C0 4F C0  H.I.J.K.L.M.N.O.
  0200: 50 C0 51 C0 52 C0 53 C0 54 C0 55 C0 56 C0 57 C0  P.Q.R.S.T.U.V.W.
  0210: 58 C0 59 C0 5A C0 5B C0 5C C0 5D C0 5E C0 5F C0  X.Y.Z.[.\.].^._.
  0220: 60 C0 61 C0 62 C0 63 C0 64 C0 65 C0 66 C0 67 C0  `.a.b.c.d.e.f.g.
  0230: 68 C0 69 C0 6A C0 6B C0 6C C0 6D C0 6E C0 6F C0  h.i.j.k.l.m.n.o.
  0240: 70 C0 71 C0 72 C0 73 C0 74 C0 75 C0 76 C0 77 C0  p.q.r.s.t.u.v.w.
  0250: 78 C0 79 C0 7A C0 7B C0 7C C0 7D C0 7E C0 7F C0  x.y.z.{.|.}.~...
  02c0: 00 00 49 00 0B 00 04 03 00 01 02 00 0A 00 34 00  ..I...........4.
  02d0: 32 00 0E 00 0D 00 19 00 0B 00 0C 00 18 00 09 00  2...............
  0300: 10 00 11 00 23 00 00 00 0F 00 01 01 00 00 00 00  ....#...........
  0bd0: 00 00 00 00 00 00 00 00 00 12 7D 01 00 10 00 02  ..........}.....

[-] Closing connection

[-] Connecting to 127.0.0.1:443 using TLSv1.1
[-] Sending ClientHello
[-] ServerHello received
[-] Sending Heartbeat
[Vulnerable] Heartbeat response was 16384 bytes instead of 3! 127.0.0.1:443 is vulnerable over TLSv1.1
[-] Displaying response (lines consisting entirely of null bytes are removed):

  0000: 02 FF FF 08 03 02 53 48 73 F0 7C CA C1 D9 02 04  ......SHs.|.....
  0010: F2 1D 2D 49 F5 12 BF 40 1B 94 D9 93 E4 C4 F4 F0  ..-I...@........
  0020: D0 42 CD 44 A2 59 00 02 96 00 00 00 01 00 02 00  .B.D.Y..........
  0060: 1B 00 1C 00 1D 00 1E 00 1F 00 20 00 21 00 22 00  .......... .!.".
  0070: 23 00 24 00 25 00 26 00 27 00 28 00 29 00 2A 00  #.$.%.&.'.(.).*.
  0080: 2B 00 2C 00 2D 00 2E 00 2F 00 30 00 31 00 32 00  +.,.-.../.0.1.2.
  0090: 33 00 34 00 35 00 36 00 37 00 38 00 39 00 3A 00  3.4.5.6.7.8.9.:.
  00a0: 3B 00 3C 00 3D 00 3E 00 3F 00 40 00 41 00 42 00  ;.<.=.>.?.@.A.B.
  00b0: 43 00 44 00 45 00 46 00 60 00 61 00 62 00 63 00  C.D.E.F.`.a.b.c.
  00c0: 64 00 65 00 66 00 67 00 68 00 69 00 6A 00 6B 00  d.e.f.g.h.i.j.k.
  00d0: 6C 00 6D 00 80 00 81 00 82 00 83 00 84 00 85 00  l.m.............
  01a0: 20 C0 21 C0 22 C0 23 C0 24 C0 25 C0 26 C0 27 C0   .!.".#.$.%.&.'.
  01b0: 28 C0 29 C0 2A C0 2B C0 2C C0 2D C0 2E C0 2F C0  (.).*.+.,.-.../.
  01c0: 30 C0 31 C0 32 C0 33 C0 34 C0 35 C0 36 C0 37 C0  0.1.2.3.4.5.6.7.
  01d0: 38 C0 39 C0 3A C0 3B C0 3C C0 3D C0 3E C0 3F C0  8.9.:.;.<.=.>.?.
  01e0: 40 C0 41 C0 42 C0 43 C0 44 C0 45 C0 46 C0 47 C0  @.A.B.C.D.E.F.G.
  01f0: 48 C0 49 C0 4A C0 4B C0 4C C0 4D C0 4E C0 4F C0  H.I.J.K.L.M.N.O.
  0200: 50 C0 51 C0 52 C0 53 C0 54 C0 55 C0 56 C0 57 C0  P.Q.R.S.T.U.V.W.
  0210: 58 C0 59 C0 5A C0 5B C0 5C C0 5D C0 5E C0 5F C0  X.Y.Z.[.\.].^._.
  0220: 60 C0 61 C0 62 C0 63 C0 64 C0 65 C0 66 C0 67 C0  `.a.b.c.d.e.f.g.
  0230: 68 C0 69 C0 6A C0 6B C0 6C C0 6D C0 6E C0 6F C0  h.i.j.k.l.m.n.o.
  0240: 70 C0 71 C0 72 C0 73 C0 74 C0 75 C0 76 C0 77 C0  p.q.r.s.t.u.v.w.
  0250: 78 C0 79 C0 7A C0 7B C0 7C C0 7D C0 7E C0 7F C0  x.y.z.{.|.}.~...
  02c0: 00 00 49 00 0B 00 04 03 00 01 02 00 0A 00 34 00  ..I...........4.
  02d0: 32 00 0E 00 0D 00 19 00 0B 00 0C 00 18 00 09 00  2...............
  0300: 10 00 11 00 23 00 00 00 0F 00 01 01 00 00 00 00  ....#...........
  0bd0: 00 00 00 00 00 00 00 00 00 12 7D 01 00 10 00 02  ..........}.....

[-] Closing connection

[-] Connecting to 127.0.0.1:443 using TLSv1.2
[-] Sending ClientHello
[-] ServerHello received
[-] Sending Heartbeat
[Vulnerable] Heartbeat response was 16384 bytes instead of 3! 127.0.0.1:443 is vulnerable over TLSv1.2
[-] Displaying response (lines consisting entirely of null bytes are removed):

  0000: 02 FF FF 08 03 03 53 48 73 F0 7C CA C1 D9 02 04  ......SHs.|.....
  0010: F2 1D 2D 49 F5 12 BF 40 1B 94 D9 93 E4 C4 F4 F0  ..-I...@........
  0020: D0 42 CD 44 A2 59 00 02 96 00 00 00 01 00 02 00  .B.D.Y..........
  0060: 1B 00 1C 00 1D 00 1E 00 1F 00 20 00 21 00 22 00  .......... .!.".
  0070: 23 00 24 00 25 00 26 00 27 00 28 00 29 00 2A 00  #.$.%.&.'.(.).*.
  0080: 2B 00 2C 00 2D 00 2E 00 2F 00 30 00 31 00 32 00  +.,.-.../.0.1.2.
  0090: 33 00 34 00 35 00 36 00 37 00 38 00 39 00 3A 00  3.4.5.6.7.8.9.:.
  00a0: 3B 00 3C 00 3D 00 3E 00 3F 00 40 00 41 00 42 00  ;.<.=.>.?.@.A.B.
  00b0: 43 00 44 00 45 00 46 00 60 00 61 00 62 00 63 00  C.D.E.F.`.a.b.c.
  00c0: 64 00 65 00 66 00 67 00 68 00 69 00 6A 00 6B 00  d.e.f.g.h.i.j.k.
  00d0: 6C 00 6D 00 80 00 81 00 82 00 83 00 84 00 85 00  l.m.............
  01a0: 20 C0 21 C0 22 C0 23 C0 24 C0 25 C0 26 C0 27 C0   .!.".#.$.%.&.'.
  01b0: 28 C0 29 C0 2A C0 2B C0 2C C0 2D C0 2E C0 2F C0  (.).*.+.,.-.../.
  01c0: 30 C0 31 C0 32 C0 33 C0 34 C0 35 C0 36 C0 37 C0  0.1.2.3.4.5.6.7.
  01d0: 38 C0 39 C0 3A C0 3B C0 3C C0 3D C0 3E C0 3F C0  8.9.:.;.<.=.>.?.
  01e0: 40 C0 41 C0 42 C0 43 C0 44 C0 45 C0 46 C0 47 C0  @.A.B.C.D.E.F.G.
  01f0: 48 C0 49 C0 4A C0 4B C0 4C C0 4D C0 4E C0 4F C0  H.I.J.K.L.M.N.O.
  0200: 50 C0 51 C0 52 C0 53 C0 54 C0 55 C0 56 C0 57 C0  P.Q.R.S.T.U.V.W.
  0210: 58 C0 59 C0 5A C0 5B C0 5C C0 5D C0 5E C0 5F C0  X.Y.Z.[.\.].^._.
  0220: 60 C0 61 C0 62 C0 63 C0 64 C0 65 C0 66 C0 67 C0  `.a.b.c.d.e.f.g.
  0230: 68 C0 69 C0 6A C0 6B C0 6C C0 6D C0 6E C0 6F C0  h.i.j.k.l.m.n.o.
  0240: 70 C0 71 C0 72 C0 73 C0 74 C0 75 C0 76 C0 77 C0  p.q.r.s.t.u.v.w.
  0250: 78 C0 79 C0 7A C0 7B C0 7C C0 7D C0 7E C0 7F C0  x.y.z.{.|.}.~...
  02c0: 00 00 49 00 0B 00 04 03 00 01 02 00 0A 00 34 00  ..I...........4.
  02d0: 32 00 0E 00 0D 00 19 00 0B 00 0C 00 18 00 09 00  2...............
  0300: 10 00 11 00 23 00 00 00 0F 00 01 01 00 00 00 00  ....#...........
  0bd0: 00 00 00 00 00 00 00 00 00 12 7D 01 00 10 00 02  ..........}.....

[-] Closing connection



[!] Vulnerable to Heartbleed bug (CVE-2014-0160) mentioned in http://heartbleed.com/
[!] Vulnerability Status: VULNERABLE


#####

Loading module: CCS Injection script by TripWire VERT ...

Checking localhost:443 for OpenSSL ChangeCipherSpec (CCS) Injection bug (CVE-2014-0224) ...

[!] The target may allow early CCS on TLSv1.2
[!] The target may allow early CCS on TLSv1.1
[!] The target may allow early CCS on TLSv1
[!] The target may allow early CCS on SSLv3


[-] This is an experimental detection script and does not definitively determine vulnerable server status.

[!] Potentially vulnerable to OpenSSL ChangeCipherSpec (CCS) Injection vulnerability (CVE-2014-0224) mentioned in http://ccsinjection.lepidum.co.jp/
[!] Vulnerability Status: Possible


#####

Checking localhost:443 for HTTP Compression support against BREACH vulnerability (CVE-2013-3587) ...

[*] HTTP Compression: DISABLED
[*] Immune from BREACH attack mentioned in https://media.blackhat.com/us-13/US-13-Prado-SSL-Gone-in-30-seconds-A-BREACH-beyond-CRIME-WP.pdf
[*] Vulnerability Status: No


--------------- RAW HTTP RESPONSE ---------------

HTTP/1.1 200 OK
Date: Wed, 23 Jul 2014 13:48:07 GMT
Server: Apache/2.4.3 (Win32) OpenSSL/1.0.1c PHP/5.4.7
X-Powered-By: PHP/5.4.7
Set-Cookie: SessionID=xxx; expires=Wed, 23-Jul-2014 12:48:07 GMT; path=/; secure
Set-Cookie: SessionChallenge=yyy; expires=Wed, 23-Jul-2014 12:48:07 GMT; path=/
Content-Length: 193
Connection: close
Content-Type: text/html

<html>
<head>
<title>Login page </title>
</head>
<body>
<script src="http://othersite/test.js"></script>

<link rel="stylesheet" type="text/css" href="http://somesite/test.css">


#####

Checking localhost:443 for correct use of Strict Transport Security (STS) response header (RFC6797) ...

[!] STS response header: NOT PRESENT
[!] Vulnerable to MITM threats mentioned in https://www.owasp.org/index.php/HTTP_Strict_Transport_Security#Threats
[!] Vulnerability Status: VULNERABLE


--------------- RAW HTTP RESPONSE ---------------

HTTP/1.1 200 OK
Date: Wed, 23 Jul 2014 13:48:07 GMT
Server: Apache/2.4.3 (Win32) OpenSSL/1.0.1c PHP/5.4.7
X-Powered-By: PHP/5.4.7
Set-Cookie: SessionID=xxx; expires=Wed, 23-Jul-2014 12:48:07 GMT; path=/; secure
Set-Cookie: SessionChallenge=yyy; expires=Wed, 23-Jul-2014 12:48:07 GMT; path=/
Content-Length: 193
Connection: close
Content-Type: text/html

<html>
<head>
<title>Login page </title>
</head>
<body>
<script src="http://othersite/test.js"></script>

<link rel="stylesheet" type="text/css" href="http://somesite/test.css">


#####

Checking localhost for HTTP support against HTTPS Stripping attack ...

[!] HTTP Support on port [80] : SUPPORTED
[!] Vulnerable to HTTPS Stripping attack mentioned in https://www.blackhat.com/presentations/bh-dc-09/Marlinspike/BlackHat-DC-09-Marlinspike-Defeating-SSL.pdf
[!] Vulnerability Status: VULNERABLE


#####

Checking localhost:443 for HTTP elements embedded in SSL page ...

[!] HTTP elements embedded in SSL page: PRESENT
[!] Vulnerable to MITM malicious content injection attack
[!] Vulnerability Status: VULNERABLE


--------------- HTTP RESOURCES EMBEDDED ---------------
 - http://othersite/test.js
 - http://somesite/test.css

#####

Checking localhost:443 for ROBUST use of anti-caching mechanism ...

[!] Cache Control Directives: NOT PRESENT
[!] Browsers, Proxies and other Intermediaries will cache SSL page and sensitive information will be leaked.
[!] Vulnerability Status: VULNERABLE


-------------------------------------------------

Robust Solution:

	- Cache-Control: no-cache, no-store, must-revalidate, pre-check=0, post-check=0, max-age=0, s-maxage=0
	- Ref: https://www.owasp.org/index.php/Testing_for_Browser_cache_weakness_(OTG-AUTHN-006)
	       http://msdn.microsoft.com/en-us/library/ms533020(v=vs.85).aspx

#####

Checking localhost:443 for Surf Jacking vulnerability (due to Session Cookie missing secure flag) ...

[!] Secure Flag in Set-Cookie:  PRESENT BUT NOT IN ALL COOKIES
[!] Vulnerable to Surf Jacking attack mentioned in https://resources.enablesecurity.com/resources/Surf%20Jacking.pdf
[!] Vulnerability Status: VULNERABLE

--------------- RAW HTTP RESPONSE ---------------

HTTP/1.1 200 OK
Date: Wed, 23 Jul 2014 13:48:07 GMT
Server: Apache/2.4.3 (Win32) OpenSSL/1.0.1c PHP/5.4.7
X-Powered-By: PHP/5.4.7
Set-Cookie: SessionID=xxx; expires=Wed, 23-Jul-2014 12:48:07 GMT; path=/; secure
Set-Cookie: SessionChallenge=yyy; expires=Wed, 23-Jul-2014 12:48:07 GMT; path=/
Content-Length: 193
Connection: close
Content-Type: text/html

#####

Checking localhost:443 for ECDHE/DHE ciphers against FORWARD SECRECY support ...

[*] Forward Secrecy: SUPPORTED
[*] Connected using cipher - TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA on protocol - TLSv1
[*] Attackers will NOT be able to decrypt sniffed SSL packets even if they have compromised private keys.
[*] Vulnerability Status: No

#####

Checking localhost:443 for RC4 support (CVE-2013-2566) ...

[!] RC4: SUPPORTED
[!] Vulnerable to MITM attack described in http://www.isg.rhul.ac.uk/tls/
[!] Vulnerability Status: VULNERABLE



#####

Checking localhost:443 for TLS 1.1 support ...

Checking localhost:443 for TLS 1.2 support ...

[*] TLS 1.1, TLS 1.2: SUPPORTED
[*] Immune from BEAST attack mentioned in http://www.infoworld.com/t/security/red-alert-https-has-been-hacked-174025
[*] Vulnerability Status: No



#####

Loading module: sslyze by iSecPartners ...

Checking localhost:443 for Session Renegotiation support (CVE-2009-3555,CVE-2011-1473,CVE-2011-5094) ...

[*] Secure Client-Initiated Renegotiation : NOT SUPPORTED
[*] Mitigated from DOS attack (CVE-2011-1473,CVE-2011-5094) mentioned in https://www.thc.org/thc-ssl-dos/
[*] Vulnerability Status: No


[*] INSECURE Client-Initiated Renegotiation : NOT SUPPORTED
[*] Immune from TLS Plain-text Injection attack (CVE-2009-3555) - http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2009-3555
[*] Vulnerability Status: No


#####

Loading module: TestSSLServer by Thomas Pornin ...

Checking localhost:443 for SSL version 2 support ...

[*] SSL version 2 : NOT SUPPORTED
[*] Immune from SSLv2-based MITM attack
[*] Vulnerability Status: No


#####

Checking localhost:443 for LANE (LOW,ANON,NULL,EXPORT) weak ciphers support ...

Supported LANE cipher suites:
  SSLv3
     RSA_EXPORT_WITH_RC4_40_MD5
     RSA_EXPORT_WITH_RC2_CBC_40_MD5
     RSA_EXPORT_WITH_DES40_CBC_SHA
     RSA_WITH_DES_CBC_SHA
     DHE_RSA_EXPORT_WITH_DES40_CBC_SHA
     DHE_RSA_WITH_DES_CBC_SHA
     TLS_ECDH_anon_WITH_RC4_128_SHA
     TLS_ECDH_anon_WITH_3DES_EDE_CBC_SHA
     TLS_ECDH_anon_WITH_AES_256_CBC_SHA
  (TLSv1.0: same as above)
  (TLSv1.1: same as above)
  (TLSv1.2: same as above)


[!] LANE ciphers : SUPPORTED
[!] Attackers may be ABLE to recover encrypted packets.
[!] Vulnerability Status: VULNERABLE


#####

Checking localhost:443 for GCM/CCM ciphers support against Lucky13 attack (CVE-2013-0169) ...

Supported GCM cipher suites against Lucky13 attack:
  TLSv1.2
     TLS_RSA_WITH_AES_128_GCM_SHA256
     TLS_RSA_WITH_AES_256_GCM_SHA384
     TLS_DHE_RSA_WITH_AES_128_GCM_SHA256
     TLS_DHE_RSA_WITH_AES_256_GCM_SHA384
     TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256
     TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384


[*] GCM/CCM ciphers : SUPPORTED
[*] Immune from Lucky13 attack mentioned in http://www.isg.rhul.ac.uk/tls/Lucky13.html
[*] Vulnerability Status: No


#####

Checking localhost:443 for TLS Compression support against CRIME (CVE-2012-4929) & TIME attack  ...

[*] TLS Compression : DISABLED
[*] Immune from CRIME & TIME attack mentioned in https://media.blackhat.com/eu-13/briefings/Beery/bh-eu-13-a-perfect-crime-beery-wp.pdf
[*] Vulnerability Status: No


#####

[+] Breacher finished scanning in 12 seconds.
[+] Get your latest copy at http://yehg.net/


```

#### 测试SSL证书有效性 - 客户端和服务端

首先升级浏览器，因为随着浏览器每个版本的发布，CA证书可能过期或更新。检查应用程序使用的证书的有效性。浏览器在遇到证书过期、证书不可信以及证书名字不匹配时会发出警告。

在访问HTTPS站点时，通过点击浏览器窗口中的小锁标志，测试人员可以查看证书信息包括发布者、有效时间、加密特性等等。如果应用程序需要客户端证书，测试人员可能需要安装一个来访问应用。证书信息可以在浏览器的已安装证书列表中找到。

这些检测应该应用在所有的SSL包装的信道中。不仅是443端口上的常见HTTPS服务，也可能有额外的服务被web应用架构或部署中使用（如HTTPS管理端口，HTTPS服务在非标准化端口等等）。因此需要将所有的检测应用于所有发现的SSL包装的服务中。例如，nmap扫描器有一种扫描模式（通过-sV选项）来识别SSL包装服务。Nessus漏洞扫描器也能够在所有SSL/TLS包装服务中实施SSL检测。


##### 例9： 人工测试证书有效性

除了提供人工创造的例子，这个指南也包括匿名的现实中的例子来强调HTTPS站点的证书名字问题是多么频繁。下面的截图展示了一个IT公司的例子。

我们访问.it站点，但是证书被赋予.com站点。IE浏览器提示了我们证书名字不匹配。

![Image:SSL Certificate Validity Testing IE Warning.gif](https://www.owasp.org/images/7/70/SSL_Certificate_Validity_Testing_IE_Warning.gif)

*IE浏览器发出的警告*

Firefox发出消息却不同。Firefox抱怨无法确定.com站点的身份，因为签署证书的CA未知。事实上，IE和Firefox没有预置相同的CA列表。因此不同浏览器的行为可能不一致。

![Image:SSL Certificate Validity Testing Firefox Warning.gif](https://www.owasp.org/images/8/87/SSL_Certificate_Validity_Testing_Firefox_Warning.gif)

*Firefox发出的警告*

#### 测试其他漏洞

正如先前提到的，存在与SSL/TLS协议、加密算法或证书无关的其他类型的漏洞。除了本指南其他部分讨论的漏洞，当服务器同时提供HTTP和HTTPS服务时候，漏洞可能存在，使得攻击者能够强制受害者使用不安全的信道来替代安全信道。

##### Surf Jacking

Surf Jacking攻击 [7] 最初是Sandro Gauci展示的，他允许攻击者在受害者的连接使用SSL或TLS加密的情况下劫持HTTP会话。

下面是攻击如何发生的场景：
* 受害者登陆安全的站点 https://somesecuresite/ 。
* 安全站点在客户登陆后分配了会话cookie。
* 当登陆后，受害者打开了新的浏览窗口，并访问http://examplesite/ 。
* 一个攻击者在同样的网络中，可以得到http://examplesite 的明文流量。
* 攻击者可以在劫持http://examplesite返回响应中发回 "301 Moved Permanently" 响应。在响应的HTTP头中包括“Location: http://somesecuresite /”头，使web浏览器请求http://somesecuresite/ ，注意现在我们是走HTTP而不是HTTPS。
* 受害者发起了通向 http://somesecuresite/ 的明文请求，并在HTTP头中包含了明文的cookie。
* 攻击者可以嗅探流量，记录cookie。

测试网站是否存在该漏可以进行如下检测：
1. 检测网站是否同时支持HTTP和HTTPS协议
2. 检测cookie是否包含“Secure”标志


##### SSL Strip

一些应用程序同时支持HTTP和HTTPS，为了可用性或者便于用户能输入两者而抵达站点。通常用户通过链接或者跳转进入HTTPS站点。典型的个人网银站点就是类似的配置，通过HTTP页面中内嵌的HTTPS登陆页面或表单属性进行。

攻击者处于一个特权位置 - 如同SSL strip [8] 中描述的 - 能够截获用户进入HTTP站点的流量，并操作该流量在HTTPS下进行中间人攻击。同时支持HTTP和HTTPS的应用程序存在该漏洞。


#### 通过HTTP代理测试

在公司内部环境中，测试者可能发现无法直接访问服务，他们需要通过HTTP代理的CONNECT方法来访问[36]。许多工具在这种场景下无法正常使用，因为他们尝试直接访问响应TCP端口来进行SSL/TLS握手。通过中继程序的帮助如socat[37]，测试者可以在HTTP代理之后使用这些工具。


##### 例10： 通过HTTP代理测试

为了通过10.13.37.100:3128的代理来连接destined.application.lan:443，按照如下运行socat：

```
$ socat TCP-LISTEN:9999,reuseaddr,fork PROXY:10.13.37.100:destined.application.lan:443,proxyport=3128
```

接着就可以将所有目标指向localhost:9999：

```
$ openssl s_client -connect localhost:9999
```

所有指向localhost:9999的连接就能被socat通过代理高效的连接到destined.application.lan:443了。


### 配置审查

#### 测试弱SSL/TLS加密套件

检查提供HTTPS服务的web服务器配置。如果web应用程序提供其他SSL/TLS包装服务，同样也需要检查。


##### 例11： Windows 服务器

通过注册表项检查微软Windows服务器（2000,2003,2008）的配置：

```
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\
```

包括一些子项目，含有加密算法，协议以及密钥交换算法。


##### 例12： Apache

为了检查Apache2服务器支持的加密套件和协议，打开ssl.conf文件，查找SSLCipherSuite，SSLProtocol，SSLHonorCipherOrder，SSLInsecureRenegotiation和SSLCompression项目。

#### 测试SSL证书有效性 - 客户端和服务端

在服务端和客户端同时检查应用程序使用的证书的有效性。虽然证书主要使用在web服务器中，但是也可能有额外的SSL保护的交流通道（如访问DBMS）。测试者应该检查应用程序架构来识别出所有SSL保护的信道。

### 测试工具
* [21][Qualys SSL Labs - SSL Server Test|https://www.ssllabs.com/ssltest/index.html]: 面向互联网的在线扫描工具。
* [27] [Tenable - Nessus Vulnerability Scanner|http://www.tenable.com/products/nessus]: 包含一些测试SSL相关漏洞、证书漏洞以及HTTP基本认证方面的插件。
* [32] [TestSSLServer|http://www.bolet.org/TestSSLServer/]: windows可执行的一个java扫描器，包括测试加密套件、CRIME和BEAST。
* [33] [sslyze|https://github.com/iSECPartners/sslyze]: 一个检测SSL/TLS漏洞的python脚本。
* [28] [SSLAudit|https://code.google.com/p/sslaudit/]: 一个参照Qualys SSL Labs评估指南的perl/windows扫描器。
* [29] [SSLScan|http://sourceforge.net/projects/sslscan/] with [SSL Tests|http://www.pentesterscripting.com/discovery/ssl_tests]: 一个SSL扫描器和用来枚举SSL漏洞的SSL包装器。
* [31] [nmap|http://nmap.org/]: 主要用来识别基于SSL的服务以及检查证书和SSL/TLS漏洞。特别是包含了检测 [Certificate and SSLv2|http://nmap.org/nsedoc/scripts/ssl-cert.html] 的脚本，以及支持 [SSL/TLS protocols/ciphers|http://nmap.org/nsedoc/scripts/ssl-enum-ciphers.html]的内部评估。
* [30] [curl|http://curl.haxx.se/] and [openssl|http://www.openssl.org/]: 可以用来手动查询SSL/TLS服务。
* [9] [Stunnel|http://www.stunnel.org]: 一个值得关注的SSL客户端，SSL代理，允许不支持SSL的工具能使用SSL服务。
* [37] [socat| http://www.dest-unreach.org/socat/]: 多用途中继程序。
* [38] [testssl.sh| https://testssl.sh/ ]


### 参考资料
**OWASP 资源**
* [5] [OWASP Testing Guide - Testing for cookie attributes (OTG-SESS-002)|https://www.owasp.org/index.php/Testing_for_cookies_attributes_(OTG-SESS-002)]
* [4] [OWASP Testing Guide - Test Network/Infrastructure Configuration (OTG-CONFIG-001)|https://www.owasp.org/index.php/Test_Network/Infrastructure_Configuration_(OTG-CONFIG-001)]
* [6] [OWASP Testing Guide - Testing for HTTP_Strict_Transport_Security (OTG-CONFIG-007)|https://www.owasp.org/index.php/Test_HTTP_Strict_Transport_Security_(OTG-CONFIG-007)]
* [2] [OWASP Testing Guide - Testing for Sensitive information sent via unencrypted channels (OTG-CRYPST-003)|https://www.owasp.org/index.php/Testing_for_Sensitive_information_sent_via_unencrypted_channels_(OTG-CRYPST-003)]
* [3] [OWASP Testing Guide - Testing for Credentials Transported over an Encrypted Channel (OTG-AUTHN-001)|https://www.owasp.org/index.php/Testing_for_Credentials_Transported_over_an_Encrypted_Channel_(OTG-AUTHN-001)]
* [22] [OWASP Cheat sheet - Transport Layer Protection|https://www.owasp.org/index.php/Transport_Layer_Protection_Cheat_Sheet]
* [23] [OWASP TOP 10 2013 - A6 Sensitive Data Exposure|https://www.owasp.org/index.php/Top_10_2013-A6-Sensitive_Data_Exposure]
* [24] [OWASP TOP 10 2010 - A9 Insufficient Transport Layer Protection|https://www.owasp.org/index.php/Top_10_2010-A9-Insufficient_Transport_Layer_Protection]
* [25] [OWASP ASVS 2009 - Verification 10|https://code.google.com/p/owasp-asvs/wiki/Verification_V10]
* [26] [OWASP Application Security FAQ - Cryptography/SSL|https://www.owasp.org/index.php/OWASP_Application_Security_FAQ#Cryptography.2FSSL]


**白皮书**
* [1] [RFC5246 - The Transport Layer Security (TLS) Protocol Version 1.2 (Updated by RFC 5746, RFC 5878, RFC 6176)|http://www.ietf.org/rfc/rfc5246.txt]
* [36] [RFC2817 - Upgrading to TLS Within HTTP/1.1|]
* [34] [RFC6066 - Transport Layer Security (TLS) Extensions: Extension Definitions|http://www.ietf.org/rfc/rfc6066.txt]
* [11] [SSLv2 Protocol Multiple Weaknesses |http://osvdb.org/56387]
* [12] [Mitre - TLS Renegotiation MiTM|http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2009-3555]
* [13] [Qualys SSL Labs - TLS Renegotiation DoS|https://community.qualys.com/blogs/securitylabs/2011/10/31/tls-renegotiation-and-denial-of-service-attacks]
* [10] [Qualys SSL Labs - SSL/TLS Deployment Best Practices|https://www.ssllabs.com/projects/best-practices/index.html]
* [14] [Qualys SSL Labs - SSL Server Rating Guide|https://www.ssllabs.com/projects/rating-guide/index.html]
* [20] [Qualys SSL Labs - SSL Threat Model|https://www.ssllabs.com/projects/ssl-threat-model/index.html]
* [18] [Qualys SSL Labs - Forward Secrecy|https://community.qualys.com/blogs/securitylabs/2013/06/25/ssl-labs-deploying-forward-secrecy]
* [15] [Qualys SSL Labs - RC4 Usage|https://community.qualys.com/blogs/securitylabs/2013/03/19/rc4-in-tls-is-broken-now-what]
* [16] [Qualys SSL Labs - BEAST|https://community.qualys.com/blogs/securitylabs/2011/10/17/mitigating-the-beast-attack-on-tls]
* [17] [Qualys SSL Labs - CRIME|https://community.qualys.com/blogs/securitylabs/2012/09/14/crime-information-leakage-attack-against-ssltls]
* [7] [SurfJacking attack|https://resources.enablesecurity.com/resources/Surf%20Jacking.pdf]
* [8] [SSLStrip attack|http://www.thoughtcrime.org/software/sslstrip/]
* [19] [PCI-DSS v2.0|https://www.pcisecuritystandards.org/security_standards/documents.php]
* [35] [Xiaoyun Wang, Hongbo Yu: How to Break MD5 and Other Hash Functions| http://link.springer.com/chapter/10.1007/11426639_2]


