# Clickjacking to Semrush Auth Login

## Metadata
- **Source:** HackerOne
- **Report:** 318295 | https://hackerone.com/reports/318295
- **Submitted:** 2018-02-21
- **Reporter:** karrrtik
- **Program:** Semrush
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Clickjacking, UI Redressing, Missing X-Frame-Options Header
- **CVEs:** None
- **Category:** uncategorised

## Summary
The geo.semrush.com authentication endpoint lacks clickjacking protections, allowing attackers to embed the login interface in an iframe and deceive users into performing unintended actions. An attacker could overlay transparent or disguised elements on top of the legitimate login page to trick victims into entering credentials or authorizing actions without realizing what they are doing.

## Attack scenario
1. Attacker creates a malicious webpage with an iframe containing https://geo.semrush.com/
2. Attacker overlays transparent elements or deceptive UI on top of the framed login page
3. Victim visits the attacker's webpage believing it is a legitimate site
4. Victim clicks on what appears to be a benign element (e.g., 'Click here to download' button)
5. Due to positioning tricks, the click actually targets the Semrush login form fields or submit button
6. Victim unknowingly submits credentials or performs account actions to the attacker

## Root cause
The Semrush authentication endpoint fails to implement X-Frame-Options or Content-Security-Policy headers that would prevent the page from being embedded in iframes on third-party domains, allowing arbitrary framing attacks.

## Attacker mindset
An attacker would seek to harvest user credentials or gain unauthorized account access by exploiting the lack of frame-busting protections. The simplicity of the attack (basic HTML iframe) combined with high-value targets (authentication pages) makes this an attractive vector for credential theft or session hijacking.

## Defensive takeaways
- Implement X-Frame-Options: DENY or X-Frame-Options: SAMEORIGIN header on all authentication pages
- Deploy Content-Security-Policy with frame-ancestors directive to restrict framing context
- Add frame-busting JavaScript code as additional layer (window.self check)
- Implement SameSite cookie attribute on session tokens to mitigate session hijacking
- Conduct clickjacking risk assessment on all interactive endpoints, especially authentication flows
- Use visual indicators or JavaScript checks to warn users if page is being framed
- Monitor for suspicious referrer patterns in authentication logs

## Variant hunting
Check other Semrush domains (semrush.com main login, api endpoints) for same vulnerability
Test password reset and account recovery endpoints for clickjacking
Examine OAuth/SSO implementation endpoints for frame protections
Verify admin/enterprise authentication portals lack frame-busting mechanisms
Test file upload and sensitive action endpoints for clickjacking applicability
Check mobile authentication flows and PWA implementations

## MITRE ATT&CK
- T1598.004
- T1187
- T1056.004

## Notes
This is a straightforward clickjacking vulnerability with clear proof-of-concept. The low technical barrier to exploitation combined with high-value authentication endpoints makes this a legitimate security concern. The researcher's impact assessment correctly identifies credential theft and account takeover as primary risks. Modern browsers and CSP have reduced clickjacking impact, but legacy support and incomplete implementation still leaves many applications vulnerable. The vulnerability demonstrates the importance of defense-in-depth on authentication mechanisms.

## Full report
<details><summary>Expand</summary>

Description:
Clickjacking (User Interface redress attack, UI redress attack, UI redressing) is a malicious technique of tricking a Web user into clicking on something different from what the user perceives they are clicking on. this attack could be perform to semrush auth user because its direct popup for geo.semrush.com login.

Steps To Reproduce:
Create HTML file containg following code:
<iframe src="https://geo.semrush.com/"></iframe>
Execute the HTML file & you will see Single Sing On login page present trough the iframe.

## Impact

Revealing confidential information(credentials) AND/OR taking control of their computer/account while clicking on seemingly innocuous web pages.

The hacker selected the **UI Redressing (Clickjacking)** weakness. This vulnerability type requires contextual information from the hacker. They provided the following answers:

**URL**
https://geo.semrush.com/

**Can a victim be tricked into unknowingly initiating a specific action?**
Yes

**What specific action can the user be tricked into?**
semrush auth login could be hack

</details>

---
*Analysed by Claude on 2026-05-24*
