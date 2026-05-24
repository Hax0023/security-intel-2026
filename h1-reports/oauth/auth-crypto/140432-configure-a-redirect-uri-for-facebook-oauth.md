# configure a redirect URI for Facebook OAuth

## Metadata
- **Source:** HackerOne
- **Report:** 140432 | https://hackerone.com/reports/140432
- **Submitted:** 2016-05-23
- **Reporter:** paulos__
- **Program:** Unknown
- **Bounty:** $10
- **Severity:** medium
- **Vuln:** Improper Authentication - Generic
- **CVEs:** None
- **Category:** auth-crypto

## Summary
Hey,

Its me again. since the Login with Facebook doesnt have a dedicated directory like gratipay.com/facebook/callback it is possible to still steal access tokens.

https://www.facebook.com/dialog/oauth?response_type=code&client_id=144124902390407&redirect_uri=https://gratipay.com/~attacka/&scope=public_profile%2Cemail%2Cuser_friends&state=mjemgKNb0s24lbEqBcyVqDEVNoYDYs

As you can see it will se

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

Hey,

Its me again. since the Login with Facebook doesnt have a dedicated directory like gratipay.com/facebook/callback it is possible to still steal access tokens.

https://www.facebook.com/dialog/oauth?response_type=code&client_id=144124902390407&redirect_uri=https://gratipay.com/~attacka/&scope=public_profile%2Cemail%2Cuser_friends&state=mjemgKNb0s24lbEqBcyVqDEVNoYDYs

As you can see it will send the token to my profile (/~attacka) and my profile points to example.com, if the user clicks on that link the referrer header will send tokenz (obviously lol)

gratipay also imports pictures from 3rd parties, forexample my img src is from ls.googleusercontent.com which means it will also leak the access_tokens to there.

Fix: add the redirect uri like: https://www.gratipay.com/facebook/callback so users have no way to tamper with it.

Thanks,
P

</details>

---
*Analysed by Claude on 2026-05-24*
