# weblate.org: X-XSS-Protection not enabled

## Metadata
- **Source:** HackerOne
- **Report:** 223723 | https://hackerone.com/reports/223723
- **Submitted:** 2017-04-25
- **Reporter:** amsda
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** low
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
Hi,

X-Xss-Protection @https://weblate.org has not been set.

This header is used to configure the built in reflective XSS protection found in Internet Explorer, Chrome and Safari (Webkit). Valid settings for the header are 0, which disables the protection, 1 which enables the protection and 1; mode=block which tells the browser to block the response if it detects an attack rather than sanitising 

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

Hi,

X-Xss-Protection @https://weblate.org has not been set.

This header is used to configure the built in reflective XSS protection found in Internet Explorer, Chrome and Safari (Webkit). Valid settings for the header are 0, which disables the protection, 1 which enables the protection and 1; mode=block which tells the browser to block the response if it detects an attack rather than sanitising the script.

NginX: add_header X-Xss-Protection "1; mode=block" always;

Apache: Header always set X-Xss-Protection "1; mode=block"

IIS:

</details>

---
*Analysed by Claude on 2026-05-24*
