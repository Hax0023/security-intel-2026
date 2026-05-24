# Login CSRF using Twitter oauth

## Metadata
- **Source:** HackerOne
- **Report:** 13555 | https://hackerone.com/reports/13555
- **Submitted:** 2014-05-27
- **Reporter:** robin
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-Site Request Forgery (CSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
this bug allows a user to be logged in as the attacker. The main reason is that no state is maintained in the authentication flow. Although the Twitter flow still uses OAuth 1.0A, which has no state parameter as in OAuth 2, it is still possible to prevent this type of attack by setting an additional parameter in the oauth_callback value.

An attacker could exploit this bug as follows:

Attacke

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

this bug allows a user to be logged in as the attacker. The main reason is that no state is maintained in the authentication flow. Although the Twitter flow still uses OAuth 1.0A, which has no state parameter as in OAuth 2, it is still possible to prevent this type of attack by setting an additional parameter in the oauth_callback value.

An attacker could exploit this bug as follows:

Attacker initiates Twitter OAuth process with Phabricator
Attacker allows access to Phabricator app
Attacker records and drops redirection to Phabricator (in order not to consume token)
Attacker directs victim to /auth/login/twitter:twitter.com/?oauth_token={attacker_token}&oauth_verifier={attacker_verifier}
Victim is now logged in as attacker
To mitigate this vulnerability, either maintain state in the authentication flow by adding a parameter in the callback value or, as Twitter seems to support OAuth 2, use that instead

</details>

---
*Analysed by Claude on 2026-05-24*
