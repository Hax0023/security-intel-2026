# Phabricator File Reference Authorization Bypass Leading to Information Disclosure

## Metadata
- **Source:** HackerOne
- **Report:** 221950 | https://hackerone.com/reports/221950
- **Submitted:** 2017-04-18
- **Reporter:** xifengweiyu
- **Program:** Phabricator
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Authorization Bypass, Information Disclosure, Insecure Direct Object Reference (IDOR)
- **CVEs:** None
- **Category:** web-api

## Summary
Phabricator's file reference system using special codes like {Fxxx} lacks proper authorization controls, allowing unauthorized users to access files uploaded by other users regardless of visibility restrictions. An attacker can enumerate file references and gain access to confidential documents by simply posting file codes in any editor context.

## Attack scenario
1. Attacker identifies that files in Phabricator are referenced using special codes like {F18}
2. Attacker observes or infers valid file IDs through normal usage or error messages
3. Attacker creates a new task, document, or comment with enumerated file codes {F1}, {F2}, {F3}... {FN}
4. Attacker posts the content containing file references
5. The system renders/exposes files without checking if the current user has access to the original file's parent object
6. Attacker gains unauthorized access to files with restricted visibility (private, user-specific, etc.)

## Root cause
The file rendering engine processes {Fxxx} codes without performing authorization checks on the referenced file. It only checks if the file exists but not whether the current user has permission to view the context (task, document) where the file was originally uploaded. The validation logic trusts file references without considering visibility scope.

## Attacker mindset
An attacker with basic access to Phabricator can systematically probe for files through enumeration. The vulnerability requires minimal effort—just posting file codes—making it attractive for discovering sensitive information. The attacker recognizes that authorization checks likely happen at the parent object level (task visibility) but not at file reference resolution.

## Defensive takeaways
- Implement authorization checks at file resolution time, not just at upload time—verify user has access to the file's parent context before rendering
- Apply the principle of least privilege: {Fxxx} references should inherit and enforce the visibility/permissions of their original parent object
- Validate that file references are only displayed to users who have explicit access to view the parent task/document
- Implement rate limiting and anomaly detection for bulk file reference enumeration attempts
- Use opaque, non-sequential file identifiers instead of simple incremental IDs to prevent enumeration
- Add audit logging for file access and reference resolution to detect unauthorized access patterns

## Variant hunting
Look for similar authorization bypass issues in other reference systems: {Txxx} for tasks, {Dxxx} for documents, {Cxxx} for commits. Check if other embedded content types bypass visibility checks. Test if file permissions are checked only at upload vs. at every access point. Investigate if API endpoints for file access implement the same authorization as the UI.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1526 - Enumerate External Targets
- T1087 - Account Discovery
- T1040 - Network Sniffing (if file enumeration via observation)
- T1078 - Valid Accounts (using legitimate user access to enumerate)

## Notes
This is a classic IDOR vulnerability compound with broken access control. The bug demonstrates why authorization must be checked at every access point, not assumed from initial creation context. The simplicity of the exploit (just posting file codes) makes it a critical finding for privilege escalation and information disclosure. The vulnerability affects all users and requires no special privileges to exploit.

## Full report
<details><summary>Expand</summary>

Here is your keyword:mongoose

Details:
- Summary:

Uploaded file will be showed as a special code `{Fxxx}` in Phabricator editor,but it has no Authority control.

- Reproduce steps:

1.Open two different browsers (to simulate two different users)
2.browser A:login as user "toma"
3.browser B:login a user "test4"
4.user "toma" create a Maniphest task with visibility "toma" only,and upload a file "toma.html" to description,its code is`{F18}`
5.user "test4" open anyone editor and write:
```
{F1}{F2}{F3}{F4}{F4}{F5}{F6}{F7}{F8}{F9}{F10}{F11}{F12}{F13}{F14}{F15}{F16}{F17}{F18}{F19}{F20}
```
then post it,then you will find user "test4" has got the file of user "toma" with visibility "toma".



</details>

---
*Analysed by Claude on 2026-05-24*
