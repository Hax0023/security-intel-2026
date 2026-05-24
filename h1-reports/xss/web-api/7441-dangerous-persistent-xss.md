# Dangerous Persistent xss

## Metadata
- **Source:** HackerOne
- **Report:** 7441 | https://hackerone.com/reports/7441
- **Submitted:** 2014-04-13
- **Reporter:** reporter
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
If a person is an op in a channel, it is possible to make all the users inside the irc channel execute javascript code.
Steps to repoduce:
1.Go to a random channel where you are op.
2.Enter the following command:
/ban <script>alert(2)</script>
3.The script will execute an alert box containing 2 in all the browsers of the users inside the irc channel.

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

If a person is an op in a channel, it is possible to make all the users inside the irc channel execute javascript code.
Steps to repoduce:
1.Go to a random channel where you are op.
2.Enter the following command:
/ban <script>alert(2)</script>
3.The script will execute an alert box containing 2 in all the browsers of the users inside the irc channel.

</details>

---
*Analysed by Claude on 2026-05-24*
