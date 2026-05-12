# Reflected XSS in Snapchat Add User Page via Username Parameter

## Metadata
- **Source:** HackerOne
- **Report:** 125849 | https://hackerone.com/reports/125849
- **Submitted:** 2016-03-25
- **Reporter:** esnard
- **Program:** Snapchat
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Reflected Cross-Site Scripting (XSS), Improper Output Encoding, Meta Tag Injection, HTML Tag Injection
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability exists on snapchat.com/add/ endpoint where user-supplied username parameter is reflected unsanitized in six locations including meta tags, object tags, and DOM elements. The vulnerability is only visible when using mobile user-agents, allowing attackers to execute arbitrary JavaScript, perform UI redressing, or facilitate open redirects.

## Attack scenario
1. Attacker crafts malicious URL with XSS payload in the username parameter: snapchat.com/add/%22%3E%3Cscript%3Ealert(1)%3C/script%3E
2. Attacker sends phishing link to victim via social engineering or social media
3. Victim clicks link on mobile device or mobile browser
4. Server reflects unsanitized username parameter into HTML response in meta tags and heading elements
5. Browser parses malicious HTML/JavaScript and executes attacker's payload in victim's session context
6. Attacker steals session cookies, performs account actions, or redirects victim to phishing site

## Root cause
User input from the username URL parameter is not properly HTML-encoded or sanitized before being reflected in multiple HTML contexts (meta tag attributes, object tag attributes, and DOM text content). The application trusts user input and inserts it directly into the response without output encoding.

## Attacker mindset
An attacker would recognize that public-facing invitation/profile pages are attractive targets for XSS since they're shared via links. Testing with HTML special characters and observing that the username appears in page metadata and DOM suggests missing output encoding. The mobile user-agent bypass indicates the developer may have tested only desktop views, creating a gap in security coverage.

## Defensive takeaways
- HTML-encode all user input before reflecting in HTML context (use libraries like DOMPurify or OWASP encoder)
- Apply context-appropriate encoding: HTML entity encoding for element content, attribute encoding for attributes, JavaScript encoding for scripts
- Implement Content Security Policy (CSP) to restrict script execution and mitigate XSS impact
- Test security controls across all user-agent variants and device types, not just desktop
- Use templating engines with auto-escaping enabled by default
- Implement input validation to reject or sanitize unexpected characters in username parameters
- Apply principle of least privilege: avoid reflecting user input in sensitive contexts like meta tags

## Variant hunting
Search for similar patterns: (1) Other endpoints accepting username/profile parameters (/profile/, /u/, /user/, /account/); (2) Other user-agent dependent code paths that may have inconsistent security; (3) Similar meta tag injection in social sharing endpoints (Facebook, Twitter, Instagram add/follow pages); (4) Object tag usage elsewhere on site that might accept user input; (5) Check for same vulnerability in API endpoints that generate HTML responses

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1598: Phishing - Link
- T1566: Phishing
- T1204: User Execution

## Notes
The report demonstrates good security research methodology by identifying multiple injection points (6 distinct locations) and noting the user-agent dependency that could otherwise go undetected. Meta tag injection is particularly dangerous for social engineering via preview text manipulation. The 'open redirect' potential mentioned suggests possible follow-on vulnerabilities in the page flow. The lack of bounty amount in report text suggests this may be a disclosure-only program or bounty was withheld.

## Full report
<details><summary>Expand</summary>

Hi Snapchat Team,

I've found a reflected XSS vulnerability on this page:
https://www.snapchat.com/add/snapchat

Example:
https://www.snapchat.com/add/%22%3E%3Ch1%3EXSS%3C%2Fh1%3E

Note: you should visit the page with a mobile user-agent since the server displays different information based on the User-Agent HTTP header sent by the browser.

There are 6 places where the username isn't protected against XSS attacks:
- 4 `meta` tags: twitter:title, twitter:image, og:title, og:image
- 1 `object` tag: snapcode
- 1 `h2` tag: username

This could lead to JavaScript execution, UI redressing or open redirects.

</details>

---
*Analysed by Claude on 2026-05-12*
