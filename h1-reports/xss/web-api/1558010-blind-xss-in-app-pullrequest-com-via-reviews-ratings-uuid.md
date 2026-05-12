# Blind XSS in /reviews/ratings/{uuid} endpoint via unencoded form fields

## Metadata
- **Source:** HackerOne
- **Report:** 1558010 | https://hackerone.com/reports/1558010
- **Submitted:** 2022-05-03
- **Reporter:** bugra
- **Program:** PullRequest
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Cross-Site Scripting (XSS), Blind XSS, Improper Output Encoding, Stored XSS
- **CVEs:** None
- **Category:** web-api

## Summary
A blind XSS vulnerability was discovered in the /reviews/ratings/{uuid} endpoint on app.pullrequest.com, where user-supplied input in review form fields (Disliked_reviewers, Liked_reviewers, Reasons) was reflected without proper HTML encoding. The vulnerability was exploited when PullRequest administrators accessed the review management interface, triggering the attacker's XSS payload.

## Attack scenario
1. Attacker identifies the /reviews/ratings/{uuid} endpoint via web archive historical records
2. Attacker accesses the endpoint and submits a blind XSS payload encoded in base64 (e.g., '"><img src=x id=███████ onerror=eval(atob(this.id))>) in review form fields
3. Payload is stored in the application database without sanitization
4. When a PullRequest administrator accesses the review management portal to view submitted reviews, the malicious payload is rendered in the HTML response
5. The img onerror event fires, decodes the base64 payload via atob(), and executes arbitrary JavaScript in the admin's browser context
6. Attacker receives exfiltration data (cookies, session tokens, admin actions) via their blind XSS monitoring service

## Root cause
The application fails to implement proper output encoding/escaping for user-controlled input in the /reviews/ratings endpoint. Data from form fields (Disliked_reviewers, Liked_reviewers, Reasons) is reflected into HTML context without HTML entity encoding, allowing injection of script tags and event handler attributes.

## Attacker mindset
Persistence through blind XSS reconnaissance - the attacker methodically searched historical web archives to identify accessible endpoints, then crafted a stealthy payload using base64 encoding to bypass basic filter detection. By targeting the admin workflow (review management), they maximized impact and privilege escalation potential.

## Defensive takeaways
- Implement comprehensive output encoding for all user-controlled data based on context (HTML entity encoding for HTML context, JavaScript escaping for JS context, URL encoding for URLs)
- Deploy a Web Application Firewall (WAF) with XSS signatures to detect and block malicious payloads before storage
- Use templating engines with auto-escaping enabled (e.g., Jinja2, Handlebars) rather than manual encoding
- Implement Content Security Policy (CSP) headers with strict-src directives to limit script execution even if XSS occurs
- Conduct security code reviews focusing on data flow from user input to output in all endpoints, particularly admin-facing interfaces
- Implement input validation to restrict form fields to expected character sets and formats
- Maintain regular security audits of historical endpoint access logs and archived versions to identify inadvertently exposed endpoints

## Variant hunting
Search for similar patterns in other /reviews/* endpoints, user profile/feedback mechanisms, comment sections, and any admin review/rating interfaces. Check for other UUID-based endpoints that may accept unvalidated input. Investigate whether other form fields in review submission flows have similar encoding gaps.

## MITRE ATT&CK
- T1190
- T1566
- T1598

## Notes
The attacker's use of base64 encoding (atob()) suggests they anticipated basic XSS filtering. The 'blind' nature required patience - alerts arrived only after admin interaction with the stored payload. This highlights the importance of securing admin portals with the same rigor as user-facing features, as they often process untrusted data. The vulnerability could escalate to session hijacking, admin account compromise, or malware distribution if combined with other techniques.

## Full report
<details><summary>Expand</summary>

**Summary:**
Hi,

While researching PullRequest yesterday, I saw some "review" endpoints in web archive of "app.pullrequest.com". (http://web.archive.org/cdx/search/cdx?url=app.pullrequest.com/*&output=text&fl=original&collapse=urlkey)

One of them was https://app.pullrequest.com/reviews/ratings/6eaa6b75-b958-4530-ba46-0d00cbe74e0b/false , I went to that endpoint and filled the all fields with my blind XSS payload.
`'"><img src=x id=█████ onerror=eval(atob(this.id))>`

This payload sends an alert to my blind XSS application in `██████`

Today (May 3, 2022, 6:09 pm UTC+3), I got a lot of alerts from https://app.pullrequest.com/███. I checked the report and I see it came from an PullRequest admin who checks reviews. 

Here is a screenshot from the report :

███████

I checked the HTML source code and I see my payload reflected to `Disliked_reviewers`,  `Liked_reviewers` and `Reasons` fields without any encoding. 

You can also check the source code : █████████

## Impact

Blind XSS in PullRequest admin portal

Regards,
Bugra

</details>

---
*Analysed by Claude on 2026-05-12*
