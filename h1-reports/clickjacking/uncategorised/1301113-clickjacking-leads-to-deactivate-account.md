# Clickjacking on User Profile Page Leads to Account Deactivation

## Metadata
- **Source:** HackerOne
- **Report:** 1301113 | https://hackerone.com/reports/1301113
- **Submitted:** 2021-08-12
- **Reporter:** scianto05
- **Program:** Upchieve
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Clickjacking, UI Redressing, CSRF
- **CVEs:** None
- **Category:** uncategorised

## Summary
The profile page at https://hackers.upchieve.org/profile is vulnerable to clickjacking attacks due to missing X-Frame-Options header, allowing attackers to overlay malicious content on the legitimate page. An attacker can trick users into clicking sensitive buttons (such as account deactivation) by positioning invisible iframes and misleading visual cues, potentially leading to unauthorized account actions and credential theft.

## Attack scenario
1. Attacker creates an HTML page with an invisible or visually obfuscated iframe pointing to the target's profile page
2. Attacker uses CSS positioning (absolute positioning with pointer-events manipulation) to overlay fake click prompts over critical buttons like 'deactivate account'
3. Attacker hosts this malicious page on a phishing website or distributes it via social engineering
4. Victim visits the attacker's page believing it is legitimate content (e.g., 'click to claim reward')
5. Victim's click on the fake overlay triggers a click on the hidden iframe's deactivation button
6. Victim's account is deactivated without their knowledge, and sensitive data may be exposed or stolen

## Root cause
The application fails to implement the X-Frame-Options HTTP response header (or Content-Security-Policy frame-ancestors directive) to prevent embedding in iframes. Additionally, critical account actions lack CSRF tokens or proper confirmation mechanisms that cannot be bypassed through clickjacking.

## Attacker mindset
An attacker would seek to perform unauthorized account actions at scale by leveraging user trust. The simplicity of the clickjacking technique combined with high-impact actions (account deactivation, profile modification) makes this an attractive vector for mass account compromise or data exfiltration campaigns.

## Defensive takeaways
- Implement X-Frame-Options: DENY or X-Frame-Options: SAMEORIGIN HTTP header on all pages, especially those with sensitive functionality
- Set Content-Security-Policy header with frame-ancestors directive to control framing behavior
- Require explicit user confirmation (via modal dialog or page refresh) for sensitive actions like account deactivation
- Implement CSRF tokens on state-changing operations and validate same-site cookie policies
- Use SameSite cookie attribute (Strict or Lax) to prevent cross-site request forgery
- Apply pointer-events: auto and user-select: auto constraints on interactive elements to prevent CSS-based input obfuscation
- Regular security testing including clickjacking/UI redressing assessments

## Variant hunting
Check for clickjacking vulnerabilities on other sensitive endpoints (settings, billing, data export, deletion)
Test if other account-modifying actions (password reset, email change, 2FA disable) are similarly vulnerable
Investigate whether the application's API endpoints properly validate origin/referer headers
Assess if subdomains or related applications have similar frame-options misconfiguration
Test for universal CSRF token validation across all state-changing operations

## MITRE ATT&CK
- T1190
- T1566
- T1598
- T1185

## Notes
The report quality is moderate; the researcher provides a working proof-of-concept with HTML code and clear reproduction steps, but the explanation conflates clickjacking with CSRF and phishing. The actual vulnerability is clickjacking leading to unauthorized account state changes. The attack is practical and requires minimal attacker resources. The recommendation would be to immediately implement X-Frame-Options header and add confirmation dialogs for account deactivation.

## Full report
<details><summary>Expand</summary>

Hello UPCHEIVE SECURITY TEAM,

I'm Anto

Vulnerability :
Clickjacking in (https://hackers.upchieve.org/profile)

Steps to Reproduce:
1). Create a HTML file with following code

<!DOCTYPE HTML>
    <html lang="en-US">
    <head>
    <meta charset="UTF-8">
    </head>
    <body>
    <p>Click the place where its shows </p>
    <div style="position: absolute; left: 1150px; top: 180px; pointer-events: none;">Click 1</div>
    <div style="position: absolute; left: 350px; top: 580px; pointer-events: none;">Click 2</div>
    <div style="position: absolute; left: 800px; top: 1650px; pointer-events: none;">Click 2</div>
<iframe height="3000" width="1300" scrolling="no" src="https://hackers.upchieve.org/profile"></iframe>
  </body>   
  </html>

2), Save and Open it on your browser the page will be appear.

## Impact

An attacker can host this domain in other evil site by using iframe and if a user fill the given filed it can directly redirect as logs to attacker and after its redirect to your web server.. its lead to steal user information too and use that host site as phishing of your site its CSRF and Clickjacking.

Regards,
Anto

</details>

---
*Analysed by Claude on 2026-05-24*
