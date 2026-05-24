# Unauthenticated Access to Private Bug Report Attachments via Broken Access Control (IDOR)

## Metadata
- **Source:** HackerOne
- **Report:** 3259610 | https://hackerone.com/reports/3259610
- **Submitted:** 2025-07-18
- **Reporter:** azraeldeathangel
- **Program:** Undisclosed
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Broken Access Control, Insecure Direct Object Reference (IDOR), Missing Authentication, Authorization Bypass
- **CVEs:** None
- **Category:** web-api

## Summary
The `/BugReport/Admin/Attachment/{id}` endpoint fails to enforce authentication and authorization checks, allowing unauthenticated attackers to access attachments from private bug reports by manipulating numeric IDs. This IDOR vulnerability exposes sensitive information including unpatched security issues, confidential business data, and personally identifiable information to complete compromise.

## Attack scenario
1. Attacker discovers the attachment endpoint pattern `/BugReport/Admin/Attachment/{id}` through reconnaissance or public information
2. Attacker sends a legitimate request with authentication to obtain a valid attachment ID (e.g., 1568600)
3. Attacker removes or omits authentication credentials from subsequent requests to the endpoint
4. Attacker systematically iterates through sequential numeric IDs (e.g., 1, 2, 3... 1568600, 1568601, etc.) to enumerate accessible attachments
5. Server responds with file contents for each valid ID without verifying user authorization or authentication status
6. Attacker gains access to confidential bug reports, security vulnerabilities, and sensitive data belonging to other users

## Root cause
The application implements object-level access control through assumption rather than explicit verification. The endpoint lacks middleware or code-level authorization checks that validate: (1) user authentication status, (2) user's relationship to the requested attachment, (3) user's role/permissions relative to the bug report. Numeric IDs enable easy enumeration without guessing.

## Attacker mindset
Low-effort, high-impact opportunism. Attacker recognizes that sequential IDs combined with absent authorization checks create trivial enumeration path to sensitive data. No special skills required—basic HTTP manipulation suffices. Motivation likely includes competitive intelligence, data harvesting, or reconnaissance for targeted attacks.

## Defensive takeaways
- Implement authentication enforcement as mandatory first-layer control; deny all unauthenticated requests to sensitive endpoints before any business logic executes
- Apply authorization checks at object level: verify authenticated user has explicit relationship to requested resource (e.g., user submitted the bug report, or is assigned to it)
- Replace sequential numeric IDs with cryptographically random identifiers (UUIDs, random tokens) to prevent enumeration attacks
- Use indirect references or access tokens that map to objects only for authorized users, implementing server-side session-based lookups
- Implement consistent access control patterns across codebase; establish framework-level enforcement (e.g., authorization middleware) rather than per-endpoint checks
- Add comprehensive logging of access attempts including failed authorization; establish alerting for repeated enumeration patterns
- Implement rate limiting and CAPTCHA challenges on direct object reference endpoints to impede mass enumeration
- Conduct security design review of all file/document retrieval endpoints to identify similar patterns
- Test all object-level access with positive (authorized) and negative (unauthorized) user cases in security testing

## Variant hunting
Check other `/Admin/*` endpoints for similar authentication bypass patterns
Test sibling endpoints like `/BugReport/Attachment/{id}`, `/Report/{id}/Download`, `/File/{id}` for identical authorization flaws
Examine other resources linked by sequential IDs: `/User/{id}`, `/Project/{id}`, `/Team/{id}`, `/Comment/{id}`
Test with different HTTP methods (POST, PUT, DELETE) against the attachment endpoint to identify additional IDOR variants
Investigate whether unauthenticated users can also enumerate valid IDs through error message timing differences or response codes
Check if authentication bypass exists for other premium/admin features by removing session tokens
Examine API endpoints separately from web UI endpoints; REST APIs often have weaker access control
Test for authorization bypass using predictable tokens or default credentials in other authentication schemes

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application (vulnerable endpoint exploitation)
- T1526 - Enumerate External Targets (ID enumeration)
- T1040 - Network Sniffing (auth header removal/observation)
- T1087 - Account Discovery (via IDOR enumeration of user-linked attachments)
- T1566 - Phishing (using discovered sensitive information for targeted attacks)
- T1040 - Network Sniffing/T1557 - Man-in-the-Middle (if credentials were transmitted unencrypted)

## Notes
This is a textbook IDOR vulnerability combining two critical flaws: (1) missing authentication enforcement, (2) missing authorization checks. The numeric ID space enables trivial enumeration. Report demonstrates proper vulnerability communication with clear reproduction steps. Lack of CVE assignment and bounty amount suggests report may be in disclosure process or from internal program. Unauthenticated access elevates severity to critical; this is not an inter-user authorization bypass but complete exposure to unauthenticated actors.

## Full report
<details><summary>Expand</summary>

The `/BugReport/Admin/Attachment/{id}` endpoint exposes attachments linked to private bug reports.
By manipulating the numeric ID in the URL, it’s possible to access attachments belonging to other users, including sensitive bug reports, without proper authorization checks.

This vulnerability works **even when unauthenticated**, meaning anyone who knows or guesses valid IDs can retrieve attachments.
This is a classic **Insecure Direct Object Reference (IDOR)**, where the application fails to enforce access control on a direct object reference (the ID).

## References
- [OWASP Top Ten 2021 – A01:2021 Broken Access Control](https://owasp.org/Top10/A01_2021-Broken_Access_Control/)
- [CWE-639: Authorization Bypass Through User-Controlled Key](https://cwe.mitre.org/data/definitions/639.html)
- [OWASP IDOR Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Insecure_Direct_Object_Reference_Prevention_Cheat_Sheet.html)

## Impact

This vulnerability allows an attacker to access attachments from private bug reports submitted by other users by simply manipulating the ID parameter in the request. Since the endpoint lacks proper authorization checks and even responds when unauthenticated, sensitive internal information, such as unpatched security issues, confidential business data, or personally identifiable information, could be fully exposed. This significantly increases the risk of targeted attacks, information leaks, and reputational damage to the organization.

## System Host(s)
███████

## Affected Product(s) and Version(s)


## CVE Numbers


## Steps to Reproduce
1. Log in with any valid user account.
2. Capture the request when viewing a bug report attachment:
```
GET /BugReport/Admin/Attachment/1568600 HTTP/1.1

Host: █████████

Cookie: ████
```


3. Remove the entire `Cookie` header from the above request, so it looks like:
```
GET /BugReport/Admin/Attachment/1568600 HTTP/1.1

Host: █████████
```
4. Send the modified request without any authentication cookies.  
5. Observe that the server responds with the file contents of the bug report attachment.

**Result:** Any unauthenticated user can view attachments of any bug report by enumerating or guessing valid IDs.

## Suggested Mitigation/Remediation Actions
- Implement strict authorization checks on the `/BugReport/Admin/Attachment/{id}` endpoint to verify that the requesting user has permission to access the specified attachment.  
- Ensure that unauthenticated requests cannot retrieve any sensitive resources by enforcing authentication at this endpoint.  
- Use indirect references (e.g., random UUIDs or tokens) instead of sequential numeric IDs to reduce the risk of enumeration.  
- Apply the principle of least privilege: users should only be able to access resources they are explicitly authorized to view.  
- Add proper logging and monitoring for unauthorized access attempts to detect potential exploitation early.  
- Consider rate limiting to prevent mass enumeration of IDs.



</details>

---
*Analysed by Claude on 2026-05-24*
