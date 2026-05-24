# Authenticated but unauthorized users may enumerate Application names via the API

## Metadata
- **Source:** HackerOne
- **Report:** 1916583 | https://hackerone.com/reports/1916583
- **Submitted:** 2023-03-24
- **Reporter:** bean-zhang
- **Program:** Unknown
- **Bounty:** $2,400
- **Severity:** medium
- **Vuln:** Information Exposure Through an Error Message
- **CVEs:** CVE-2022-41354
- **Category:** uncategorised

## Summary
All versions of Argo CD starting with v0.5.0 are vulnerable to an information disclosure bug allowing unauthorized users to enumerate application names by inspecting API error messages. 

STEPS:
1. Login argocd with a user who has not application module's priviledge.
2. The user request 'api/v1/application/**/logs' restful api to download a log file.
3. The log file's content lead a information di

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

All versions of Argo CD starting with v0.5.0 are vulnerable to an information disclosure bug allowing unauthorized users to enumerate application names by inspecting API error messages. 

STEPS:
1. Login argocd with a user who has not application module's priviledge.
2. The user request 'api/v1/application/**/logs' restful api to download a log file.
3. The log file's content lead a information disclosure bug, which allowing unauthorized users to enumerate application names by inspecting API error messages. The error messages like 'error gettingg applicaiton by name: ** not found'.

## Impact

An attacker could use the discovered application names as the starting point of another attack. For example, the attacker might use their knowledge of an application name to convince an administrator to grant higher privileges (social engineering).

</details>

---
*Analysed by Claude on 2026-05-24*
