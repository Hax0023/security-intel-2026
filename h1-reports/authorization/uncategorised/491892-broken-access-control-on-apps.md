# Broken Access Control on Rocket.Chat Application Installation

## Metadata
- **Source:** HackerOne
- **Report:** 491892 | https://hackerone.com/reports/491892
- **Submitted:** 2019-02-06
- **Reporter:** theappsec
- **Program:** Rocket.Chat on HackerOne
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Broken Access Control (CWE-284), Missing Authorization Check, Privilege Escalation, Insufficient Access Control
- **CVEs:** None
- **Category:** uncategorised

## Summary
Non-administrative users could upload and install arbitrary applications into Rocket.Chat instances without proper authorization checks. Attackers could additionally activate installed applications by manipulating the app ID in request payloads, enabling deployment of malicious apps with full system access.

## Attack scenario
1. Attacker creates a low-privilege user account on the target Rocket.Chat instance
2. Attacker navigates to /admin/app/install endpoint which lacks proper authorization validation
3. Attacker uploads a malicious application package containing arbitrary code in app.json with attacker-controlled app ID
4. Attacker sends POST request to /api/apps/<attacker_controlled_id>/status with status manually_enabled
5. Malicious app activates without admin approval and executes with application-level privileges
6. Attacker gains ability to intercept messages, manipulate users, exfiltrate data, or pivot to underlying infrastructure

## Root cause
The /admin/app/install endpoint and /api/apps/<ID>/status endpoint lack proper authorization checks to verify administrative privileges before allowing application upload and activation. Access control enforcement was either missing entirely or relied on client-side validation rather than server-side authorization logic.

## Attacker mindset
An attacker would recognize that application management interfaces often require administrative privileges. By attempting to access admin features as a regular user, the attacker discovers the authorization checks are missing. This allows them to abuse the application installation mechanism as an initial access point to compromise the entire Rocket.Chat instance and potentially the underlying infrastructure.

## Defensive takeaways
- Implement server-side authorization checks on ALL sensitive endpoints, not just client-side restrictions
- Use a centralized authorization framework that validates user roles/permissions before executing privileged operations
- Restrict application installation to administrative users only with explicit capability checks
- Validate that the authenticated user has 'admin' or 'app-management' roles before allowing app upload/activation
- Implement audit logging for all application installation and activation events
- Use allowlist approach for app IDs rather than allowing user-controlled specification of arbitrary IDs
- Apply principle of least privilege - application runtime should have minimal necessary permissions
- Regularly audit admin-only endpoints to ensure authorization is properly enforced
- Consider sandboxing or signing requirements for uploaded applications

## Variant hunting
Check other admin endpoints (/admin/users, /admin/rooms, /admin/plugins) for similar missing authorization checks
Test application update and deletion endpoints for authorization bypass
Verify if other plugin/extension management systems have similar vulnerabilities
Test if authorization bypass applies to other privileged operations like user role assignment or workspace settings modification
Check if RBAC (Role-Based Access Control) is consistently applied across all management APIs

## MITRE ATT&CK
- T1190
- T1548
- T1562
- T1566
- T1199

## Notes
This is a classic broken access control vulnerability in admin functionality. The impact is severe as it allows arbitrary code execution through malicious applications. The fix is straightforward - add authorization checks - but the vulnerability suggests inadequate security review of privileged endpoints. Version 0.73.2 is affected; unclear if fixed in later versions from report content alone.

## Full report
<details><summary>Expand</summary>

**Summary:** 

The user without administrative privileges can upload and install any Application into the rocket.chat
As ID of application is controlled in the app.json file (which is controlled by uploader) user can also activate the app.

## Releases Affected:

  * 0.73.2

## Steps To Reproduce:
- User log-in into the chat
- User open the following link:

```
http://<rocket-chat.link>>/admin/app/install
```
- Upload any app
- Activate it by send the following POST request to the installed app:

```http
POST /api/apps/<ID_of_the_installed_App>/status HTTP/1.1
Host: rocket-chat.link
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Content-Type: application/json
X-User-Id: [redacted]
X-Auth-Token: [redacted]
X-Requested-With: XMLHttpRequest
Cookie: [redacted]
DNT: 1
Connection: close
Content-Length: 29

{"status":"manually_enabled"}
```

## Supporting Material/References:

You can see the uploading process in the attached video. Left user is admin, right -  user without any additional privileges. 

## Suggested mitigation
Managing apps should be available to admins only.

## Impact

Users can install and activate malicious apps into the rocket.chat.

</details>

---
*Analysed by Claude on 2026-05-24*
