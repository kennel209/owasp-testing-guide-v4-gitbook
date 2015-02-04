# 会话管理测试

任何web应用程序的核心内容之一是控制和维持用户交互状态的机制。这通常被认为是会话管理，定义为一系列用于管理用户和web应用系统交互状态的措施。这广泛覆盖了从用户如何认证到他们登出时发生的任何事情。

HTTP是一个无状态的协议，意味着web服务器在相应用户请求时不需要联系其他请求。但甚至有时是简单的应用程序逻辑也可能需要通过一个“会话”来关联用户发送的多个请求。这便需要第三方解决方案的介入，通过现有的中间件或web服务器解决方案或者是定制的开发任务。大多数流行的web应用环境，如ASP和PHP，都给开发者提供了内置的会话处理例程。通常会提到一些身份令牌，被称作“会话ID”或者Cookie。

web应用程序有许多方法和用户交互。每种方法可以由于站点不同、安全等级不同和应用可用性要求不同而各不相同。同时也存在适用的应用程序开发安全实践，比如在[OWASP Guide to Building Secure Web Applications](https://www.owasp.org/index.php/OWASP_Guide_Project)中提到的。在软件提供者的需求和预期中考虑应用程序安全是非常重要的。

这个章节覆盖如下主题：

* [会话管理绕过测试 (OTG-SESS-001)](./testing_for_bypassing_session_management_schema_otg-sess-001.html)
* [Cookies属性测试 (OTG-SESS-002)](./testing_for_cookies_attributes_otg-sess-002.html)
* [会话固定测试 (OTG-SESS-003)](./testing_for_session_fixation_otg-sess-003.html)
* [会话令牌泄露测试 (OTG-SESS-004)](./testing_for_exposed_session_variables_otg-sess-004.html)
* [跨站点请求伪造（CSRF）测试 (OTG-SESS-005)](./testing_for_cross_site_request_forgery_csrf_otg-sess-005.html)
* [登出功能测试 (OTG-SESS-006)](./testing_for_logout_functionality_otg-sess-006.html)
* [会话超时测试 (OTG-SESS-007)](./test_session_timeout_otg-sess-007.html)
* [会话令牌重载测试 (OTG-SESS-008)](./testing_for_session_puzzling_otg-sess-008.html)

