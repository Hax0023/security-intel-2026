# Stored XSS on Wordpress 5.3 via Title Post

## Metadata
- **Source:** HackerOne
- **Report:** 754352 | https://hackerone.com/reports/754352
- **Submitted:** 2019-12-09
- **Reporter:** muhammaddaffa
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** high
- **Vuln:** Cross-site Scripting (XSS) - Stored
- **CVEs:** None
- **Category:** web-api

## Summary
I have identified a WordPress security vulnerability , a Stored XSS vulnerability that affects latest version of WordPress (5.3)

POC:
1) Login to wordpress website
2) Make a post with title payload xss like example <script>alert(document.domain);</script>
3) Publish then open the post, XSS Will trigger

## Impact

Can stealing cookie user

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

I have identified a WordPress security vulnerability , a Stored XSS vulnerability that affects latest version of WordPress (5.3)

POC:
1) Login to wordpress website
2) Make a post with title payload xss like example <script>alert(document.domain);</script>
3) Publish then open the post, XSS Will trigger

## Impact

Can stealing cookie user

</details>

---
*Analysed by Claude on 2026-05-24*
