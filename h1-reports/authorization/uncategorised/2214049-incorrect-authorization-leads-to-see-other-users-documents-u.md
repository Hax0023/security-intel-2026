# Incorrect Authorization leads to see other users Documents Uploaded

## Metadata
- **Source:** HackerOne
- **Report:** 2214049 | https://hackerone.com/reports/2214049
- **Submitted:** 2023-10-18
- **Reporter:** mohs3n
- **Program:** Unknown (qcn.mytva.com)
- **Bounty:** Unknown
- **Severity:** high
- **Vuln:** Broken Access Control, Insecure Direct Object Reference (IDOR), Insufficient Authorization Checks
- **CVEs:** None
- **Category:** uncategorised

## Summary
Authenticated users can view and download documents uploaded by other users by directly accessing the FileHandler endpoint with an encrypted file reference parameter. The application fails to verify that the requesting user has permission to access the document before serving it. This allows any authenticated user to enumerate and access sensitive documents belonging to other users in the system.

## Attack scenario
1. Attacker authenticates as User B to the application
2. Attacker obtains a direct link to a document uploaded by User A (via social engineering, disclosure, or error message)
3. Attacker navigates to the FileHandler endpoint with the ENC parameter containing User A's encrypted file reference
4. Server decrypts the ENC parameter but fails to validate if User B has authorization to access User A's document
5. Server returns the requested file to User B without checking document ownership or access permissions
6. Attacker successfully downloads and views confidential documents from other users

## Root cause
The FileHandler endpoint performs file retrieval based solely on the encrypted reference (ENC parameter) without implementing proper authorization checks. The application decrypts the file path but does not verify that the currently authenticated user owns or has explicit permission to access the requested document. Authorization logic is missing or incomplete at the endpoint level.

## Attacker mindset
An attacker would recognize that encrypted parameters often provide a false sense of security and that authorization checks must validate user ownership. They would systematically test file access across different user sessions, potentially automating enumeration of valid ENC values to discover and access other users' documents for competitive intelligence, data theft, or privacy violations.

## Defensive takeaways
- Implement explicit authorization checks before serving any file - verify the requesting user owns the document or has explicit access rights
- Use session-based user context to enforce document ownership validation on every file access request
- Avoid relying on encryption of file references as a security mechanism; encrypt for privacy but validate permissions separately
- Implement access control lists (ACL) or ownership verification for all document retrieval endpoints
- Log and monitor file access attempts, particularly cross-user access patterns
- Conduct thorough authorization testing across all file handling endpoints in security testing phases
- Apply principle of least privilege - users should only access their own documents unless explicitly granted access

## Variant hunting
Search for other file download/retrieval endpoints that may use similar encrypted parameter patterns without authorization checks
Test image serving endpoints, document preview handlers, and attachment downloaders for IDOR vulnerabilities
Check if user-specific resources (reports, exports, backups) implement proper authorization validation
Enumerate other Admin section endpoints for similar authorization bypass vulnerabilities
Test if file listing endpoints disclose other users' file references or allow directory traversal

## MITRE ATT&CK
- T1190
- T1566
- T1005
- T1041

## Notes
This is a classic IDOR vulnerability in file handling. The use of encryption in the ENC parameter may have provided false confidence in security. The vulnerability affects the admin section specifically but likely has broader implications if similar file handling patterns exist elsewhere in the application. The simplicity of exploitation (direct URL manipulation) and high sensitivity of impact (document access) make this a critical authorization flaw.

## Full report
<details><summary>Expand</summary>

## Summary:
Hi team,
when user upload document, other user can see this docs only with link

## Steps To Reproduce:
1. loign to portal with user A : https://qcn.mytva.com
2. go to admin section and upload a document.
{F2782891}

3. click on link to see uploaded image. [like](https://qcn.mytva.com/Admin/FileHandler?ENC=RUFBQUFITmtabk00TjJGa1ptRTVNV0Z6TW5JMHV0S2hNTHNYR1J1SDNMMFBqeElLajlTNGNjTHcxVUhqcHhuL1R1cUxyVkxoS0RSRUFqUjRDTlFEd2E4S1diUkNYMlhGNFdSTDRrdE1yUUgvNkVhYWtUR251RjVYc1V6RDdwZkZXdTlCV0tZY2JmWGlVSkNjcHEyK0VvQU1Fc2R2RklDQW1MM25kNEZMTStxMTlhRnBrdStuOGs4N3lTU1Q1R2FsQ1ZrTHhnPT0)

{F2782892}

4. login to portal with user B
5. go to above url, we can see and download user A document.

{F2782896}

## Impact

any login user can see other user documents

</details>

---
*Analysed by Claude on 2026-05-24*
