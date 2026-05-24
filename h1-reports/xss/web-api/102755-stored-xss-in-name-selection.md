# Stored XSS in name selection

## Metadata
- **Source:** HackerOne
- **Report:** 102755 | https://hackerone.com/reports/102755
- **Submitted:** 2015-12-01
- **Reporter:** daveysec
- **Program:** Unknown
- **Bounty:** $100
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
You have a stored XSS vuln when you set your name in your account information.

to reproduce just set your name field to:
</script><script>alert('xss')</script>

and most pages on your account you will show XSS.



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

You have a stored XSS vuln when you set your name in your account information.

to reproduce just set your name field to:
</script><script>alert('xss')</script>

and most pages on your account you will show XSS.



</details>

---
*Analysed by Claude on 2026-05-24*
