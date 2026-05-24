# Reflected Self-XSS in Slack

## Metadata
- **Source:** HackerOne
- **Report:** 97683 | https://hackerone.com/reports/97683
- **Submitted:** 2015-11-04
- **Reporter:** harrymg
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
1. Go to https://(domainname).slack.com/services/new
2. In the searchbar, type an XSS payload (I used <img src=x onerror=alert(document.domain)>)
3. Hit Enter
4. XSS pop-up

Thanks!

I have provided POCs

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

1. Go to https://(domainname).slack.com/services/new
2. In the searchbar, type an XSS payload (I used <img src=x onerror=alert(document.domain)>)
3. Hit Enter
4. XSS pop-up

Thanks!

I have provided POCs

</details>

---
*Analysed by Claude on 2026-05-24*
