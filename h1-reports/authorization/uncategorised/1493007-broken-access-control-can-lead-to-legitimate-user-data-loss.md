# Broken Access Control - Unauthorized Deletion of User Access Requests

## Metadata
- **Source:** HackerOne
- **Report:** 1493007 | https://hackerone.com/reports/1493007
- **Submitted:** 2022-02-27
- **Reporter:** lubak
- **Program:** Undisclosed
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Broken Access Control, Insecure Direct Object References (IDOR), Missing Authentication, Data Loss
- **CVEs:** None
- **Category:** uncategorised

## Summary
An unauthenticated attacker can delete arbitrary user access requests by directly accessing a deletion endpoint with sequential request IDs. Since request IDs are predictable sequential numbers, an attacker can systematically delete all requests in the system, causing data loss and disrupting normal operations.

## Attack scenario
1. Attacker identifies the user request submission form and submits a test form to obtain a request ID
2. Server responds with a sequential numeric ID identifying the user request
3. Attacker discovers the deletion endpoint (potentially through reconnaissance or leaked information)
4. Attacker crafts a POST request to the deletion endpoint with a target request ID parameter
5. Due to missing authentication checks, the deletion succeeds without requiring authentication
6. Attacker iterates through sequential request IDs to delete all legitimate user requests in the system

## Root cause
The deletion endpoint lacks proper authentication and authorization validation. The application does not verify that the user is logged in or has permission to delete requests before processing the deletion. Combined with predictable sequential resource identifiers (request IDs), this creates a trivial attack vector for mass data destruction.

## Attacker mindset
An attacker would systematically exploit this vulnerability to cause maximum disruption by deleting all pending access requests, effectively blocking legitimate users from gaining system access and creating operational chaos. This could be motivated by competitive sabotage, revenge, or simply causing chaos.

## Defensive takeaways
- Implement mandatory authentication checks on all sensitive endpoints, especially those handling data modification or deletion
- Require authorization verification to confirm the user has explicit permission to delete specific resources
- Use non-sequential, cryptographically random identifiers (UUIDs) for sensitive resources instead of predictable sequential numbers
- Implement rate limiting on deletion endpoints to slow down automated mass deletion attempts
- Add audit logging for all deletion operations to enable detection and recovery
- Consider implementing soft deletes (logical deletion with recovery capability) instead of permanent deletion
- Apply principle of least privilege - users should only access/modify their own requests
- Implement CSRF tokens for state-changing operations

## Variant hunting
Check for similar missing authentication on other administrative endpoints (bulk operations, exports, approvals)
Test other resource types with sequential IDs for similar IDOR vulnerabilities (user accounts, reports, documents)
Verify if other state-changing operations (approve, reject, modify) have the same vulnerability
Test if authenticated users can delete requests belonging to other users or administrators
Check if deletion endpoint validates the request actually exists before deletion (information disclosure)
Test if cascading deletes occur (do related records get deleted automatically)

## MITRE ATT&CK
- T1190
- T1110
- T1078
- T1531
- T1485
- T1491

## Notes
This is part of a chain of vulnerabilities in the same system - the researcher references two prior reports (1489470 and 1489744) suggesting systemic security issues. The vulnerability is particularly dangerous because: (1) it requires no authentication whatsoever, (2) IDs are easily enumerable, (3) deletion appears to be permanent with no recovery mechanism mentioned, and (4) it directly impacts legitimate business operations. The researcher demonstrates responsible disclosure by warning about the danger of the PoC and not attempting to delete legitimate requests.

## Full report
<details><summary>Expand</summary>

Hi team,
During testing the security of ██████████ I found another possible attack vector:
(There are two reports preceding this one -  https://hackerone.com/reports/1489470 and  https://hackerone.com/reports/1489744)

I will try to explain:
When an user need access to that information system he fills a request form at:
https://█████████/████████
or
https://█████████/██████
After submitting the form the server response contains a █████████ which identifies this user request.
Then  the request is reviewed by an administrator, and he decides if user access will be granted or rejected.
The vulnerability I found is that unauthorized person can access the end point responsible for deleting user requests - █████████ and by providing just the ███ parameter he can delete any request.

## References

## Impact

An attacker can delete  legitimate user requests, disturbing the normal operation  of the system and causing data loss.
The user request ids are sequential numbers - my requests were given ids - ████████, so the attacker can delete all requests in the system by accessing the ████ end point with each ██████ from ██████████.

## System Host(s)
███████

## Affected Product(s) and Version(s)
██████████

## CVE Numbers


## Steps to Reproduce
1.  Activate Burp proxy, go to https://███/██████████, fill and submit the form (screenshot1)
2. Inspect server response in Burp and take a note of the returned █████ (screenshot2) which is number, referencing this user access request
3. (optional) we can confirm our request is in the system by performing the attack described in the other report I made (https://hackerone.com/reports/1489470) - resulting in our request being exfiltrated from the database:
execute following command, and replace the █████ parameter with the one you noted on step 2 (screenshot)
curl https://██████/██████████ -X POST -data="url=%2F████&██████████=████████" -k

4. Deleting the request - CAUTION - execute this step only by referencing ██████████ for requests, you made otherwise you will delete legitimate user request!(sceenshot4)
the command abusing the delete request endpoint is:
curl https://██████/███████████████ -X POST -data="url=%2F███████&███████=██████" -k

5. (optional) to confirm request is deleted you can execute again Step 3, which now responds with empty body - the request is no longer present in the database.

## Suggested Mitigation/Remediation Actions
The ██████████ endpoint should perform check if the user is logged in and authorized to use it.



</details>

---
*Analysed by Claude on 2026-05-24*
