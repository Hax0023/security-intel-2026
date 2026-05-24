# Insecure Direct Object Reference (IDOR) on Profile Image Upload Functionality

## Metadata
- **Source:** HackerOne
- **Report:** 741683 | https://hackerone.com/reports/741683
- **Submitted:** 2019-11-20
- **Reporter:** risinghunter
- **Program:** HackerOne Report #741683
- **Bounty:** Not specified in writeup
- **Severity:** High
- **Vuln:** Insecure Direct Object Reference (IDOR), Broken Access Control, Authorization Bypass
- **CVEs:** None
- **Category:** web-api

## Summary
An attacker can upload a profile image to any user account by modifying the 'personId' parameter in the upload request, bypassing authorization checks. The application fails to verify that the authenticated user owns the account before processing the image upload, allowing unauthorized modification of other users' profile images.

## Attack scenario
1. Attacker authenticates to their own account and navigates to the profile image upload page
2. Attacker captures the upload request in Burp Suite proxy
3. Attacker identifies the 'personId' parameter in the POST request containing their account ID
4. Attacker modifies the 'personId' value to a victim's account ID (account2_id)
5. Attacker forwards the modified request with the victim's ID and their chosen image
6. The image is successfully uploaded and appears in the victim's profile, confirming the IDOR vulnerability

## Root cause
The application implements client-side or insufficient server-side authorization checks. The upload endpoint accepts the personId as a user-controllable parameter without verifying that the authenticated user is the owner of that account. No token validation, session verification, or ownership confirmation is performed before processing the upload request.

## Attacker mindset
An attacker would recognize this as a common authorization bypass vulnerability. By fuzzing or modifying parameters in requests, they discover that changing the personId parameter allows manipulation of other users' data. This is a low-effort, high-impact attack requiring only basic proxy tools and no additional authentication.

## Defensive takeaways
- Implement server-side authorization checks to verify the authenticated user owns the resource before processing any modifications
- Use session tokens or user context from authentication to determine resource ownership, never rely solely on user-supplied parameters
- Validate that the personId in requests matches the authenticated user's ID; reject requests where users attempt to modify other accounts
- Implement proper access control lists (ACLs) or ownership verification at the application logic level
- Log and monitor upload requests for suspicious patterns (multiple personIds from single user, rapid account changes)
- Use indirect object references (e.g., sequential tokens) instead of direct account IDs when possible
- Perform security testing specifically targeting parameter manipulation in state-changing operations

## Variant hunting
Look for similar IDOR patterns in other user-centric operations: profile information updates, document uploads, preference changes, notification settings, payment method changes, and any endpoint accepting user IDs as parameters. Test all PUT/POST/DELETE requests with modified ID parameters to identify similar authorization bypass vulnerabilities.

## MITRE ATT&CK
- T1190
- T1566

## Notes
This is a straightforward IDOR vulnerability in a web application. The fix requires minimal code changes but significant security impact. The vulnerability affects user data integrity and could be exploited for harassment, reputation damage, or system abuse. The video evidence would clearly demonstrate the impact by showing the unauthorized image appearing in another user's profile.

## Full report
<details><summary>Expand</summary>

Vulnerable URL: https://██████████/███████ID/#Common/EditOne/Person/{account_id}
steps to reproduce:
1).browse the image and click on the upload button
2).capture this request in burp suite 
3). change the value 'personId' parameter to account2 account_id 
(please see screenshot1)
4).then goes to account2, then you will see the uploaded image is successfully goes to the approved tab 

please see video attach below you will understand completely

## Impact

an attacker is able to change profile image of any user

</details>

---
*Analysed by Claude on 2026-05-24*
