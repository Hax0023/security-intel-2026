# OTP Verification Response Manipulation Leading to Account Takeover on shop.mtn.ng

## Metadata
- **Source:** HackerOne
- **Report:** 2762462 | https://hackerone.com/reports/2762462
- **Submitted:** 2024-10-07
- **Reporter:** trev0ck
- **Program:** MTN Nigeria (shop.mtn.ng)
- **Bounty:** Not specified in writeup
- **Severity:** Critical
- **Vuln:** Improper Input Validation, Lack of Response Integrity Verification, Client-Side Trust Issues, Authentication Bypass, Insecure Direct Object References
- **CVEs:** None
- **Category:** auth-crypto

## Summary
The OTP verification endpoint on shop.mtn.ng fails to validate response integrity, allowing attackers to intercept and modify server responses to bypass OTP verification. By manipulating HTTP responses through a proxy, attackers can link arbitrary mobile numbers to their accounts and gain full account takeover without possessing the target phone number.

## Attack scenario
1. Attacker initiates login/registration flow on shop.mtn.ng and enters a victim's mobile number
2. Attacker requests OTP generation for the victim's number, which receives a legitimate OTP challenge
3. Attacker intercepts the OTP verification request using Burp Suite/proxy and deliberately submits an incorrect OTP
4. Server returns a 400 error response with 'Invalid OTP' message to the client
5. Attacker modifies the intercepted response in their proxy to change status from 400 to 200 and success flag to true
6. Client-side application accepts the tampered response as valid verification and grants access to the victim's account without ever validating the OTP server-side

## Root cause
The application implements OTP verification logic with client-side trust in server responses without cryptographic integrity protection. The server fails to implement HMAC, digital signatures, or response validation mechanisms, allowing attackers to modify responses in transit. Additionally, the verification logic likely relies on client-side state rather than server-side session validation of the OTP attempt.

## Attacker mindset
An attacker recognizes that modern web applications often transmit sensitive responses to clients and assumes the client-side code may naively trust these responses. By intercepting HTTP/HTTPS traffic at the application layer (before TLS termination on client), the attacker can modify JSON responses. The attacker realizes that if the server doesn't cryptographically sign responses or validate them server-side on subsequent requests, the application will accept the fraudulent response as legitimate, bypassing the entire OTP security mechanism.

## Defensive takeaways
- Implement server-side OTP state validation - maintain OTP verification status on the server and validate it before granting access, not client-side response acceptance
- Add response integrity verification using HMAC-SHA256 or digital signatures on all security-critical responses
- Enforce HTTPS with certificate pinning on mobile clients to prevent proxy interception attacks
- Implement rate limiting and IP-based restrictions on OTP verification attempts
- Add server-side account linking constraints - verify the OTP was actually submitted and validated before linking phone numbers
- Log all OTP verification attempts with device fingerprints and require re-authentication for account recovery
- Use server-side session tokens that expire quickly and tie OTP verification to specific session identifiers
- Implement anti-replay mechanisms and nonce validation for OTP requests

## Variant hunting
Check if password reset endpoints have similar response manipulation vulnerabilities
Test if email verification, 2FA codes, or security questions suffer from identical response tampering
Examine if other telecom providers (Airtel, Vodafone, Glo) implement OTP verification with similar client-side trust patterns
Test if the application accepts modified MSISDN values in the response to link different phone numbers than requested
Check if the API returns bearer tokens or session tokens in the verification response that can be forged
Test if the vulnerability extends to the actual login flow after account linking is bypassed
Examine if payment or transaction confirmation endpoints have similar response integrity issues

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1111 - Multi-Factor Authentication Interception
- T1589 - Gather Victim Identity Information
- T1110 - Brute Force
- T1556 - Modify Authentication Process
- T1539 - Steal Web Session Cookie
- T1040 - Network Sniffing

## Notes
This vulnerability is particularly severe because it affects a telecom service provider's authentication layer, potentially impacting millions of users. The fact that the attacker could link uncontrolled phone numbers suggests the application may not validate OTP delivery to the MSISDN before confirming verification. The vulnerability appears to be pure client-side response manipulation rather than exploiting cryptographic weaknesses, making it trivial to execute with basic proxy tools. The writeup demonstrates proof-of-concept with actual account access to a victim's phone number, indicating successful account takeover. Recommendation: Perform immediate security audit of all authentication endpoints and implement server-side verification before granting access.

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
