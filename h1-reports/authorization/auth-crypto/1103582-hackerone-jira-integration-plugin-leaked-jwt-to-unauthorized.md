# HackerOne Jira Integration Plugin JWT Exposure to Unauthorized Users

## Metadata
- **Source:** HackerOne
- **Report:** 1103582 | https://hackerone.com/reports/1103582
- **Submitted:** 2021-02-15
- **Reporter:** updatelap
- **Program:** HackerOne
- **Bounty:** Not specified in writeup
- **Severity:** high
- **Vuln:** Broken Access Control, Missing Authorization Checks, Privilege Escalation, Sensitive Information Disclosure, Insecure Direct Object References
- **CVEs:** None
- **Category:** auth-crypto

## Summary
The HackerOne for Jira application fails to verify user permissions before generating JWT tokens for Jira instance linking. Users with Basic privileges, who should have no access to application configuration, can obtain valid JWT tokens and link the Jira instance to their own HackerOne account, bypassing administrative controls and gaining unauthorized access to private projects and data.

## Attack scenario
1. Attacker creates or joins a Jira Cloud instance with Basic user role
2. Administrator installs HackerOne for Jira plugin on the shared instance
3. Attacker navigates to /plugins/servlet/ac/com.hackerone/get-started-with-hackerone-on-jira (configuration page accessible without permission checks)
4. Application generates valid JWT token without validating attacker's role or permissions
5. Attacker extracts JWT from claim-app URL and uses it to link the entire Jira instance to their own HackerOne account
6. Attacker can now create issues in restricted private projects, read private project names, inject comments, and link private issues to their HackerOne reports

## Root cause
The HackerOne for Jira plugin servlet fails to perform role-based access control (RBAC) checks before rendering the configuration page and generating JWT tokens. The application accepts requests from any authenticated user regardless of their privilege level (Basic, Trusted, Site Admin), violating the principle of least privilege and Jira's own permission model.

## Attacker mindset
An insider threat or opportunistic user within a Jira instance seeks to escalate privileges and gain unauthorized access to sensitive security data. The attacker recognizes that the integration plugin does not validate permissions, allowing them to hijack the integration process and assume control of the Jira-to-HackerOne connection to exfiltrate or manipulate private vulnerability data.

## Defensive takeaways
- Implement mandatory role-based access control (RBAC) checks in all privileged endpoints, especially integration/configuration pages
- Verify user permissions against the application's permission model before generating sensitive tokens like JWT
- Apply principle of least privilege: restrict configuration pages to Site Administrator role only
- Validate user context and authorization on every request, not just at entry points
- Include permission validation in token generation logic, not just in UI rendering
- Log and audit access attempts to configuration endpoints, especially from non-admin users
- Implement rate limiting and anomaly detection on JWT generation endpoints
- Document permission requirements clearly in plugin documentation and enforcement code
- Perform security testing of third-party integrations with multiple user roles before deployment
- Use Jira's built-in permission checking APIs rather than custom authorization logic

## Variant hunting
Check other Atlassian Marketplace plugins for similar JWT/token generation without permission validation
Test other configuration pages in HackerOne for Jira plugin for authorization bypass
Examine other integrations that generate linking tokens (OAuth flows, API key generation) for permission checks
Test if other token types (API keys, OAuth tokens, temporary credentials) have similar issues
Check if permission validation can be bypassed via direct API calls vs UI access
Test whether JWT tokens generated for one instance can be reused on different Jira instances
Investigate if JWT validation on HackerOne backend properly validates issuer and audience claims
Check other Atlassian add-ons and marketplace apps for similar authorization flaws

## MITRE ATT&CK
- T1190
- T1546
- T1078
- T1552
- T1199
- T1566
- T1087
- T1530

## Notes
This vulnerability demonstrates a critical gap between the Atlassian permission model and third-party plugin implementation. The plugin did not properly integrate with Jira's native permission checking mechanisms. The impact is amplified because the JWT token provides broad access to instance configuration, not just individual resource access. The attacker's ability to hijack the admin integration link also creates a denial-of-service impact where legitimate administrators cannot complete setup.

## Full report
<details><summary>Expand</summary>

**Summary:**
HackerOne provides an application tool [HackerOne for Jira](https://marketplace.atlassian.com/vendors/1214355/hackerone), an application that allows programs to track security issues through a jira instance. After testing the integration feature in the application, it was found that the application leads to the leakage of the `JWT` to unauthorized users.

### About jira:

Jira Cloud allows the system administrator to add users with different Roles such as "__Basic, Trusted, and Site administrator__" with the highest authority being "Site administrator" and least "Basic". Based on these Roles allows:

1. The administrator can fully manage the account by accessing all projects, issues, dashboards and configuring applications.
2. Access to specific projects or issues. It is not possible to access to configure applications or to change any of the account settings.

**Description:**
As we mentioned earlier, the HackerOne for Jira application, after installing it, creates an integration between the HackerOne platform and the atlassian where cases can be synchronized from HackerOne to atlassian
  And vice versa. So, after installation, __administrators__  jira account is allowed to go https://YOUDOMIN.atlassian.net/plugins/servlet/ac/com.hackerone/get-started-with-hackerone-on-jira When going to this page, the following message will appear:

{F1196098}

When you click on "click here", you will be directed to a link  this "`https://hackerone.com/apps/atlassian/claim-app?jwt=<TOKEN>`" containing JWT parameter to complete the integration process. So. Based on the __About jira description__, an employee with "`BSSIC`" privileges is not allowed to access the application configuration.  After testing if the [HackerOne for Jira](https://marketplace.atlassian.com/vendors/1214355/hackerone) app. checks the permissions of Jira users before providing the user with the `JWT`, it is found that the  [HackerOne for Jira] application does not verify the user's permissions and generates the JWT code for a user with `basic privileges`. This allows this malicious user to link their hackerone account to an instance of a jira that they do not own. Which leads, for example, to leak names of private projects or create issues in private projects .. etc

{F1196129}

The normal or expected behavior that the tool should work with is to verify the role of the user who requests the configuration page, and if he does not have the privilege to display the page, a message similar to this should appear.
{F1196135}

### Steps To Reproduce

1. Go to Jira cloud and create jira instance.
2. Add user with `Basic` roles.
1. The administrator creates 8 projects and is restricted to accessing 5 projects for the administrator only.
3. Admin Install [HackerOne for Jira](https://marketplace.atlassian.com/vendors/1214355/hackerone) app.
4. User Go to {BaseUrl}/plugins/servlet/ac/com.hackerone/get-started-with-hackerone-on-jira
5. User steals a hackerone generated configuration link `https://hackerone.com/apps/atlassian/claim-app?jwt=<TOKEN>` and uses it to link a Jira instance to their hackerone account
1. Now user can create issue in private project or linked H1 report with private issue project.


PoC █████████

## Impact

1. attacker can Create issue in priavet jira Project
1. attacker can Leaked priavet jira Project name.
1. When an administrator tries to link an instance of jira to the H1 account, they will not be able to because the instance has been linked to the attacking H1 account 

{F1196177}
1. Injecting comments on private issues into private jira projects.
1. Linking private jira issues with attacker H1 report

</details>

---
*Analysed by Claude on 2026-05-24*
