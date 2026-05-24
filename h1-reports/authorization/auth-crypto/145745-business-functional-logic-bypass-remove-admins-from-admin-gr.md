# Business/Functional Logic Bypass: Remove Admins from Admin Group via Trailing Space

## Metadata
- **Source:** HackerOne
- **Report:** 145745 | https://hackerone.com/reports/145745
- **Submitted:** 2016-06-18
- **Reporter:** paglababa
- **Program:** Nextcloud
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Business Logic Flaw, Authorization Bypass, Input Validation Bypass
- **CVEs:** None
- **Category:** auth-crypto

## Summary
Nextcloud prevents removal of the default admin from the admin group, but this protection can be bypassed by submitting a group toggle request with a trailing space in the group parameter (e.g., 'admin ' instead of 'admin'). This allows an attacker to remove administrative privileges from the default admin account, effectively disabling system administration capabilities.

## Attack scenario
1. Attacker gains access to an authenticated session with sufficient privileges to toggle group membership
2. Attacker crafts a POST request to /settings/ajax/togglegroups.php with username=admin and group='admin ' (with trailing space)
3. The server's input validation compares 'admin ' against 'admin' as literal strings, treating them as different groups
4. The application removes the admin user from what it perceives as a different group, bypassing the protection logic
5. The admin user is now removed from the actual admin group despite the intended protection
6. The system loses its default administrator, potentially leaving it in an unrecoverable state

## Root cause
The application implements group removal protection by comparing the group name directly against 'admin' without normalizing whitespace. The validation checks if group === 'admin' but fails to account for trailing spaces, leading to a bypass where 'admin ' is treated as a distinct group name and passes validation.

## Attacker mindset
An authenticated user with group management capabilities could exploit this to escalate privileges by eliminating the default admin account, gaining effective control of the system or rendering it administratorless. This could be a disgruntled insider or an attacker who has compromised a moderator account.

## Defensive takeaways
- Implement input normalization for all security-critical parameters (trim whitespace, normalize case)
- Use strict equality checks with normalized inputs for sensitive operations
- Apply protection logic at the data model layer, not just at the presentation/validation layer
- Test edge cases for all security restrictions, including whitespace variations
- Consider preventing removal of the last/default admin through database constraints rather than application logic alone
- Use parameterized queries and ORM frameworks that handle string comparison consistently
- Implement comprehensive logging for privilege-related operations to detect such attacks

## Variant hunting
Search for similar logic flaws in group/role management systems where: (1) Protection checks use string comparison without normalization, (2) Special user/group restrictions exist but don't account for whitespace/encoding variations, (3) Admin removal is restricted but group toggle has looser validation, (4) Other administrative endpoints that check against hardcoded strings like 'admin', 'root', 'system', (5) User deletion or privilege removal operations with insufficient input validation

## MITRE ATT&CK
- T1190
- T1548
- T1078

## Notes
This is a classic example of insufficient input validation combined with weak business logic protection. The vulnerability demonstrates that security-critical operations should never rely on simple string comparison without normalization. The fix would be straightforward: apply trim() to the group parameter before comparison. This type of bug is particularly dangerous in admin management systems as it can render a system unrecoverable without database-level intervention.

## Full report
<details><summary>Expand</summary>

In nextcloud the default admin can not be removed from his admin group. The group toggle request looks like this:

```
POST /nextcloud/index.php/settings/ajax/togglegroups.php HTTP/1.1
Host: 139.59.9.184
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:47.0) Gecko/20100101 Firefox/47.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
requesttoken: JQB5F2pqZwh8OUNVRzwVPxdmKCEbJDssbAUcORtfTVM=:bIHyZZPyIV67tsLPsWgrxCInGdOC40f2yD61Qn4HrTw=
OCS-APIREQUEST: true
X-Requested-With: XMLHttpRequest
Cookie: oc1jzqgvx8b9=e6gprie4u2ffkq83ivm68ccp80; oc_sessionPassphrase=BL2ccA7kLG%2FpxKWf5znZSBLWSvARKK%2Bv3oLuCFyGd8a5SAqPeeBjIaD88AVnwnMS8ompIL7tN45YiZeeODdFHyPBYZrZAavWsHJqMKZdvU3U6eZUW%2FHCGLMd62y6ty7P; nc_sameSiteCookielax=true; nc_sameSiteCookiestrict=true
Connection: close
Content-Length: 25

username=test&group=test
```

If we use **admin** as the value of username and **admin ** as the value of group ( admin with a trailing space), the admin will be removed from the admin group.



</details>

---
*Analysed by Claude on 2026-05-24*
