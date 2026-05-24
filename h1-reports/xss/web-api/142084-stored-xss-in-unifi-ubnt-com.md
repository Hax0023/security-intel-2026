# Stored XSS in unifi.ubnt.com

## Metadata
- **Source:** HackerOne
- **Report:** 142084 | https://hackerone.com/reports/142084
- **Submitted:** 2016-05-30
- **Reporter:** b7882330c6060c6b277c5a1
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
Dear @ubnt-matt,

I've found a stored xss in unifi.ubnt.com

##Step to reproduce :##
```
Step 1: Login to unifi.ubnt.com
Step 2: Connect latest unifi controller with unifi.ubnt.com via cloud access.
Step 3: Create site with any name in that controller.
Step 4: Click on launch site in unifi.ubnt.com then you will again redirect to unifi.ubnt.com with controls.
Step 5: Create Network with xss payloa

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

Dear @ubnt-matt,

I've found a stored xss in unifi.ubnt.com

##Step to reproduce :##
```
Step 1: Login to unifi.ubnt.com
Step 2: Connect latest unifi controller with unifi.ubnt.com via cloud access.
Step 3: Create site with any name in that controller.
Step 4: Click on launch site in unifi.ubnt.com then you will again redirect to unifi.ubnt.com with controls.
Step 5: Create Network with xss payload "><img src=x onerror=prompt(document.cookie)>
Step 6: XSS will execute.
```

**Note : ** force WebRTC should we enable.

I've attached screenshot of the same.
let me know if you need more info.

Best Regard
Shubham

</details>

---
*Analysed by Claude on 2026-05-24*
