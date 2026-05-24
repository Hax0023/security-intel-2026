# File Upload via Unauthorized Private IM Channel Access

## Metadata
- **Source:** HackerOne
- **Report:** 143903 | https://hackerone.com/reports/143903
- **Submitted:** 2016-06-09
- **Reporter:** thisishrsh
- **Program:** Unknown (HackerOne #143903)
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Broken Access Control, Insecure Direct Object Reference (IDOR), Privilege Escalation
- **CVEs:** None
- **Category:** auth-crypto

## Summary
A team member can upload files to private IM channels belonging to other users by directly manipulating the IM channel ID parameter. This breaks the intended access control model where users should only upload files to channels they own or are explicitly invited to. The vulnerability allows unauthorized file placement in other users' private communication spaces.

## Attack scenario
1. Attacker identifies target user's private IM channel ID (via enumeration, disclosure, or inference from other requests)
2. Attacker crafts a file upload request to the application's file upload endpoint
3. Attacker modifies the 'channel_id' parameter to match the target user's private IM channel ID
4. Application fails to validate if the uploading user has authorization to upload to that specific channel
5. File is successfully uploaded to the target user's private IM channel without consent
6. Uploaded file appears in target user's private chat, potentially containing malicious content

## Root cause
The application performs insufficient authorization checks on file upload requests. While the application likely verifies that the user is authenticated, it fails to validate that the authenticated user has permission to upload files to the specific channel indicated by the channel_id parameter. The application trusts user-supplied channel IDs without proper ownership/membership verification.

## Attacker mindset
An opportunistic insider or low-privilege user seeks to disrupt other team members' communications or inject malicious files into their private channels. The attacker recognizes that file upload endpoints are often less rigorously protected than other privileged operations and exploits IDOR patterns by enumeration or guessing channel IDs.

## Defensive takeaways
- Implement server-side authorization checks on all file upload endpoints verifying the user has explicit permission to upload to the target channel
- Never trust user-supplied IDs (channel_id, user_id, etc.) without validation against the authenticated user's access control list
- Use indirect references or opaque IDs instead of sequential/predictable channel identifiers to increase enumeration difficulty
- Log all file upload attempts including channel_id, user, and authorization decisions for audit trails
- Perform authorization checks before accepting file data, not after
- Use the principle of least privilege: default deny access, then explicitly grant permissions based on ownership/membership
- Add rate limiting and anomaly detection on file uploads to catch bulk IDOR exploitation attempts
- Implement per-channel audit logs showing who uploaded what files and when

## Variant hunting
Check other file operations (download, delete, move) for the same IDOR pattern on channel_id
Test whether users can read/modify other users' private channels by channel_id
Investigate if group channels have similar vulnerabilities (users uploading to groups they don't belong to)
Test if the vulnerability extends to shared document upload endpoints
Check if user can modify channel metadata/permissions by directly referencing channel_id
Look for IDOR in direct message file access (accessing DM history from other users)
Test API endpoints vs web interface for inconsistent authorization logic

## MITRE ATT&CK
- T1190
- T1548
- T1566

## Notes
This is a classic IDOR vulnerability in a communication platform context. The writeup lacks POC details and specific endpoints, making reproduction difficult. The vulnerability could escalate if the upload endpoint accepts malicious file types (polyglot files, scripts) or allows path traversal. This type of flaw is particularly dangerous in team collaboration tools where private channels are intended for sensitive discussions.

## Full report
<details><summary>Expand</summary>

A team member can upload the files in the private IM chat channel of other members.This can be done by using the IM channel id.
Please refer to the attached POC's.
Let me know if any more details are needed.

</details>

---
*Analysed by Claude on 2026-05-24*
