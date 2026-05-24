# Multiple Stored XSS

## Metadata
- **Source:** HackerOne
- **Report:** 120324 | https://hackerone.com/reports/120324
- **Submitted:** 2016-03-03
- **Reporter:** itly
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
Hello Team,

I have found multiple vulnerable fields which accepts malicious javascript inputs and reflects on another form which fails to sanitize the malicious javascript input.

Vulnerable Input Form: Edit Group Details

Reflects where: View Rule Book

Payload used: 1) <img src=x onerror=alert(document.domain)>

                         2) <img src=x onerror=alert(document.cookie)>

Browsers us

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

Hello Team,

I have found multiple vulnerable fields which accepts malicious javascript inputs and reflects on another form which fails to sanitize the malicious javascript input.

Vulnerable Input Form: Edit Group Details

Reflects where: View Rule Book

Payload used: 1) <img src=x onerror=alert(document.domain)>

                         2) <img src=x onerror=alert(document.cookie)>

Browsers used: Mozilla Firefox and Google Chrome (Latest Version)

Steps to Reproduce:

1. Go to Edit Group Details Form.
2. Inject the above mentioned payload in both the input fields as shown in screenshot.
3. Submit and Save it.
4. Go to Rulebook and View it.
5. Tadaa! XSS Triggers. 

Proof of Concept: Please find the attached screenshots.

Do evaluate it and inform me accordingly.

Best Regards,

Hely H. Shah 

</details>

---
*Analysed by Claude on 2026-05-24*
