# Stored XSS in Postal Code Field - Advance Cash On Delivery Feature

## Metadata
- **Source:** HackerOne
- **Report:** 190951 | https://hackerone.com/reports/190951
- **Submitted:** 2016-12-13
- **Reporter:** prem1807
- **Program:** Unknown (HackerOne report 190951)
- **Bounty:** Unknown
- **Severity:** high
- **Vuln:** Cross-Site Scripting (XSS), Stored XSS, Input Validation Failure
- **CVEs:** None
- **Category:** web-api

## Summary
A stored XSS vulnerability was discovered in the manual postal code entry field of the newly launched Advance Cash On Delivery feature for Indian users. The application fails to properly sanitize user input, allowing attackers to inject malicious JavaScript code that persists in the database and executes for all users viewing that data.

## Attack scenario
1. Attacker navigates to the Advance Cash On Delivery checkout option
2. Attacker selects manual postal code entry instead of automated lookup
3. Attacker enters malicious JavaScript payload (e.g., <script>alert('XSS')</script>) in the postal code field
4. Attacker completes the transaction/submission, causing the payload to be stored in the database
5. When the order details page or payment confirmation is viewed by the victim or admin, the stored payload executes
6. Attacker can steal session cookies, redirect users, or perform actions on behalf of victims

## Root cause
Inadequate input validation and output encoding on the postal code field. The application accepts arbitrary input without proper sanitization and stores it directly in the database without escaping special characters or validating against postal code formats.

## Attacker mindset
An attacker would target this field because: (1) users typically trust payment/checkout forms, (2) postal code fields are often overlooked in security testing, (3) stored XSS in order data affects multiple users including admins, (4) the newly launched feature may have rushed implementation without security review.

## Defensive takeaways
- Implement strict input validation: validate postal codes against known formats for the respective country (India postal codes are 6 digits)
- Apply output encoding when displaying postal codes (HTML entity encoding or context-appropriate escaping)
- Use allowlist validation for postal code format before database storage
- Implement Content Security Policy (CSP) headers to mitigate XSS impact
- Perform security testing on new features before production launch, especially payment flows
- Apply principle of least privilege - sanitize and validate all user inputs regardless of field type
- Use parameterized queries and prepared statements to prevent injection attacks

## Variant hunting
Check other location-based fields (city, state, street address) for similar XSS vulnerabilities
Test other new features launched alongside Cash On Delivery for input validation gaps
Examine international shipping/postal code fields for similar issues
Review stored data in admin panels for reflected XSS in order viewing interfaces
Test other form fields that accept free-text input (phone numbers, names) with XSS payloads
Check if the vulnerability exists in the edit/update postal code functionality

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1598: Phishing - Spearphishing Link (if used in follow-up attacks)
- T1566: Phishing (delivery mechanism)
- T1539: Steal Web Session Cookie (via XSS execution)

## Notes
The report lacks technical depth (mentions screenshot but no payload details shown). The vulnerability affects a payment-critical feature, increasing severity. India-specific launch suggests this feature may have had accelerated development timeline. The fact that it's in a checkout flow makes it particularly dangerous as it affects transaction integrity and user trust.

## Full report
<details><summary>Expand</summary>

Hello,
I had found a XSS vulnerability in manually entering postal codes in "Advance Cash On Delivery" option which is newly launched for indians.Below is the screenshot attached.
Thank You.

</details>

---
*Analysed by Claude on 2026-05-12*
