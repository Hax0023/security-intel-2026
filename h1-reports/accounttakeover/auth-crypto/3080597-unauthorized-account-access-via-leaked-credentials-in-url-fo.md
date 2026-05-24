# Unauthorized Account Access via Leaked Credentials in URL Format (Account Takeover )

## Metadata
- **Source:** HackerOne
- **Report:** 3080597 | https://hackerone.com/reports/3080597
- **Submitted:** 2025-04-07
- **Reporter:** firec4t
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** critical
- **Vuln:** Cleartext Storage of Sensitive Information
- **CVEs:** None
- **Category:** auth-crypto

## Summary
I discovered a critical vulnerability that allows attackers to access user accounts on khanAcademy.com using credentials publicly available on VirusTotal., an attacker can directly authenticate into a user’s account without any secondary verification or alert to the user.
i have reported a similar issue , here's the report ( 2981324 ) 

this time the email and password of the victim is archived in

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

I discovered a critical vulnerability that allows attackers to access user accounts on khanAcademy.com using credentials publicly available on VirusTotal., an attacker can directly authenticate into a user’s account without any secondary verification or alert to the user.
i have reported a similar issue , here's the report ( 2981324 ) 

this time the email and password of the victim is archived in clear text ( https://en.khanacademy.org/login,██████,,█████████,,,█████████,██████████,Personal )

by entering the mail ( ██████████ ) and password ( ███████ ) in the login , the attacker can easily perform account takeover

Please Enforce 2FA: Make two-factor authentication mandatory, especially for accounts with detected exposure.

## Impact

Full account takeover: Unauthorized access to user accounts with no user awareness.

Exposure of personal data: Private information such as learning progress, messages, and linked accounts may be compromised.

Potential financial or reputational damage: If linked to other services, this access may lead to wider exploitation.

</details>

---
*Analysed by Claude on 2026-05-24*
