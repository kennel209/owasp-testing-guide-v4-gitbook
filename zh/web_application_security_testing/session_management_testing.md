# 会话管理测试



One of the core components of any web-based application is the mechanism by which it controls and maintains the state for a user interacting with it. This is referred to this as Session Management and is defined as the set of all controls governing state-full interaction between a user and the web-based application. This broadly covers anything from how user authentication is performed, to what happens upon them logging out.


HTTP is a stateless protocol, meaning that web servers respond to client requests without linking them to each other.  Even simple application logic requires a user's multiple requests to be associated with each other across a "session”.  This necessitates third party solutions – through either Off-The-Shelf (OTS) middleware and web server solutions, or bespoke developer implementations.  Most popular web application environments, such as ASP and PHP, provide developers with built-in session handling routines. Some kind of identification token will typically be issued, which will be referred to as a “Session ID” or Cookie.
<br>


There are a number of ways in which a web application may interact with a user.  Each is dependent upon the nature of the site, the security, and availability requirements of the application. Whilst there are accepted best practices for application development, such as those outlined in the [OWASP Guide to Building Secure Web Applications](https://www.owasp.org/index.php/OWASP_Guide_Project), it is important that application security is considered within the context of the provider’s requirements and expectations.

This chapter covers the following topics:
<br>

* [会话管理绕过测试 (OTG-SESS-001)](./testing_for_bypassing_session_management_schema_otg-sess-001.html)
* [Cookies属性测试 (OTG-SESS-002)](./testing_for_cookies_attributes_otg-sess-002.html)
* [会话固定测试 (OTG-SESS-003)](./testing_for_session_fixation_otg-sess-003.html)
* [会话令牌泄露测试 (OTG-SESS-004)](./testing_for_exposed_session_variables_otg-sess-004.html)
* [跨站点请求伪造（CSRF）测试 (OTG-SESS-005)](./testing_for_cross_site_request_forgery_csrf_otg-sess-005.html)
* [登出功能测试 (OTG-SESS-006)](./testing_for_logout_functionality_otg-sess-006.html)
* [会话超时测试 (OTG-SESS-007)](./test_session_timeout_otg-sess-007.html)
* [会话令牌重载测试 (OTG-SESS-008)](./testing_for_session_puzzling_otg-sess-008.html)
