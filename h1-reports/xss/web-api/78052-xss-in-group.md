# xss in group

## Metadata
- **Source:** HackerOne
- **Report:** 78052 | https://hackerone.com/reports/78052
- **Submitted:** 2015-07-23
- **Reporter:** ashishdhaduk
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
step:

payload : "><svg onload=prompt(document.domain) >

1.first create a new group.
2. now create new post,
3. now put payload in new topic and than click on add poll.
4. xss executed.


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

step:

payload : "><svg onload=prompt(document.domain) >

1.first create a new group.
2. now create new post,
3. now put payload in new topic and than click on add poll.
4. xss executed.


</details>

---
*Analysed by Claude on 2026-05-24*
