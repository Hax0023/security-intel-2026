# Stored xss in shop name @ lp.reverb.com

## Metadata
- **Source:** HackerOne
- **Report:** 329862 | https://hackerone.com/reports/329862
- **Submitted:** 2018-03-26
- **Reporter:** sandeep_hodkasia
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** high
- **Vuln:** Cross-site Scripting (XSS) - Stored
- **CVEs:** None
- **Category:** web-api

## Summary
hello team,

There is a stored xss in lp.reverb.com.
Attacker can inject malicious script into server while adding shop name as `lll"></script><script>alert('xss');</script>`.
Exploit: https://lp.reverb.com/shops/faniyos-boutique/listings

Steps to reproduce:
1. Navogate to https://reverb.com/my/lp_shop/edit
2. Change your lp shop name to this: lll"></script><script>alert('xss')</script>
3. Save t

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

hello team,

There is a stored xss in lp.reverb.com.
Attacker can inject malicious script into server while adding shop name as `lll"></script><script>alert('xss');</script>`.
Exploit: https://lp.reverb.com/shops/faniyos-boutique/listings

Steps to reproduce:
1. Navogate to https://reverb.com/my/lp_shop/edit
2. Change your lp shop name to this: lll"></script><script>alert('xss')</script>
3. Save the changes.
4. View your lp shop.

Fix:
Sanitise the given input in the backend and encode the special characters.

Thanks,
Sandeep

## Impact

Attack can save malicious script directly into the server. Malicious script can be used to gain users session.

The hacker selected the **Cross-site Scripting (XSS) - Stored** weakness. This vulnerability type requires contextual information from the hacker. They provided the following answers:

**URL**
https://lp.reverb.com/shops/faniyos-boutique/listings

**Verified**
Yes



</details>

---
*Analysed by Claude on 2026-05-24*
