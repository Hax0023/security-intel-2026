# XSS through document projects

## Metadata
- **Source:** HackerOne
- **Report:** 244902 | https://hackerone.com/reports/244902
- **Submitted:** 2017-06-30
- **Reporter:** ethanluismcdonough
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** high
- **Vuln:** Cross-site Scripting (XSS) - Stored
- **CVEs:** None
- **Category:** web-api

## Summary
Hello, I'm Ethan Luis McDonough ([@elmt2](https://www.khanacademy.org/profile/elmt2/) on Khan Academy), and I found a way to inject scripts into document projects.  Since KA document projects output HTML, I can edit the PUT request that updates projects (https://www.khanacademy.org/api/internal/scratchpads/ID) and inject JavaScript code inside an `<img>` tag's `onload` attribute.  Here's a demo th

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

Hello, I'm Ethan Luis McDonough ([@elmt2](https://www.khanacademy.org/profile/elmt2/) on Khan Academy), and I found a way to inject scripts into document projects.  Since KA document projects output HTML, I can edit the PUT request that updates projects (https://www.khanacademy.org/api/internal/scratchpads/ID) and inject JavaScript code inside an `<img>` tag's `onload` attribute.  Here's a demo that completely redirects a learner from KA to another site: https://www.khanacademy.org/physics/woah/4740384569491456.  

**Note**: the stored script does not run in Firefox because document projects don't seem to be working on that browser (at least on my machine).

</details>

---
*Analysed by Claude on 2026-05-24*
