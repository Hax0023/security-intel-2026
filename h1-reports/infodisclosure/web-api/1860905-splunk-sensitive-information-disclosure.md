# Splunk Sensitive Information Disclosure @████████

## Metadata
- **Source:** HackerOne
- **Report:** 1860905 | https://hackerone.com/reports/1860905
- **Submitted:** 2023-02-03
- **Reporter:** spell1
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Insecure Storage of Sensitive Information
- **CVEs:** CVE-2018-11409
- **Category:** web-api

## Summary
Hi Team,

Hope you are doing great.
I got a domain that contains Splunk Sensitive Information Disclosure @██████████
PoC:
https://███████/en-US/splunkd/__raw/services/server/info/server-info?output_mode=json
█████████

Splunk through 7.0.1 allows information disclosure by appending __raw/services/server/info/server-info?output_mode=json to a query, as demonstrated by discovering a license key.

Re

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

Hi Team,

Hope you are doing great.
I got a domain that contains Splunk Sensitive Information Disclosure @██████████
PoC:
https://███████/en-US/splunkd/__raw/services/server/info/server-info?output_mode=json
█████████

Splunk through 7.0.1 allows information disclosure by appending __raw/services/server/info/server-info?output_mode=json to a query, as demonstrated by discovering a license key.

Reference:
    - https://nvd.nist.gov/vuln/detail/CVE-2018-11409
    - https://github.com/kofa2002/splunk
    - https://www.exploit-db.com/exploits/44865/
    - http://web.archive.org/web/20211208114213/https://securitytracker.com/id/1041148

## Impact

Splunk Sensitive Information Disclosure

## System Host(s)
██████

## Affected Product(s) and Version(s)


## CVE Numbers


## Steps to Reproduce
Open this link:
https://█████████/en-US/splunkd/__raw/services/server/info/server-info?output_mode=json

## Suggested Mitigation/Remediation Actions




</details>

---
*Analysed by Claude on 2026-05-24*
