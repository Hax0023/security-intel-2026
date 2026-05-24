# CSRF protection on OIDC login is broken

## Metadata
- **Source:** HackerOne
- **Report:** 1878381 | https://hackerone.com/reports/1878381
- **Submitted:** 2023-02-18
- **Reporter:** mikaelgundersen
- **Program:** Unknown
- **Bounty:** $500
- **Severity:** medium
- **Vuln:** Cross-Site Request Forgery (CSRF)
- **CVEs:** CVE-2023-28848
- **Category:** web-api

## Summary
To protect against CSRF the "state" is used in the OIDC flow. On callback this code is verified against the code stored in the session for that user. However in case the token does not match a JSON response is provided that includes the expected state. Thus making it trivial for the attacker to obtain the correct state.

Judging from the code it clearly seem to be debug leftovers https://github.co

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

To protect against CSRF the "state" is used in the OIDC flow. On callback this code is verified against the code stored in the session for that user. However in case the token does not match a JSON response is provided that includes the expected state. Thus making it trivial for the attacker to obtain the correct state.

Judging from the code it clearly seem to be debug leftovers https://github.com/nextcloud/user_oidc/blob/main/lib/Controller/LoginController.php#L336-L344

Fixing the todo there should mitigate the issue and ensure the OIDC flow is more secure.


I didn't test ID4ME. But the code is almost identical. So I assume the bug is also the same https://github.com/nextcloud/user_oidc/blob/main/lib/Controller/Id4meController.php#L175-L181

## Impact

The CSRF protection provided with the state is practically useless now.

</details>

---
*Analysed by Claude on 2026-05-24*
