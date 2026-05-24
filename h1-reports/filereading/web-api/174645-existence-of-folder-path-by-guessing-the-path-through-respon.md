# Information Disclosure via Path Enumeration Through Response Differentiation

## Metadata
- **Source:** HackerOne
- **Report:** 174645 | https://hackerone.com/reports/174645
- **Submitted:** 2016-10-08
- **Reporter:** ashish_r_padelkar
- **Program:** BrickFTP
- **Bounty:** Not specified
- **Severity:** Medium
- **Vuln:** Information Disclosure, Path Traversal/Enumeration, Insufficient Access Control, Timing/Response-based Enumeration
- **CVEs:** None
- **Category:** web-api

## Summary
An authenticated user with limited permissions can enumerate the existence of restricted folders they lack access to by observing different error responses when attempting to move files. The application returns distinguishable errors for non-existent folders versus forbidden folders, allowing attackers to guess valid folder names and confirm their existence without authorization to view them.

## Attack scenario
1. Attacker authenticates as a low-privilege user with Admin access to only 'Test1' folder
2. Attacker selects a file from Test1 and initiates the move operation
3. Attacker enters a guessed folder name (e.g., 'Test2') in the destination path field
4. Application returns 'cannot write' error, confirming folder existence (vs. generic 404 for non-existent folder)
5. Attacker systematically guesses common folder names and validates their existence through response differentiation
6. Attacker gains knowledge of the file structure and restricted areas without proper authorization

## Root cause
The application implements inconsistent error handling for the move operation. It returns different HTTP responses or error messages based on whether a folder doesn't exist (invalid path) versus whether the user lacks permissions (forbidden access), allowing attackers to infer folder existence through response analysis.

## Attacker mindset
A disgruntled employee or competitor with legitimate system access seeks to discover the complete organizational structure and sensitive folder hierarchy. By exploiting response differentiation, they can map restricted areas without triggering obvious security alerts, enabling targeted attacks or social engineering.

## Defensive takeaways
- Always return identical error responses for both 'not found' and 'forbidden' scenarios to prevent information disclosure
- Implement uniform HTTP status codes (e.g., 404) for any unauthorized access regardless of resource existence
- Log and monitor enumeration attempts where users repeatedly test invalid paths
- Apply rate limiting to file move operations to prevent systematic brute-force enumeration
- Validate user permissions before any operation that could leak structural information
- Use generic error messages in user-facing responses ('Access Denied') rather than status-specific messages

## Variant hunting
Similar path enumeration in other file operations: copy, delete, rename, download
Response differentiation in API endpoints returning file/folder metadata
Timing-based attacks where permission checks take measurably different durations
Check if folder existence can be inferred through file search results or sharing dialogs
Examine breadcrumb navigation or autocomplete features for path disclosure
Test archive/backup features for enumeration vulnerabilities

## MITRE ATT&CK
- T1526 - System Network Configuration Discovery
- T1087 - Account Discovery
- T1580 - Cloud Infrastructure Discovery
- T1592 - Gather Victim Host Information

## Notes
This is a classic information disclosure vulnerability stemming from poor error handling. The fix is straightforward but commonly missed: collapse all permission-related errors into a single generic response. The vulnerability demonstrates that in access control contexts, revealing whether a resource exists versus whether access is denied can be equally damaging. The vulnerability was filed in 2016 and exploited the move operation's error messaging, but similar flaws likely existed in other operations.

## Full report
<details><summary>Expand</summary>

**Enter the support PIN from your test site:**
 423088
**Enter the name of your test site :**
 https://bugbounty5.brickftp.com
**Enter the subdomain from your test site :**
 https://bugbounty5.brickftp.com

----

**Description**

Suppose there are 2 `Folders` in the site

`Test1`
`Test2`

but a member has only `Admin` permission to `Test1` , he cant see the folder `Test2`

However, it is possible to know if such `folder/path` (Test2) exist in a site by guessing the names of the folder.


**Steps**

1.There are 2 `folders` in a site namely `Test1` and `Test2`
2. Member has full `Admin` permission to `Test1` and no permission at all to `Test2`. Member wont be able to see the folder `Test2` in his account at all.
3. Now member selects any file from `Test1` using checkbox and select move option from dropdown. he gets only path to `Test1` folders. 
4. now if i type some random names of the folders in the box and say move, it will throw the error. but if type the valid names of folders which may be in a site, it will say can not write. 
5. this proves that, if you can guess correct name of folder/path, it tells you the existence of the path.

**POC**
https://youtu.be/mzPXVHIDnzs

**Resolution**
The response should be same for both requests. folder exist or not, it should throw 404!



**The date you tested for and found the vulnerability**
08/10/2016

**The following affirmative statement **
I HAVE READ AND UNDERSTAND AND AGREE TO THE TERMS OF THE BUG BOUNTY PROGRAM. I AGREE TO THE BRICKFTP TERMS OF SERVICE. I HAVE COMPLIED AND WILL COMPLY WITH THE RULES OF THE PROGRAM AND THE TERMS OF SERVICE. I HAVE NOT DISCLOSED THIS SUBMISSION TO ANYONE. I DISCOVERED IT MYSELF. I WILL NOT DISCLOSE THIS SUBMISSION TO ANYONE. I DO WANT MY NAME PUBLISHED ON YOUR HALL OF FAME IF THIS IS ACCEPTED


</details>

---
*Analysed by Claude on 2026-05-24*
