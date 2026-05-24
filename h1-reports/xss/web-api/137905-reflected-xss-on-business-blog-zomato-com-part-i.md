# Reflected XSS on business-blog.zomato.com - Part I

## Metadata
- **Source:** HackerOne
- **Report:** 137905 | https://hackerone.com/reports/137905
- **Submitted:** 2016-05-11
- **Reporter:** dsopas
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
Hi guys,

I would like to report a reflected XSS on business-blog.zomato.com.

1. Open Chrome and Firefox (latest versions)
2. Open https://business-blog.zomato.com/wp-includes/js/mediaelement/flashmediaelement.swf?jsinitfunctio%gn=alert`1`
3. Payload is executed

Check the attached screenshot.

Solution:
- Update Wordpress to 4.5.2
- Update flashmediaelement.swf to 2.21.1

Feel free to contact me

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

Hi guys,

I would like to report a reflected XSS on business-blog.zomato.com.

1. Open Chrome and Firefox (latest versions)
2. Open https://business-blog.zomato.com/wp-includes/js/mediaelement/flashmediaelement.swf?jsinitfunctio%gn=alert`1`
3. Payload is executed

Check the attached screenshot.

Solution:
- Update Wordpress to 4.5.2
- Update flashmediaelement.swf to 2.21.1

Feel free to contact me if you need further assistance.

Best,
-David Sopas

</details>

---
*Analysed by Claude on 2026-05-24*
