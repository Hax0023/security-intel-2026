# Broken Access Control - Unauthenticated Admin Access via Direct Page Navigation in Oracle Apex Express

## Metadata
- **Source:** HackerOne
- **Report:** 1991290 | https://hackerone.com/reports/1991290
- **Submitted:** 2023-05-18
- **Reporter:** bulldawg
- **Program:** US Department of Defense (DoD) Bug Bounty
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Broken Access Control, Privilege Escalation, Insecure Direct Object Reference (IDOR), Missing Authentication
- **CVEs:** None
- **Category:** uncategorised

## Summary
A critical access control vulnerability in an Oracle Apex Express application allows unauthenticated users to gain full administrator privileges by directly navigating to page 56 (?p=165:56), which automatically redirects to the admin portal while granting admin session credentials. An adjacent application further exacerbates the issue by providing a 'Go To Admin' button that directly triggers the vulnerable endpoint.

## Attack scenario
1. Attacker discovers the application structure and identifies the page parameter format (p=165:XX)
2. Attacker attempts navigation to restricted page 45 (?p=165:45) and receives access denied
3. Attacker systematically enumerates page numbers and discovers page 56 (?p=165:56) lacks proper authorization checks
4. Attacker navigates to page 56, triggering automatic redirect to page 45 with valid admin session cookie/token
5. Attacker gains access to admin functions including user management, file upload/download, and document editing
6. Attacker exfiltrates sensitive data, modifies user roles, uploads malicious files, or deletes critical user accounts

## Root cause
The application fails to enforce authentication and authorization checks on page 56 before establishing an admin session. The page 56 endpoint appears to be designed for administrative setup or testing but was left accessible without proper access controls. Session establishment occurs without validating user identity or role eligibility. The redirects are implemented at the presentation layer without backend authorization validation.

## Attacker mindset
An attacker would recognize this as a classic access control bypass opportunity - the presence of an enumerable page parameter suggests systematic testing of page IDs is viable. The discovery of page 56 providing admin access represents a jackpot scenario for privilege escalation. The adjacent application's 'Go To Admin' button confirms the developers intended this functionality but failed to secure it. An attacker would immediately weaponize this for complete application compromise given the sensitive DoD context.

## Defensive takeaways
- Implement server-side authorization checks on every page/endpoint before rendering or establishing privileged sessions - never rely on client-side access control
- Use role-based access control (RBAC) validated on each request; verify user permissions against a secure backend store, not through page enumeration
- Remove or properly restrict administrative setup/testing pages from production environments; never use predictable numeric page identifiers without access controls
- Implement audit logging for all privilege escalation events and failed authorization attempts to detect exploitation
- Conduct security code review of all authentication and session management logic, particularly redirect mechanisms
- Apply principle of least privilege - default deny access and explicitly grant permissions rather than relying on blacklists
- Implement rate limiting and anomaly detection on privilege escalation attempts
- Regularly perform access control testing and penetration testing focusing on authorization bypass scenarios

## Variant hunting
Test other page numbers in the p= parameter range (165:1 through 165:999) for similar access control gaps
Enumerate other application IDs (p=160:XX, p=161:XX, etc.) for similar authorization bypasses
Check for similar endpoints in /apexcrrel/ path and other Oracle Apex applications
Test session manipulation - attempt to hijack or modify session tokens/cookies from page 56
Look for other 'Go To' or 'Admin' buttons across the application ecosystem that may trigger similar vulnerable redirects
Test parameter tampering - modify p=165:56 with additional parameters to bypass security checks
Review Oracle Apex default pages and known initialization/setup pages that might have similar issues
Test for insecure deserialization in session management that might allow privilege escalation

## MITRE ATT&CK
- T1190
- T1199
- T1566
- T1078
- T1110
- T1548

## Notes
This vulnerability exists in a US Department of Defense system, making it a critical national security risk. The presence of a 'Go To Admin' button in an adjacent application (p=164:5) suggests this was either intentional development that was never secured or a significant oversight in the authorization framework. The /apexcrrel/DISDI_PORTAL_DEV.login_admin endpoint name suggests development/testing functionality that reached production. Oracle Apex Express deployments should be audited organization-wide for similar patterns. The ability to manage admin users post-compromise significantly amplifies the impact, allowing attackers to persist access and cover tracks.

## Full report
<details><summary>Expand</summary>

**Summary:**
By navigating to https://████████.mil/apexcrrel/f?p=165:56, the user will automatically be redirected to the web application admin portal with Admin access.

**Description:**
There is a web application running at the following URL:

https://█████.mil/apexcrrel/f?p=165:1::::::

████

For context, this is a web application running on a Oracle Apex Express platform. The '165' in the 'p' parameter in the URL is a unique identifier for the web application. The '1' following the '165' represents the page that the user is viewing. 

The page '56' can be used to automatically obtain administrator access to this application. 

Here we can see that we can't access the 45th page (https://████.mil/apexcrrel/f?p=165:45) because we are not an Admin.

███████

However, navigating to the 56th page (https://██████████.mil/apexcrrel/f?p=165:56) automatically redirects to the 45th page but provides a valid admin session. 

█████████

We can also see that we have the ability to manage users, including admin users.

██████████

As a note, I found this due to the application at https://████.mil/apexcrrel/f?p=164:5::::::
This is a separate web application, given that the unique identifier is now 164. 

On this page there is a 'Go To Admin' button. When clicking this, it calls the /apexcrrel/DISDI_PORTAL_DEV.login_admin endpoint. This redirects the user to the 56th page, breaking the access control and providing Admin access.

███████

## Impact

This is a critical severity bug that impacts confidentiality, integrity, and availability. 

Confidentiality: An attacker can obtain first names, last names, email addresses, and filenames of uploaded files.
Integrity: An attacker can upload files, edit documents, and edit user roles
Availability: An attacker could remove all users, including admins, making it difficult for users to use the application.

## System Host(s)
█████.mil

## Affected Product(s) and Version(s)
Oracle Apex Express

## CVE Numbers


## Steps to Reproduce
1. To verify that you do not have any valid sessions to view the admin pages, visit https://██████.mil/apexcrrel/f?p=165:45
2. Now, navigate to https://█████████.mil/apexcrrel/f?p=165:56
3. You now have admin access to the application.

## Suggested Mitigation/Remediation Actions




</details>

---
*Analysed by Claude on 2026-05-24*
