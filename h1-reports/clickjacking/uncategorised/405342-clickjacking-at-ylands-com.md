# Clickjacking Vulnerability at ylands.com and Related Domains

## Metadata
- **Source:** HackerOne
- **Report:** 405342 | https://hackerone.com/reports/405342
- **Submitted:** 2018-09-04
- **Reporter:** kryptomon
- **Program:** Bohemia Interactive (ylands.com)
- **Bounty:** Not specified in report
- **Severity:** Medium
- **Vuln:** Clickjacking, UI Redress Attack, Missing Security Headers
- **CVEs:** None
- **Category:** uncategorised

## Summary
Multiple domains owned by Bohemia Interactive are vulnerable to clickjacking attacks due to missing X-Frame-Options HTTP response headers. This allows attackers to embed the websites in iframes and perform UI redress attacks to trick users into unintended actions. The vulnerability affects ylands.com, workshop.ylands.com, dayz.com, armamobileops.com, and minidayz.com.

## Attack scenario
1. Attacker creates a malicious webpage containing an iframe that loads a vulnerable ylands.com page
2. Attacker overlays the iframe with transparent or visually deceptive content positioned over clickable elements
3. Victim visits the attacker's webpage, believing they are interacting with legitimate content
4. Victim clicks on what appears to be innocuous content, but actually clicks on hidden elements within the embedded iframe
5. Unintended actions are performed on the victim's account (e.g., changing settings, making purchases, or initiating transfers)
6. Attacker could additionally capture keystrokes if password fields are positioned under transparent input boxes

## Root cause
The web servers hosting the vulnerable domains do not implement the X-Frame-Options HTTP response header or Content-Security-Policy header with frame-ancestors directive. This omission allows any website to embed these pages in iframes without restrictions.

## Attacker mindset
An attacker would recognize that without frame-protection headers, they can easily embed legitimate-looking pages in malicious contexts. The low effort required to craft clickjacking exploits combined with potential access to user accounts, sensitive actions, or credential theft makes this an attractive attack vector for social engineering campaigns.

## Defensive takeaways
- Implement X-Frame-Options header with 'DENY' or 'SAMEORIGIN' value on all HTTP responses
- Set Content-Security-Policy header with 'frame-ancestors' directive to restrict embedding contexts
- Perform security header audit across all domains and subdomains in the asset inventory
- Implement SameSite cookie attributes to mitigate session hijacking via clickjacking
- Use frame-breaking JavaScript as a secondary defense mechanism
- Conduct security testing for clickjacking on a regular basis as part of SDLC
- Apply security headers consistently across all applications and CDN configurations

## Variant hunting
Check for missing security headers on other Bohemia Interactive properties and game portals
Test for incomplete CSP policies that allow framing from specific origins
Verify if SAMEORIGIN is properly configured and not bypassed via subdomain framing attacks
Look for dynamically generated pages or APIs that may bypass header configurations
Check mobile applications and progressive web app variants for similar vulnerabilities
Test API endpoints for clickjacking vulnerability in admin/sensitive function pages

## MITRE ATT&CK
- T1189
- T1598

## Notes
This is a straightforward security header implementation issue. The vulnerability report is technically accurate but lacks specific impact demonstration beyond theoretical keystroke hijacking. The POC correctly demonstrates that pages can be framed, confirming the vulnerability. The report was likely accepted as a legitimate security issue, though the bounty amount was not disclosed. This type of vulnerability is common in organizations with inconsistent security header deployment across multiple domains.

## Full report
<details><summary>Expand</summary>

Hi team,

While performing security testing of your website i have found the vulnerability called Clickjacking.
Many URLS are in scope and vulnerable to Clickjacking. 

What is Clickjacking ?
Clickjacking (User Interface redress attack, UI redress attack, UI redressing) is a malicious technique of tricking a Web user into clicking on something different from what the user perceives they are clicking on, thus potentially revealing confidential information or taking control of their computer while clicking on seemingly innocuous web pages.
The server didn't return an X-Frame-Options header which means that this website could be at risk of a clickjacking attack. The X-Frame-Options HTTP response header can be used to indicate whether or not a browser should be allowed to render a page in a <frame> or <iframe>. Sites can use this to avoid clickjacking attacks, by ensuring that their content is not embedded into other sites.
This vulnerability affects Web Server.

        Steps to Reproduce / POC

Vulnerable Urls:
        https://ylands.com/
	https://workshop.ylands.com/
	https://dayz.com/
	http://armamobileops.com/
	https://minidayz.com/


 Put every above url one by one in the code of iframe, which is given below
---------------------------------------------------

<!DOCTYPE HTML>
<html lang="en-US">
<head>
<meta charset="UTF-8">
<title>I Frame</title>
</head>
<body>
<h3>clickjacking vulnerability</h3>
<iframe src="https://vigorgame.com/" height="550px" width="700px"></iframe>
</body>
</html>

By Tahir Javed
tahirjavedbhutta@gmail.com

------------------------------------------------------

    Notice that site is visible in the Iframe

POC is in the attachments. Thanks, waiting for your response.

## Impact

Using a similar technique, keystrokes can also be hijacked. With a carefully crafted combination of stylesheets, iframes, and text boxes, a user can be led to believe they are typing in the password to their email or bank account, but are instead typing into an invisible frame controlled by the attacker.

</details>

---
*Analysed by Claude on 2026-05-24*
