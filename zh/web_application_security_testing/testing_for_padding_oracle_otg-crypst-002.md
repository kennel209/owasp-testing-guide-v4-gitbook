# 测试 Padding Oracle (OTG-CRYPST-002)



### 综述
Padding Oracle是指应用程序的一个解密客户端提供的加密数据（比如客户端中存储的内部会话状态）的功能函数在完成解密后的验证填充字节正确性的时候泄露了其状态（填充是否正确）。Padding Oracle漏洞的存在允许攻击者解密加密后的数据以及在不知道密码算法中的密钥的情况下加密任意数据。这可能导致敏感信息泄露或者导致权限提升漏洞，如果应用程序对加密数据的完整性有要求的话。

分组加密算法以一定字节的块为单位来加密数据。常见的加密算法使用8字节或16字节作为块长度。需要加密的数据长度如果不是加密算法使用的块长度的整数倍的话，需要通过一定的填充算法来对齐，使得解密程序能够去掉填充的数据。常见的填充模式是 PKCS#7 。他通过将不足的字节填充为剩余字节长度。


**例子:**

如果填充长度为5字节，那么在明文最后添加上5个 0x05 。

如果填充无法匹配使用的填充模式的形式就会发生错误。Padding Oracle 漏洞就是应用程序泄露了加密数据解密后的特定的填充错误情况。这可能通过直接曝出的异常信息（如 Java中的BadPaddingException），不同服务器响应信息的中细微差别或者其他的边信道发现（如耗时差异区别）。

一些密码的加密模式允许位反转攻击（bit-flipping attacks），也就是说在密文中反转一个比特位会引起明文中也反转比特位。在CBC加密数据中反转第N个数据块中的一个比特位会引起第N+1个数据块解密后的数据中相同比特位也反转。这个操作会导致第N个数据块的解密信息会成为垃圾信息。

Padding Oracle 攻击使攻击者能够在不知道加密密钥和加密算法的条件下解密数据，通过发送精心构造的密文数据来造成Padding Oracle，并观察返回的结果。这破坏了加密数据的秘密性。比如，在存储在客户端的会话数据的例子中，攻击者可以得到应用程序的内部状态和架构信息。

Padding Oracle 攻击也能使攻击者在不知道加密密钥和加密算法条件下加密任意明文数据。如果应用程序通过解密数据进行认证，并假定解密数据的完整性，那么攻击者可能通过操作内部会话状态来获得更高的权限。

### 如何测试
#### 黑盒测试

**测试Padding Oracle漏洞:**

首先必须识别出可能存在漏洞的输入点。通常需要满足下面条件：

1. 数据必须的加密的，通常看上去是随机数值的地方可能会是好的选择点。
2. 需要使用分组加密算法。解码后（通常使用Base64解码）的密文长度应该是常见的8字节或者16字节加密块的整数倍。不同的密文（如通过不同会话或操纵会话状态收集的）使用相同的分组块长度。


**例子:**

`Dg6W8OiWMIdVokIDH15T/A==` Base64解码后为 `0e 0e 96 f0 e8 96 30 87 55 a2 42 03 1f 5e 53 fc`。看上去像16字节的随机数据。

如果找到了这样的输入入口，验证是否可以对加密数据进行位篡改操作。通常情况下，这个Base64编码值会包含初始化向量（IV）。给定明文 `p` 和 分组块长度为 `n` 的加密算法，那么分组块的数量为 `b = ceil( length(b) / n)` 。由于IV的存在，加密字符串的长度为 `y=(b+1)*n`。

为了验证漏洞存在，解码字符串，反转倒数第二个数据块（`b-1`）的最后一比特位（位于 `y-n-1` 字节的最低位（LSB）），重新编码后发送。接着解码原始字符串，反转倒数第三个数据块（`b-2`）的最后一个比特位（位于`y-2*n-1`字节的最低位（LSB）），重新编码后发送。

如果已知的加密字符串是单个数据块（IV保存在服务器中或应用程序使用硬编码的IV），必须依次反转多个比特位。另一个方法是假装一个随机数据块，反转比特位来保证最后添加的数据块能便利所有的数值（0到255）。

测试用例和基本数值应该至少引发三种状态（解密时和解密之后）：
* 密文被解密，解密结果数据正确。
* 密文被解密，解密结果为垃圾数据，并触发了应用程序逻辑中的某些异常或错误处理程序。
* 由于填充错误导致的密文解密失败。

仔细比较这些响应结果。特别是寻找提示填充错误的异常和消息。如果存在这类的消息，那么应用程序存在Padding Oracle漏洞。如果上面提到的三种状态都能观察到（通过错误消息区别或时间边信道观测），很有可能在这个地方存在Padding Oracle漏洞。尝试进行Padding Oracle攻击来确认这一点。


**例子:**

* ASP.NET 在发生解密填充数据出错时候抛出 "System.Security.Cryptography.CryptographicException: Padding is invalid and cannot be removed." 异常。
* 在Java中为 javax.crypto.BadPaddingException 。
* 发生类似的解密错误都可能存在Padding Oracle攻击。


**期望结果:**

一个安全的实现是检查完整性，并只作出两个响应：成功和失败。同时保证没有边其他信道途径能确定内部错误状态。


#### 灰盒测试

**测试Padding Oracle漏洞:**

确认所有需要从客户端获取加密数据，服务器端参与解密过程的地方。这些代码应该满足下面的条件：

1. 密文的完整性应该被安全的机制所验证，像HMAC或一些认证过的加密模式如GCM或CCM。
2. 所有在解密中或者解密之后的处理过程中发现的错误已经被统一处理。


### 测试工具
* PadBuster - [https://github.com/GDSSecurity/PadBuster](https://github.com/GDSSecurity/PadBuster)
* python-paddingoracle - [https://github.com/mwielgoszewski/python-paddingoracle](https://github.com/mwielgoszewski/python-paddingoracle)
* Poracle - [https://github.com/iagox86/Poracle](https://github.com/iagox86/Poracle)
* Padding Oracle Exploitation Tool (POET) - [http://netifera.com/research/](http://netifera.com/research/)

**例子**
* Visualization of the decryption process - [http://erlend.oftedal.no/blog/poet/](http://erlend.oftedal.no/blog/poet/)


### 参考资料
**白皮书**
* Wikipedia - Padding oracle attack - [http://en.wikipedia.org/wiki/Padding_oracle_attack](http://en.wikipedia.org/wiki/Padding_oracle_attack)
* Juliano Rizzo, Thai Duong, "Practical Padding Oracle Attacks" - [http://www.usenix.org/event/woot10/tech/full_papers/Rizzo.pdf](http://www.usenix.org/event/woot10/tech/full_papers/Rizzo.pdf)
