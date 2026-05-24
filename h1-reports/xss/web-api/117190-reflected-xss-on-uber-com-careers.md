# Reflected XSS on Uber.com careers

## Metadata
- **Source:** HackerOne
- **Report:** 117190 | https://hackerone.com/reports/117190
- **Submitted:** 2016-02-18
- **Reporter:** pavanw3b
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
###Location
www.uber.com/careers/

###Description:
It is possible for an attacker to inject an arbitrary javascript into city GET parameter. This leads to phishing, defacing from URL, stealing credentials by using a fake login page and many other client side risks.

###POC:
- Logon to [uber.com/careers/list/?city=...](https://www.uber.com/careers/list/?city=allicg<%2fscript><script>alert('xss by p

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

###Location
www.uber.com/careers/

###Description:
It is possible for an attacker to inject an arbitrary javascript into city GET parameter. This leads to phishing, defacing from URL, stealing credentials by using a fake login page and many other client side risks.

###POC:
- Logon to [uber.com/careers/list/?city=...](https://www.uber.com/careers/list/?city=allicg<%2fscript><script>alert('xss by pavanw3b')<%2fscript>fupaiiz&country=all&keywords=&subteam=all&team=all) on firefox.
- Note the alert *xss by pavanw3b* as the screenshot attached.

Tested on latest firefox: 4.0.2

Please let me know if you need further explanation or details.​

Cheers,
Pavan
www.pavanw3b.com | fb/pavanw3b | @pavanw3b

</details>

---
*Analysed by Claude on 2026-05-24*
