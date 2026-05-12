# Stored XSS in WordPress.com Comments and Posts

## Metadata
- **Source:** HackerOne
- **Report:** 733248 | https://hackerone.com/reports/733248
- **Submitted:** 2019-11-09
- **Reporter:** adhamsadaqah
- **Program:** WordPress.com (HackerOne)
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Stored Cross-Site Scripting (XSS), HTML Injection, Insufficient Input Sanitization
- **CVEs:** None
- **Category:** web-api

## Summary
WordPress.com failed to properly sanitize user input in post titles, post bodies, and comments, allowing authenticated attackers to inject malicious HTML/JavaScript payloads. The vulnerability persists in stored form across multiple endpoints, affecting any user who views the compromised content.

## Attack scenario
1. Attacker authenticates to WordPress.com and creates a new blog post or navigates to an existing post
2. Attacker injects XSS payload into post title, body, or comment field using iframe and javascript: protocol handler
3. Attacker publishes the post or submits the comment, which stores the unsanitized payload in the database
4. Victim visits the blog post or reads comments on WordPress.com feed or subdomain
5. Victim's browser renders the malicious HTML and executes JavaScript in the context of wordpress.com domain
6. Attacker's script exfiltrates session cookies, performs actions on behalf of victim, or steals sensitive data

## Root cause
WordPress.com's content sanitization mechanism failed to properly filter or escape HTML special characters and event handlers. The parser accepted malformed HTML constructs like `<iframe <>` and allowed `javascript:` protocol URIs within href attributes, bypassing basic XSS filters.

## Attacker mindset
An authenticated user (low privilege) could escalate impact by poisoning popular blogs with credential-stealing payloads. The stored nature makes it particularly dangerous as victims don't need to interact with the attacker directly. Targeting high-traffic WordPress.com blogs maximizes victim exposure.

## Defensive takeaways
- Implement robust HTML parsing and sanitization using allowlists rather than blocklists (use libraries like DOMPurify or similar)
- Enforce Content Security Policy (CSP) headers to prevent inline script execution and restrict script sources
- Apply output encoding/escaping appropriate to context (HTML entity encoding for displayed content)
- Validate and reject malformed HTML tags during input processing
- Block dangerous protocols like javascript:, data:, and vbscript: in URL attributes
- Use security-focused templating engines that auto-escape by default
- Implement regular security testing including XSS fuzzing across all user input fields

## Variant hunting
Test other protocol handlers: data:, vbscript:, file:, etc.
Try SVG-based XSS payloads: `<svg onload=alert(1)>`
Test event handler injection in other tags: `<img onerror=alert(1)>`, `<body onload=alert(1)>`
Attempt CSS injection via style attributes for exfiltration
Test polyglot payloads combining multiple encoding schemes
Check if sanitization differs between post preview vs. published view
Test comment nesting and nested HTML structures
Verify if rich text editor applies different filters than plain text
Test DOM-based XSS in client-side comment rendering

## MITRE ATT&CK
- T1190
- T1566.002
- T1598.003

## Notes
The payload cleverly uses `<>` to bypass simple tag validators and `javascript&colon;` encoding to evade protocol filters. WordPress.com's architecture serving user content across multiple subdomains (*.wordpress.com) amplifies impact. The vulnerability affects both direct victims and platform reputation. Report lacks specific bounty amount and remediation timeline information.

## Full report
<details><summary>Expand</summary>

## Summary:
Stored XSS as a comment or as a post (body or title)  at 
`https://wordpress.com/read/feeds/{blog_id}/posts/{post_id}`
`https://yoursubdomain.wordpress.com`
using the payload:
 ```
<iframe <><a href=javascript&colon;alert(document.cookie)>Click Here</a>=&gt;&lt;/iframe&gt;
```
## Steps To Reproduce:
- As a comment 
  1. Log in to wordpress.com
  2. Choose a post from the feeds
  3. Add a comment with the payload:
         `<iframe <><a href=javascript&colon;alert(document.cookie)>Click Here</a>=&gt;&lt;/iframe&gt;`
 4. By clicking on `Click Here`, an alert will fire with cookies of the domain `wordpress.com`
- As a post
  1. Log in to wordpress.com
  2. Create a new post or site.
  3. Add the payload `<iframe <><a href=javascript&colon;alert(document.cookie)>Click Here</a>=&gt;&lt;/iframe&gt;`  to the body or the title of the blog post
  4. preview or publish your new blog post
  5. By clicking on `Click Here`, an alert will fire with cookies of the domain `yoursubdomain.wordpress.com` or `wordpress.com` if the post is previewed from the WordPress feed.  
 6. If you add comments to your blog post and using the payload mentioned above as a comment an Stored XSS alert will fire when you click on the link.

## Impact

- Perform arbitrary requests on the behalf of other users with security context of  wordpress.com or blogsubdomain.wordpress.com
- Read any data the attacked user has access to.

</details>

---
*Analysed by Claude on 2026-05-11*
