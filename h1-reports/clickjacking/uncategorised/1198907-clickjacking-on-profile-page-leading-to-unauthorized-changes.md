# Clickjacking on profile page leading to unauthorized changes

## Metadata
- **Source:** HackerOne
- **Report:** 1198907 | https://hackerone.com/reports/1198907
- **Submitted:** 2021-05-16
- **Reporter:** shivanshmalik2
- **Program:** UPchieve
- **Bounty:** Not specified
- **Severity:** Medium
- **Vuln:** Clickjacking, UI Redressing, Missing X-Frame-Options Header
- **CVEs:** None
- **Category:** uncategorised

## Summary
The profile page at app.upchieve.org/profile lacks X-Frame-Options headers, allowing attackers to embed the page in an iframe on a malicious website. An attacker could perform clickjacking attacks to trick authenticated users into unknowingly performing unauthorized actions on their profile.

## Attack scenario
1. Attacker identifies that the profile page lacks X-Frame-Options protection
2. Attacker creates a malicious website embedding the target profile page in a transparent iframe
3. Attacker overlays deceptive UI elements on the iframe to trick users into clicking
4. User visits attacker's website while logged into app.upchieve.org
5. User clicks on what appears to be a legitimate button but actually interacts with the hidden profile page
6. Unauthorized profile modifications (email change, password reset, etc.) are executed with the user's credentials

## Root cause
The application fails to implement X-Frame-Options or Content-Security-Policy frame-ancestors directives in HTTP response headers, allowing the page to be framed by any external domain.

## Attacker mindset
An attacker recognizes that lack of framing protection enables clickjacking attacks. They can craft a convincing phishing page that overlays the real application interface with misleading prompts, exploiting user trust and session cookies to perform unauthorized actions on authenticated accounts.

## Defensive takeaways
- Implement X-Frame-Options: DENY or SAMEORIGIN header on all sensitive pages
- Use Content-Security-Policy header with frame-ancestors directive to restrict framing
- Implement frame-busting JavaScript as defense-in-depth measure
- Add SameSite cookie attribute to prevent cross-site cookie transmission
- Require user confirmation and re-authentication for sensitive profile changes
- Implement clickjacking detection and frame integrity checks on client-side

## Variant hunting
Check other authenticated pages (settings, account, admin panels) for missing frame-options
Test API endpoints for CSRF protection when called from cross-origin frames
Verify if session cookies have SameSite protection
Check if CSP policy restricts framing on all sensitive endpoints
Test for dangling iframes or frame-busting bypasses
Examine if user-modifiable content pages can be embedded and attacked

## MITRE ATT&CK
- T1189
- T1583
- T1598

## Notes
This is a classic clickjacking vulnerability with straightforward mitigation. The reporter provided clear reproduction steps. The impact is moderate as it requires user interaction and active session. The fix is simple server-side configuration, making this a common oversight in security implementations. No authentication bypass is involved; exploitation requires the user to already be logged in.

## Full report
<details><summary>Expand</summary>

## Summary:
Any attacker could use iFrame options to connect remotely to the real website, And he can craft his own website using the iFrame options of the specific link and can lead to unauthorized changes if the user will be logged in.

## Steps To Reproduce:
1. Login to https://app.upchieve.org/profile
2. Download the attached file and run it on the same browser 
3. You will see a small window which shows us the profile page, Ive currently set the size to small
4. Attacker can make it bigger and gain info.

## Recommendations for Fixing/Mitigation
Use X-Frame Options in the HTTP Responses of the page, This will help content going straight to user and not a 3rd Party.

## Impact

Unauthorized control

</details>

---
*Analysed by Claude on 2026-05-24*
