# Broken Access Control - Horizontal Privilege Escalation via Phone Number Parameter Manipulation

## Metadata
- **Source:** HackerOne
- **Report:** 2319586 | https://hackerone.com/reports/2319586
- **Submitted:** 2024-01-15
- **Reporter:** aliyueka
- **Program:** MTN Nigeria
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Broken Access Control, Horizontal Privilege Escalation, Insecure Direct Object Reference (IDOR), Missing Authorization Check
- **CVEs:** None
- **Category:** auth-crypto

## Summary
The MTN offers dashboard fails to properly validate that authenticated users can only access their own phone number's offers and data. An attacker can modify the phone parameter in the URL to access any arbitrary phone number's sensitive information and perform unauthorized actions like subscribing data plans or airtime to victims. This allows complete horizontal privilege escalation where any authenticated user gains unauthorized access to all other users' accounts.

## Attack scenario
1. Attacker authenticates to https://mtn.ng/offers/ using their own phone number and OTP
2. After successful authentication, attacker is redirected to /offers/list?phone=<their_number>
3. Attacker identifies the phone parameter is user-controlled and not properly validated server-side
4. Attacker modifies the phone parameter to a different target number (e.g., ?phone=2349138557692)
5. Server returns sensitive offer data and account details for the victim's number without re-validating authorization
6. Attacker can now subscribe services, view transaction history, and send fraudulent messages on behalf of the victim

## Root cause
The application implements client-side or insufficient server-side authorization checks. The backend likely validates that a user is authenticated but fails to verify that the phone number in the request parameter matches the authenticated user's phone number before returning sensitive data or processing actions.

## Attacker mindset
An attacker with basic technical knowledge would quickly recognize that a phone number parameter in the URL is a direct object reference. The ability to freely change this parameter and receive unrestricted data suggests minimal server-side authorization enforcement, making this an obvious vector for account takeover at scale.

## Defensive takeaways
- Implement server-side authorization checks on every request - verify the authenticated user owns/has permission to access the requested resource
- Use indirect references (random tokens/UUIDs) instead of direct object references like phone numbers in URLs
- Validate that the phone number in the request matches the authenticated user's session/token on the backend
- Implement rate limiting and monitoring on sensitive operations like service subscriptions
- Add logging and alerting for access attempts to phone numbers other than the authenticated user's
- Conduct regular security audits focusing on IDOR and horizontal privilege escalation vectors
- Use security headers and implement CSRF protection for state-changing operations

## Variant hunting
Check other user-account endpoints for similar IDOR patterns (/profile, /transactions, /settings, /beneficiaries)
Test other identifiers beyond phone numbers (user IDs, email parameters, account numbers) for IDOR
Verify if the vulnerability extends to administrative functions or cross-tenant access
Check if JWT/session tokens properly validate ownership before processing requests
Test bulk operations or export functions for authorization bypass
Look for timing-based or predicable patterns in object IDs that could enable enumeration attacks

## MITRE ATT&CK
- T1190
- T1556
- T1578
- T1530

## Notes
This is a classic IDOR/Horizontal Privilege Escalation vulnerability affecting a telecommunications provider's customer-facing platform. The impact is critical as it enables attackers to compromise any customer account without their knowledge, perform fraudulent transactions, and impersonate MTN in communications with victims. The vulnerability is trivial to exploit and likely affects thousands of users. The fact that it affects sensitive telecom operations (airtime, data plans, SMS) makes this a high-priority fix.

## Full report
<details><summary>Expand</summary>

SUMMARY
access controls are broken, unauthorized users may gain access to sensitive information, modify data, or perform actions that they shouldn't be allowed to. This can lead to various security risks, including data breaches, unauthorized privilege escalation, and other malicious activities.

STEPS TO REPRODUCE
STEP 1:
Go to https://mtn.ng/offers/ {F2982514}
Enter your number and click on Submit Button {F2982517}
Click on Ok {F2982518}



STEP 2:
Enter the OTP code sent to your number {F2982521}
Click on Validate



STEP 3:
MTN offer dashboard will automatically display  {F2982526}
https://mtn.ng/offers/list?phone=2348160817474


STEP 4:
I changed the number that i logged in with my alternative number and it works successfully
{F2982536}
https://mtn.ng/offers/list?phone=2349138557692

In this situation an attacker change the phone number to number of his choice

Example:
If you click on this link you will have access to my MTN number without an authentication
https://mtn.ng/offers/list?phone=2349138557692

## Impact

This vulnerability allow an attacker to access any MTN number in Nigeria and allow threat actors to subscribe data or airtime to the victims.

It can also allow attackers to send messages of their choice to their targeted victims and the victims might think that the message come from MTN.

</details>

---
*Analysed by Claude on 2026-05-24*
