# XSS in Bootbox

## Metadata
- **Source:** HackerOne
- **Report:** 508446 | https://hackerone.com/reports/508446
- **Submitted:** 2019-03-12
- **Reporter:** yonjah
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
Hi.  
  
Sorry for taking the time with this report.  
  
This is already publicly disclosed issue at -[https://github.com/makeusabrew/bootbox/issues/661](https://github.com/makeusabrew/bootbox/issues/661)  
  
In essence all dialogs of bootbox vulnurable to XSS injections ( bootbox.alert("\<script\>alert(1);\</script\>"); )  

This is apparently a feature to allow injecting HTML in messages but i

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

Hi.  
  
Sorry for taking the time with this report.  
  
This is already publicly disclosed issue at -[https://github.com/makeusabrew/bootbox/issues/661](https://github.com/makeusabrew/bootbox/issues/661)  
  
In essence all dialogs of bootbox vulnurable to XSS injections ( bootbox.alert("\<script\>alert(1);\</script\>"); )  

This is apparently a feature to allow injecting HTML in messages but it is not very clear from the documentation.  
Even though this issue has been reported for a while no changes were made to fix this issue or even update the documentation

Kind Regards,  
Yoni

## Impact

Websites using bootbox to display messages containing user input are vulnerable to XSS

</details>

---
*Analysed by Claude on 2026-05-24*
