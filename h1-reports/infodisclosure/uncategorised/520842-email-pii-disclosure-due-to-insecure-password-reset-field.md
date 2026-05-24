# Email PII Disclosure via Insecure Password Reset Field - Information Enumeration

## Metadata
- **Source:** HackerOne
- **Report:** 520842 | https://hackerone.com/reports/520842
- **Submitted:** 2019-04-02
- **Reporter:** alyssa_herrera
- **Program:** HackerOne (Company name redacted)
- **Bounty:** Not specified in report
- **Severity:** Medium-High
- **Vuln:** Information Disclosure, User Enumeration, Insufficient Input Validation, Missing Rate Limiting, Inadequate Account Security
- **CVEs:** None
- **Category:** uncategorised

## Summary
The password reset endpoint leaks user email addresses when valid usernames are submitted, allowing attackers to enumerate and harvest sensitive email addresses. The lack of rate limiting compounds the issue by enabling large-scale enumeration attacks through username/name guessing. This represents an incomplete remediation of a previously reported vulnerability (report #235041).

## Attack scenario
1. Attacker identifies the password reset endpoint at /griduc/accounts/request_reactivation/
2. Attacker submits common names or usernames (e.g., 'Alex', 'Bryan', 'admin') to the password reset form
3. System responds with or exposes the associated email address for valid accounts
4. Attacker compiles a list of harvested email addresses through repeated enumeration attempts
5. Due to absent rate limiting, attacker performs brute-force enumeration against a dictionary of names/usernames
6. Attacker uses collected email addresses for targeted phishing campaigns or credential stuffing attacks against other services

## Root cause
The password reset mechanism was not properly redesigned to prevent information disclosure. The system returns differentiated responses for valid versus invalid accounts, and fails to implement rate limiting or request throttling. Previous remediation efforts were either reverted in code updates or incomplete in scope.

## Attacker mindset
An attacker would leverage this vulnerability for reconnaissance in targeted phishing campaigns. The ability to harvest real email addresses significantly increases phishing success rates. The enumeration capability enables attackers to build targeted lists of potential victims within the organization, particularly if they can identify high-value accounts (admin, knowles, etc.).

## Defensive takeaways
- Implement generic success responses for password reset requests regardless of account validity ('If this account exists, an email has been sent')
- Enforce strict rate limiting on password reset endpoints (e.g., max 3-5 requests per IP per hour)
- Log and alert on suspicious enumeration patterns (multiple failed username attempts from single IP)
- Require additional verification for password resets (security questions, email verification tokens with short TTL)
- Implement CAPTCHA on password reset forms to prevent automated enumeration
- Use consistent response times and message formatting to prevent timing-based user enumeration
- Conduct periodic security audits to verify previous vulnerability fixes weren't reverted
- Monitor for behavioral anomalies in password reset request patterns

## Variant hunting
Check other authentication endpoints (login, registration, account recovery) for similar information disclosure
Test for response time differences between valid and invalid usernames (timing attacks)
Attempt enumeration via other identifiers: email addresses, phone numbers, user IDs
Test password reset functionality across different user roles/privileges
Investigate whether error messages or HTTP status codes differ for valid vs invalid accounts
Check if the vulnerability extends to API endpoints if password reset has an API version
Test for account enumeration via account activation/confirmation endpoints
Verify if historical password reset logs can be accessed to identify previously enumerated accounts

## MITRE ATT&CK
- T1589.002
- T1590.002
- T1078.001
- T1110.004
- T1598.003

## Notes
This is a re-report of a previously identified vulnerability (report #235041) that was not properly remediated. The researcher suspects either a code reversion or incomplete patching. This demonstrates the importance of verification testing after security patches and the risks of incomplete vulnerability fixes. The combination of information disclosure with missing rate limiting creates a severe enumeration vulnerability suitable for large-scale reconnaissance operations.

## Full report
<details><summary>Expand</summary>

**Summary:**
I revisited report #235041 and discovered the vulnerability isn't patched properly as I was able to discover more emails I could gleam. It appears the core mechanism allows anyone who knows specific names or user names to leak sensitive emails 
**Description:**
This password reset field allows an attacker to guess at user accounts such as admin and it will then expose the account user's email, this coupled with the lack of rate limiting allows me to easily bruteforce through a list of names to grab various sensitive emails.  Normally password reset fields keep the account emails hidden to prevent any attempt to directly attack the user, for example phishing emails. 
## Impact
medium-high
## Step-by-step Reproduction Instructions

 First we visit, https://██████████/griduc/accounts/request_reactivation/
Then we type in Alex, and click reset. Observe the email █████ is leaked 

I was able to discover few other emails as well,  
Bryan =█████████
knowles = █████ bein

## Product, Version, and Configuration (If applicable)
N/A
## Suggested Mitigation/Remediation Actions
As per my previous report, I'd say the same solution is needed. I would recommend changing the account reset field to log any attempts for password resets to check for any malicious or abusive attempts to harvest account names, set a limit for amount of requests for the field, and additionally make a general message such as "We have sent the reset request to the email you used on registration"

My current theories either point to a possible code reversion or simply just removing the accounts  i used to previously test

## Impact

Attackers will be able to grab sensitive emails which can be targeted directly for phishing attacks or simple hijacked if the user in question reused their password and it has been previously leaked

</details>

---
*Analysed by Claude on 2026-05-24*
