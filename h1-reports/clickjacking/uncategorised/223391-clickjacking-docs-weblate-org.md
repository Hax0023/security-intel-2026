# Clickjacking vulnerability on docs.weblate.org due to missing X-Frame-Options header

## Metadata
- **Source:** HackerOne
- **Report:** 223391 | https://hackerone.com/reports/223391
- **Submitted:** 2017-04-24
- **Reporter:** akbarparambil
- **Program:** Weblate
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Clickjacking, UI Redress Attack, Missing Security Header
- **CVEs:** None
- **Category:** uncategorised

## Summary
The docs.weblate.org domain is vulnerable to clickjacking attacks because it does not return an X-Frame-Options HTTP response header. This allows an attacker to embed the site in an iframe and overlay malicious content on top of legitimate UI elements, tricking users into performing unintended actions.

## Attack scenario
1. Attacker creates a malicious HTML page containing an iframe that loads docs.weblate.org
2. Attacker overlays transparent or visually disguised clickable elements (buttons, links) on top of the framed content
3. Attacker hosts the malicious page and tricks users into visiting it through social engineering or malicious links
4. When users interact with what they perceive as legitimate UI elements on docs.weblate.org, they actually click the hidden malicious elements
5. Attacker captures sensitive information (credentials, CSRF tokens, documentation access) or performs unauthorized actions on behalf of the user

## Root cause
The web server hosting docs.weblate.org fails to set the X-Frame-Options HTTP response header (or Content-Security-Policy frame-ancestors directive) to restrict iframe embedding. Without this header, browsers default to allowing the page to be framed in any context.

## Attacker mindset
An attacker looks for high-traffic documentation sites that users trust implicitly. By embedding these sites in iframes and overlaying deceptive UI, they can harvest credentials, trick users into subscribing to services, or exploit trust in official documentation to deliver malware.

## Defensive takeaways
- Implement X-Frame-Options header set to 'DENY' or 'SAMEORIGIN' depending on legitimate framing requirements
- Use Content-Security-Policy frame-ancestors directive as a modern alternative: 'frame-ancestors none' or 'frame-ancestors 'self''
- Apply these headers globally across all web assets, not just main pages
- Implement frame-busting JavaScript as a secondary defense layer
- Regularly scan headers using tools like OWASP ZAP, Burp Suite, or online header checkers
- Monitor security.txt and implement security headers scanning in CI/CD pipeline
- Educate users about the risks of clicking on suspicious links, especially to documentation or admin panels

## Variant hunting
Look for other Weblate subdomains (weblate.org, app.weblate.org, admin interfaces) that may also lack frame protection. Check related projects or similar documentation hosting platforms. Test other documentation sites from the same organization for consistent header implementation gaps.

## MITRE ATT&CK
- T1566.002
- T1189
- T1598.004

## Notes
While the vulnerability is real and well-documented by OWASP, this particular report demonstrates basic proof-of-concept without demonstrating actual payload delivery, credential theft, or business impact. The vulnerability is relatively low-severity for documentation sites unless they handle sensitive data or authentication endpoints. Modern browsers and content security policies provide additional protections, but the header remains the primary defense mechanism.

## Full report
<details><summary>Expand</summary>

Hi,
Clickjacking (User Interface redress attack, UI redress attack, UI redressing) is a malicious technique of tricking a Web user into clicking on something different from what the user perceives they are clicking on, thus potentially revealing confidential information or taking control of their computer while clicking on seemingly innocuous web pages.

The server didn't return an X-Frame-Options header which means that this website could be at risk of a clickjacking attack. The X-Frame-Options HTTP response header can be used to indicate whether or not a browser should be allowed to render a page in a <frame> or <iframe>. Sites can use this to avoid clickjacking attacks, by ensuring that their content is not embedded into other sites.

This vulnerability affects Web Server.

POC

Here are th steps to reproduce the vulnerability

1.save the below file as anything.html and run it u can see its vulnerable to clickjacking

<html>
   <head>
     <title>Clickjack test page</title>
   </head>
   <body>
     <p>Website is vulnerable to clickjacking!</p>
     <iframe src="http://docs.weblate.org" width="500" height="500"></iframe>
   </body>
</html>

As far as i know this data is enough to prove that your site is vulberable to Clickjacking..
according to OWASP its more than enough..
https://www.owasp.org/index.php/Testing_for_Clickjacking_(OWASP-CS-004)

Solution

https://www.owasp.org/index.php/Clickjacking_Defense_Cheat_Sheet



</details>

---
*Analysed by Claude on 2026-05-24*
