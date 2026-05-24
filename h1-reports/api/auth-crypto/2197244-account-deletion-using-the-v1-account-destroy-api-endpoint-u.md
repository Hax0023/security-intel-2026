# Account deletion using the /v1/account/destroy API endpoint using account password without 2FA verification

## Metadata
- **Source:** HackerOne
- **Report:** 2197244 | https://hackerone.com/reports/2197244
- **Submitted:** 2023-10-07
- **Reporter:** erdy
- **Program:** Unknown
- **Bounty:** $1,000
- **Severity:** medium
- **Vuln:** Improper Authentication - Generic
- **CVEs:** None
- **Category:** auth-crypto

## Summary
## Summary:
The account deletion endpoint at `POST /v1/account/destroy` does not check for 2FA and doesn't require an authorization header. Therefore, an unauthenticated attacker who knows the password of a user can delete their account without the need of 2FA.

## Steps To Reproduce:

  1. Send a POST request to https://api-accounts.stage.mozaws.net/v1/account/destroy with the following body (do 

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

## Summary:
The account deletion endpoint at `POST /v1/account/destroy` does not check for 2FA and doesn't require an authorization header. Therefore, an unauthenticated attacker who knows the password of a user can delete their account without the need of 2FA.

## Steps To Reproduce:

  1. Send a POST request to https://api-accounts.stage.mozaws.net/v1/account/destroy with the following body (do not include an Authorization header, if it is included and doesn't match the e-mail in the body, the request will fail):
```
{"email":"<email>","authPW":"<authPW>"}
```
The authPW can be calculated by the attacker since it is created client-side and the source code is [publicly available](https://github.com/mozilla/fxa/blob/fd716ec3f3461d22b847f337f6b1e899d671ee0d/packages/fxa-auth-client/lib/crypto.ts#L18).

Please refer to {F2756126} to calculate the authPW.

## Supporting Material/References:

An example of a successful account deletion:
{F2756132}

## Impact

## Summary:
An unauthenticated attacker can delete Firefox accounts of other users without needing 2FA, if the attacker knows their password.

</details>

---
*Analysed by Claude on 2026-05-24*
