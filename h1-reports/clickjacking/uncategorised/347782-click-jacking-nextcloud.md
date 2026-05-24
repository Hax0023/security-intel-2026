# Missing X-Frame-Options Header - Clickjacking Vulnerability in Nextcloud

## Metadata
- **Source:** HackerOne
- **Report:** 347782 | https://hackerone.com/reports/347782
- **Submitted:** 2018-05-05
- **Reporter:** enz0
- **Program:** Nextcloud
- **Bounty:** Not specified in report
- **Severity:** medium
- **Vuln:** Clickjacking, UI Redressing, Missing Security Header
- **CVEs:** None
- **Category:** uncategorised

## Summary
Nextcloud's login portal fails to implement the X-Frame-Options HTTP response header, allowing the application to be embedded in iframes on malicious websites. An attacker can perform clickjacking attacks by overlaying transparent frames to trick users into unintended actions such as logging in or initiating password resets on attacker-controlled pages.

## Attack scenario
1. Attacker creates a malicious website and embeds Nextcloud's login page in an iframe using sandbox attributes to bypass restrictions
2. Attacker overlays transparent or disguised UI elements (buttons, forms) on top of the framed Nextcloud login page
3. Victim visits the attacker's malicious site, believing they are interacting with legitimate content
4. Victim's clicks intended for the attacker's page are redirected to the framed Nextcloud login form
5. Victim unknowingly submits credentials or initiates sensitive actions (password reset, account recovery) on the attacker's controlled page
6. Attacker captures credentials or uses the action chain for phishing, credential theft, or account takeover

## Root cause
Nextcloud web server fails to include the X-Frame-Options HTTP response header in its login portal responses, allowing the application to be rendered within iframe elements on external domains without restriction.

## Attacker mindset
An attacker recognizes that many users trust familiar login interfaces and can be socially engineered when those interfaces appear in unexpected contexts. By embedding legitimate-looking login pages on phishing sites, the attacker reduces user suspicion while capturing sensitive credentials. The lack of framing protection suggests a configuration oversight that can be exploited at scale with minimal technical complexity.

## Defensive takeaways
- Implement X-Frame-Options: DENY or SAMEORIGIN header on all web server responses, particularly authentication and sensitive pages
- Use Content-Security-Policy frame-ancestors directive as a modern alternative or complementary control
- Conduct regular security header audits across all application endpoints to ensure consistent protection
- Implement clickjacking protection testing in security assessment procedures
- Educate users about verifying URL and page source before entering sensitive information
- Consider implementing frame-busting JavaScript as a secondary defense layer

## Variant hunting
Check other Nextcloud endpoints beyond login.php (file upload, settings, sharing pages) for missing X-Frame-Options
Test other Nextcloud deployment scenarios (cloud providers, on-premises) for consistent header implementation
Verify X-Frame-Options implementation on API endpoints and administrative interfaces
Test Content-Security-Policy effectiveness alongside X-Frame-Options
Examine if sandbox attribute restrictions can be bypassed with specific attribute combinations
Check if other authentication mechanisms (OAuth, SAML) are similarly vulnerable

## MITRE ATT&CK
- T1189 - Service Exploitation
- T1598 - Phishing
- T1566 - Phishing
- T1114 - Email Collection
- T1110 - Brute Force

## Notes
This is a classic clickjacking vulnerability with clear proof-of-concept. The report quality is moderate - it identifies the vulnerability and provides working PoC, though the impact description conflates clickjacking with CSRF. The vulnerability is contextual to authentication pages where credential compromise is a primary concern. The reporter correctly identifies that sandbox attributes alone do not prevent clickjacking if the target page lacks X-Frame-Options. The report's mention of redirects suggests potential chaining with phishing attacks for credential harvesting.

## Full report
<details><summary>Expand</summary>

Hello Security,
Clickjacking (User Interface redress attack, UI redress attack, UI redressing) is a malicious technique of tricking a Web user into clicking on something different from what the user perceives they are clicking on, thus potentially revealing confidential information or taking control of their computer while clicking on seemingly innocuous web pages.
The server didn't return an X-Frame-Options header which means that this website could be at risk of a clickjacking attack. The X-Frame-Options HTTP response header can be used to indicate whether or not a browser should be allowed to render a page in a <frame> or <iframe>. Sites can use this to avoid clickjacking attacks, by ensuring that their content is not embedded into other sites.
This vulnerability affects Web Server.
IMPACT:
An attacker can host this domain in other evil site by using iframe and if a user fill the given filed it can directly redirect as logs to attacker and after its redirect to your web server.. its lead to steal user information too and use that host site as phishing of your site its CSRF and Clickjacking

POC:
1. open https://portal.nextcloud.com/login.php or https://nextcloud.com
2. Put the url in the below code of iframe
<html>
<body>
<iframe 
sandbox="allow-modals allow-scripts allow-forms allow-popups allow-same-origin"
src="https://portal.nextcloud.com/login.php" width=600 height=400>
</iframe>
</body>
</html>
3.Observe that site is getting displayed in Iframe

## Impact

By using Clickjacking technique, an attacker hijack's click's
meant for one page and route them to another page, most likely
for another application, domain, or both.

The hacker selected the **UI Redressing (Clickjacking)** weakness. This vulnerability type requires contextual information from the hacker. They provided the following answers:

**URL**
https://portal.nextcloud.com/login.php

**Can a victim be tricked into unknowingly initiating a specific action?**
Yes

**What specific action can the user be tricked into?**
This is the nexcloud login page, it can trick user login or forgot password function

</details>

---
*Analysed by Claude on 2026-05-24*
