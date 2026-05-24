# Stored XSS in Templates>Enahance>Social Badges

## Metadata
- **Source:** HackerOne
- **Report:** 238906 | https://hackerone.com/reports/238906
- **Submitted:** 2017-06-11
- **Reporter:** hackedbrain
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Stored
- **CVEs:** None
- **Category:** web-api

## Summary
Hi, just like the report #237927, I found stored XSS in Templates>Enhance> Social Badges section.

1. Go to templates section and click on one of your templates.
2. Enhance> Social Badges.
3. Enter the payload: javascript:alert(1) in any of the social networking button url.
4. You'll see that the xss is being triggered.

Note: The similar social sections in Call to Action button are not accepting 

## Attack scenario
*(see original)*

## Root cause
*(see original)*

## Attacker mindset
*(see original)*

## Defensive takeaways
*(see original)*

## Variant hunting
*(see original)*

## MITRE ATT&CK
*(see original)*

## Notes
*(see original)*

## Full report
<details><summary>Expand</summary>

Hi, just like the report #237927, I found stored XSS in Templates>Enhance> Social Badges section.

1. Go to templates section and click on one of your templates.
2. Enhance> Social Badges.
3. Enter the payload: javascript:alert(1) in any of the social networking button url.
4. You'll see that the xss is being triggered.

Note: The similar social sections in Call to Action button are not accepting this payload, so but this is not fixed in Social Badges section.

Thanks.

</details>

---
*Analysed by Claude on 2026-05-24*
