# Critical - Insecure Direct Object Reference - Deleting any member of any organization remotely

## Metadata
- **Source:** HackerOne
- **Report:** 120115 | https://hackerone.com/reports/120115
- **Submitted:** 2016-03-02
- **Reporter:** itly
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Privilege Escalation
- **CVEs:** None
- **Category:** web-api

## Summary
Hello Team,

I have found an extremely critical issue with the help of which an attacker can delete any member of any organization. The vulnerability is Insecure Direct Object Reference(IDOR) which leads to privilege escalation as an attacker can perform such a critical attack from his own account.

Vulnerable URL: DELETE /api/v1/org-member/4/[MEMBER_ID]/

On changing the member id, application al

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

I have found an extremely critical issue with the help of which an attacker can delete any member of any organization. The vulnerability is Insecure Direct Object Reference(IDOR) which leads to privilege escalation as an attacker can perform such a critical attack from his own account.

Vulnerable URL: DELETE /api/v1/org-member/4/[MEMBER_ID]/

On changing the member id, application allows an attacker to delete that member. I tried using my 2 accounts and got success in the same.

Steps to Reproduce:'

1. Login to your Veris View Portal.
2. Go to Member Book.
3. Set up Burp Suite to intercept the request OR simply edit the member id from browser's Inspect Element feature.
4. Delete a Member and intercept the request.
5. Replace the member id with some other member of other organization.
6. Forward the request.
7. Check in the other organization. Member would be deleted.

Proof of Concept: Please find the attached screenshots.

Do evaluate it and inform me accordingly.

Best Regards,

Hely H. Shah

</details>

---
*Analysed by Claude on 2026-05-24*
