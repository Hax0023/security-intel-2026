# Stored XSS in Email Templates via Link in judge.me Shopify App

## Metadata
- **Source:** HackerOne
- **Report:** 1376672 | https://hackerone.com/reports/1376672
- **Submitted:** 2021-10-20
- **Reporter:** rioncool22
- **Program:** judge.me
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Stored Cross-Site Scripting (XSS), Persistent XSS, Second-order XSS
- **CVEs:** None
- **Category:** web-api

## Summary
A stored XSS vulnerability exists in the Email Templates feature of judge.me Shopify app, allowing attackers to inject malicious JavaScript payloads via link fields. When administrators or users interact with the crafted email template link, the payload executes in their browser context, potentially leading to session hijacking and credential theft.

## Attack scenario
1. Attacker gains access to judge.me Email Templates section (via legitimate account or compromised credentials)
2. Attacker navigates to Requests > Email Templates and creates a new template
3. Attacker edits the email template block and inserts a malicious XSS payload disguised as a link URL (e.g., javascript: protocol or data: URI)
4. Attacker saves the poisoned email template, storing the payload in the application database
5. Administrator or user views the email template and clicks the 'Click Here' link
6. Malicious JavaScript executes in the victim's browser with their session privileges, enabling cookie theft and session hijacking

## Root cause
Insufficient input validation and output encoding on email template link fields. The application fails to sanitize or properly escape user-supplied link URLs before storing them in the database and rendering them in HTML responses, allowing arbitrary HTML/JavaScript injection.

## Attacker mindset
Opportunistic insider threat or compromised account holder seeking to escalate privileges, pivot to other users, or establish persistence. Could also be a supply-chain attacker targeting Shopify merchants through a popular review application.

## Defensive takeaways
- Implement strict input validation on all URL/link fields - whitelist allowed protocols (http, https, mailto) and reject javascript:, data:, vbscript: schemes
- Apply context-aware output encoding - use proper HTML entity encoding for link hrefs and JavaScript escaping in script contexts
- Utilize Content Security Policy (CSP) headers to restrict script execution and prevent inline script injection
- Implement a robust HTML sanitization library (e.g., DOMPurify, Bleach) for user-generated content in rich editors
- Apply the principle of least privilege - limit template editing capabilities to trusted administrators only
- Conduct security code review of template rendering logic and rich text editor integrations
- Implement automated security testing (SAST/DAST) focused on injection vulnerabilities in dynamic content features

## Variant hunting
Check other template/rich-text editor features (product descriptions, customer messages, notifications) for similar XSS
Test reflected XSS in email template preview functionality
Examine DOM-based XSS in client-side template rendering or AJAX-based template updates
Look for XSS in custom field values within email templates
Test for XSS via HTML attributes (onclick, onerror, onload handlers in email template elements)
Check if template export/import features preserve or sanitize payloads

## MITRE ATT&CK
- T1190
- T1566.002
- T1598.003
- T1056.004
- T1539
- T1557.002

## Notes
This vulnerability is particularly critical in SaaS/multi-tenant environments like Shopify apps where template modifications by one user can affect email delivery to merchants and customers. The judge.me app handles merchant reviews and ratings, making it a high-value target for attackers seeking to compromise e-commerce operations. The vulnerability requires relatively low privileges (template editor role) to exploit, increasing practical attack surface.

## Full report
<details><summary>Expand</summary>

## Summary:
Stored cross-site scripting (also known as second-order or persistent XSS) arises when an application receives data from an untrusted source and includes that data within its later HTTP responses in an unsafe way.

## FYI:
I Install judge.me in Shopify E-Commerce

## Steps To Reproduce:

  1.  Go to `Requests > Email Templates`

{F1488407}

  2. Click `New Templates`

{F1488408}

3. Edit this block 

{F1488410}

4. Insert Link with XSS payload (See image below)

{F1488413}

5. Then save email
6. To trigger the XSS, you can click `Click Here` text

{F1488415}

## Impact

Session Hijacking, Cookie Stealing

</details>

---
*Analysed by Claude on 2026-05-12*
