# Missing Server Side Validation of CSRF Middleware Token in Change Password Request

## Metadata
- **Source:** HackerOne
- **Report:** 120143 | https://hackerone.com/reports/120143
- **Submitted:** 2016-03-02
- **Reporter:** itly
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-Site Request Forgery (CSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
Hello Team,

I have found that CSRF Middleware Token is not getting validated at server side in CHANGE PASSWORD request. This request even works without csrfmiddlewaretoken.

Steps to Reproduce:

1. Login to your Veris View Account.
2. Go to Settings.
3. Change your password.
4. Submit the form.
5. Intercept this request in burp suite.
6. Remove csrfmiddlewaretoken parameter from the request.
7. F

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

I have found that CSRF Middleware Token is not getting validated at server side in CHANGE PASSWORD request. This request even works without csrfmiddlewaretoken.

Steps to Reproduce:

1. Login to your Veris View Account.
2. Go to Settings.
3. Change your password.
4. Submit the form.
5. Intercept this request in burp suite.
6. Remove csrfmiddlewaretoken parameter from the request.
7. Forward the request.
8. You'll notice the success message as Password changed Successfully.

Proof of Concept: Please find it attached.

Do evaluate it and inform me accordingly.

Best Regards,

Hely H. Shah

</details>

---
*Analysed by Claude on 2026-05-24*
