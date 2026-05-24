# SQLi in LASCO CME Query

## Metadata
- **Source:** HackerOne
- **Report:** 186367 | https://hackerone.com/reports/186367
- **Submitted:** 2016-11-29
- **Reporter:** 0daystolive
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** high
- **Vuln:** SQL Injection
- **CVEs:** None
- **Category:** web-api

## Summary
**Summary:**
There is sqli in the form █████████ on the "CME DateTime" parameter.

I'm also fairly sure ████████ has similar SQLis but its somehow protected by a WAF.

**Description:**

## Impact
The impact is probably quite low but I have not checked to see what other data is accessible via the sqli (loadfile, other databases etc. )

## Step-by-step Reproduction Instructions

1.  Go to ████████. 

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

**Summary:**
There is sqli in the form █████████ on the "CME DateTime" parameter.

I'm also fairly sure ████████ has similar SQLis but its somehow protected by a WAF.

**Description:**

## Impact
The impact is probably quite low but I have not checked to see what other data is accessible via the sqli (loadfile, other databases etc. )

## Step-by-step Reproduction Instructions

1.  Go to ████████. Enter ```' and 1 or 1 GROUP BY CONCAT_WS(0x3a,VERSION(),FLOOR(RAND(0)*2)) HAVING MIN(0) OR 1 -- -``` in CME DateTime field
3. It will print out the MySQL server version

</details>

---
*Analysed by Claude on 2026-05-24*
