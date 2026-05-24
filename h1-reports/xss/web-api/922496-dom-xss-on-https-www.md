# DOM XSS on https://www.███████

## Metadata
- **Source:** HackerOne
- **Report:** 922496 | https://hackerone.com/reports/922496
- **Submitted:** 2020-07-13
- **Reporter:** gamer7112
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Cross-site Scripting (XSS) - DOM
- **CVEs:** None
- **Category:** web-api

## Summary
#Description
DOM XSS can be achieved due to missing sanitation  when setting the source of an iframe.

#POC
1. Visit https://www.████frame.html#javascript:alert(document.domain)
2. View alert

#Vulnerable Code
```javascript
function Load()
{
	str=document.location.hash,idx=str.indexOf('#')
	if(idx>=0) str=str.substr(1);
	if(str) PPTSld.location.replace(str);
}
```

## Impact

An attacker could exe

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

#Description
DOM XSS can be achieved due to missing sanitation  when setting the source of an iframe.

#POC
1. Visit https://www.████frame.html#javascript:alert(document.domain)
2. View alert

#Vulnerable Code
```javascript
function Load()
{
	str=document.location.hash,idx=str.indexOf('#')
	if(idx>=0) str=str.substr(1);
	if(str) PPTSld.location.replace(str);
}
```

## Impact

An attacker could execute arbitrary javascript on another user.

</details>

---
*Analysed by Claude on 2026-05-24*
