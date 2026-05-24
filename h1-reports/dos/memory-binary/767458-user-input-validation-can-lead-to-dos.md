# Lack of Input Validation on Phone Number Field Allows Denial of Service

## Metadata
- **Source:** HackerOne
- **Report:** 767458 | https://hackerone.com/reports/767458
- **Submitted:** 2020-01-03
- **Reporter:** meepmerp
- **Program:** Twitter
- **Bounty:** Not specified in report
- **Severity:** medium
- **Vuln:** Improper Input Validation, Denial of Service (DoS), Resource Exhaustion
- **CVEs:** None
- **Category:** memory-binary

## Summary
The phone number input field on Twitter's account completion page lacks proper length validation and input constraints, allowing attackers to submit arbitrarily large payloads. This causes backend processing to consume excessive resources, resulting in 503 Service Unavailable errors and denial of service conditions.

## Attack scenario
1. Attacker navigates to https://twitter.com/account/complete
2. Attacker identifies the phone number input field has no character limit validation
3. Attacker crafts a payload consisting of an extremely long string of characters
4. Attacker submits the oversized payload through the phone number textbox
5. Backend server attempts to process and encode the excessive payload
6. Server resources become exhausted, resulting in 503 Service Temporarily Unavailable error

## Root cause
Missing input validation on the phone number field, specifically the absence of maximum length constraints and payload size limits before backend processing. The backend appears to encode the input without first validating its size, causing resource exhaustion.

## Attacker mindset
The attacker recognized that a common user input field lacked basic validation controls. They tested boundary conditions by submitting abnormally large input to discover that the backend would attempt to process it regardless of size, leading to resource exhaustion and service degradation.

## Defensive takeaways
- Implement strict input validation with maximum length limits on all user input fields, especially phone numbers (typically 15-20 characters including formatting)
- Apply validation both client-side and server-side before any processing or encoding operations
- Implement request size limits and timeout mechanisms to prevent resource exhaustion attacks
- Add rate limiting on form submissions to prevent rapid repeated submissions of malicious payloads
- Use allowlist-based validation for phone numbers (permit only digits, spaces, hyphens, parentheses)
- Implement circuit breakers or graceful degradation to handle backend processing failures without exposing 503 errors
- Monitor for unusual input patterns and processing times that may indicate DoS attempts

## Variant hunting
Check other user input fields (email, username, address, etc.) for similar lack of length validation
Test form fields during account signup, profile editing, and password reset flows
Attempt to submit oversized payloads to API endpoints that accept phone number parameters
Test for similar resource exhaustion issues with other data types (large JSON objects, nested structures)
Look for missing validation on optional fields that might be overlooked during development

## MITRE ATT&CK
- T1190
- T1498
- T1499

## Notes
Report quality is reduced due to redacted content (█████), making it difficult to assess exact payload size and nature. Phone number validation is a common oversight in form development. The fact that backend encoding was triggered before validation suggests the application architecture processes user input before sanitization, a critical security anti-pattern. The 503 error indicates the application may lack proper timeout handling and circuit breaker patterns.

## Full report
<details><summary>Expand</summary>

Hi Security Team,

**Summary:** 
There is no limit to the number of characters on phone numbers and using this you can perform a DOS Attack

**Description:**
On the input form of phone number in ***https://twitter.com/account/complete*** there's no Input validation using this you can send more payload and may cause of Denial of service or **503 Service Temporarily Unavailable**

## Steps To Reproduce:

So this is the normal page 
█████████

Input this payload on the Phone number textbox ████ then submit as you can see the payload was encoded on backend so the payload may load more

████

After submitting this is the response on burp **503 Service Temporarily Unavailable**

█████████

And on the page this is the result .

████████

## Supporting Material/References:

+ payload.txt

Thank you! 
Regards

## Impact

Attacker can perform a DOS because of lack of input validation

</details>

---
*Analysed by Claude on 2026-05-24*
