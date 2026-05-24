# XSS with Time-of-Day Format

## Metadata
- **Source:** HackerOne
- **Report:** 52822 | https://hackerone.com/reports/52822
- **Submitted:** 2015-03-20
- **Reporter:** candux
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
- Go to your user preferences
- Put the following into Time-of-Day Format (with the quote): 
 `'<\i\m\g \s\r\c=x \o\n\e\r\r\o\r=\a\l\e\r\t(\'X\S\S\')\>' `
- Open a repository (diffusion) -> XSS-Popup

The repository file-overview is the only place where I could see the XSS so far.

Because it's a user own preference, it is not easy to actually do something malicious in a real-world scenario

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

- Go to your user preferences
- Put the following into Time-of-Day Format (with the quote): 
 `'<\i\m\g \s\r\c=x \o\n\e\r\r\o\r=\a\l\e\r\t(\'X\S\S\')\>' `
- Open a repository (diffusion) -> XSS-Popup

The repository file-overview is the only place where I could see the XSS so far.

Because it's a user own preference, it is not easy to actually do something malicious in a real-world scenario. But it's definitely possible if you think hard enough about it :)

Cheers,
David

mongoose

</details>

---
*Analysed by Claude on 2026-05-24*
