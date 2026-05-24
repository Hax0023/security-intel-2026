# Administration Authentication Bypass on https://█████

## Metadata
- **Source:** HackerOne
- **Report:** 1146600 | https://hackerone.com/reports/1146600
- **Submitted:** 2021-04-02
- **Reporter:** fiveguyslover
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** critical
- **Vuln:** Improper Authentication - Generic
- **CVEs:** None
- **Category:** auth-crypto

## Summary
Hi there
I found a way to connect to an administration space on your website https://██████████

#how to reproduce ?

1) - go to this link : https://███/██████████
2) - create a html file with : 
```html
<form action="https://████████/██████████" method="post">
    <input type="hidden" name="█████" value="">
    <input type="hidden" name="█████" value="1">
    <input type="submit">
</form>
```
3) 

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

Hi there
I found a way to connect to an administration space on your website https://██████████

#how to reproduce ?

1) - go to this link : https://███/██████████
2) - create a html file with : 
```html
<form action="https://████████/██████████" method="post">
    <input type="hidden" name="█████" value="">
    <input type="hidden" name="█████" value="1">
    <input type="submit">
</form>
```
3) - launch the file, click on the button and return to the page https://███████/█████
4) - refresh the page and you have access to the administration

POC : 

██████████

if you need more information, contact me

best regards,
fiveguyslover

## Impact

access to sensitive data and the ability to modify information.

## System Host(s)
█████

## Affected Product(s) and Version(s)


## CVE Numbers


## Steps to Reproduce
1) - go to this link : https://█████/███████
2) - create a html file with : 
```html
<form action="https://█████/███" method="post">
    <input type="hidden" name="███" value="">
    <input type="hidden" name="████" value="1">
    <input type="submit">
</form>
```
3) - launch the file, click on the button and return to the page https://██████/█████
4) - refresh the page and you have access to the administration

## Suggested Mitigation/Remediation Actions




</details>

---
*Analysed by Claude on 2026-05-24*
