# Two factor authentication bypass

## Metadata
- **Source:** HackerOne
- **Report:** 2463279 | https://hackerone.com/reports/2463279
- **Submitted:** 2024-04-15
- **Reporter:** pranshux0x_
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** auth
- **CVEs:** None
- **Category:** auth-crypto

## Summary
**Summary:**

Two factor authentication bypass means. We have access to victim email and password. But we don't have access to 2fa code. So somehow we have to bypass 2fa code requirement.
so what I do here.
I had access to victim email that is used in his hackerone account. 
Victim also deactivate his account
I find out that when  user deactivate his account. Then reset his password and login agai

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

**Summary:**

Two factor authentication bypass means. We have access to victim email and password. But we don't have access to 2fa code. So somehow we have to bypass 2fa code requirement.
so what I do here.
I had access to victim email that is used in his hackerone account. 
Victim also deactivate his account
I find out that when  user deactivate his account. Then reset his password and login again ,  2fa removed. 

**Description:**

### Steps To Reproduce

#### As a victim
- Login to your hackerone account
- Turn on your two factor authentication. 
- Deactivate your account

#### As an attacker
- You have access to victim email
- Forgot victim password on hackerone, because you have access to victim email you can do this easily.
- Now login with new password on hackerone , you will see 2fa removed completely.

## Impact

Impact is quite high two factor authentication bypass.

</details>

---
*Analysed by Claude on 2026-05-24*
