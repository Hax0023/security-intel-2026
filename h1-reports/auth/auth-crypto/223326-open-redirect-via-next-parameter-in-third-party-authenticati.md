# Open Redirect via "next" parameter in third-party authentication

## Metadata
- **Source:** HackerOne
- **Report:** 223326 | https://hackerone.com/reports/223326
- **Submitted:** 2017-04-24
- **Reporter:** ysx
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Open Redirect
- **CVEs:** None
- **Category:** auth-crypto

## Summary
Hi,

It is currently possible to execute an open redirection attack via the `next` parameter with the inclusion of a triple-slash prefix.

## Proof of Concept
### Redirect URL
```
https://demo.weblate.org/accounts/login/github/?next=///google.com
```

After authenticating, the user will be immediately redirected to the attacker-specified target.  I believe this affects all third-party authenticati

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

It is currently possible to execute an open redirection attack via the `next` parameter with the inclusion of a triple-slash prefix.

## Proof of Concept
### Redirect URL
```
https://demo.weblate.org/accounts/login/github/?next=///google.com
```

After authenticating, the user will be immediately redirected to the attacker-specified target.  I believe this affects all third-party authentication providers on the Weblate platform.

Please let me know if you require any additional details regarding this vulnerability.

Thanks!

</details>

---
*Analysed by Claude on 2026-05-24*
