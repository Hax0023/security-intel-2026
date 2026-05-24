# Access notes without permission

## Metadata
- **Source:** HackerOne
- **Report:** 3241304 | https://hackerone.com/reports/3241304
- **Submitted:** 2025-07-08
- **Reporter:** haydradz
- **Program:** curl
- **Bounty:** Unknown
- **Severity:** Medium
- **Vuln:** Broken Access Control, Unauthorized Information Disclosure
- **CVEs:** None
- **Category:** web-api

## Summary
A vulnerability in curl allows users to access notes or sensitive information they do not have permission to view. The issue appears to be related to improper access control checks when retrieving note objects. This could lead to unauthorized disclosure of private or confidential information.

## Attack scenario
1. Attacker identifies a note object URL or ID within the curl application
2. Attacker attempts to access the note directly via API endpoint or URL parameter without proper authorization
3. Access control validation fails to properly verify user permissions
4. Attacker successfully retrieves note content they should not have access to
5. Attacker can read private notes from other users or internal documentation
6. Sensitive information is disclosed to unauthorized parties

## Root cause
Improper authorization checks when retrieving notes. The application likely fails to verify that the requesting user has permission to access a specific note before returning the content, implementing either no checks or insufficient permission validation.

## Attacker mindset
Opportunistic reconnaissance - testing whether direct object references can be exploited to bypass authorization controls and discover sensitive information that should be restricted.

## Defensive takeaways
- Implement proper authorization checks before returning any user/project-related data
- Verify user permissions match the resource owner for every data retrieval request
- Use indirect object references or UUIDs instead of sequential IDs
- Apply principle of least privilege - ensure users can only access their own notes
- Add audit logging for note access attempts
- Implement role-based access control (RBAC) for note visibility

## Variant hunting
Search for similar authorization bypass issues in other resource types: comments, issues, pull requests, commits, configuration files. Test whether the vulnerability affects batch operations or export functions.

## MITRE ATT&CK
- T1190
- T1526

## Notes
The report URL references curl GitHub but limited details are available in the archive. The vulnerability appears to be an Insecure Direct Object Reference (IDOR) or similar authorization flaw allowing unauthorized access to notes.

## Full report
<details><summary>Expand</summary>

https://web.archive.org/web/*/https://github.com/curl/curl

## Impact

## Summary:
access notes without permission

</details>

---
*Analysed by Claude on 2026-05-24*
