# Clickjacking in Rocket.Chat Admin Page

## Metadata
- **Source:** HackerOne
- **Report:** 728004 | https://hackerone.com/reports/728004
- **Submitted:** 2019-11-02
- **Reporter:** ant_pyne
- **Program:** Rocket.Chat
- **Bounty:** Not specified in report
- **Severity:** Medium
- **Vuln:** Clickjacking, UI Redressing, Missing Security Headers
- **CVEs:** None
- **Category:** uncategorised

## Summary
Rocket.Chat's admin pages lack X-Frame-Options headers, allowing them to be embedded in iframes and subjected to clickjacking attacks. An attacker can overlay transparent or disguised UI elements to trick administrators into performing unintended actions such as creating admin accounts or deleting users.

## Attack scenario
1. Attacker creates a malicious HTML page that embeds the target Rocket.Chat admin page (e.g., /admin/users) in an invisible iframe
2. Attacker overlays transparent or visually deceptive UI elements (buttons, forms) on top of the framed admin page to trick the admin user
3. Attacker lures the logged-in admin to the malicious page through phishing or social engineering
4. Admin unknowingly clicks on the attacker's UI elements, which interact with the hidden admin interface
5. Attacker's JavaScript captures the clicks and executes admin actions such as user creation, deletion, or privilege escalation
6. Attacker gains control over the Rocket.Chat instance through administrative manipulation

## Root cause
Rocket.Chat admin pages do not set the X-Frame-Options HTTP response header, allowing the pages to be embedded in iframes on any external domain. This missing security header is the direct cause of the clickjacking vulnerability.

## Attacker mindset
An attacker would identify that admin pages are valuable targets due to the sensitive operations they control. By bypassing the need for direct admin credentials, clickjacking allows the attacker to leverage the admin's existing session to perform account takeover, privilege escalation, and user manipulation without detection.

## Defensive takeaways
- Implement X-Frame-Options: DENY or X-Frame-Options: SAMEORIGIN headers on all sensitive pages, especially admin interfaces
- Use Content-Security-Policy (CSP) frame-ancestors directive as a modern alternative: frame-ancestors 'none'
- Apply frame-busting JavaScript as a defense-in-depth measure to prevent page rendering in frames
- Implement additional CSRF tokens and re-authentication checks for sensitive admin operations
- Use clickjacking protection libraries or middleware that automatically set appropriate headers
- Conduct security header audits across all critical pages during development and in CI/CD pipelines
- Educate administrators about clickjacking risks and the importance of careful interaction with admin panels

## Variant hunting
Check all admin pages and privileged functionality endpoints for missing X-Frame-Options headers
Test user management pages, settings pages, configuration pages, and API management interfaces
Verify that subdomains and API endpoints also properly set frame-options headers
Look for pages that perform state-changing operations (POST/DELETE) without additional anti-clickjacking protections
Check for SameSite cookie attributes that might provide partial protection against cross-site interactions
Test other Rocket.Chat deployments and custom installations for consistent header implementation

## MITRE ATT&CK
- T1190
- T1566
- T1547
- T1021

## Notes
The reporter correctly notes that while clickjacking is often considered a low-severity issue, the impact on administrative interfaces is significant. The attack requires the target to be logged in as an admin but requires no authentication from the attacker. This is a textbook example of why security headers are critical for sensitive pages. The vulnerability affects all Rocket.Chat installations by default, making it a widespread issue with high impact potential.

## Full report
<details><summary>Expand</summary>

**Summary:** 

Hello Rocket.Chat,

There is a clickjacking vulnerability in a very critical page which is the admin info page. For my installation, the URL https://penetrationtester.rocket.chat/admin/users was used for creating the PoC.

**Description:** 

Clickjacking (User Interface redress attack, UI redress attack, UI redressing) is a malicious technique of tricking a Web user into clicking on something different from what the user perceives they are clicking on, thus potentially revealing confidential information or taking control of their computer while clicking on seemingly innocuous web pages.

The server didn't return an X-Frame-Options header which means that this website could be at risk of a clickjacking attack. The X-Frame-Options HTTP response header can be used to indicate whether or not a browser should be allowed to render a page in a <frame> or <iframe>. Sites can use this to avoid clickjacking attacks, by ensuring that their content is not embedded into other sites.

The admin info page of all rocket.chat installations would be vulnerable.

## Steps To Reproduce (from initial installation to vulnerability):

1. Open the attached `Clickjacking.html` on a browser and if you are logged in from an admin account, you will see that the page is loaded.

Requirement for attack - Knowledge of the admin email and rocket.chat installation link.

**Reason for marking this as medium** - Even though Clickjacking is always considered a low hanging fruit, the impact this can have is humongous.

**Recommendation** - X-Frame options header.

## Impact

If the UI overlay can be performed correctly by the attacker, this can lead to account takeover, manipulation of admin account, making any user admin or deleting and/or adding any user.

</details>

---
*Analysed by Claude on 2026-05-24*
