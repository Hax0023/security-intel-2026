# CSRF on add comment section

## Metadata
- **Source:** HackerOne
- **Report:** 2638 | https://hackerone.com/reports/2638
- **Submitted:** 2014-03-01
- **Reporter:** anandpingsafe
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-Site Request Forgery (CSRF)
- **CVEs:** None
- **Category:** web-api

## Summary


Hi,

Steps to repro:

1) Go to this link https://sehacure.slack.com/help/requests/237956

2) The malicious guy should now the request number and the username.

3) Open Tamper data using tamper data firefox addon,Fill the reply in the form.

4) Submit the request.You will see there are no anti-csrf token in the request.

Impact:

Submit a lot of fake response from the victim accou

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

Steps to repro:

1) Go to this link https://sehacure.slack.com/help/requests/237956

2) The malicious guy should now the request number and the username.

3) Open Tamper data using tamper data firefox addon,Fill the reply in the form.

4) Submit the request.You will see there are no anti-csrf token in the request.

Impact:

Submit a lot of fake response from the victim account.

Please have a look.

Best,
Anand

</details>

---
*Analysed by Claude on 2026-05-24*
