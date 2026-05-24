# Double Clickjacking Attack on WakaTime OAuth Authorization Flow

## Metadata
- **Source:** HackerOne
- **Report:** 3287060 | https://hackerone.com/reports/3287060
- **Submitted:** 2025-08-05
- **Reporter:** zeesozee
- **Program:** WakaTime
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Clickjacking, OAuth Authorization Bypass, UI Redressing, Cross-Window Attack
- **CVEs:** None
- **Category:** auth-crypto

## Summary
An attacker can exploit a double-clickjacking vulnerability in WakaTime's OAuth authorization dialog to trick logged-in users into unknowingly authorizing malicious applications. By overlaying a deceptive button that aligns with the legitimate 'Connect my WakaTime account' button across multiple windows, attackers can capture authorization codes and obtain full API access to the victim's WakaTime account.

## Attack scenario
1. Attacker creates a malicious WakaTime OAuth application and hosts a phishing webpage
2. Attacker crafts a page with a 'Double Click' button positioned to overlay the legitimate WakaTime authorization button
3. Victim visits attacker's page and clicks the deceptive button, which opens a new window to the WakaTime OAuth authorize endpoint
4. First click closes the attacker's tab; second click automatically clicks the 'Connect my WakaTime account' button on the WakaTime OAuth page
5. WakaTime generates an authorization code and redirects to attacker's redirect_uri with the code parameter
6. Attacker exchanges the authorization code for an access token and performs API calls with victim's permissions

## Root cause
WakaTime's OAuth authorization page lacks protection against double-clickjacking attacks. The critical 'Connect my WakaTime account' button is not disabled by default and does not require gesture verification (mouse movement, keyboard input) to activate, making it vulnerable to automated or delayed clicks from cross-window attacks. Traditional X-Frame-Options headers do not prevent this attack vector.

## Attacker mindset
An attacker seeks to gain unauthorized access to WakaTime user accounts and their associated data/permissions without requiring credential theft. By leveraging UI manipulation techniques that bypass traditional clickjacking defenses, the attacker can mass-compromise users through social engineering while remaining stealthy. The attacker recognizes that OAuth tokens grant broader permissions than simple credential compromise and targets the authorization flow as a weak point.

## Defensive takeaways
- Implement gesture verification on critical authorization buttons (require mouse movement, keyboard input, or explicit user gestures before enabling interaction)
- Disable authorization buttons by default and only enable them after detecting genuine user interaction (e.g., mouse enter + keyboard focus)
- Add rate-limiting and timing checks to detect unnatural click patterns or rapid consecutive interactions
- Implement frame-busting techniques and additional window/origin validation to detect cross-window attacks
- Use Content Security Policy (CSP) with frame-ancestors directive stricter than X-Frame-Options
- Add visual security indicators and confirmation steps specific to authorization flows
- Implement popup/window detection and warning mechanisms when authorization is triggered from external contexts
- Log and monitor suspicious authorization patterns (multiple windows, unusual click timing, referrer anomalies)
- Require user confirmation through alternative channels for high-permission scope requests

## Variant hunting
Similar vulnerabilities likely exist in other OAuth providers' authorization flows. Look for: (1) Authorization pages without gesture verification on approval buttons, (2) OAuth flows that don't validate window/popup origin or timing, (3) Multi-step authorization processes where intermediate steps lack protection, (4) Authorization pages served without anti-framing or popunder protections, (5) Third-party integrations (GitHub, Google, Facebook OAuth) that may have similar gaps, (6) WebAuthn/MFA enrollment flows that use similar approval button patterns, (7) Critical account actions (password reset, 2FA disable) that use unprotected authorization buttons

## MITRE ATT&CK
- T1190
- T1598
- T1566
- T1199
- T1187

## Notes
The vulnerability requires the victim to be pre-authenticated to WakaTime. The PoC demonstrates the attack is reproducible and practical. The researcher provided functional proof-of-concept code with Flask backend, indicating this is not theoretical. WakaTime's permission model grants broad API access to authorized applications, increasing impact severity. The attack is browser-agnostic and OS-independent. The double-clickjacking technique is an evolution of traditional clickjacking that bypasses X-Frame-Options by using multiple windows, making it a novel attack vector that may affect multiple OAuth providers and web applications.

## Full report
<details><summary>Expand</summary>

## Summary:
An attacker can trick users into unknowingly clicking the "Connect my WakaTime account" button in the WakaTime App consent dialog using a double-clickjacking attack. This allows an attacker to register a WakaTime  OAuth App, host a phishing page, and make the victim accidentally click the Authorize button. 

The attacker can then capture the authorization code and exchange it for an access token, allowing them to perform actions on behalf of the victim. This is similar to a clickjacking attack, but traditional protections like X-Frame-Options do not prevent it. The impact is the attacker application has full access to defined [permissions](https://wakatime.com/developers).

## PoC Video:
{F4647670}

## Attack Flow:
1. The attacker creates an initial webpage with a button that opens a new window (or just opens a new window without user interaction), let's say it's https://attacker.com
2. Current tab is redirected to WakaTime OAuth Authorization URL, for example: 
https://wakatime.com/oauth/authorize?client_id=joUNHCTnWqQ9hsmrWS5CTokR&response_type=code&redirect_uri=https://webhook.site/15495620-7c98-4643-a6df-9e7864c0dead&scope=read_orgs,write_orgs, which looks like this:

{F4647671}

3. At the same time, a new tab opened to https://attacker.com/attack, which looks like this:

{F4647672}

4. Notice that the "Double Click" button is aligned to be the same as the "Connect my WakaTime account" button. If it's not aligned perfectly, just play with the positions variable in the source code. The first click will close the /attack tab, then the second click will click the "Authorize" button.
5. The URL gets redirected to `https://webhook.site/15495620-7c98-4643-a6df-9e7864c0dead?code=CODE`. At this point, it's up to the attacker to store the code and exchange it for access token. Now the attacker can hit the API endpoint with defined permissions. To make the victim not realize an attack happens, the attacker page can be redirected to another website after getting the code.

## Steps To Reproduce:
1. You can download the source code from the attached file: {F4647674}.
2. Create a new WakaTime app at https://wakatime.com/apps/new.
3. Fill the details like this:

{F4647682}

7. In the source code in `index.html` on `const url=...`, simply change with your `client ID` and `redirect_uri`.
8. Run the flask app with **python main.py**.
9. Try to simulate the attack as victim account.

## Notes:
- The victim needs to be already logged in to WakaTime .
- The double-click button may not align perfectly, but there are ways to make the button flexible. You can adjust the position of button in `attack.html`. In the simple PoC, I only demonstrated the technique.
- Browser, OS and/or app version used during testing: Firefox Browser 140.0.2 (64-bit), Windows.

## Fix Suggestion:
Eliminate the risk of DoubleClickjacking by disabling critical buttons by default unless a gesture is detected (e.g., moving the mouse or using the keyboard).

## Supporting Material/References:
- https://jorianwoltjer.com/blog/p/hacking/pressing-buttons-with-popups
- https://www.evil.blog/2024/12/doubleclickjacking-what.html
- https://www.evil.blog/2024/02/cross-window-forgery-web-attack-vector.html?m=1

## Impact

This vulnerability allows an attacker to trick a logged-in WakaTime user into unknowingly authorizing a third-party application created by an attacker which an attacker can obtain access token to get resources from WakaTime API depending on the scopes and permissions. The maximum permission attacker can get is all scopes as explained at https://wakatime.com/developers.

</details>

---
*Analysed by Claude on 2026-05-24*
