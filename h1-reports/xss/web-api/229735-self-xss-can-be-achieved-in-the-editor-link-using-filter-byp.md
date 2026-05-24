# Self-XSS can be achieved in the editor link using filter bypass

## Metadata
- **Source:** HackerOne
- **Report:** 229735 | https://hackerone.com/reports/229735
- **Submitted:** 2017-05-18
- **Reporter:** sp1d3rs
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** none
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
##Description
I saw the fixed issue in the https://hackerone.com/reports/223692 and i think i found another filter bypass. I noticed that we actually can use special keywords like %(branch)s, %(file)s and %(line)s.
So XSS can be achieved in this way:
`%(branch)s:alert(1);//https://`
if the branch will be named `javascript`, the payload will be executed upon pressing the source code link of the fil

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

##Description
I saw the fixed issue in the https://hackerone.com/reports/223692 and i think i found another filter bypass. I noticed that we actually can use special keywords like %(branch)s, %(file)s and %(line)s.
So XSS can be achieved in this way:
`%(branch)s:alert(1);//https://`
if the branch will be named `javascript`, the payload will be executed upon pressing the source code link of the file inside it.

##Steps to reproduce
1. Create some branch and name it javascript
2. Put some source files.
3. Click the link on source file. The `%(branch)s` will be replaced by branch name (`javascript`) and popup will be fired.

##Suggested fix
I recommend you to additionally sanitize string by disallowing special symbolst before first `:` occurence (if exist)

</details>

---
*Analysed by Claude on 2026-05-24*
