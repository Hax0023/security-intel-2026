# SQL injection when configuring a database 

## Metadata
- **Source:** HackerOne
- **Report:** 983710 | https://hackerone.com/reports/983710
- **Submitted:** 2020-09-16
- **Reporter:** solov9ev
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** low
- **Vuln:** SQL Injection
- **CVEs:** None
- **Category:** uncategorised

## Summary
## Summary:
I found a SQL Injection in the form of a system install (Database configuration)

## Steps To Reproduce:
- Run command: `git clone https://github.com/ImpressCMS/impresscms.git`
- Stop at a menu item: `Database configuration`
- In the `Database name` field, insert the following exploit:


```sql
 impresscms`;create database `vuln
```

{F990522}

-  Submit the form

{F990524}

- Two data

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

## Summary:
I found a SQL Injection in the form of a system install (Database configuration)

## Steps To Reproduce:
- Run command: `git clone https://github.com/ImpressCMS/impresscms.git`
- Stop at a menu item: `Database configuration`
- In the `Database name` field, insert the following exploit:


```sql
 impresscms`;create database `vuln
```

{F990522}

-  Submit the form

{F990524}

- Two databases (`impresscms`, `vuln`) created successfully. POC is attached to the report

## Supporting Material/References:
[PHP addslashes](https://www.php.net/manual/en/function.addslashes.php) - single quote ('), double quote ("), backslash, NUL (the NUL byte), but **Backtick is not escaped!**

## Impact

Executing arbitrary code on a database

</details>

---
*Analysed by Claude on 2026-05-24*
