# Persistent Cross Site Scripting within the IRCCloud Pastebin 

## Metadata
- **Source:** HackerOne
- **Report:** 7121 | https://hackerone.com/reports/7121
- **Submitted:** 2014-04-11
- **Reporter:** mantis
- **Program:** Unknown
- **Bounty:** $500
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
The HTML within a paste does not get correctly sanitized after an initial new line. So the following code gets executed: \r\n<script>alert(1);</script> 

https://www.irccloud.com/pastebin/FADYQPrO

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

The HTML within a paste does not get correctly sanitized after an initial new line. So the following code gets executed: \r\n<script>alert(1);</script> 

https://www.irccloud.com/pastebin/FADYQPrO

</details>

---
*Analysed by Claude on 2026-05-24*
