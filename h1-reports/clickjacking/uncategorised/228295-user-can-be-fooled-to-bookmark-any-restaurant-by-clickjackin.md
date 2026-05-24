# User can be fooled to Bookmark any restaurant by clickjacking

## Metadata
- **Source:** HackerOne
- **Report:** 228295 | https://hackerone.com/reports/228295
- **Submitted:** 2017-05-14
- **Reporter:** na5ne3t
- **Program:** Zomato (inferred from restaurant context)
- **Bounty:** Not specified in report
- **Severity:** medium
- **Vuln:** Clickjacking, UI Redressing, CSRF (indirect)
- **CVEs:** None
- **Category:** uncategorised

## Summary
An attacker can trick users into bookmarking arbitrary restaurants through a clickjacking attack, bypassing previous security patches. By overlaying transparent or disguised iframe content, the attacker redirects user clicks intended for legitimate actions to hidden bookmark buttons.

## Attack scenario
1. Attacker creates a malicious webpage with an embedded iframe of the vulnerable restaurant application
2. The bookmark button is positioned off-screen or made transparent/hidden
3. Attacker overlays decoy content (e.g., 'Click to claim free voucher') above the hidden bookmark functionality
4. User clicks on the decoy content, unaware their click is actually activating the bookmark button
5. Multiple restaurants can be bookmarked in succession through repeated deceptive interactions
6. User's account shows unwanted bookmarks without their conscious consent

## Root cause
Insufficient X-Frame-Options header or Content-Security-Policy implementation allowing the application to be framed. The application lacks frame-busting code or proper anti-clickjacking protections that were supposedly fixed in the previous report.

## Attacker mindset
Attacker likely researches previous vulnerability disclosures to identify incomplete patches. They recognize that fixing clickjacking requires comprehensive defenses across multiple layers, and exploit gaps in the remediation. The goal may be spam/SEO manipulation or account degradation.

## Defensive takeaways
- Implement X-Frame-Options: DENY header to prevent framing entirely
- Deploy Content-Security-Policy with frame-ancestors 'none' directive
- Add client-side frame-busting JavaScript as defense-in-depth
- Implement SameSite cookie attributes to limit CSRF-related clickjacking
- Use UI integrity checks and randomized token positions for critical actions
- Require explicit user confirmation for sensitive state-changing operations like bookmarking
- Conduct regression testing after security patches to verify completeness
- Monitor and alert on unusual bookmarking patterns

## Variant hunting
Test other state-changing operations (likes, follows, ratings) for clickjacking susceptibility
Attempt clickjacking on authentication flows (login, password reset)
Check if payment/subscription actions are vulnerable
Analyze whether the fix was applied to all endpoints or only specific ones
Test different framing techniques (object, embed, svg, picture tags)
Verify if CSP can be bypassed through nonce/hash weaknesses

## MITRE ATT&CK
- T1190
- T1566.002
- T1040

## Notes
This report references a previous fix (report #214087), indicating the vulnerability was not fully patched. The reporter provided video PoC evidence. This is a follow-up to an incomplete remediation, suggesting the development team did not implement defense-in-depth measures. The ability to bookmark 'n numbers of restaurants' suggests batch operation potential and possible account manipulation attacks.

## Full report
<details><summary>Expand</summary>

In this report  https://hackerone.com/reports/214087 you people said the clickjacking issue is fixed but i have found another issue of clickjacking. Using clickjacking attacker can fooled an user to bookmark n numbers of restuarants. I am attaching a PoC video , watch the video.

</details>

---
*Analysed by Claude on 2026-05-24*
