# Stored XSS templates -> 'call for action' feature

## Metadata
- **Source:** HackerOne
- **Report:** 237927 | https://hackerone.com/reports/237927
- **Submitted:** 2017-06-08
- **Reporter:** r0h17
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** high
- **Vuln:** xss
- **CVEs:** None
- **Category:** web-api

## Summary
Hi Jeff,

Reporting the Stored XSS in template section on 'call for action' button. (Already discussed in mail)
1] Login to Mixmax and navigate to template section
2] Click on enhance and select call for action button
3] Enter anything in button text and in URL enter XSS payload (javascript:alert(document.cookie))
4] Insert the button and click it to execute XSS.

Impact : XSS can be stored in tem

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

Hi Jeff,

Reporting the Stored XSS in template section on 'call for action' button. (Already discussed in mail)
1] Login to Mixmax and navigate to template section
2] Click on enhance and select call for action button
3] Enter anything in button text and in URL enter XSS payload (javascript:alert(document.cookie))
4] Insert the button and click it to execute XSS.

Impact : XSS can be stored in template and when Team manager/admin uses that template and clicks the button , our XSS executes 

Thank you

</details>

---
*Analysed by Claude on 2026-05-24*
