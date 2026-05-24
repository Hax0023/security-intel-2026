# Clickjacking at join.nordvpn.com

## Metadata
- **Source:** HackerOne
- **Report:** 765955 | https://hackerone.com/reports/765955
- **Submitted:** 2019-12-30
- **Reporter:** ddaasddd1
- **Program:** NordVPN
- **Bounty:** Not specified in report
- **Severity:** medium
- **Vuln:** Clickjacking, UI Redressing, Missing X-Frame-Options Header
- **CVEs:** None
- **Category:** uncategorised

## Summary
The join.nordvpn.com domain is vulnerable to clickjacking attacks due to missing X-Frame-Options HTTP header, allowing attackers to embed the page in an iframe and overlay malicious content. An attacker can trick users into performing unintended actions such as subscribing to VPN services, clicking on advertisements, or completing other interactions through a hidden or disguised iframe.

## Attack scenario
1. Attacker creates a malicious HTML page with a transparent iframe embedding join.nordvpn.com
2. Attacker overlays the iframe with legitimate-looking content (e.g., 'Click here to claim prize' or 'Verify account')
3. Victim visits the attacker's malicious page
4. Victim clicks on what they believe is harmless content, but actually clicks on hidden elements within the NordVPN signup page
5. Victim unknowingly completes actions on join.nordvpn.com such as signing up for premium services or clicking referral links
6. Attacker potentially gains commission/referral benefits or captures victim data

## Root cause
The web server hosting join.nordvpn.com does not implement the X-Frame-Options HTTP response header (or implements it with an unsafe value like 'ALLOW-ALL'). Without this header or Content-Security-Policy frame-ancestors directive, browsers allow any website to embed the page in an iframe.

## Attacker mindset
An attacker seeks to monetize the NordVPN affiliate/referral program by tricking users into signing up through their referral link via clickjacking. Alternatively, they may perform UI redressing attacks to harvest user data or credentials during signup.

## Defensive takeaways
- Implement X-Frame-Options: DENY or X-Frame-Options: SAMEORIGIN header on all pages
- Add Content-Security-Policy header with frame-ancestors 'self' directive as defense-in-depth
- Conduct security headers audit across all subdomains and ensure consistent protection
- Implement frame-busting JavaScript code as additional client-side mitigation
- Test for clickjacking vulnerabilities during security assessments of all user-facing pages
- Monitor and alert on unusual referral signup patterns that may indicate clickjacking campaigns

## Variant hunting
Check other NordVPN subdomains (account.nordvpn.com, billing.nordvpn.com, etc.) for same vulnerability
Test other payment/signup flows in the NordVPN ecosystem
Look for similar missing security headers on partner domains or affiliate pages
Check if the vulnerability exists on mobile versions of the site
Test with different framing techniques (object, embed, picture-in-picture) to bypass partial mitigations

## MITRE ATT&CK
- T1189
- T1598
- T1566

## Notes
This is a classic and well-understood vulnerability with straightforward remediation. The PoC is simple and reproducible. The impact extends beyond direct user manipulation to potential affiliate fraud and brand abuse through clickjacking campaigns. The vulnerability was likely in a lower-priority subdomain (join.nordvpn.com) rather than the main site, suggesting inconsistent security header deployment across the organization.

## Full report
<details><summary>Expand</summary>

PoC at attach

Create a new HTML file
Put <iframe src ="https://join.nordvpn.com" width="500" height="500"></iframe>
Save the file
Open document in browser

## Impact

https://www.owasp.org/index.php/Clickjacking

</details>

---
*Analysed by Claude on 2026-05-24*
