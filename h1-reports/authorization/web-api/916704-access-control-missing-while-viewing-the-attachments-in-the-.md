# Missing Access Control on Attachment Download - Insecure Direct Object Reference (IDOR)

## Metadata
- **Source:** HackerOne
- **Report:** 916704 | https://hackerone.com/reports/916704
- **Submitted:** 2020-07-06
- **Reporter:** dpx01
- **Program:** Nextcloud Deck (us.cloudamo.com)
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Insecure Direct Object Reference (IDOR), Broken Access Control, Missing Authentication/Authorization
- **CVEs:** CVE-2020-8235
- **Category:** web-api

## Summary
The attachment download functionality in Nextcloud Deck's task management feature lacks proper access control, allowing any authenticated user to view and download files uploaded by other users. Attachment IDs are sequential numeric values with no cryptographic protection, enabling brute-force enumeration of all uploaded files across the provider instance.

## Attack scenario
1. Attacker creates an account and logs into the Nextcloud Deck application
2. Attacker identifies a valid attachment URL structure by uploading a file: /apps/deck/cards/{cardId}/attachment/{attachmentId}
3. Attacker observes that attachment IDs are simple incrementing integers with no access control verification
4. Attacker systematically enumerates attachment IDs (e.g., 1, 2, 3, ..., N) to discover files uploaded by other users
5. Attacker downloads sensitive documents, spreadsheets, or confidential files belonging to other users without authorization
6. Attacker potentially shares leaked information or uses it for corporate espionage or blackmail

## Root cause
The application implements a direct object reference pattern for attachment retrieval without verifying that the requesting user has permission to access the target attachment or its parent task/board. The endpoint likely retrieves attachments based solely on the numeric ID parameter without checking ownership, board membership, or task permissions.

## Attacker mindset
An attacker recognizes that sequential IDs are trivial to enumerate and that many developers forget to implement proper authorization checks on indirect object references. They assume no CSRF protection or session validation is required and leverage the simplistic ID scheme to harvest files at scale.

## Defensive takeaways
- Implement proper authorization checks on all resource access - verify user has permission to view the parent task/board before serving attachments
- Use cryptographically random or opaque identifiers (UUIDs) for resources instead of sequential integers
- Implement rate limiting and brute-force detection on attachment endpoints
- Add CSRF token validation on sensitive operations
- Log and monitor unusual attachment access patterns (high volume, sequential IDs, cross-user access)
- Conduct security audit of all file serving endpoints across the application
- Implement proper session validation and re-authentication for sensitive operations

## Variant hunting
Search for other file/attachment endpoints in Nextcloud Deck and similar collaboration tools (comments, document sharing, media libraries). Look for any GET/POST endpoints serving user-generated content with numeric or predictable identifiers. Check for missing authorization checks on APIs returning file paths, download endpoints, or preview functionality.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1566 - Phishing (potential use of leaked documents)
- T1526 - Reconnaissance (enumeration of files)
- T1040 - Network Sniffing (if combined with network access)

## Notes
This is a classic IDOR vulnerability. The report demonstrates a complete exploitation chain from discovery to brute-force enumeration. The lack of access control combined with predictable IDs creates a severe data leak risk. This vulnerability likely affects all users of the provider instance and could expose confidential business documents. Immediate patching required.

## Full report
<details><summary>Expand</summary>

The vulnerability lies in the "view attachment" of the tasks . When a user uploads the file to the Task, the attachment is given a numeric number and is increased +1 on further uploads. It is easy for any user to view and download all the files uploaded to the tasks by any user. The access is not controlled with the session or csrf token.

Steps to Reproduce:
1. Connect to the server login with user A and visit the webpage. I used the provider "us.cloudamo.com"
2. Visit https://us.cloudamo.com/apps/deck and create a task.
3. Upload any file to the attachments and capture the request. The request will looks like "https://us.cloudamo.com/apps/deck/cards/8420/attachment/30" where 30 is the ID of the uploaded attachment. 
4. Login with  user B and access the URL and you should be able to view the attachment of user A.
5. Since the attachment IDs are numerical number with poor entropy can be easily brute-forced and  one can get all the uploaded attachments by all the users of the particular  provider.

## Impact

Unauthorized user can view and download the files of other users. This may leak the sensitive information of users.

</details>

---
*Analysed by Claude on 2026-05-24*
