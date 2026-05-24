# Sensitive information disclosure on grafana

## Metadata
- **Source:** HackerOne
- **Report:** 1448218 | https://hackerone.com/reports/1448218
- **Submitted:** 2022-01-12
- **Reporter:** asce21
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** low
- **Vuln:** infodisclosure
- **CVEs:** None
- **Category:** web-api

## Summary
## Summary:

While running through scan I got some endpoints on jetblue subdomains which discloses sensitive information. I know these are out of scope but I think it is necessary to report them

## Steps To Reproduce:

  1. Visit the urls in browser

`https://████.jetblue.com/metrics`

███

Discloses  grafana metrics  to unauthorized users

```
https://█████████.jetblue.com/sap/public/info
https:

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

## Summary:

While running through scan I got some endpoints on jetblue subdomains which discloses sensitive information. I know these are out of scope but I think it is necessary to report them

## Steps To Reproduce:

  1. Visit the urls in browser

`https://████.jetblue.com/metrics`

███

Discloses  grafana metrics  to unauthorized users

```
https://█████████.jetblue.com/sap/public/info
https://████.jetblue.com/sap/public/info
```

██████

Disclose sensitive information about SAP  such as internal IP address and OS

`https://███████.travelproducts.jetblue.com/`

███████

aws bucket listing is enabled which discloses sensitive endpoints to unauthorized users

## Impact

Unauthorized user can access sensitive info about server resources.

</details>

---
*Analysed by Claude on 2026-05-24*
