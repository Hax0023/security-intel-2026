# Self XSS/HTML Injection via Comments in Nextcloud Deck App

## Metadata
- **Source:** HackerOne
- **Report:** 2058556 | https://hackerone.com/reports/2058556
- **Submitted:** 2023-07-09
- **Reporter:** hackit_bharat
- **Program:** Nextcloud
- **Bounty:** Not specified
- **Severity:** Medium
- **Vuln:** Cross-Site Scripting (XSS), HTML Injection, Self-XSS
- **CVEs:** CVE-2024-22213
- **Category:** web-api

## Summary
A Self-XSS vulnerability exists in the Nextcloud Deck application's comment functionality, allowing users to inject arbitrary HTML and malicious scripts into card comments. The injected content executes when rendered, potentially leading to one-time script execution and account compromise if made persistent.

## Attack scenario
1. Attacker creates or accesses a Nextcloud Deck instance with appropriate permissions
2. Attacker navigates to a card and opens the comments section
3. Attacker injects HTML payload containing malicious links or scripts in the comment field (e.g., <a href=...><base target=)
4. Attacker sends the comment containing the payload
5. When other users or the attacker views the comment, the injected HTML is rendered and executed
6. Malicious script executes in the victim's browser context, potentially stealing session cookies or performing unauthorized actions

## Root cause
Insufficient input validation and output encoding in the Deck app's comment rendering mechanism. The application fails to properly sanitize or escape HTML entities in user-supplied comment data before displaying it to users.

## Attacker mindset
An attacker seeks to demonstrate that user-controlled input in comments is not properly sanitized, enabling HTML/JavaScript injection. The attacker recognizes this as a stepping stone for potential account takeover, cookie theft, and persistence mechanisms if the vulnerability can be chained with other weaknesses.

## Defensive takeaways
- Implement strict input validation and whitelist allowed HTML tags in comment fields
- Apply proper output encoding/escaping for all user-supplied content before rendering in HTML context
- Use security-focused templating engines that auto-escape by default
- Implement Content Security Policy (CSP) headers to mitigate XSS impact
- Perform security testing on user input handling across all interactive features (comments, descriptions, etc.)
- Consider using HTML sanitization libraries (e.g., DOMPurify) for user-generated content

## Variant hunting
Check other comment or text input fields in Deck (card descriptions, board names, list names)
Test similar functionality in other Nextcloud apps (Notes, Tasks, Talk, etc.)
Verify if the vulnerability affects different content types (markdown, rich text, plain text)
Test nested comment scenarios or comment editing functionality
Check if the vulnerability persists in comment threads or nested replies
Examine API endpoints used by Deck for comment submission and retrieval

## MITRE ATT&CK
- T1190
- T1203
- T1566

## Notes
This is classified as a Self-XSS rather than stored XSS based on the description, though the reporter suggests it could become persistent. The vulnerability requires user interaction and affects the attacker's own or target users' sessions. The payloads use older HTML techniques (dangling markup, <font> tags) rather than modern JavaScript. The report lacks technical depth and formal analysis typical of mature security research.

## Full report
<details><summary>Expand</summary>

Hi Team,

I hope you are doing well.

I found an XSS/HTML Injection Via Comments in Deck Cards.

Vulnerability Name :- XSS/HTML Injection Via Comments in Deck Cards

Vulnerability Description :- Hi Team , I found an XSS/HTML Injection Via Comments in Deck Cards, which leads to One time Malicious Script execution .
I performed my Testing on  Localhost Latest version of Nextcloud  27.0.0.8.

{F2481183}

Steps to Reproduce :- 1. Setup the Nextcloud Instance Locally.
2. After setting up locally --> login.
3. After that Go to Deck --> Create Cards --> Click on that card --> Go to comments.
4. Enter this payload in comments :- <a href=http://██████/dangling_markup/name.html><font size=100 color=red>You must click me</font></a><base target="
5. You can also use this --> <a href=http://███████/dangling_markup/name.html><font size=100 color=blue>You Hacked by BhaRat</font></a><base target="
6. Put this script in comments and click and send and Boom! you see the one time execution.
7. Attacker can easily found a way to make it persistent or execute their malicious script once.

## Impact

1. Malicious Script Execution.
2. If attacker can able to make it persistent --> it leads to cookie stealing and account takeover.

POC Attached

If you need further info I am here to help you.

Thanks and Regards,
BhaRat

</details>

---
*Analysed by Claude on 2026-05-12*
