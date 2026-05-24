# MSSQL injection via param Customwho in https://█████/News/Transcripts/Search/Sort/ and WAF bypass

## Metadata
- **Source:** HackerOne
- **Report:** 577612 | https://hackerone.com/reports/577612
- **Submitted:** 2019-05-11
- **Reporter:** bohdansec
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** high
- **Vuln:** SQL Injection
- **CVEs:** None
- **Category:** uncategorised

## Summary
**Summary:**

MSSQL injection via param `Customwho` in https://███████/News/Transcripts/Search/Sort/

**Description:**

MSSQL injection via param `Customwho` in https://██████████/News/Transcripts/Search/Sort/

There is WAF, but we can make bypass and via global variable `@@LANGID` we can know that the base is used here - MSSQL

## Impact

Critical

## Step-by-step Reproduction Instructions

Via g

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

MSSQL injection via param `Customwho` in https://███████/News/Transcripts/Search/Sort/

**Description:**

MSSQL injection via param `Customwho` in https://██████████/News/Transcripts/Search/Sort/

There is WAF, but we can make bypass and via global variable `@@LANGID` we can know that the base is used here - MSSQL

## Impact

Critical

## Step-by-step Reproduction Instructions

Via global variable `@@LANGID` we can find out that here is MSSQL database. ████

https://█████/News/Transcripts/Search/Sort/?Customwho=31002/**/|/**/@@LANGID

And if use a non-existing global variable, then we get an error. ██████

https://██████████/News/Transcripts/Search/Sort/?Customwho=31002/**/|/**/@@nonexisting

## Suggested Mitigation/Remediation Actions

Using prepared statement

## Impact

We can read and do other manipulations in the database. We can also try to make RCE

</details>

---
*Analysed by Claude on 2026-05-24*
