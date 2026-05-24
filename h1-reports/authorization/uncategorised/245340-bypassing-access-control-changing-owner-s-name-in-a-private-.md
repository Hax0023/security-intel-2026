# Access Control Bypass: Non-Owner Member Can Edit Owner's Name in Private Leaderboard

## Metadata
- **Source:** HackerOne
- **Report:** 245340 | https://hackerone.com/reports/245340
- **Submitted:** 2017-07-02
- **Reporter:** tikoo_sahil
- **Program:** HackerOne (specific platform not disclosed in report)
- **Bounty:** Not specified in writeup
- **Severity:** Medium
- **Vuln:** Access Control Bypass, Privilege Escalation, Authorization Flaw
- **CVEs:** None
- **Category:** uncategorised

## Summary
A non-owner member of a private leaderboard can bypass access controls to edit the owner's name despite receiving a forbidden error on the first attempt. By retrying the edit action, the member gains access to edit the owner's profile information, violating the intended access control model where only owners should have such privileges.

## Attack scenario
1. Attacker creates a private leaderboard as the initial owner and invites another account they control
2. Attacker accepts the invitation using the second account, joining the leaderboard as a member
3. Attacker demotes themselves to member role and promotes the second account to owner
4. Attacker attempts to edit the current owner's name through the members management section
5. System returns a forbidden error on initial edit attempt, suggesting proper access control
6. Attacker clicks the edit button again and successfully accesses the name editing popup, bypassing the access control check

## Root cause
The application implements access control checks that appear to fail on first request but succeed on retry, likely due to a race condition, improper session state validation, or inconsistent authorization logic between different request handlers. The initial forbidden response may be cached or the authorization state may not be properly persisted across consecutive requests.

## Attacker mindset
An attacker would recognize that initial rejection doesn't always mean permanent denial—retry attempts can reveal inconsistent security implementations. By testing persistence of authorization checks and state management, they discover the vulnerability is exploitable through simple repetition.

## Defensive takeaways
- Implement consistent authorization checks across all request paths, not just initial attempts
- Validate user permissions at every access point, not relying on initial state validation
- Ensure authorization logic is idempotent—same permission check should return same result regardless of retry count
- Implement proper session state validation to prevent race conditions in permission evaluation
- Use role-based access control (RBAC) verified server-side on every modification request
- Add audit logging for all member management operations, especially ownership changes
- Test security controls with automated retry scenarios to detect inconsistent behavior

## Variant hunting
Test other member management operations (delete, role change, email update) for similar bypass patterns
Check if rapid sequential requests to the same endpoint can bypass authorization
Test with different HTTP methods (PUT vs POST) for the same resource modification
Verify if authorization checks are cached and can be bypassed by modifying request headers
Attempt to modify other sensitive leaderboard attributes using the same retry technique
Check if concurrent requests from different sessions can cause race condition in permission validation
Test if changing user role mid-request affects authorization outcome

## MITRE ATT&CK
- T1190
- T1548
- T1078

## Notes
The vulnerability demonstrates a common pattern where authorization is checked but not properly enforced—the forbidden response on first attempt creates false confidence in security controls while the actual bypass is trivially repeatable. The report lacks specific technical details about the application platform and endpoint structure, which suggests this may be from a private/undisclosed bug bounty program or the reporter redacted sensitive details. The writeup would benefit from including HTTP request/response details and timing information to better understand the root cause.

## Full report
<details><summary>Expand</summary>

Hello, 

I would like to mention a bug here that is regarding changing the name of the owner of a leaderboard by a member that is first shown forbidden but when you again try to change owner's name you can see the changes to name made in the pop up that appears.
Basically when I created a private leaderboard  named test1 on my account ███ then in the next step I sent invitation to ████ so as this email was also mine I accepted the request to join the leaderboard and then I visited the members section  of the leaderboard through my ████████ account (owner account)

There I saw an edit option for the name of the member of leaderboard test1 that was the member with email ███ , so before that I opened a new settings page and made the member with email ████ the owner and made my account role as member , see below 

{ ███████} 

Then on the editing page when i tried to edit the name of the user to testing  with email █████ which had now become the owner and I was a member so I got the below forbidden error 

{ ████████}

But when I clicked on edit button again I saw the pop up saying 'Enter new name for testing ' see below pic 

{ ████} 

So clearly I was able to bypass the access control set for the members of a leaderboard.
So please patch it .

Regards
Sahil tikoo

</details>

---
*Analysed by Claude on 2026-05-24*
