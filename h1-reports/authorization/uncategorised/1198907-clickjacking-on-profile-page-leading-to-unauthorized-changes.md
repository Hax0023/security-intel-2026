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
The profile page at app.upchieve.org lacks X-Frame-Options header protection, allowing attackers to embed the page in an iframe on attacker-controlled sites. An authenticated user can be tricked into performing unintended actions on the profile page through UI redressing attacks.

## Attack scenario
1. Attacker creates a malicious website and embeds the legitimate profile page in an invisible or disguised iframe
2. Attacker overlays their own UI elements on top of the framed content or positions clickable elements to align with profile modification buttons
3. Attacker tricks a logged-in user into visiting the malicious website through social engineering or phishing
4. When the user interacts with what they think are legitimate elements, they actually click on hidden buttons in the framed profile page
5. The user's browser performs unauthorized actions on the profile (changing email, password, settings) while authenticated
6. Attacker gains control over the user's account or extracts sensitive information displayed on the profile page

## Root cause
The application fails to set the X-Frame-Options HTTP response header, which would prevent the page from being embedded in iframes on third-party sites. This is a fundamental UI security control that was not implemented.

## Attacker mindset
Low-effort opportunistic attack requiring minimal technical skill. Attackers recognize that framing protection is a basic security control and exploit its absence to hijack authenticated user sessions for account takeover or data manipulation.

## Defensive takeaways
- Implement X-Frame-Options header set to 'DENY' or 'SAMEORIGIN' on all pages, especially sensitive ones like profile/settings
- Use Content-Security-Policy frame-ancestors directive as a modern alternative to X-Frame-Options
- Implement additional clickjacking defenses like frame-busting JavaScript for defense-in-depth
- Add CSRF tokens to state-changing requests even with frame protection in place
- Consider implementing user interaction confirmation (CAPTCHAs or re-authentication) for sensitive operations
- Regularly audit HTTP security headers across the application

## Variant hunting
Check all pages handling sensitive operations (settings, payment, admin panels) for X-Frame-Options protection
Test embedded versions of profile pages in iframes to verify framing restrictions work
Look for pages where users can be tricked into clicking to perform actions (password reset, permission grants, form submissions)
Examine APIs that power UI actions to see if they validate request origins or implement CSRF protection
Test whether sensitive pages can be framed with Content-Security-Policy bypass techniques

## MITRE ATT&CK
- T1189 - Service Exploitation (clickjacking via iframe embedding)
- T1598 - Phishing (social engineering to visit attacker's malicious site)
- T1539 - Steal Web Session Cookie (if combined with other attacks to exfiltrate session)

## Notes
This is a classic clickjacking vulnerability with low implementation complexity but significant impact. The fix is straightforward (adding one HTTP header), making this a high-ROI security improvement. The report demonstrates good understanding of the vulnerability and provides clear reproduction steps and mitigation advice.

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
