# Lack of Input Validation on Username Field Leading to Denial of Service

## Metadata
- **Source:** HackerOne
- **Report:** 768677 | https://hackerone.com/reports/768677
- **Submitted:** 2020-01-06
- **Reporter:** meepmerp
- **Program:** Twitter/X
- **Bounty:** Not specified in report
- **Severity:** Medium
- **Vuln:** Improper Input Validation, Denial of Service (DoS), Resource Exhaustion
- **CVEs:** None
- **Category:** memory-binary

## Summary
The Twitter username change endpoint at /settings/screen_name lacks input validation on the username field, allowing attackers to submit excessively long payloads that cause server-side errors (HTTP 500). This denial of service vulnerability affects the availability of the account settings functionality for impacted users.

## Attack scenario
1. Attacker authenticates to their Twitter account
2. Attacker navigates to Settings > screen_name (username change page)
3. Attacker crafts a malicious payload exceeding normal username length constraints
4. Attacker submits the oversized payload through the username input form
5. Server processes the unvalidated input, triggering resource exhaustion or processing error
6. Server returns HTTP 500 Internal Server Error, denying legitimate service to the user

## Root cause
The backend API endpoint processing username changes fails to implement proper input validation, specifically missing: (1) maximum length restrictions on username field, (2) character set whitelisting, (3) input sanitization before processing, and (4) rate limiting on submission attempts.

## Attacker mindset
A low-skill attacker can easily discover and exploit this vulnerability through simple form manipulation. The attacker may be motivated by disrupting Twitter's service, testing defensive capabilities, or demonstrating security gaps. The simplicity of exploitation (just submit long text) makes it an attractive target for script-kiddies and vulnerability researchers.

## Defensive takeaways
- Implement strict input validation on all user-supplied data, enforcing length limits, character whitelisting, and format validation before backend processing
- Define clear username constraints (max/min length, allowed characters) and enforce consistently across frontend and backend
- Add rate limiting and CAPTCHA challenges on sensitive endpoints like account settings to prevent automated abuse
- Implement proper exception handling to return appropriate HTTP status codes (400 Bad Request) instead of exposing 500 errors
- Use parameterized queries and prepared statements to prevent injection-based DoS attacks
- Implement input size limits at the web server level (e.g., max POST body size) as a defense-in-depth measure
- Monitor for unusual input patterns and implement alerting on repeated invalid submissions from single accounts

## Variant hunting
Check other settings pages (bio, display name, location) for similar validation gaps
Test other profile modification endpoints for missing input validation (profile picture upload size, header image dimensions)
Investigate form fields accepting free-text input across the platform for length/character restrictions
Review API endpoints for batch operations that might amplify DoS impact (e.g., bulk user updates)
Test comment/tweet submission fields for similar unbounded input vulnerabilities
Analyze password reset and email change flows for input validation weaknesses

## MITRE ATT&CK
- T1190
- T1499
- T1499.1
- T1499.2

## Notes
The report lacks specific details about payload size/content and the exact error triggering mechanism. The 'payload.txt' attachment is referenced but not provided in the content. Twitter likely has standard username constraints (15 characters max historically), suggesting the fuzzing test exceeded these limits significantly. This is a relatively low-severity DoS since it only affects the attacker's own account settings temporarily, not infrastructure-wide availability. The fix is trivial (add validation), making this a good example of oversight rather than complex security architecture failure.

## Full report
<details><summary>Expand</summary>

Hi Security Team,

## Summary:
There is no limit to the number of characters in the issue comments, which allows a DoS attack. The DoS attack affects server-side.

## Description

On the input form of Username in `https://twitter.com/settings/screen_name` there's no Input validation using this you can send more payload and may cause of Denial of service or error code 500 Internal Server Error/Internal Error

## Proof of Concept

1. First login your twitter account 
2. Go to the Settings of your account 
3. Click Username
4. Change your username and put the payload then submit

And the response was pop up and say.
==Something went wrong, but don't fret --- it's not your fault.==
and the response code on the server side is `500 Internal Server Error`

Kindly check 2 uploaded photo for my additional Proof of Concept

### Remediation:

    Implementing input validation
    Validating free-form Unicode text
    Define the allowed set of characters to be accepted.
    Minimum and maximum value range


Supporting Material/References:

    payload.txt

Thank you!
Regards

## Impact

Attacker can perform a DOS because of lack of input validation

</details>

---
*Analysed by Claude on 2026-05-24*
