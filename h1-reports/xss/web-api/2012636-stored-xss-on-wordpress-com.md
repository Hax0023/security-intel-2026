# Stored XSS on wordpress.com via Crowdsignal Poll Integration

## Metadata
- **Source:** HackerOne
- **Report:** 2012636 | https://hackerone.com/reports/2012636
- **Submitted:** 2023-06-05
- **Reporter:** riadalrashed
- **Program:** WordPress.com
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Stored Cross-Site Scripting (XSS), Improper Input Validation, Insufficient Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A Stored XSS vulnerability exists in WordPress.com through the Crowdsignal poll integration service, allowing attackers to inject malicious JavaScript via poll answer fields. The payload persists and executes when users view poll results, potentially enabling session hijacking, credential theft, or malware distribution.

## Attack scenario
1. Attacker creates a poll on app.crowdsignal.com and injects JavaScript payload in the answer field using event handlers and CSS positioning
2. Attacker shares the poll link and tricks users into embedding it in WordPress.com posts
3. When legitimate users view the WordPress post, the embedded poll loads with the malicious payload
4. Users interact with the poll (hover, click) triggering the onmouseover event handler
5. Malicious script executes in the victim's browser with their session cookies and privileges
6. Attacker captures sensitive data (cookies, tokens) or performs actions on behalf of the victim

## Root cause
Crowdsignal poll service fails to properly sanitize and encode user input in poll answer fields before storing and rendering them. WordPress.com embeds the poll content without proper Content Security Policy or additional validation, allowing stored payloads to execute.

## Attacker mindset
Opportunistic vulnerability researcher or malicious actor seeking to compromise WordPress.com users through a third-party integrated service. Leveraging the trust relationship between wordpress.com and crowdsignal.com to bypass security boundaries.

## Defensive takeaways
- Implement strict input validation on all user-supplied fields (answers, poll titles, descriptions)
- Apply context-aware output encoding when rendering poll content (HTML entity encoding, URL encoding)
- Deploy Content Security Policy (CSP) headers to restrict inline script execution
- Sanitize HTML/JavaScript using established libraries (DOMPurify, HTML Purifier)
- Implement subresource integrity checks for third-party embedded content
- Apply security headers to iframe embeds (sandbox attribute, X-Frame-Options)
- Conduct security audits of integrated third-party services
- Implement automated security testing for XSS vulnerabilities in user input flows

## Variant hunting
Search for similar patterns in other WordPress.com integrated services (forms, quizzes, surveys). Test other Crowdsignal features (poll titles, descriptions, custom branding fields). Examine how other survey/polling platforms handle embedded content on WordPress.com. Check for Stored XSS in comment sections when polls are shared.

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1566: Phishing
- T1598: Phishing for Information
- T1005: Data from Local System
- T1539: Steal Web Session Cookie
- T1072: Software Deployment Tools

## Notes
Report references similar prior vulnerability #1987172, suggesting previous XSS issues in the same integration. Vulnerability chain demonstrates importance of securing third-party integrations. The use of CSS positioning (position:fixed, top:0, left:0, border:999em) is a common XSS obfuscation technique. Attack requires user interaction (mouseover) to trigger payload, slightly lowering impact but still serious given the virality of shared polls.

## Full report
<details><summary>Expand</summary>

## Summary:
Hello team,
I found a Stored XSS vulnerability in WordPress.com via app.crowdsignal.com. It is similar to report #1987172.

## Platform(s) Affected:
wordpress.com

1 .Go to https://app.crowdsignal.com/dashboard and create a poll.
2. Enter the following payload as an answer: "style="position:fixed;top:0;left:0;border:999em solid green;" onmouseover="alert(document.cookie)"
3. Go to "Share Your Poll" and copy the link.
4. Navigate to https://wordpress.com/posts and add a new post.
5. Include the copied link in the post.
6. Save the post.
7. Open the page and click on "View Results."
8. The XSS vulnerability will be triggered.

████

## Impact

The attacker can use this issue to execute malicious script code in the victim user browser also redirect the victim user to malicious sites

</details>

---
*Analysed by Claude on 2026-05-12*
