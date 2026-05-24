# WordPress DB Class, bad implementation of prepare method guides to sqli and information disclosure

## Metadata
- **Source:** HackerOne
- **Report:** 179920 | https://hackerone.com/reports/179920
- **Submitted:** 2016-11-03
- **Reporter:** b258ea62bf297b02afa9854
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** critical
- **Vuln:** SQL Injection
- **CVEs:** None
- **Category:** web-api

## Summary
Issue 1: Method checks if first argument is an array and if it is, it avoids the rest of the arguments and uses the first argument array values as input.

Issue 2: When input query has %s in it, then it quote and this guides to sql injection in case query that need to be prepared have quoted user controlled input in it.  

This leaves all wordpress plugins/ themes potentially vulnerable on this tw

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

Issue 1: Method checks if first argument is an array and if it is, it avoids the rest of the arguments and uses the first argument array values as input.

Issue 2: When input query has %s in it, then it quote and this guides to sql injection in case query that need to be prepared have quoted user controlled input in it.  

This leaves all wordpress plugins/ themes potentially vulnerable on this two types of attack. As PoC sqli in bbpress wp plugin and core wp function is shown.

PoC: 
1. There is SQLi in bbpress in case anonymous posting is allowed. ( check  bbpress-sqli.png)
2.  Demo for the Issue 1 and Issue 2 for the prepare method
3. Wordpress core function delete_metadata is vulnerable to sqli in case delete all e.g. last argument is true and meta value has value e.g. is user supplied / controlled.

</details>

---
*Analysed by Claude on 2026-05-24*
