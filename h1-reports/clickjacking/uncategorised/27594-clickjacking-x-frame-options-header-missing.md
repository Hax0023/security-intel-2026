# Clickjacking: X-Frame-Options header missing on glasswire.com

## Metadata
- **Source:** HackerOne
- **Report:** 27594 | https://hackerone.com/reports/27594
- **Submitted:** 2014-09-09
- **Reporter:** bigbear
- **Program:** GlassWire
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Clickjacking, Missing Security Header, UI Redressing
- **CVEs:** None
- **Category:** uncategorised

## Summary
Multiple pages on glasswire.com lack the X-Frame-Options HTTP security header, allowing the site to be embedded in frames on attacker-controlled domains. An attacker can exploit this to perform clickjacking attacks, potentially tricking users into performing unintended actions such as adding arbitrary tasks.

## Attack scenario
1. Attacker creates a malicious website and embeds glasswire.com content in an invisible iframe
2. Attacker overlays transparent buttons or clickable elements on top of the framed content at strategic locations
3. Legitimate users visit the attacker's malicious site, believing they are interacting with normal content
4. Users unknowingly click on hidden elements that trigger actions on glasswire.com (e.g., adding tasks, changing settings)
5. The attacker achieves their goal (task injection, account modification, data exfiltration) without user awareness
6. Attack persists across multiple user sessions due to missing header on all vulnerable pages

## Root cause
Server fails to include X-Frame-Options: DENY or X-Frame-Options: SAMEORIGIN header in HTTP responses, allowing any domain to frame the content without restriction

## Attacker mindset
Low-effort, high-impact social engineering attack requiring no authentication bypass or technical exploits, merely relying on missing defensive headers

## Defensive takeaways
- Configure X-Frame-Options header globally to DENY or SAMEORIGIN on all pages
- Implement Content-Security-Policy frame-ancestors directive as modern alternative/complement
- Audit all endpoints to ensure consistent security header deployment
- Use security header scanning tools in CI/CD pipeline to prevent regression
- Implement clickjacking protection tests in security validation suite

## Variant hunting
Search for similar missing security headers (Missing CSP, Missing STS), check for partial header implementation (only on certain paths), test X-Frame-Options bypass techniques, identify pages handling sensitive operations (payments, authentication) without framing protection

## MITRE ATT&CK
- T1189
- T1598
- T1566

## Notes
This is a classic, well-understood vulnerability. The researcher references a nearly identical prior report (HackerOne #17896), indicating this was a known issue category. The vulnerability is particularly concerning on GlassWire due to potential task automation capabilities. Fix is trivial (add header) but impact can be significant depending on what actions users can be tricked into performing.

## Full report
<details><summary>Expand</summary>

Hello. Typical simple bug.

Victim - www.glasswire.com

"It allows remote attackers to do some clickjacking which can be used for adding arbitrary tasks . Why? Almost all of your page has missing X-FRAME-OPTIONS header.

Websites are at risk of a clickjacking attack when they allow content to be embedded within a frame.

An attacker may use this risk to invisibly load the target website into their own site and trick users into clicking on links which they never intended to. An "X-Frame-Options" header should be sent by the server to either deny framing of content, only allow it from the same origin or allow it from a trusted URIs." (c) https://hackerone.com/reports/17896

</details>

---
*Analysed by Claude on 2026-05-24*
