# Clickjacking: X-Frame-Options header missing

## Metadata
- **Source:** HackerOne
- **Report:** 163646 | https://hackerone.com/reports/163646
- **Submitted:** 2016-08-26
- **Reporter:** sadhu16
- **Program:** Legal Robot
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Clickjacking, UI Redress Attack, Missing Security Headers
- **CVEs:** None
- **Category:** uncategorised

## Summary
The target website fails to implement the X-Frame-Options HTTP response header, allowing the site to be embedded in iframes on attacker-controlled domains. This enables clickjacking attacks where users can be tricked into performing unintended actions on the vulnerable site through visual obfuscation.

## Attack scenario
1. Attacker identifies that target website lacks X-Frame-Options header validation
2. Attacker creates a malicious webpage that embeds the target site in a transparent or hidden iframe
3. Attacker overlays legitimate-looking UI elements (buttons, links) on top of the embedded iframe at precise coordinates
4. Victim visits attacker's webpage believing they are interacting with benign content
5. Victim's clicks are actually redirected to the embedded iframe, performing actions on the target site (e.g., transferring funds, changing settings, account takeover)
6. Actions are executed with victim's authenticated session if they were previously logged into the target site

## Root cause
Web server configuration does not include X-Frame-Options header in HTTP responses, failing to restrict iframe embedding of page content

## Attacker mindset
Opportunistic attacker leveraging missing security controls to conduct UI-based social engineering. The simplicity of the exploit (basic HTML iframe) suggests attackers view this as low-hanging fruit for credential harvesting or unauthorized transactions.

## Defensive takeaways
- Implement X-Frame-Options header with appropriate value (DENY for most cases, SAMEORIGIN if framing is required)
- Deploy Content-Security-Policy header with frame-ancestors directive as modern alternative/supplement
- Implement additional UI protections: frame-busting JavaScript, SameSite cookie attributes
- Add security headers audit to CI/CD pipeline and server configuration baseline
- Educate users about phishing and suspicious framing indicators
- Monitor and alert on unexpected iframe embedding attempts through CSP violation reports

## Variant hunting
Search for other endpoints that may lack X-Frame-Options; test subdomains and API endpoints. Verify X-Frame-Options is correctly set across all response types (HTML, JSON, media). Check for header injection vulnerabilities that could bypass protections. Test for CSP header presence and frame-ancestors directive configuration.

## MITRE ATT&CK
- T1189
- T1192
- T1199

## Notes
Simple vulnerability with straightforward remediation. The POC demonstrates ease of exploitation. Legal Robot appears to have been a legitimate target in this 2016 report. Clickjacking severity depends on target actions available on the vulnerable page; financial/account modification pages warrant higher severity. This was a common finding during the era of widespread missing security headers.

## Full report
<details><summary>Expand</summary>

Clickjacking (User Interface redress attack, UI redress attack, UI redressing) is a malicious technique of tricking a Web user into clicking on something different from what the user perceives they are clicking on, thus potentially revealing confidential information or taking control of their computer while clicking on seemingly innocuous web pages.

The server didn't return an X-Frame-Options header which means that this website could be at risk of a clickjacking attack. The X-Frame-Options HTTP response header can be used to indicate whether or not a browser should be allowed to render a page in a <frame> or <iframe>. Sites can use this to avoid clickjacking attacks, by ensuring that their content is not embedded into other sites.

This vulnerability affects Web Server.

POC

Here are th steps to reproduce the vulnerability

1.open notepad and paste the following code

<html>
   <head>
     <title>Clickjack test page</title>
   </head>
   <body>
     <p>Website is vulnerable to clickjacking!</p>
     <iframe src="https://www.legalrobot.com/swag/" width="500" height="500"></iframe>
   </body>
</html>
2.save it as <anyname>.html eg cj.html
3.and just simply open that in browser

As far as i know this data is enough to prove that your site is vulberable to Clickjacking..
according to OWASP its more than enough..
https://www.owasp.org/index.php/Testing_for_Clickjacking_(OWASP-CS-004)

Solution

https://www.owasp.org/index.php/Clickjacking_Defense_Cheat_Sheet
check this out..here is the solution for that...

Please also find the attached screenshots (one of response & one of  attack being exploited in browser )



</details>

---
*Analysed by Claude on 2026-05-24*
