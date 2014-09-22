# 说明

### 欢迎使用 OWASP 测试指南 4.0

“OWASP 的宗旨:技术的开放与协作”<br>
我们意识到这份新的测试指南4.0将会成为实施web应用渗透测的标准。
-- [Matteo Meucci](https://www.owasp.org/index.php/User:Mmeucci)


OWASP 感谢每一个作者,修订人员以及编辑人员,没有他们的努力,这份测试指南也没有今天。如果你有任何意见或建议,请发 E-mail 到测试指南邮箱:

> http://lists.owasp.org/mailman/listinfo/owasp-testing

或者 E-mail 给该指南的策划者:
[Andrew Muller](mailto:andrew.muller@owasp.org)
[Matteo Meucci](mailto:matteo.meucci@owasp.org)


### Version 4.0

OWASP测试指南第四版比起第3版在三个方面更加改善了：


1. 这份指南整合了另外两个旗舰级的OWASP文档：开发者指南和代码评估指南。我们重新编排了章节和测试顺序，目的就是通过测试和代码评估来达到开发者指南中描述的安全控制。

2. 所有章节都被改进，并扩充至87个测试案例（v3版本是64个），包括4项新的章节：
    - 身份鉴别管理测试 <br>
    - 错误处理 <br>
    - 密码学 <br>
    - 客户端测试 <br><br>

3. 在指南中我们希望大家不仅仅简单应用测试案例，更加鼓励安全测试人员整合和发现更多的相关测试案例。如果发现的测试案例能广泛应用，我们鼓励大家分享他们，并回馈测试指南。这将建立起更加丰富的安全知识，并将指南发展过程迭代化，而不是仅仅单次发展。


### 版权和许可

Copyright (c) 2014 The OWASP Foundation.

本文档由[Creative Commons 2.5 License](http://creativecommons.org/licenses/by-sa/2.5/)许授权。请阅读并理解该文档的许可和版权。


### 修订历史

测试指南第四版将于2014年发布。这份测试指南由 Dan Cuthbert 作为第一位编辑于 2003 年第一次发布。2005年这份测试指南移交给 Eoin Keary 并转变成 Wiki 超文本系统。Matteo Meucci 现在接管这份测试指南,成为 OWASP 测试指南项目负责人。Andrew Muller 自2012年起成为该项目共同负责人。

**2014 年**
- OWASP 测试指南第 4 版

**2008 年 9 月 15 日**
- OWASP 测试指南第 3 版

**2006 年 12 月 25 日**
- OWASP 测试指南第 2 版

**2004 年 7 月 14 日**
- OWASP WEB 应用安全渗透指引列表第 1.1 版

**2004 年 12 月**
- OWASP 测试指南第 1 版


### 编辑

**Andrew Muller**: 自 2013 年, OWASP 测试指南项目负责人。<BR>

**Matteo Meucci**: 自 2007 年, OWASP 测试指南项目负责人。<BR>

**Eoin Keary**: 2005-2007 OWASP 测试指南项目负责人。<BR>

**Daniel Cuthbert**: 2003-2005 OWASP 测试指南项目负责人。


### 第四版作者

* Matteo Meucci
* Pavol Luptak
* Marco Morana
* Giorgio Fedon
* Stefano Di Paola
* Gianrico Ingrosso
* Giuseppe Bonfà
* Andrew Muller
* Robert Winkel
* Roberto Suggi Liverani
* Robert Smith
* Tripurari Rai
* Thomas Ryan
* Tim Bertels
* Cecil Su
* Aung KhAnt
* Norbert Szetei
* Michael Boman
* Wagner Elias
* Kevin Horvat
* Tom Brennan
* Juan Galiana Lara
* Sumit Siddharth
* Mike Hryekewicz
* Simon Bennetts
* Ray Schippers
* Raul Siles
* Jayanta Karmakar
* Brad Causey
* Vicente Aguilera
* Ismael Gonçalves
* David Fern
* Tom Eston
* Kevin Horvath
* Rick Mitchell
* Eduardo Castellanos
* Simone Onofri
* Harword Sheen
* Amro AlOlaqi
* Suhas Desai
* Ryan Dewhurst
* Zaki Akhmad
* Davide Danelon
* Alexander Antukh
* Thomas Kalamaris
* Alexander Vavousis
* Clerkendweller
* Christian Heinrich
* Babu Arokiadas
* Rob Barnes
* Ben Walther


### 第四版审核人员

* Davide Danelon
* Andrea Rosignoli
* Irene Abezgauz
* Lode Vanstechelman
* Sebastien Gioria
* Yiannis Pavlosoglou
* Aditya Balapure

### 第三版作者

* Anurag Agarwwal
* Daniele Bellucci
* Ariel Coronel
* Stefano Di Paola
* Giorgio Fedon
* Adam Goodman
* Christian Heinrich
* Kevin Horvath
* Gianrico Ingrosso
* Roberto Suggi Liverani
* Kuza55
* Pavol Luptak
* Ferruh Mavituna
* Marco Mella
* Matteo Meucci
* Marco Morana
* Antonio Parata
* Cecil Su
* Harish Skanda Sureddy
* Mark Roxberry
* Andrew Van der Stock

### 第三版审核人员

* Marco Cova
* Kevin Fuller
* Matteo Meucci
* Nam Nguyen
* Rick Mitchell

### 第二版作者

* Vicente Aguilera
* Mauro Bregolin
* Tom Brennan
* Gary	Burns
* Luca Carettoni
* Dan Cornell
* Mark Curphey
* Daniel Cuthbert
* Sebastien Deleersnyder
* Stephen DeVries
* Stefano Di Paola
* David	Endler
* Giorgio Fedon
* Javier Fernández-Sanguino
* Glyn Geoghegan
* Stan Guzik
* Madhura Halasgikar
* Eoin Keary
* David Litchfield
* Andrea Lombardini
* Ralph M. Los
* Claudio Merloni
* Matteo Meucci
* Marco	Morana
* Laura Nunez
* Gunter Ollmann
* Antonio Parata
* Yiannis Pavlosoglou
* Carlo Pelliccioni
* Harinath Pudipeddi
* Alberto Revelli
* Mark Roxberry
* Tom Ryan
* Anush Shetty
* Larry Shields
* Dafydd Studdard
* Andrew van der Stock
* Ariel	Waissbein
* Jeff Williams
* Tushar Vartak

### 第二版审核人员

* Vicente Aguilera
* Marco Belotti
* Mauro Bregolin
* Marco Cova
* Daniel Cuthbert
* Paul Davies
* Stefano Di Paola
* Matteo G.P. Flora
* Simona Forti
* Darrell Groundy
* Eoin Keary
* James Kist
* Katie McDowell
* Marco Mella
* Matteo Meucci
* Syed Mohamed A.
* Antonio Parata
* Alberto Revelli
* Mark Roxberry
* Dave Wichers

### 商标

* Java,Java Web 服务器,Sun Microsystems 有限公司 JSP 注册商标
* Merriam-Webster 有限公司 Merriam-Webster 注册商标
* 微软公司 Microsoft 注册商标
* Carnegie Mellon 大学服务商标 Octave
* VeriSign 有限公司安全认证注册商标 VeriSign 和 Thawte
* 美国 VISA 注册商标 Visa
* OWASP 基金会注册商标 OWASP

所有其他产品和公司的名称可能是其各自所有者的商标。长期使用本文档,不影响任何商标或服务标志的有效性。

### 致谢与译者声明

#### 第四版

由[风镰月舞](mailto:kennel209@gmail.com)结合第三版翻译内容，自行翻译，纯属自娱自乐。由于译者水平有限,并不保证译文完全正确,请参照英文版以准。

#### 第三版

本指南为业界首套系统的介绍应用安全测试的指导性文档。

数十位自愿者经过半年的辛苦工作,终于完成 OWASP 测试指南的翻译及校对。

##### OWASP 测试指南中文版修订

| 项目进展                | 时间            | 主要参与人 |
|-------------------------|-----------------|------------|
| OWASP 测试指南中文 V0.1 | 2009.7-2009.10  | FrankAaron |
| OWASP 测试指南中文 V0.2 | 2009.10-2009.11 | RIP        |
| OWASP 测试指南中文 V0.3 | 2009.11-2009.1  | Eric       |

##### 翻译及校对人员(排名不分先后)

* 程琼 (Microsoft)
* Frank Fan (DBAPPSECURITY)
* 贺佳琳 (Microsoft)
* 李伟荣 (Microsoft)
* 沈巍 (Microsoft)
* 王超 (Microsoft)
* 韦炜 (Microsoft)
* 张柏明 (Microsoft)
* 趙嘉言 (Microsoft)
* Aaron (DBAPPSECURITY)
* RIP (OWASP China Chair)

##### 声明

* 由于译者及校对人员水平有限,并不保证译文完全正确,请参照英文版以准。
* 非常感谢您的支持,有任何问题,请及时邮件到 RIP@OWASP.ORG。

