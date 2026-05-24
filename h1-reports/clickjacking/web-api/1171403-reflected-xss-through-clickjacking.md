# Reflected XSS via Clickjacking Attack Chain

## Metadata
- **Source:** HackerOne
- **Report:** 1171403 | https://hackerone.com/reports/1171403
- **Submitted:** 2021-04-21
- **Reporter:** sazouki
- **Program:** DoD Bug Bounty
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Reflected Cross-Site Scripting (XSS), Clickjacking, Open Redirect
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability was discovered that can be exploited through a clickjacking attack. The attacker chains an XSS payload in a URL parameter with a visually deceptive iframe overlay to trick users into clicking on the malicious link. This allows arbitrary JavaScript execution in the victim's browser within the vulnerable domain's context.

## Attack scenario
1. Attacker identifies a reflected XSS parameter in the target application that echoes user input without proper sanitization
2. Attacker crafts a malicious URL containing JavaScript payload (e.g., javascript:alert(document.domain)) in the vulnerable parameter
3. Attacker creates a HTML page with a transparent iframe pointing to the XSS payload URL overlaid on top of a legitimate-looking background image
4. Attacker hosts this page and sends the link to potential victims via social engineering (email, chat, etc.)
5. Victim visits the attacker's page and sees what appears to be a legitimate website (due to background image)
6. Victim unknowingly clicks on the transparent iframe area, triggering the reflected XSS payload execution

## Root cause
The vulnerable application fails to properly sanitize and encode user-supplied input in URL parameters before reflecting it back in the HTML response, allowing injection of arbitrary JavaScript. Additionally, the application lacks X-Frame-Options headers to prevent iframe embedding.

## Attacker mindset
Attacker recognizes that reflected XSS alone requires user interaction (clicking a suspicious link), so combines it with clickjacking to mask the attack origin and make the social engineering more convincing by overlaying the attack with a legitimate-looking visual context.

## Defensive takeaways
- Implement strict input validation and output encoding for all user-supplied parameters
- Set X-Frame-Options: DENY or SAMEORIGIN headers to prevent clickjacking
- Use Content-Security-Policy headers with frame-ancestors directive to restrict iframe embedding
- Apply HTML entity encoding and JavaScript escaping to all reflected content
- Implement input whitelisting rather than blacklisting for URL parameters
- Use Content-Security-Policy to disable inline JavaScript (unsafe-inline)
- Educate users about social engineering and suspicious links from unknown sources
- Implement SameSite cookie attribute to mitigate session hijacking aspects

## Variant hunting
Search for other URL parameters that might reflect user input without encoding
Test all redirects and open redirect vulnerabilities that could chain with XSS
Look for POST-based reflected XSS that might bypass URL filtering
Check for DOM-based XSS vulnerabilities in client-side parameter handling
Test for stored XSS if user input is persisted in any form
Examine error pages and response messages for unencoded reflections
Test SVG and image upload functionality for XSS vectors

## MITRE ATT&CK
- T1190
- T1566
- T1598
- T1608
- T1204

## Notes
The report demonstrates a sophisticated attack chain combining two web vulnerabilities. The use of URL encoding (%0D%0A for CRLF) and HTML entity encoding (&#x22;) suggests the attacker was bypassing basic filtering. The payload appears to attempt breaking out of attributes while also including a fake Google redirect for legitimacy. The redacted content indicates this was a DoD target, suggesting critical infrastructure vulnerability. Modern browsers' security features may block some variants of this attack, but older systems remain vulnerable.

## Full report
<details><summary>Expand</summary>

**Description:**

Hello DoD team

i found an reflected XSS that require user interaction, but it's suspicious due the reflected payload in the page

███████

So in this case i chain it with click-jacking with image background same like the legal website to make it more trusting

████████

below is the code

```code
<style>

div {
       position:absolute;
       top:200px;
       left:900px;
       
   }
 body {

 	background-image: url('1.png');
 	background-repeat: no-repeat;
 	background-position: 300px 5px;

 }
</style>

<iframe src="https://███████?URL=javascript:alert(document.domain)//%0D%0A&#x22;https://google.com" id="xxx" width=100% height=100% style="opacity: 0;"></iframe>

```

## Impact

attacked can run malicious code in the victim browser

## System Host(s)
www.██████

## Affected Product(s) and Version(s)


## CVE Numbers


## Steps to Reproduce
host the provided code with the background image and send it to the victim

## Suggested Mitigation/Remediation Actions




</details>

---
*Analysed by Claude on 2026-05-24*
