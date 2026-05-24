# Unauthorized Merchant Information Update via /php/merchant_details.php

## Metadata
- **Source:** HackerOne
- **Report:** 255651 | https://hackerone.com/reports/255651
- **Submitted:** 2017-08-02
- **Reporter:** adibou
- **Program:** Zomato
- **Bounty:** Unknown (not specified in report)
- **Severity:** high
- **Vuln:** Broken Access Control, Insufficient Authorization Checks, Mass Assignment, Account Takeover
- **CVEs:** None
- **Category:** uncategorised

## Summary
An unauthenticated or inadequately authenticated attacker can modify merchant account details including email, contact information, bank account details, and other sensitive fields via a POST request to /php/merchant_details.php. This could lead to merchant account takeover by changing the associated email address and potentially gaining access to confidential communications and financial information.

## Attack scenario
1. Attacker identifies the vulnerable endpoint /php/merchant_details.php and its update-merchant action parameter
2. Attacker enumerates valid merchant_id values (possibly through information disclosure or previous reports like #255648)
3. Attacker crafts a POST request with action=update-merchant and a target merchant_id they do not own
4. Attacker modifies critical fields including email address to one under their control
5. System accepts the unauthorized update without proper ownership validation
6. Attacker receives password reset emails and account verification messages, leading to account takeover

## Root cause
The application fails to implement proper authorization checks before updating merchant information. The endpoint likely only verifies that a user is authenticated (if at all) but does not verify that the authenticated user actually owns the merchant_id being modified. This is a classic Broken Access Control vulnerability combined with Mass Assignment, allowing modification of sensitive fields that should be restricted.

## Attacker mindset
An attacker would target this vulnerability to hijack merchant accounts for financial fraud, business impersonation, or to redirect customer communications and payments. By changing the email address, they can bypass account recovery mechanisms and lock out legitimate merchants while maintaining persistent access.

## Defensive takeaways
- Implement proper authorization checks: verify that the authenticated user owns/manages the merchant_id before allowing updates
- Use whitelist-based input validation: only allow modification of intended fields, not all parameters sent in requests
- Implement rate limiting and change confirmation mechanisms for sensitive fields like email and banking details
- Add audit logging for all merchant account modifications with timestamp, user ID, and IP address
- Require multi-factor authentication or additional verification for changes to critical fields
- Implement session-based merchant context binding to prevent cross-merchant access
- Use API versioning and deprecate outdated endpoints like /php/ style paths

## Variant hunting
Test other merchant management endpoints for similar authorization bypass patterns
Check if user_id or company_id parameters can be similarly manipulated
Investigate if merchant_id can be modified via GET requests or other HTTP methods
Test if the vulnerability applies to admin endpoints for managing multiple merchants
Check for authorization bypass in related endpoints that retrieve merchant information
Examine if merchant deletion, suspension, or financial report access have similar issues

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1199 - Trusted Relationship
- T1556 - Modify Authentication Process
- T1098 - Account Manipulation
- T1563 - Account Impersonation

## Notes
This report demonstrates a clear understanding of the vulnerability but lacks complete proof-of-concept documentation. The researcher responsibly noted that they couldn't fully test the account takeover scenario due to responsible disclosure guidelines. The reference to report #255648 (merchant creation vulnerability) suggests this is part of a chain of related authorization flaws. The vulnerability is particularly severe in the e-commerce/payments context (Zomato merchants handle financial information).

## Full report
<details><summary>Expand</summary>

Hello!

I discovered an interesting file : 
`https://www.zomato.com/php/merchant_details.php`

If I add in post content :
`action=update-merchant&merchant_id=95292&type=1&email=update@hotmail.fr&contact=update@hotmail.fr&name=update`

With the report #255648, I was able to create a merchant, I should use this merchant to provide a screenshot like in a real situation.


I'm also able to change :
`address, pincode, city, email, phone tan_number, bank account name, company_id, payu_id, contact, restaurants` and more...


An attacker would change the mail to receive confidential mails it may can be leading to an merchant takeover if you use the mail to bound it with the account of the user. I couldn't try this scenario due to your rules about users data.

Do you have a test merchant_id i can play with to test that before you resolve the report?

Screenshot : updatehttp.png

If you have any questions...
nbsp


</details>

---
*Analysed by Claude on 2026-05-24*
