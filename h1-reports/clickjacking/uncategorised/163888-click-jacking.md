# Clickjacking Vulnerability via Missing X-Frame-Options Header

## Metadata
- **Source:** HackerOne
- **Report:** 163888 | https://hackerone.com/reports/163888
- **Submitted:** 2016-08-27
- **Reporter:** muhaddix
- **Program:** legalRobot
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Clickjacking, UI Redress Attack, Missing Security Headers
- **CVEs:** None
- **Category:** uncategorised

## Summary
legalRobot's website lacks proper X-Frame-Options headers, allowing the site to be embedded in iframes on attacker-controlled domains. An attacker can overlay transparent or disguised UI elements to trick users into performing unintended actions like account modifications, fund transfers, or credential disclosure.

## Attack scenario
1. Attacker creates a malicious HTML page that embeds legalRobot.com in a transparent iframe
2. Attacker overlays fake UI elements (buttons, forms) on top of the legitimate iframe content
3. Attacker hosts the malicious page and tricks users into visiting it via phishing or social engineering
4. Unsuspecting user clicks what appears to be a benign button but actually clicks on hidden elements within the legalRobot iframe
5. User unintentionally performs sensitive actions (e.g., confirming transactions, changing settings, deleting data)
6. Attacker gains unauthorized access to user accounts or sensitive information through the clickjacking attack

## Root cause
The application fails to implement the X-Frame-Options HTTP response header or Content-Security-Policy directive to restrict iframe embedding. This allows any external domain to embed the application in an iframe without restrictions.

## Attacker mindset
An attacker seeks to perform unauthorized actions on behalf of legitimate users by leveraging their existing authenticated sessions. Clickjacking is attractive because it doesn't require exploiting complex vulnerabilities—simple UI manipulation can lead to credential theft, unauthorized transactions, or account compromise.

## Defensive takeaways
- Implement X-Frame-Options header with DENY or SAMEORIGIN value
- Use Content-Security-Policy frame-ancestors directive to control iframe embedding
- Implement frame-breaking JavaScript as a secondary defense mechanism
- Require additional confirmation for sensitive operations (CSRF tokens, user verification)
- Use SameSite cookie attribute to limit cookie scope in cross-origin contexts
- Monitor and alert on unusual cross-origin iframe embedding attempts
- Educate users about the risks of visiting untrusted websites

## Variant hunting
Check for missing Content-Security-Policy headers
Test if other sensitive endpoints (admin panels, payment gateways) are also vulnerable
Verify if authentication bypass is possible through clickjacking on login mechanisms
Investigate potential combination with other attacks (CSRF, XSS) for amplified impact
Test for vulnerabilities in drag-and-drop interactions within iframes
Look for clickjacking vulnerabilities in mobile app WebViews

## MITRE ATT&CK
- T1190
- T1566

## Notes
This is a straightforward clickjacking vulnerability report. The POC is simplistic but valid. The researcher provided clear remediation guidance referencing OWASP standards. While the severity is medium (not allowing direct system compromise), clickjacking can be combined with social engineering or other attacks to achieve higher impact. The fix is relatively simple and should be prioritized for security baseline compliance.

## Full report
<details><summary>Expand</summary>

Hey **legalRobot!** I have found **Click Jacking type** of Vulnerability in your Website

Now The Question is What is **Click Jacking.**
**Click Jacking** (User Interface redress attack, UI redress attack, UI redressing) is a malicious technique of tricking a Web user into clicking on something different from what the user perceives they are clicking on, thus potentially revealing confidential information or taking control of their computer while clicking on seemingly innocuous web pages.

How to Produce Click Jacking in your Website,
**Steps to Produce this Issue:-**
1) Create new .Html file. (I also send this file to you)
2) Copy & Paste this code in Html & save it
`<html>
   <head>
     <title>Clickjack test page</title>
   </head>
   <body>
     <p>Website is vulnerable to clickjacking!</p>
     <iframe src="https://www.legalrobot.com/" width="500" 
height="500"></iframe>
   </body>
</html>`
 3) Open that html file and you are seeing your website content opening in other frame.

**Fix:** Use a proper X-Frame to your website, So other domains can not use your website content, Mostly Spammers & Attackers can use this technique. (See My Example File too)

Get More Help From Owasp guides:
https://www.owasp.org/index.php?title=Testing_for_Clickjacking_(OTG-CLIENT-009)&setlang=en
https://www.owasp.org/index.php/Clickjacking
https://www.owasp.org/index.php/Clickjacking_Defense_Cheat_Sheet

Glad to be, If you fix this Click Jacking flaw in your website,
Thanks! Regards: Muhammad Muhaddis (Cyber Security Researcher)

</details>

---
*Analysed by Claude on 2026-05-24*
