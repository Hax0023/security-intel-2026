# Self XSS at translation page through Editor Link at demo.weblate.org

## Metadata
- **Source:** HackerOne
- **Report:** 223692 | https://hackerone.com/reports/223692
- **Submitted:** 2017-04-25
- **Reporter:** csanuragjain
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** low
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
User input is not sanitized properly at Editor link causing self xss.

**Steps to reproduce**
1) Navigate to https://demo.weblate.org/accounts/profile/#preferences
2) Provide Editor link as javaScript:alert(document.cookie);//confirm(1); and click on Save
3) Navigate to English Translation page of the project at https://demo.weblate.org/translate/hello/master/en_GB/?type=all
4) Click on the main.c

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

User input is not sanitized properly at Editor link causing self xss.

**Steps to reproduce**
1) Navigate to https://demo.weblate.org/accounts/profile/#preferences
2) Provide Editor link as javaScript:alert(document.cookie);//confirm(1); and click on Save
3) Navigate to English Translation page of the project at https://demo.weblate.org/translate/hello/master/en_GB/?type=all
4) Click on the main.c under Source Information
5) Self XSS executes showing user cookie

Mitigation:
Proper server side filtering of user input

</details>

---
*Analysed by Claude on 2026-05-24*
