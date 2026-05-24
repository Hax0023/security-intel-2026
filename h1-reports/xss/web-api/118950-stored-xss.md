# Stored XSS 

## Metadata
- **Source:** HackerOne
- **Report:** 118950 | https://hackerone.com/reports/118950
- **Submitted:** 2016-02-26
- **Reporter:** itly
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
Hello,

I have found XSS on https://sandbox.veris.in/portal/members/

Steps to reproduce:

1.  Sign in your Veris account.
2. Go to Member Book -> Add new member.
3. Fill this payload <svg onload=alert(1)>  in "Name" and "Description" field.
4. Now visit  https://sandbox.veris.in/portal/members/ or go to groups->Add member from member book
5. Tadaa! XSS Triggers

Proof of Concept: Please find it a

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

Hello,

I have found XSS on https://sandbox.veris.in/portal/members/

Steps to reproduce:

1.  Sign in your Veris account.
2. Go to Member Book -> Add new member.
3. Fill this payload <svg onload=alert(1)>  in "Name" and "Description" field.
4. Now visit  https://sandbox.veris.in/portal/members/ or go to groups->Add member from member book
5. Tadaa! XSS Triggers

Proof of Concept: Please find it attached.

Do evaluate it and inform me accordingly.

Best Regards,

Hely H. Shah 
 

</details>

---
*Analysed by Claude on 2026-05-24*
