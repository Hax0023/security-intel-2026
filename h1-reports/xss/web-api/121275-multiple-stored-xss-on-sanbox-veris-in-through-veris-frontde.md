# Multiple Stored XSS on Sanbox.veris.in through Veris Frontdesk Android App

## Metadata
- **Source:** HackerOne
- **Report:** 121275 | https://hackerone.com/reports/121275
- **Submitted:** 2016-03-08
- **Reporter:** itly
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
Hello Team,

I have found multiple cross site scripting vulnerabilities on sanbox.veris.in due to the malicious input injected through veris frontdesk android app.

Vulnerable App : Veris Frontdesk Android App

Vulnerable Input Fields: 1) Who do you wish to meet?
                                2) Additional Information

Payload used: <img src=x onerror=alert(3)> and <img src=x onerror=alert(4)>



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

I have found multiple cross site scripting vulnerabilities on sanbox.veris.in due to the malicious input injected through veris frontdesk android app.

Vulnerable App : Veris Frontdesk Android App

Vulnerable Input Fields: 1) Who do you wish to meet?
                                2) Additional Information

Payload used: <img src=x onerror=alert(3)> and <img src=x onerror=alert(4)>

Reflects where: https://sandbox.veris.in/portal/visitor-log/

Steps to Reproduce:

1. Open Veris Front Desk App.
2. Go to Check In.
3. Enter the required details like first name, last name and phone number.
4. Proceed to Next.
5. Inject the above mentioned payload in vulnerable input fields.
6. Submit it and Check In.
7. Login to your account on sandbox.veris.in
8. Go to https://sandbox.veris.in/portal/visitor-log/
9. Tadaa! XSS Triggers.

Proof of Concept: Please find the attached screenshots.

Do evaluate it and inform me accordingly.

Best Regards,

Hely H. Shah



</details>

---
*Analysed by Claude on 2026-05-24*
