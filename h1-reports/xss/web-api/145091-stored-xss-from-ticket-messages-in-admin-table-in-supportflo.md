# Stored XSS from ticket messages in admin table in SupportFlow

## Metadata
- **Source:** HackerOne
- **Report:** 145091 | https://hackerone.com/reports/145091
- **Submitted:** 2016-06-16
- **Reporter:** whitehatter
- **Program:** Unknown
- **Bounty:** $50
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
SupportFlow containers a stored XSS vulnerability in how it generates the admin table of tickets at _SupportFlow -> All Tickets_ (`/wp-admin/edit.php?post_type=sf_ticket`).

Any ticket can be created with an XSS payload like this:

```
<script>alert('XSS');</script>
```

When an admin goes to view the table of tickets, XSS is triggered, because the value is never escaped here:

https://github.com/

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

SupportFlow containers a stored XSS vulnerability in how it generates the admin table of tickets at _SupportFlow -> All Tickets_ (`/wp-admin/edit.php?post_type=sf_ticket`).

Any ticket can be created with an XSS payload like this:

```
<script>alert('XSS');</script>
```

When an admin goes to view the table of tickets, XSS is triggered, because the value is never escaped here:

https://github.com/SupportFlow/supportflow/blob/71a6053848c523f7b50b61a1f3770013badc76c0/classes/class-supportflow-admin.php#L1175

I've attached a screenshot demonstrating the XSS payload - please let me know if there are any questions.

</details>

---
*Analysed by Claude on 2026-05-24*
