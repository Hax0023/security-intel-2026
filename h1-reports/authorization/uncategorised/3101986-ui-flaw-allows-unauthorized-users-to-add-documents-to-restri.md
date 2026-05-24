# UI Flaw Allows Unauthorized Document Upload to Restricted Folders via Client-Side Bypass

## Metadata
- **Source:** HackerOne
- **Report:** 3101986 | https://hackerone.com/reports/3101986
- **Submitted:** 2025-04-20
- **Reporter:** kymu_
- **Program:** Undisclosed
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Insecure Direct Object Reference (IDOR), Broken Access Control, Client-Side Security Enforcement
- **CVEs:** None
- **Category:** uncategorised

## Summary
A UI flaw in the document management system allows unprivileged users to upload documents to folders restricted to administrators. Although the add document button appears disabled in the UI, client-side manipulation or direct API calls enable unauthorized file uploads, bypassing intended access controls. This breaks object-level authorization and compromises data integrity.

## Attack scenario
1. Attacker logs in as a member account with limited permissions
2. Attacker navigates to a restricted folder they should not have write access to
3. Attacker clicks the 'add multiple documents' button which appears disabled but remains functional
4. Attacker selects and uploads a document despite lacking authorization
5. Document upload succeeds, confirming the backend does not properly validate user permissions
6. Attacker can now repeatedly add documents to restricted folders, potentially inserting malicious or sensitive content

## Root cause
Backend authorization logic fails to validate user permissions before processing document upload requests. The application relies on client-side UI restrictions (disabled buttons) rather than enforcing server-side access control checks. No permission validation occurs on the API endpoint handling document uploads to specific folder objects.

## Attacker mindset
An opportunistic insider or low-privilege user seeks to escalate their capabilities by discovering that permission checks are only enforced on the frontend. By recognizing that disabled UI elements don't prevent actual functionality, the attacker exploits the gap between intended and actual access controls to manipulate shared resources.

## Defensive takeaways
- Implement server-side authorization checks on all document upload endpoints before processing any file
- Validate that the authenticated user has explicit write permissions to the target folder before accepting uploads
- Never rely solely on client-side UI restrictions (disabled buttons, hidden fields) for security enforcement
- Implement role-based access control (RBAC) consistently across all API endpoints
- Log all document upload attempts including failed authorization attempts for audit trails
- Use HTTP status codes 403 Forbidden for unauthorized requests rather than silently processing them
- Implement folder-level permission caching with regular invalidation to prevent stale authorization decisions

## Variant hunting
Check if other document operations (delete, edit, move, share) bypass authorization in similar ways
Test if the vulnerability affects other object types beyond folders (projects, workspaces, collections)
Verify if file type restrictions can be bypassed through the same mechanism
Investigate if folder permission inheritance is properly validated across API endpoints
Check if bulk operations bypass individual object permission checks
Test if the vulnerability affects different user roles and permission levels

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1548 - Abuse Elevation Control Mechanism
- T1556 - Modify Authentication Process
- T1078 - Valid Accounts

## Notes
The writeup explicitly identifies this as an IDOR vulnerability rooted in client-side security enforcement. The critical finding is that the backend does not validate permissions before processing uploads. This is a textbook example of broken access control (OWASP A01:2021). The fact that the button 'looks disabled but works fine' strongly suggests the backend is the vulnerable component, not just a UI glitch. Organizations must audit all API endpoints for similar authorization bypass vulnerabilities.

## Full report
<details><summary>Expand</summary>

hey team
A UI issue allows a user to upload or add documents to a folder they should not have access to. This bypasses intended permissions and could lead to unauthorized access or data integrity issues.

steps to reproduce: 
1- login in account a which is the admin, add any document to the folder
2-login as account b which is member and go to the same folder then click on add multiple documents and choose any document
3-the document will be uploaded successfully, the button of adding looks disabled but it works fine, the member is not supposed to do this function

█████████

## Impact

This issue constitutes an Insecure Direct Object Reference (IDOR) vulnerability. Although the UI is intended to restrict access, users can manipulate the client-side behavior to perform unauthorized actions — in this case, uploading documents to folders they shouldn't have access to. This breaks access control at the object level and could allow:

Unauthorized insertion of documents into restricted folders

</details>

---
*Analysed by Claude on 2026-05-24*
