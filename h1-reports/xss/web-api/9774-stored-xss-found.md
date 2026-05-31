# Stored XSS Found

## Metadata
- **Source:** HackerOne
- **Report:** 9774 | https://hackerone.com/reports/9774
- **Submitted:** 2014-04-25
- **Reporter:** karshxz7593
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
The type of XSS Vulnerability I found on your website is a stored xss. after i connect my github account   and add a new integration then i chose my repositories then on the right side of that is a textfield that has a placeholder of  Branches (optional). then i put the following code on that textfield "><img src=x onerror=alert(document.domain);>  then i click save integration button. then after 

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

The type of XSS Vulnerability I found on your website is a stored xss. after i connect my github account   and add a new integration then i chose my repositories then on the right side of that is a textfield that has a placeholder of  Branches (optional). then i put the following code on that textfield "><img src=x onerror=alert(document.domain);>  then i click save integration button. then after that an alert box popup containing the domain of the site.

</details>

---
*Analysed by Claude on 2026-05-31*
