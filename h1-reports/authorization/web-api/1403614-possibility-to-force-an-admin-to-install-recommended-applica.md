# CSRF vulnerability in Nextcloud recommended apps installation endpoint

## Metadata
- **Source:** HackerOne
- **Report:** 1403614 | https://hackerone.com/reports/1403614
- **Submitted:** 2021-11-18
- **Reporter:** igorpyan
- **Program:** Nextcloud
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Cross-Site Request Forgery (CSRF), Missing CSRF Token Validation, Improper Access Control
- **CVEs:** CVE-2022-24889
- **Category:** web-api

## Summary
The Nextcloud endpoint /nextcloud/index.php/core/apps/recommended is vulnerable to CSRF attacks as it accepts GET requests without validating anti-CSRF tokens. An attacker can trick an admin into visiting a malicious page to automatically trigger installation of recommended applications, expanding the attack surface of the Nextcloud instance.

## Attack scenario
1. Attacker identifies that the /core/apps/recommended endpoint is accessible via GET without CSRF protection
2. Attacker creates a malicious webpage containing an embedded request to the vulnerable endpoint (e.g., via img tag, iframe, or fetch request)
3. Attacker socialengineers or tricks a Nextcloud administrator into visiting the malicious webpage
4. Admin's browser automatically sends authenticated request to the vulnerable endpoint due to existing session cookies
5. The recommended applications installation process begins automatically without explicit admin consent
6. Potentially unwanted or malicious applications become installed on the Nextcloud instance

## Root cause
The endpoint /core/apps/recommended lacks CSRF token validation on GET requests and initiates application installation automatically without requiring explicit user action or token verification. The use of GET method for state-changing operations violates REST principles and enables CSRF attacks.

## Attacker mindset
An attacker seeks to expand the attack surface of a target Nextcloud instance by coercing admins into installing applications that could be exploited for further compromise. This could be part of a supply chain attack or persistence mechanism.

## Defensive takeaways
- Implement mandatory CSRF token validation (requestToken) for all state-changing operations, especially administrative actions
- Convert state-changing operations from GET to POST/PUT/DELETE HTTP methods
- Require explicit user interaction (manual click/confirmation) for sensitive operations like application installation
- Implement Content Security Policy (CSP) headers to prevent unauthorized frame embedding and script execution
- Add rate limiting on administrative endpoints to detect automated exploitation attempts
- Log and alert on application installation activities for anomaly detection
- Use SameSite cookie attributes to mitigate CSRF attacks browser-side

## Variant hunting
Check other /core/apps/* endpoints for similar CSRF vulnerabilities
Audit all administrative endpoints that modify system state for CSRF protection
Search for other GET endpoints that trigger automatic installation or configuration changes
Review plugin management, theme installation, and extension management endpoints
Test theme installation endpoints for the same vulnerability pattern
Examine app update endpoints for CSRF protection

## MITRE ATT&CK
- T1189
- T1566
- T1548

## Notes
Affected version: Nextcloud Server 22.2.2 (at least). The vulnerability is particularly dangerous in multi-tenant or shared Nextcloud instances where admins may visit untrusted websites. The fix should prioritize converting to POST requests with proper token validation over simple token addition to GET requests.

## Full report
<details><summary>Expand</summary>

## Summary:
Endpoint /nextcloud/index.php/core/apps/recommended is accessible via GET http method and doesn't check anti-csrf token. If an admin visits this endpoint in a browser the process of installation of recommended applications begins immediately.

## Steps To Reproduce:
1. an attacker creates a malicious page on controlled domain
1. an attacker enforce an admin to visit this page
1. an admin visits this page
1. applications will be installed in a while

## Affected version:
nextcloud/server: 22.2.2 (at least)

## Recommendation:
require requesttoken for this GET query
or you can change behaviour so to initiate the installation process by manual click (POST query with checking of requesttoken)

## [attachment / reference]
{F1517676}

## Impact

Increasing of attack surface.
Any unused plugins should be disabled or removed. But this way allows to install them.

</details>

---
*Analysed by Claude on 2026-05-24*
