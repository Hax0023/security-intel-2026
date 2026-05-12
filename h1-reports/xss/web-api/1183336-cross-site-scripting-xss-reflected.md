# Reflected Cross-Site Scripting (XSS) in Change Password Portal

## Metadata
- **Source:** HackerOne
- **Report:** 1183336 | https://hackerone.com/reports/1183336
- **Submitted:** 2021-05-03
- **Reporter:** lu3ky-13
- **Program:** MTN Uganda (eweb01.mtn.co.ug)
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Reflected XSS, Improper Input Validation, Improper Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability exists in the change_password.htm endpoint where the terminalId GET parameter is directly reflected within a JavaScript context without proper encoding or validation. An attacker can inject arbitrary JavaScript code by crafting a malicious URL that, when visited by a victim, executes in their browser with full access to session tokens and sensitive data.

## Attack scenario
1. Attacker crafts a malicious URL containing JavaScript payload in the terminalId parameter (e.g., alert statement or session stealer)
2. Attacker sends the malicious URL to a target user via email, chat, or social engineering
3. Victim clicks the link and visits the vulnerable change_password.htm endpoint
4. Server reflects the unencoded terminalId parameter value directly into a JavaScript context within the HTML response
5. Victim's browser parses and executes the injected JavaScript code
6. Attacker gains access to cookies, session tokens, or performs actions on behalf of the victim

## Root cause
The application fails to properly validate and encode user-supplied input (terminalId parameter) before embedding it in JavaScript code. The parameter is placed directly within double quotes in a script tag without escaping special characters or implementing Content Security Policy (CSP) protections.

## Attacker mindset
The attacker likely discovered this vulnerability through manual testing of URL parameters, observing that input was reflected in page source. The choice to demonstrate with an alert() payload suggests proof-of-concept intent rather than exploitation, though the vulnerability could easily be weaponized to steal session cookies or perform account takeover via credential harvesting.

## Defensive takeaways
- Implement strict input validation on all user-supplied parameters, using whitelisting of expected values
- Apply context-aware output encoding: use JavaScript encoding for values reflected in script contexts, HTML encoding for HTML contexts
- Avoid placing user input directly in JavaScript code; use data attributes or JSON serialization instead
- Deploy Content Security Policy (CSP) headers to restrict script execution and prevent inline script injection
- Use security-focused templating engines that auto-escape output by default
- Implement HTTPOnly and Secure flags on session cookies to limit JavaScript access
- Conduct regular security code reviews focusing on data flow from input to output
- Perform penetration testing on all parameter handling, especially in authentication-related endpoints

## Variant hunting
Search for similar patterns in other password-related endpoints (/reset_password, /update_credentials), other GET parameters that might be reflected in script tags, and check if other MTN properties or similar financial/telecom portals have the same vulnerability. Review EVDS portal for similar parameter injection points in JavaScript contexts.

## MITRE ATT&CK
- T1190
- T1566
- T1598

## Notes
The payload uses URL encoding and attempts to break out of quotes context with double-quote character. The report demonstrates basic XSS but lacks detail on actual impact exploitation or proof of session token theft. The vulnerability affects a sensitive endpoint (change_password) making it particularly critical for account security. No indication of whether the program is active or what bounty tier this represents.

## Full report
<details><summary>Expand</summary>

hello dear support

Cross-site Scripting (XSS) refers to client-side code injection attack wherein an attacker can execute malicious scripts into a legitimate website or web application. XSS occurs when a web application makes use of unvalidated or unencoded user input within the output it generates.

i have found the issue on https://eweb01.mtn.co.ug

param and path /evds_portal_fe/change_password.htm?terminalId=

payload "%3c%3c%73%63%72%5c%61%61%61%2f%73%72%63%3d%3e%3c%2f%73%63%72%69%70%74%3e%3c%73%63%72%69%70%74%3e%61%6c%65%72%74%28%22%70%6c%61%79%73%74%61%74%69%6f%6e%20%72%65%66%6c%65%63%74%65%64%20%78%73%73%20%42%59%20%42%34%47%47%33%52%22%29%3c%2f%73%63%72%69%70%74%3e"


https://eweb01.mtn.co.ug/evds_portal_fe/change_password.htm?terminalId=%22%3c%3c%73%63%72%5c%61%61%61%2f%73%72%63%3d%3e%3c%2f%73%63%72%69%70%74%3e%3c%73%63%72%69%70%74%3e%61%6c%65%72%74%28%22%70%6c%61%79%73%74%61%74%69%6f%6e%20%72%65%66%6c%65%63%74%65%64%20%78%73%73%20%42%59%20%42%34%47%47%33%52%22%29%3c%2f%73%63%72%69%70%74%3e%22

URL encoded GET input terminalId was set to 19146"();}]9520

The input is reflected inside a <script> tag between double quotes.

## Impact

XSS
Malicious JavaScript has access to all the same objects as the rest of the web page, including access to cookies and local storage, which are often used to store session tokens. If an attacker can obtain a user's session cookie, they can then impersonate that user.

Furthermore, JavaScript can read and make arbitrary modifications to the contents of a page being displayed to a user. Therefore, XSS in conjunction with some clever social engineering opens up a lot of possibilities for an attacker.

</details>

---
*Analysed by Claude on 2026-05-12*
