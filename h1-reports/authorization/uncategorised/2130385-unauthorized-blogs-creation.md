# Unauthorized Blogs Creation via Session Cookie Manipulation

## Metadata
- **Source:** HackerOne
- **Report:** 2130385 | https://hackerone.com/reports/2130385
- **Submitted:** 2023-08-31
- **Reporter:** albetisi
- **Program:** Lichess.org
- **Bounty:** Not specified
- **Severity:** Medium
- **Vuln:** Broken Access Control, Insufficient Authorization Validation, Session Fixation/Manipulation, Account Privilege Escalation
- **CVEs:** None
- **Category:** uncategorised

## Summary
A Lichess user discovered that blog creation restrictions can be bypassed by replacing session cookies from an authorized account with those of a new/restricted account during the blog creation process. The server fails to validate authorization at critical points, allowing unauthorized blog creation on accounts that should not have this privilege.

## Attack scenario
1. Attacker creates a new account and confirms it lacks blog creation privileges
2. Attacker logs into an authorized account in a separate browser with full blog creation capabilities
3. Attacker begins creating a blog post on the authorized account and intercepts the request before submission using a proxy tool (Burp Suite)
4. Attacker replaces the session cookies in the intercepted request with the session cookies from the restricted new account
5. Attacker sends the modified request, receiving a successful response with a location header containing the newly created blog URL
6. Attacker accesses the location URL while logged into the restricted account and can now edit and finalize the blog post creation

## Root cause
The server performs authorization checks only at initial blog creation form access but fails to re-validate authorization during the actual blog submission/save operation. The application trusts the request parameters and cookies inconsistently, allowing an authorized request's blog creation payload to be executed with a different account's session context.

## Attacker mindset
The attacker recognized a timing window between authorization checks and submission. By understanding the request flow and intercepting at the critical pre-submission phase, they identified that server-side validation was insufficient. The attack exploits the assumption that if a user can initiate a blog creation, they can complete it, without proper per-operation authorization verification.

## Defensive takeaways
- Implement authorization checks at every critical operation boundary, not just at entry points
- Validate user eligibility/permissions immediately before any state-changing operation
- Use server-side session validation and account ownership verification for all blog-related operations
- Implement consistent authorization logic that cannot be bypassed through request manipulation
- Consider implementing CSRF tokens tied to specific accounts to prevent cross-account request execution
- Add logging and monitoring for authorization failures and suspicious cross-account activity
- Verify that authorization state is re-checked after form submission, not just on form load

## Variant hunting
Check other content creation features (forum posts, comments, wiki edits) for similar authorization bypass patterns
Test other restricted features for timing window vulnerabilities between permission checks and execution
Attempt session fixation attacks on other user-privilege-dependent operations
Test whether authorization is checked per-operation or per-session, identifying granularity gaps
Look for other endpoints that accept session cookies in requests that could be manipulated
Investigate if account modification operations (profile, settings) have similar vulnerabilities

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1550.001 - Use Alternate Authentication Material: Application Access Token
- T1548 - Abuse Elevation Control Mechanism

## Notes
This is a classic broken access control vulnerability with a clever exploitation technique. The attacker identified that the authorization boundary did not properly encompass the entire blog creation workflow. The vulnerability is particularly impactful because it allows account privilege escalation without credentials compromise. The fix requires shifting from request-level authorization checks to operation-level checks that verify the logged-in account at execution time, regardless of request origin.

## Full report
<details><summary>Expand</summary>

Hi,

An unauthorized blog creation vulnerability has been identified on the lichess.org . By manipulating certain request and leveraging the session cookies of a different account, an attacker can bypass account-specific limitations and create a blog post on an account that is not yet eligible to do so.


Steps:
1.Open a new account  and attempt to create a blog post, you will face this message below.

{F2653923}

2.Log in with a different browser and  an old account that has the ability to create blog posts , go to create some blog with test data and solve the capatcha, but before click save fire up the burp suite, catch the request and send it to repeater and then drop it

{F2653943}

3.Here ,I Replaced the cookies in the request with the cookeis of  the new account ,I clicked send and response be like:

{F2653958}

4.I coppied the location url and I visited it  in the browser while logged in with the new account.
https://lichess.org/[The Location Header]

5.You can see that as a new account we are able to edit the content and submit the form

6.Verify that the unauthorized blog post is successfully created in the new account.
{F2653979}


## Recommendation:

The platform's blog creation feature should be thoroughly reviewed and validated to ensure that all account restrictions are enforced correctly.

## Impact

Allows unauthorized users to circumvent the intended restrictions on blog creation and create posts on accounts that are not yet eligible to do so. This  lead to the spread of unauthorized or malicious content on the platform, potentially damaging the platform's reputation and user experience.

</details>

---
*Analysed by Claude on 2026-05-24*
