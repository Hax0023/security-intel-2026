# Stored XSS in wis.pr

## Metadata
- **Source:** HackerOne
- **Report:** 149571 | https://hackerone.com/reports/149571
- **Submitted:** 2016-07-06
- **Reporter:** huntingforbugs
- **Program:** Unknown
- **Bounty:** $100
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
Hi,

I detected a Stored XSS in wis.pr. These are the steps to reproduce the bug:

1. Create a new group named: Test>"<script>alert('test');</script>
2. Copy the sharing URL (http://wis.pr/*****).
3. Open this URL in a browser.

Please find the attached screenshots.

Fix: Sanitize the output in twitter:description meta. Please find attached the screenshot named "fix.jpg".

Don't hesitate to contac

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

Hi,

I detected a Stored XSS in wis.pr. These are the steps to reproduce the bug:

1. Create a new group named: Test>"<script>alert('test');</script>
2. Copy the sharing URL (http://wis.pr/*****).
3. Open this URL in a browser.

Please find the attached screenshots.

Fix: Sanitize the output in twitter:description meta. Please find attached the screenshot named "fix.jpg".

Don't hesitate to contact me if you need further details.



</details>

---
*Analysed by Claude on 2026-05-24*
