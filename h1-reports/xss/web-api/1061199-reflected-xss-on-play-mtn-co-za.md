# Reflected XSS on play.mtn.co.za

## Metadata
- **Source:** HackerOne
- **Report:** 1061199 | https://hackerone.com/reports/1061199
- **Submitted:** 2020-12-17
- **Reporter:** lu3ky-13
- **Program:** MTN (play.mtn.co.za)
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Reflected Cross-Site Scripting (XSS), Improper Input Validation, Insufficient Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability was discovered in the play.mtn.co.za application through the 'page' query parameter on the /callertunez/ endpoint. User-supplied input is not properly sanitized or encoded before being reflected in the HTTP response, allowing attackers to inject malicious JavaScript code. The vulnerability can be exploited to steal session tokens, modify page content, or perform actions on behalf of authenticated users.

## Attack scenario
1. Attacker crafts a malicious URL containing JavaScript payload in the 'page' parameter: play.mtn.co.za/callertunez/?page=2%27%22%3E%3Cimg%20src=x%20onerror=alert(document.domain)%3E
2. Attacker distributes the URL via phishing email, social media, or other social engineering tactics to target users
3. Victim clicks the malicious link while authenticated to play.mtn.co.za
4. Browser executes the reflected payload in the context of the victim's session and domain
5. Attacker's JavaScript code gains access to session cookies, local storage, and can read/modify page content
6. Attacker exfiltrates session tokens, captures credentials, or performs unauthorized actions (e.g., account changes, fraud)

## Root cause
The application fails to properly validate and encode user input from the 'page' query parameter before including it in the HTTP response. The parameter value is directly concatenated into the HTML output without sanitization, allowing arbitrary HTML and JavaScript to be injected.

## Attacker mindset
An attacker would recognize that MTN's play.mtn.co.za platform likely contains valuable user data (authentication tokens, personal information, payment methods). By crafting a simple phishing campaign with this XSS vector, they could harvest session cookies from multiple users without needing to compromise credentials directly. The reflected nature makes it easy to distribute via links, and the entertainment/caller tunes context suggests a casual user base less likely to scrutinize suspicious links.

## Defensive takeaways
- Implement strict input validation on all query parameters; whitelist allowed values for the 'page' parameter (e.g., numeric values only)
- Apply proper output encoding/escaping based on context (HTML entity encoding for HTML content, JavaScript escaping for script contexts)
- Use templating engines with auto-escaping enabled to prevent accidental injection
- Implement Content Security Policy (CSP) headers to restrict script execution and mitigate XSS impact
- Perform security code review of all user input handling, particularly query parameters and search functionality
- Conduct regular penetration testing and vulnerability scanning of public-facing applications
- Implement HTTPOnly and Secure flags on session cookies to prevent JavaScript access and transmission over HTTP

## Variant hunting
Look for similar parameter injection points: 'search' parameter also appears in the URL (likely vulnerable as well); test other GET parameters like 'filter', 'sort', 'category'; check POST parameters in forms; test other MTN subdomains and applications for similar patterns; investigate if 'page' parameter accepts numeric values that could lead to directory traversal or SSRF; examine all user-controlled inputs in error messages and redirects

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1566.002 - Phishing: Spearphishing Link
- T1598.003 - Gather Victim Identity Information: Spearphishing Link
- T1559.001 - Inter-Process Communication: Component Object Model
- T1539 - Steal Web Session Cookie

## Notes
The reported payload uses both img onerror event handler and video tag for XSS execution. The vulnerability is straightforward and likely high-impact on an entertainment platform with active user authentication. The 'search' parameter in the same URL should be tested for the same vulnerability. No bounty amount was specified in the report, which may indicate the program has a responsible disclosure policy or the bounty was to be determined during triage.

## Full report
<details><summary>Expand</summary>

hello dear

I have found Reflected XSS on play.mtn.co.za
parameters injectable ?page=2

my payload "><img src=x onerror=prompt``>;<video>

URL: https://play.mtn.co.za/callertunez/?page=2%27%22%3E%3Cimg%20src=x%20onerror=alert(document.domain)%3E&search=A

{F1120432}

## Impact

Malicious JavaScript has access to all the same objects as the rest of the web page, including access to cookies and local storage, which are often used to store session tokens. If an attacker can obtain a user's session cookie, they can then impersonate that user.

Furthermore, JavaScript can read and make arbitrary modifications to the contents of a page being displayed to a user. Therefore, XSS in conjunction with some clever social engineering opens up a lot of possibilities for an attacker.

</details>

---
*Analysed by Claude on 2026-05-12*
