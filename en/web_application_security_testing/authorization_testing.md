# Authorization Testing

Authorization is the concept of allowing access to resources only to those permitted to use them. Testing for Authorization means understanding how the authorization process works, and using that information to circumvent the authorization mechanism.<br><br>
Authorization is a process that comes after a successful authentication, so the tester will verify this point after he holds valid credentials, associated with a well-defined set of roles and privileges. During this kind of assessment, it should be verified if it is possible to bypass the authorization schema, find a path traversal vulnerability, or find ways to escalate the privileges assigned to the tester.

* [Testing Directory traversal/file include (OTG-AUTHZ-001)](./testing_directory_traversalfile_include_otg-authz-001.html)
* [Testing for bypassing authorization schema (OTG-AUTHZ-002)](./testing_for_bypassing_authorization_schema_otg-authz-002.html)
* [Testing for Privilege Escalation (OTG-AUTHZ-003)](./testing_for_privilege_escalation_otg-authz-003.html)
* [Testing for Insecure Direct Object References (OTG-AUTHZ-004)](./testing_for_insecure_direct_object_references_otg-authz-004.html)
