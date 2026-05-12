# Stored XSS in Private Message System

## Metadata
- **Source:** HackerOne
- **Report:** 729424 | https://hackerone.com/reports/729424
- **Submitted:** 2019-11-05
- **Reporter:** mosuan
- **Program:** Shopify
- **Bounty:** Not specified in writeup
- **Severity:** High
- **Vuln:** Stored Cross-Site Scripting (XSS), Improper Input Validation, Insufficient Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A stored XSS vulnerability exists in the private messaging system accessible through the admin customers panel. An attacker can inject malicious JavaScript into private messages that will execute when an admin views the message, potentially compromising admin accounts.

## Attack scenario
1. Attacker sends a private message to a customer containing JavaScript payload (e.g., <script>alert('XSS')</script> or event handler)
2. Message is stored in the database without proper sanitization or encoding
3. Admin navigates to Customers section and clicks on the customer's email address
4. Admin clicks to view the sent message containing the payload
5. JavaScript executes in the admin's browser session with admin privileges
6. Attacker can steal session tokens, modify customer data, or perform administrative actions

## Root cause
The private messaging feature fails to properly sanitize user input before storing it in the database and does not apply adequate output encoding when displaying messages. The application trusts stored message content without validating or escaping HTML/JavaScript special characters.

## Attacker mindset
An attacker with access to send messages (customer or lower-privileged user) recognizes that admin staff view these messages in a privileged context. By injecting persistent XSS, they can compromise admin accounts to escalate privileges, access sensitive customer data, or modify store settings.

## Defensive takeaways
- Implement strict input validation and sanitization for all user-supplied content before storage
- Apply context-appropriate output encoding (HTML entity encoding) when rendering stored messages
- Use Content Security Policy (CSP) headers to restrict script execution
- Implement automated security testing for XSS vulnerabilities across all user input points
- Sanitize message content using established libraries (e.g., DOMPurify, bleach)
- Apply principle of least privilege to admin functions
- Use templating engines that auto-escape by default

## Variant hunting
Check other messaging features (internal notes, support tickets, comments, notifications)
Test private messages with various payload encodings (URL encoding, HTML entities, Unicode)
Examine if other customer-facing input areas lack similar protections
Look for stored XSS in bulk messaging or automated message systems
Test message export/backup features for XSS preservation
Check if message search/filter functions properly escape query results

## MITRE ATT&CK
- T1190
- T1566.002
- T1566.003
- T1059.007

## Notes
This is a classic stored XSS where user-controlled data persists in the application. The vulnerability's impact is amplified by targeting admin panels where compromised sessions grant significant access. The write-up lacks specific payload details and bounty amount, but the attack path is clear and reproducible.

## Full report
<details><summary>Expand</summary>

1.Open customer function `https://mosuan-img-src-x.myshopify.com/admin/customers`
2.Click on the customer's email address
F625957
3.Click the sent message on the current page
F625959

## Impact

admin

</details>

---
*Analysed by Claude on 2026-05-12*
