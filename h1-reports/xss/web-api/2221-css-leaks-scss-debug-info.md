# CSS leaks SCSS debug info

## Metadata
- **Source:** HackerOne
- **Report:** 2221 | https://hackerone.com/reports/2221
- **Submitted:** 2014-02-23
- **Reporter:** guido
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Information Disclosure
- **CVEs:** None
- **Category:** web-api

## Summary
Download CSS style sheet referenced from the HTML and do:

grep -oP "file.:.*?scss" application-facbdb64a504bb08ec272860320e1941.css | sort | uniq

As you can see it exposes information about the file system, source CSS files and software used.

See enclosed file for a dump of the output of the command above.

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

Download CSS style sheet referenced from the HTML and do:

grep -oP "file.:.*?scss" application-facbdb64a504bb08ec272860320e1941.css | sort | uniq

As you can see it exposes information about the file system, source CSS files and software used.

See enclosed file for a dump of the output of the command above.

</details>

---
*Analysed by Claude on 2026-05-24*
