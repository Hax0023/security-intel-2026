# Clickjacking Vulnerability in Legalrobot App

## Metadata
- **Source:** HackerOne
- **Report:** 270454 | https://hackerone.com/reports/270454
- **Submitted:** 2017-09-22
- **Reporter:** 9it0wl
- **Program:** Legalrobot
- **Bounty:** Not specified
- **Severity:** Medium
- **Vuln:** Clickjacking, UI Redressing, Missing X-Frame-Options Header
- **CVEs:** None
- **Category:** uncategorised

## Summary
The Legalrobot application fails to implement X-Frame-Options HTTP headers, allowing the email verification page to be embedded in iframes on attacker-controlled websites. This enables clickjacking attacks where users can be tricked into performing unintended actions while believing they are interacting with the legitimate application.

## Attack scenario
1. Attacker creates a malicious website with an invisible or disguised iframe embedding the Legalrobot verification page
2. Attacker crafts a compelling social engineering message (e.g., 'Verify your account to claim a reward') and distributes the link via phishing emails or social media
3. Victim visits the attacker's website believing they are performing a legitimate action
4. Victim unknowingly clicks buttons on the invisible/overlaid iframe, triggering unintended actions on the Legalrobot application
5. Attacker captures clicks that could lead to account verification, form submissions, or other sensitive operations
6. Victim's account or data is compromised without their knowledge or explicit consent

## Root cause
The application does not implement X-Frame-Options HTTP response header or frame-busting JavaScript code to prevent embedding in iframes. This allows any external website to load the application content within an iframe context.

## Attacker mindset
An attacker would recognize that the verification page performs sensitive operations (email verification) and seek to redirect user interactions to unintended targets. The lack of framing protection makes this trivial to exploit, requiring minimal technical sophistication and only basic HTML knowledge.

## Defensive takeaways
- Implement X-Frame-Options HTTP header with 'DENY' or 'SAMEORIGIN' value on all sensitive pages
- Add Content-Security-Policy header with frame-ancestors directive as defense-in-depth
- Implement frame-busting JavaScript code as secondary protection for legacy browser support
- Apply clickjacking protections to all pages handling sensitive operations, not just authentication pages
- Use security headers scanning tools to validate proper implementation across the entire application
- Test clickjacking protection as part of security testing methodology for every release

## Variant hunting
Check all authentication-related pages (login, registration, password reset, MFA) for X-Frame-Options headers
Scan for similar vulnerabilities on related subdomains and staging environments
Review all user-facing forms that trigger sensitive operations (fund transfers, data deletion, permission changes)
Test API endpoints to ensure they also return appropriate headers
Verify that error pages and redirect pages also have proper framing protection

## MITRE ATT&CK
- T1189
- T1566
- T1539

## Notes
Vulnerability affects both production (app.legalrobot.com) and UAT (app.legalrobot-uat.com) environments. The POC demonstrates the issue using simple HTML iframe embedding with sandbox attributes. This is a well-known vulnerability class that is straightforward to remediate but often overlooked. The sandbox='allow-scripts allow-forms' attribute in the POC shows that even with sandbox restrictions, the vulnerability remains exploitable for clickjacking purposes.

## Full report
<details><summary>Expand</summary>

Dear Team,

#POC
Please find attached screenshots

#Steps to reproduce:

create index.html file with following content:
<iframe sandbox="allow-scripts allow-forms" src="https://app.legalrobot-uat.com/pending-verification" width="1000" height="600"></iframe>

Open index.html in browser

Actual result: Legalrobot email verification page is viewed in iframe.

#Remediation:
Frame busting technique is the better framing protection technique.
Sending the proper X-Frame-Options HTTP response headers that instruct the browser to not allow raming from other domains.

Same issue found in https://app.legalrobot.com/pending-verification as well.


</details>

---
*Analysed by Claude on 2026-05-24*
