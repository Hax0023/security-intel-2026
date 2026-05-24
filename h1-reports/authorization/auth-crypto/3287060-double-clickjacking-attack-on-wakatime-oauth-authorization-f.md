# Double Clickjacking Attack on WakaTime OAuth Authorization Flow

## Metadata
- **Source:** HackerOne
- **Report:** 3287060 | https://hackerone.com/reports/3287060
- **Submitted:** 2025-08-05
- **Reporter:** zeesozee
- **Program:** WakaTime
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Clickjacking, OAuth Misconfiguration, User Interaction Manipulation, Cross-Window Forgery
- **CVEs:** None
- **Category:** auth-crypto

## Summary
A double-clickjacking vulnerability in WakaTime's OAuth authorization flow allows attackers to trick logged-in users into unknowingly authorizing malicious applications. By aligning a hidden button in a popup window with the authorization button, an attacker can capture the authorization code and obtain access tokens with full API permissions. This bypasses traditional clickjacking protections like X-Frame-Options by leveraging multiple browser windows.

## Attack scenario
1. Attacker creates a malicious WakaTime OAuth application and hosts a phishing page at attacker.com
2. Attacker crafts an HTML page with a button aligned to overlap with WakaTime's 'Connect my WakaTime account' authorization button when windows are positioned side-by-side
3. User's current tab is redirected to WakaTime's OAuth authorization endpoint while a new popup opens to attacker.com/attack
4. User clicks what they believe is the attacker's button, but the click is captured and used to trigger the authorization button in the WakaTime window
5. Authorization code is generated and redirected to attacker's callback URL with the authorization code parameter
6. Attacker exchanges the authorization code for an access token and gains full API access with defined scopes

## Root cause
The OAuth authorization dialog lacks protection against double-clickjacking attacks where buttons can be triggered through coordinated clicks across multiple browser windows. The authorization button is enabled by default without requiring gesture verification (mouse movement, keyboard input) to confirm user intent.

## Attacker mindset
An attacker recognizes that traditional clickjacking defenses (X-Frame-Options, CSP frame-ancestors) only protect against framing within a single window. By orchestrating clicks across multiple windows, they can bypass these protections. The attacker understands that users may not notice the window arrangement and can exploit the muscle memory of clicking buttons in similar positions.

## Defensive takeaways
- Implement gesture verification on critical authorization buttons - require mouse movement or keyboard input before button activation
- Add rate limiting on authorization attempts per session to detect automated click patterns
- Implement origin validation and referer checks for OAuth authorization requests
- Add user confirmation mechanisms such as CAPTCHA or additional verification steps for sensitive OAuth scopes
- Disable authorization buttons by default until explicit user gesture is detected (not just page load)
- Add visual indicators or delays between page load and button availability to prevent instantaneous exploitation
- Implement cross-origin communication checks to prevent window manipulation from untrusted origins
- Log and monitor for suspicious authorization patterns (multiple rapid authorizations, different IPs, etc.)
- Educate users about OAuth flows and risks of clicking buttons on unfamiliar pages

## Variant hunting
Similar double-clickjacking attacks on other OAuth providers (GitHub, Google, Microsoft) authorization flows
Double-clickjacking on sensitive financial transaction buttons (payment confirmations, money transfers)
Cross-window attacks targeting form submissions with CSRF tokens
Multi-window exploitation of admin panel sensitive actions
Attack variations using iframe overlays combined with window positioning
Mobile variants exploiting tap targets and touch gesture misalignment
Attacks targeting password reset or 2FA bypass flows using similar techniques

## MITRE ATT&CK
- T1566.002
- T1598.003
- T1187
- T1040
- T1185

## Notes
The vulnerability requires the victim to already be logged into WakaTime. The attack relies on browser window positioning and user interaction patterns. PoC includes Flask application demonstrating the attack with customizable button positioning. The researcher provided detailed reproduction steps and referenced emerging double-clickjacking research from security community.

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
