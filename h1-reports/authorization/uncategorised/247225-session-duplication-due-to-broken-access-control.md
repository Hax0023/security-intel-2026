# Session Duplication due to Broken Access Control and Improper Email Validation

## Metadata
- **Source:** HackerOne
- **Report:** 247225 | https://hackerone.com/reports/247225
- **Submitted:** 2017-07-08
- **Reporter:** anurag98
- **Program:** WakaTime
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Broken Access Control, Improper Input Validation, Insufficient Authentication, Account Takeover, Privilege Escalation
- **CVEs:** None
- **Category:** uncategorised

## Summary
The platform fails to properly validate email ownership during account creation and API key generation, allowing attackers to register accounts using victims' email addresses and obtain valid API keys. Combined with insufficient password reset procedures, this enables session duplication where both attacker and legitimate user can simultaneously access the same account with parallel sessions.

## Attack scenario
1. Attacker enumerates valid email addresses through failed registration attempts or other reconnaissance
2. Attacker creates a new account using victim's email address without email verification requirement
3. Attacker generates and downloads API key from the newly created account
4. Legitimate victim attempts to create account with same email, fails due to existing registration
5. Victim initiates password reset, which succeeds without proper email verification checks
6. Both attacker and victim obtain valid API keys and can simultaneously perform actions (coding, submissions) under the same account identity

## Root cause
The application lacks proper email ownership verification during account creation and does not invalidate attacker-controlled sessions upon legitimate password reset. The API key generation mechanism does not validate that the requester is the actual account owner, and insufficient session management allows multiple concurrent sessions from different sources.

## Attacker mindset
An attacker recognizes that email validation is not enforced during signup and can preemptively claim victim accounts before legitimate users. By understanding the password reset flow bypasses email verification, the attacker maintains parallel access. The attacker's goal is account takeover, reputation damage, and the ability to manipulate user rankings and coding metrics.

## Defensive takeaways
- Implement mandatory email verification via confirmation link before account activation
- Validate email ownership before allowing API key generation
- Invalidate all existing sessions and API keys when password reset is initiated
- Implement rate limiting and CAPTCHA on registration endpoints to prevent account enumeration and mass registration
- Use secure random token generation for password reset links with strict expiration times
- Monitor for suspicious parallel sessions from different IP addresses on same account
- Implement activity logging to detect unauthorized API key usage patterns
- Require user confirmation when new API keys are generated
- Add email notification when new sessions or API keys are created

## Variant hunting
Check if email verification can be bypassed using homograph attacks (similar looking domains)
Test if disposable/temporary email services are blocked during registration
Verify if password reset tokens can be reused or are single-use only
Check if API keys remain valid after account deletion or suspension
Test concurrent login sessions from multiple geographic locations
Verify if account creation with '+' email aliasing is properly deduplicated
Check if invitation/sharing features allow unauthorized access to victim accounts
Test if two-factor authentication invalidates existing sessions on setup

## MITRE ATT&CK
- T1586 - Compromise Accounts
- T1190 - Exploit Public-Facing Application
- T1110 - Brute Force
- T1078 - Valid Accounts
- T1556 - Modify Authentication Process
- T1098 - Account Manipulation
- T1133 - External Remote Services

## Notes
This is a classic broken access control vulnerability compounded by insufficient input validation. The video proof-of-concept confirms the ability to maintain parallel sessions. The attacker can impact integrity (reputation damage, difficulty manipulation) and confidentiality (access to victim's work/metrics). The vulnerability is particularly dangerous as it affects a developer-focused platform where code quality and metrics are professionally important. The lack of email verification is a fundamental security oversight that should have been caught in initial architecture review.

## Full report
<details><summary>Expand</summary>

Due to improper validation of user before generating an API-KEY and improper measures taken at the time of password reset, it is possible to generate a parallel session at the attacker's end.

Proof of concept video is attached to confirm the vulnerability and to demonstrate the Impact of this _logical_ bug.

Steps to Reproduce
=============
Attacker
---------
- Create an account with victims email.
- Download the coding platforms and get API-KEY.
- He can code from the platforms using the victims API-key.

Victim
-------
- User fails to create an account, due to email already registered and does a password reset.
- Downloads the coding platform and get API-KEY.
- He codes using API-KEY.

It is possible for the Attacker and Victim, for coding at the same time, which will be shown at the dashboard. Attacker can reduce the difficulty and can damage the reputation of the coder.

 Impact
=====

__Attacker can brute-force email and register multiple account on wakatime to get API-Key of many users.__
 
Improper rank calculation.

Session duplication by the attacker



</details>

---
*Analysed by Claude on 2026-05-24*
