# open authentication bug

## Metadata
- **Source:** HackerOne
- **Report:** 48065 | https://hackerone.com/reports/48065
- **Submitted:** 2015-02-18
- **Reporter:** ckmk44
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Improper Authentication - Generic
- **CVEs:** None
- **Category:** auth-crypto

## Summary
Hi,
If developer registers one of the three url's with out http protocol (ex:example.com) in oauth registration then he would be redirected to www.coinbase.comexample.com.This makes the user to redirect to another site than the real application.Attacker could take advantage of this and steal the token using that site as a medium.
Type:Oauth
impact:high
authentication:yes
this works if develop

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
If developer registers one of the three url's with out http protocol (ex:example.com) in oauth registration then he would be redirected to www.coinbase.comexample.com.This makes the user to redirect to another site than the real application.Attacker could take advantage of this and steal the token using that site as a medium.
Type:Oauth
impact:high
authentication:yes
this works if developer does a mistake but the vulnerability lies in the coinbase oauth.
Proof of concept:
https://www.coinbase.com/oauth/authorize?response_type=code&client_id=3616ab93541ef90540a0c991e113b22c1ccefa96996f70fcdc49a68d900cb761&redirect_uri=prashanthvarma.in/code.php&scope=user

Thank you,
prashanth varma 

</details>

---
*Analysed by Claude on 2026-05-24*
