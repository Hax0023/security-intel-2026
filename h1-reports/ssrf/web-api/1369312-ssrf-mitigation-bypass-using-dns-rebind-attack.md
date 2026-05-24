# SSRF mitigation bypass using DNS Rebind attack

## Metadata
- **Source:** HackerOne
- **Report:** 1369312 | https://hackerone.com/reports/1369312
- **Submitted:** 2021-10-13
- **Reporter:** adrian_t
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** low
- **Vuln:** Server-Side Request Forgery (SSRF)
- **CVEs:** CVE-2021-22969
- **Category:** web-api

## Summary
We noticed that the upload functionality contains the ability to upload files from remote server, however there are some mitigations against accessing the AWS Instance Metadata service.

We've managed to bypass these mitigations using DNS rebinding and we've managed to fetch the AWS IAM keys when Concrete CMS is running in the cloud.

We've used http://1u.ms/ service for DNS rebinding, please see 

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

We noticed that the upload functionality contains the ability to upload files from remote server, however there are some mitigations against accessing the AWS Instance Metadata service.

We've managed to bypass these mitigations using DNS rebinding and we've managed to fetch the AWS IAM keys when Concrete CMS is running in the cloud.

We've used http://1u.ms/ service for DNS rebinding, please see screenshots with evidence.

## Impact

An attacker can bypass the SSRF protections and he can fetch the AWS IAM keys under which the application is running. From here on he can do enumeration and mount other attacks.

</details>

---
*Analysed by Claude on 2026-05-24*
