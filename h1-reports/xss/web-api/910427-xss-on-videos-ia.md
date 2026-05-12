# Stored XSS in Videos IA - User Tag Injection

## Metadata
- **Source:** HackerOne
- **Report:** 910427 | https://hackerone.com/reports/910427
- **Submitted:** 2020-06-28
- **Reporter:** benzetaa
- **Program:** Rutube (Russian video hosting platform)
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Stored Cross-Site Scripting (XSS), Improper Input Validation, Improper Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A stored XSS vulnerability was discovered in Rutube's videos section where user-created tags containing malicious JavaScript payloads (e.g., `"><img src=x onerror=alert(1)>`) were not properly sanitized or encoded. The injected script persists and executes when the video is viewed or indexed by search engines, affecting all users who interact with the compromised content.

## Attack scenario
1. Attacker creates a user account on Rutube with a malicious tag containing XSS payload: `"><img src=x onerror=alert(1)>`
2. The malicious tag is stored in the database without proper sanitization or HTML entity encoding
3. When a video associated with this user is searched on DuckDuckGo or viewed on Rutube, the payload is reflected in the DOM
4. The JavaScript payload executes in victims' browsers within the security context of the application
5. Attacker can steal session cookies, perform actions on behalf of users, redirect to phishing pages, or inject additional malicious content
6. The XSS persists and affects all users accessing the compromised video or search results

## Root cause
Insufficient input validation and output encoding of user-supplied data in the user tag field. The application failed to sanitize HTML special characters or encode them as HTML entities before storing and displaying the tag in the `c-detail__user` class element.

## Attacker mindset
An attacker with basic XSS knowledge identifies that user-created tags lack input validation. They craft a simple payload that breaks out of attribute context and injects an img tag with an event handler. The stored nature of the vulnerability makes it attractive as it affects all users without requiring individual exploitation.

## Defensive takeaways
- Implement strict input validation on all user-supplied fields, especially those displayed publicly (usernames, tags, profiles)
- Apply HTML entity encoding to all dynamic content before rendering in HTML context (encode <, >, ", ', &)
- Use a Content Security Policy (CSP) header to restrict script execution and mitigate XSS impact
- Implement output encoding context-aware to the specific context (HTML, JavaScript, URL, CSS)
- Use security-focused templating engines that auto-escape by default
- Perform security code review and penetration testing on user input handling paths
- Maintain a security incident response plan for XSS vulnerabilities in production

## Variant hunting
Check all user-editable fields (bio, display name, comments, profile descriptions) for similar encoding issues
Test other special characters and encoding bypasses (Unicode, HTML5 variations, event handlers beyond onerror)
Investigate if video titles, descriptions, and metadata undergo the same vulnerable processing
Check if the vulnerability affects other search engines or external indexing services
Test for DOM-based XSS variants in video detail page JavaScript handling
Look for similar patterns in other sections of the application (user profiles, messaging, forums)

## MITRE ATT&CK
- T1190
- T1566
- T1598

## Notes
The report demonstrates a classic stored XSS vulnerability where attacker-controlled input (user tag) is persisted and rendered without proper encoding. The cross-site context (search engine integration) amplifies the impact. The vulnerability is particularly concerning because it affects video metadata that may be indexed by external search engines, increasing exposure. The simple payload (`><img src=x onerror=alert(1)>`) suggests basic sanitization filters were either absent or easily bypassed.

## Full report
<details><summary>Expand</summary>

Failure found in the videos tab.

A user was created on a [website] (https://rutube.ru/video/83a4775f020b3fd68efd3dc9a73031e8/) one with the tag `"> <img src = x onerror = alert (1)> `.

When we search DuckDuckGo for the video or user tag, we find a xss flaw in [page] (https://duckduckgo.com/?q=%22%2F%3E%22%2F%3E%3Cimg+src%3Dxss+onerror%3Dalert(2)%3E&t=hk&iar=videos&iax=videos&ia=videos&iai=https%3A%2F%2Frutube.ru%2Fvideo%2F83a4775f020b3fd68efd3dc9a73031e8%2F)  detail, in the class tag with the name `c-detail__user`

{F886397}
{F886398}

## Impact

Stored XSS, also known as persistent XSS, is the more damaging than non-persistent XSS. It occurs when a malicious script is injected directly into a vulnerable web application.

</details>

---
*Analysed by Claude on 2026-05-12*
