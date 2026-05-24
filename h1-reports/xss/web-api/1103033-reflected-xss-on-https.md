# Reflected XSS on https://█████

## Metadata
- **Source:** HackerOne
- **Report:** 1103033 | https://hackerone.com/reports/1103033
- **Submitted:** 2021-02-14
- **Reporter:** ibring
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Cross-site Scripting (XSS) - Reflected
- **CVEs:** None
- **Category:** web-api

## Summary
#Summary:

Reflected xss can use to steal user information because it is coming from trusted website.
an user can easily trust it and attacker can easily steal user information

#Steps To Reproduce:

  1.  go to https://████?profile_id=%22%3E%3C/script%3E%3Cscript%3Ealert(%27xss%27)%3C/script%3E

2.    you will able to see xss


#Supporting Material/References:

screenshot

Thank you
@ibring
Impac

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

#Summary:

Reflected xss can use to steal user information because it is coming from trusted website.
an user can easily trust it and attacker can easily steal user information

#Steps To Reproduce:

  1.  go to https://████?profile_id=%22%3E%3C/script%3E%3Cscript%3Ealert(%27xss%27)%3C/script%3E

2.    you will able to see xss


#Supporting Material/References:

screenshot

Thank you
@ibring
Impact

## Impact

attacker can steal user information via xss

## System Host(s)
█████

## Affected Product(s) and Version(s)


## CVE Numbers


## Steps to Reproduce
#Steps To Reproduce:

  1.  go to https://█████████?profile_id=%22%3E%3C/script%3E%3Cscript%3Ealert(%27xss%27)%3C/script%3E

2.    you will able to see xss

## Suggested Mitigation/Remediation Actions
validate user input don't allow execute special character in source code



</details>

---
*Analysed by Claude on 2026-05-24*
