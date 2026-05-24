# OTP Verification Bypass via Response Manipulation Leading to Account Takeover

## Metadata
- **Source:** HackerOne
- **Report:** 2762462 | https://hackerone.com/reports/2762462
- **Submitted:** 2024-10-07
- **Reporter:** trev0ck
- **Program:** MTN Nigeria (shop.mtn.ng)
- **Bounty:** Not specified in writeup
- **Severity:** Critical
- **Vuln:** Broken Authentication, Client-Side Validation, Lack of Response Integrity Verification, OTP Bypass, Account Takeover
- **CVEs:** None
- **Category:** auth-crypto

## Summary
A critical authentication vulnerability exists in MTN Nigeria's OTP verification process that allows attackers to bypass OTP validation by manipulating HTTP responses. By intercepting and modifying the server's OTP verification response to indicate success, attackers can link any mobile number to their account and achieve complete account takeover without possessing the victim's phone number.

## Attack scenario
1. Attacker initiates OTP request for victim's phone number on shop.mtn.ng platform
2. Attacker intercepts OTP verification POST request using proxy tool (Burp Suite/Caido)
3. Attacker submits intentionally incorrect OTP to observe server response structure
4. Attacker modifies intercepted response to change status from 400 to 200 and success flag to true
5. Client-side application accepts forged response and grants authentication without valid OTP
6. Attacker gains full account access with victim's phone number linked and can perform unauthorized actions

## Root cause
The application relies entirely on client-side validation of OTP verification responses without implementing server-side integrity checks. The server fails to cryptographically sign responses or implement session binding, allowing arbitrary response manipulation. Authentication decisions are made based on client-controlled response data rather than server-side session state verification.

## Attacker mindset
An attacker recognizes that modern web applications often trust client responses for speed/performance and identifies that OTP verification—a critical security control—lacks response integrity protection. The attacker uses standard security testing tools to observe the response structure, then performs simple JSON manipulation to bypass multi-factor authentication entirely, gaining access to high-value targets.

## Defensive takeaways
- Never trust client-side response data for authentication decisions; maintain server-side session state and verify all credentials server-side
- Implement cryptographic signing (HMAC/JWT) of all authentication responses to ensure integrity and prevent tampering
- Use server-side session tokens rather than relying on client responses to indicate authentication success
- Implement rate limiting and account lockout policies on OTP verification endpoints to prevent brute force attacks
- Add additional verification steps after OTP validation (step-up authentication) for sensitive account changes
- Log and monitor suspicious OTP verification patterns (invalid OTPs followed by immediate success)
- Implement response integrity checks with Content Security Policy and Subresource Integrity where applicable
- Conduct security-focused code reviews specifically examining authentication and authorization flows

## Variant hunting
Check if similar response manipulation bypasses exist in password reset flows
Test if email verification endpoints have identical client-side validation vulnerabilities
Examine two-factor authentication implementations across other MTN services
Review if session tokens are properly validated on subsequent requests after bypassed OTP
Test if response status codes alone (without body verification) are used for authorization decisions
Check SMS delivery and OTP generation endpoints for potential direct manipulation
Review if identical vulnerability exists in registration, login, and account recovery flows

## MITRE ATT&CK
- T1190
- T1110
- T1621
- T1528
- T1111

## Notes
This vulnerability represents a fundamental authentication bypass where the most critical security control—OTP verification—is undermined by poor implementation of response integrity. The fact that attackers can link any phone number without possession demonstrates complete failure of the authentication mechanism. The vulnerability is trivially exploitable and would affect all users of the platform, making this a worm-class vulnerability. The writeup demonstrates proper POC methodology by showing the exact request/response format and clearly documenting the manipulation steps.

## Full report
<details><summary>Expand</summary>

## Summary
A critical vulnerability was identified in the OTP verification process on the shop.mtn.ng platform, which allows attackers to add and verify mobile numbers that they do not control. By tampering with the OTP verification request, an attacker can link a victim's mobile number to their account. This leads to an Account Takeover (ATO) scenario where the attacker gains full access to the victim's account without owning or controlling the victim's phone number.

## Steps to Reproduce

###  Initiate OTP Request
- Begin the login or registration process on the platform.
- Enter a valid mobile number (MSISDN) and request an OTP.

### Capture OTP Verification Request
- Use a proxy tool like **Burp Suite** or **Caido** to intercept the OTP verification request when submitting the OTP.
- The intercepted request will look like this

```http
POST /mtn_otp/index/verification/ HTTP/2
Host: shop.mtn.ng
Content-Type: application/x-www-form-urlencoded
Content-Length: 53

ajax=1&action=verifyotp&msisdn=██████&otp=███████
```
### Manipulate Server Response

- Upon capturing the request, submit an incorrect OTP to receive the server's response

```json
{
  "status": 400,
  "message": "Invalid OTP",
  "msisdn": "█████████",
  "success": false
}
```

Modify the response in the intercepted traffic to indicate a successful verification

```json
{
  "status": 200,
  "message": "success",
  "msisdn": "██████████",
  "success": true
}
```
This will trick the client into thinking that the OTP was successfully verified, even though the OTP is incorrect.

- The manipulated server response now grants full access to the victim's phone number account. Even though the OTP was incorrect, the altered response bypasses the verification, which could allow the attacker to log in as the target user.

## NOTE I do not own this phone number at all and as you can see it is now linked to my account
████████

# Root Cause

- The application fails to protect against the manipulation of the OTP verification response. The server does not perform integrity checks on the response sent back to the client, allowing attackers to alter it and bypass OTP verification entirely.

## Impact

An attacker can exploit this flaw to hijack user accounts by manipulating the OTP verification response. This allows the attacker to

1. Access personal user information such as names, phone numbers, and email addresses.
2. Modify sensitive account settings like passwords, linked emails, and phone numbers.
3. Perform unauthorized actions such as transactions or purchases.
4. Further escalate the attack to other services connected to the victim's account.

</details>

---
*Analysed by Claude on 2026-05-24*
