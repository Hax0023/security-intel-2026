# Oracle ADF Faces Information Disclosure via Exposed Version Information and Unauthenticated Access

## Metadata
- **Source:** HackerOne
- **Report:** 1422641 | https://hackerone.com/reports/1422641
- **Submitted:** 2021-12-10
- **Reporter:** h3xr
- **Program:** Not specified (Redacted)
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Information Disclosure, Sensitive Data Exposure, Improper Access Control, Configuration Weakness, Privacy Violation
- **CVEs:** None
- **Category:** web-api

## Summary
Oracle ADF Faces framework was misconfigured with oracle.adf.view.rich.versionString.HIDDEN set to false, exposing sensitive version information in HTML source code. Multiple endpoints were accessible without proper authentication, allowing unauthenticated users to view and potentially modify sensitive user data including names and phone numbers.

## Attack scenario
1. Attacker discovers publicly accessible ADF Faces application endpoints through reconnaissance
2. Attacker accesses application without authentication and views HTML source code
3. Attacker identifies exposed version information and ADF framework details from meta tags/comments
4. Attacker uses version information to identify known vulnerabilities in outdated ADF components
5. Attacker navigates to sensitive endpoints (Link 3) that should require authentication but are accessible
6. Attacker modifies user profile data fields (First Name, Last Name, Phone Number) without authorization

## Root cause
Multiple configuration and security failures: (1) oracle.adf.view.rich.versionString.HIDDEN parameter set to false in production environment, (2) insufficient authentication controls on sensitive endpoints, (3) outdated Oracle ADF Faces framework version, (4) lack of input validation and authorization checks on data modification endpoints

## Attacker mindset
Opportunistic reconnaissance-driven attacker exploiting default/misconfigured settings. Initial discovery through code inspection revealed version information, leading to identification of outdated frameworks and known vulnerabilities. Escalation from information gathering to data manipulation demonstrated lack of access controls.

## Defensive takeaways
- Always set oracle.adf.view.rich.versionString.HIDDEN to true in production environments to prevent version enumeration
- Implement mandatory authentication checks on all sensitive endpoints, not relying on UI-level protection
- Regularly update Oracle ADF framework and all dependent components to latest patched versions
- Implement proper authorization controls before allowing data modification operations
- Remove or obfuscate debug information, comments, and framework identifiers from production code
- Conduct security configuration reviews specifically for framework-level security parameters
- Implement comprehensive input validation and CSRF protection on all state-changing operations

## Variant hunting
Search for other Oracle ADF applications with versionString.HIDDEN parameter set to false
Identify other Oracle ADF Faces installations by looking for characteristic error pages and meta tags
Test for similar misconfiguration in other Oracle Fusion middleware components
Look for unauthenticated access to other workflow/approval-related endpoints in ADF applications
Check for data modification endpoints lacking proper CSRF tokens in ADF applications
Enumerate other version disclosure vectors in Oracle products (Server headers, error messages, admin pages)

## MITRE ATT&CK
- T1190
- T1592
- T1526
- T1087
- T1078
- T1566
- T1589

## Notes
Report heavily redacted limiting complete analysis. Vulnerability chain demonstrates how information disclosure (version enumeration) can enable privilege escalation to unauthorized data modification. This is a configuration-based vulnerability rather than a code flaw, making it widespread in misconfigured ADF deployments. The presence of outdated ADF version combined with missing authentication represents a critical security posture issue.

## Full report
<details><summary>Expand</summary>

Hello, Team.

Found some interesting links which leads to information disclosure in █████
Link 1: [██████████]███
Link 2: [████████]██████████
Link 3: [██████████]███

Every link goes through https://██████to https://████
**For Link 3 is possible to change data in the fields: First Name, Last Name, Phone Number. Just click "██████".**

Viewing the code gives us some more info about the system:
```
██████
```

ADF ███████ is outdated
The [Ref. Page](https://docs.oracle.com/cd/E41362_01/web.1111/b31973/ap_config.htm) says:
*A.2.3.16 Version Number Information
Use the oracle.adf.view.rich.versionString.HIDDEN parameter to determine whether or not to display version information an a page's HTML. When the parameter is set to false, the HTML of an ADF Faces page contains information about the version of ADF Faces and other components used to create the page as shown in Example A-2.
When you create a new application, the parameter is set to true. It should also be set to true in a production environment. Set the parameter to false to display this version information for debugging information.
Note:
In a production environment, set this parameter to true to avoid security issues. It should be set to false only in a development environment for debugging purposes.*

[This Ref.](https://imlive.s3.amazonaws.com/Federal%20Government/ID188660931371312277217448460962608356160/Attachment_E_███S_Request_for_Role_Guide.pdf) points us that Link 3 is:
*██████S lists any █████s waiting for your approval. If there are none, there will be a message like the one in ███████. Click the Logout button to exit ██████████S.  You can use the link in your email to return to the ██████████.*

But we see the Logout button and can modify some data - so **perhaps** we are logged in.

## Impact

Sensitive information disclosure
Information modification
Privacy Violation

## System Host(s)
███████

## Affected Product(s) and Version(s)
Oracle ADF Faces

## CVE Numbers


## Steps to Reproduce
In the Desc. section

## Suggested Mitigation/Remediation Actions
Update Oracle ADF
Close sensitive information from unauthenticated users



</details>

---
*Analysed by Claude on 2026-05-24*
