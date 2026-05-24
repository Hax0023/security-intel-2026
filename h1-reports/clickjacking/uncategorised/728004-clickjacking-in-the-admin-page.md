# Clickjacking in Rocket.Chat Admin Page

## Metadata
- **Source:** HackerOne
- **Report:** 728004 | https://hackerone.com/reports/728004
- **Submitted:** 2019-11-02
- **Reporter:** ant_pyne
- **Program:** Rocket.Chat
- **Bounty:** Not specified in report
- **Severity:** medium
- **Vuln:** clickjacking, UI redress attack, missing security headers
- **CVEs:** None
- **Category:** uncategorised

## Summary
Rocket.Chat's admin pages lack X-Frame-Options headers, allowing attackers to embed the admin interface in an iframe and trick administrators into performing unintended actions through UI redressing. An attacker can manipulate admin functions including user creation, deletion, privilege escalation, and account takeover by overlaying invisible frames on legitimate-looking web pages.

## Attack scenario
1. Attacker creates a malicious HTML page containing an invisible iframe pointing to the victim's Rocket.Chat admin panel (e.g., https://penetrationtester.rocket.chat/admin/users)
2. Attacker crafts a transparent overlay with misleading content (e.g., 'Click to claim free gift' or 'Verify your account') positioned exactly over clickable admin elements
3. Attacker socially engineers an admin user to visit the malicious page via email, message, or ad
4. When the logged-in admin clicks the fake overlay, they unknowingly interact with the hidden admin panel (creating users, deleting accounts, granting admin privileges)
5. Admin actions execute with full privileges, allowing attackers to escalate permissions, compromise accounts, or modify system configuration
6. Attack succeeds silently without the admin realizing they performed unauthorized actions

## Root cause
Rocket.Chat server fails to include X-Frame-Options HTTP response header in admin pages, allowing the application to be rendered within iframe elements on external domains. This missing security control enables clickjacking attacks against authenticated administrators.

## Attacker mindset
An attacker seeks to compromise high-privilege accounts with minimal technical complexity. Clickjacking requires only HTML/CSS knowledge and social engineering—no exploit code needed. The high-value target (admin accounts) with direct access to user management, configuration, and system controls makes this an attractive attack vector for account takeover and privilege escalation.

## Defensive takeaways
- Implement X-Frame-Options header set to 'DENY' or 'SAMEORIGIN' on all pages, especially administrative interfaces
- Add Content-Security-Policy frame-ancestors directive as defense-in-depth measure
- Implement frame-busting JavaScript code to prevent rendering within iframes (defense-in-depth)
- Use SameSite cookie attribute to mitigate CSRF/clickjacking attacks
- Apply security headers consistently across all response types and endpoints
- Conduct security awareness training for administrators about clickjacking risks
- Regular security header audits using tools like securityheaders.com

## Variant hunting
Check all admin pages for missing X-Frame-Options headers (settings, logs, plugins, workspace management)
Test user-facing sensitive pages (password reset, email verification, API token generation) for clickjacking
Verify if CSP frame-ancestors directive is present where X-Frame-Options exists
Test authenticated vs unauthenticated endpoints for header inconsistency
Check iframe rendering behavior on different subdomains and URLs
Look for dynamic page generation that may bypass static header configuration
Test with other security headers (Referrer-Policy, Permissions-Policy) for comprehensive UI redress attacks

## MITRE ATT&CK
- T1190
- T1566
- T1598
- T1539
- T1098

## Notes
This vulnerability affects all Rocket.Chat installations by default, making it a widespread security issue. While categorized as medium, the impact is significant due to targeting admin accounts with full system control. The attack is practical with low technical barriers—requiring only knowledge of installation URL and ability to social engineer an admin. Exploitation leaves minimal forensic evidence, making detection difficult. The fix is trivial (adding one HTTP header), suggesting this was an oversight rather than a design flaw.

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
