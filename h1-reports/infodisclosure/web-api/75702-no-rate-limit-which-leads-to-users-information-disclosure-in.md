# No Rate Limit on PIN Verification Endpoint Leads to User Information Disclosure

## Metadata
- **Source:** HackerOne
- **Report:** 75702 | https://hackerone.com/reports/75702
- **Submitted:** 2015-07-15
- **Reporter:** tmfelwu
- **Program:** Romit (HackerOne Report #75702)
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Brute Force Attack, Missing Rate Limiting, Information Disclosure, Broken Authentication, Insufficient Access Control
- **CVEs:** None
- **Category:** web-api

## Summary
The /v0/cash/auth/login endpoint on api.romit.io lacks rate limiting on PIN verification attempts, allowing attackers to brute force PINs using algorithmically generated signatures. Upon successful PIN verification (before SMS/GA code validation), sensitive user information including verification documents, email, and DOB is automatically added to the attacker's operator wallet, disclosing the target user's private data.

## Attack scenario
1. Attacker creates a legitimate account at app.romit.io and obtains API credentials (apiKey, apiSecret, Location-ID)
2. Attacker selects 'Send Money' feature and inputs a target user's phone number
3. Attacker develops/uses the provided signature generation algorithm to create valid Authorization headers for PIN verification attempts
4. Attacker sends repeated POST requests to /v0/cash/auth/login with different PIN values without encountering rate limiting blocks
5. Upon correct PIN submission, the target user's complete profile (including verification documents, email, DOB) is automatically provisioned to attacker's operator wallet
6. Attacker gains unauthorized access to sensitive PII and compliance documentation for any user whose phone number is known

## Root cause
The application implements two critical security failures: (1) No rate limiting on the PIN verification endpoint allows brute force attacks on a 4-digit PIN space (~10,000 combinations), and (2) User information is added to operator wallet upon PIN verification alone rather than after completing multi-factor authentication (SMS/GA code), premature exposure of sensitive data during incomplete authentication flows.

## Attacker mindset
An attacker with basic technical knowledge can identify this vulnerability by recognizing the missing rate limit protection on authentication endpoints and observing that sensitive user data is exposed at an intermediate authentication stage. The ability to generate valid signatures reduces friction, making the attack scalable. The attacker's motivation is identity fraud, compliance document theft, or creating fraudulent accounts using stolen verification documents.

## Defensive takeaways
- Implement strict rate limiting on all authentication endpoints (recommend: 3-5 failed attempts per 15 minutes per IP/phone number)
- Delay sensitive user information provisioning until ALL authentication factors are successfully verified (PIN + SMS/GA code)
- Implement CAPTCHA or progressive delays after repeated failed authentication attempts
- Log and alert on suspicious authentication patterns (multiple PINs for same phone number)
- Use account lockout mechanisms after N failed PIN attempts
- Implement IP-based and device fingerprinting to detect distributed brute force attacks
- Mask sensitive user information in intermediate authentication responses
- Require explicit user consent before adding to operator wallet, not automatic provisioning
- Implement server-side PIN hashing rather than client-side signature generation for authentication

## Variant hunting
Check other endpoints using phone number as identifier for similar rate limit issues
Investigate if signature generation algorithm has predictability or cryptographic weaknesses
Test if attacker can retrieve user information through other endpoints after partial authentication
Verify if session tokens are issued prematurely before MFA completion, allowing lateral movement
Check SMS/GA verification endpoint for similar rate limiting bypasses
Test if operator wallet provisioning can be triggered through API manipulation without PIN
Examine if verification documents are stored with predictable identifiers or accessible through other endpoints
Probe for timing attacks revealing whether PIN was partially correct

## MITRE ATT&CK
- T1190
- T1110
- T1110.001
- T1078
- T1555
- T1526
- T1589
- T1040

## Notes
Report lacks specificity on PIN length, signature algorithm strength, and whether SMS/GA code also lacks rate limiting. The vulnerability chain is severe: authentication bypass (brute force) + premature data exposure (broken authorization) + PII disclosure. The provided signature generation code (calSignature.js) suggests client-side cryptographic operations which may be reversible or predictable. Financial application context (money transfer, operator wallets) elevates impact. Romit appears to be a remittance/money transfer platform, making compliance document theft particularly damaging.

## Full report
<details><summary>Expand</summary>

**HOST**
api.romit.io

**Endpoint**
/v0/cash/auth/login

**Issue**
When an attacker tries to login at app.romit.io, he is prompted to enter the PIN . There is no rate limit to verify this. Although there is a an authorization header `Authorization: Credential=b67b0b10571ac00444de3cffde0b5b05, SignedHeaders=host;x-locale;x-location-id;x-request-date;x-session-id, Signature=976aeeeb8a3d07aa9a927a4d8972c819674b4385a6466b17aad345d5cee1c082` which sends a signature with the request,which is generated using the PIN specified by the user, the attacker can simply generate this signature[see attached calSignature.js] Now this can be used to bruteforce the PIN but its pretty useless because the server prompts for the SMS code or GA code which the attacker has no way to know.

Now , it gets interesting because as soon as the correct pin is added, the users info is added to the operator waller(in this case the attackers wallet) including all the verification documents, email, DOB etc.[see attached pictures]
The attacker can see any users info once he knows the users phone number.

**PoC**
1. Setup an account at app.romit.io, use your apiKey, apiSecret and Location-ID to setup.
2. Now click on Send Money, add the Phone Number you want to bruteforce.
3. Once you get the correct PIN the users info will be added to your operator wallet.

**Solution**
1.  I believe there should be rate limit.
2. User should be added to operator wallet only after he/she has provided the SMS /GA code.


Thanks
crab

</details>

---
*Analysed by Claude on 2026-05-24*
