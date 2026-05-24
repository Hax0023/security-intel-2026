# Login CSRF using Twitter OAuth

## Metadata
- **Source:** HackerOne
- **Report:** 2228 | https://hackerone.com/reports/2228
- **Submitted:** 2014-02-23
- **Reporter:** mathias
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-Site Request Forgery (CSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
This bug is related to bug report [#774 (Log in a user to another account)](https://hackerone.com/reports/774) by @dawidczagan as this bug also allows a user to be logged in as the attacker. The main reason is that no state is maintained in the authentication flow. Although the Twitter flow still uses OAuth 1.0A, which has no `state` parameter as in OAuth 2, it is still possible to prevent this ty

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

This bug is related to bug report [#774 (Log in a user to another account)](https://hackerone.com/reports/774) by @dawidczagan as this bug also allows a user to be logged in as the attacker. The main reason is that no state is maintained in the authentication flow. Although the Twitter flow still uses OAuth 1.0A, which has no `state` parameter as in OAuth 2, it is still possible to prevent this type of attack by setting an additional parameter in the `oauth_callback` value.

An attacker could exploit this bug as follows:

1. Attacker initiates Twitter OAuth process with Phabricator
2. Attacker allows access to Phabricator app
3. Attacker records and drops redirection to Phabricator (in order not to consume token)
4. Attacker directs victim to `/auth/login/twitter:twitter.com/?oauth_token={attacker_token}&oauth_verifier={attacker_verifier}`
5. Victim is now logged in as attacker

To mitigate this vulnerability, either maintain state in the authentication flow by adding a parameter in the callback value or, as Twitter seems to support OAuth 2, use that instead.

</details>

---
*Analysed by Claude on 2026-05-24*
