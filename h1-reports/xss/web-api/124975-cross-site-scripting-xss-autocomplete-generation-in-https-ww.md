# Cross-site Scripting (XSS) autocomplete generation in https://www.uber.com/

## Metadata
- **Source:** HackerOne
- **Report:** 124975 | https://hackerone.com/reports/124975
- **Submitted:** 2016-03-22
- **Reporter:** exodia_forbidden_one
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary

Description:
The website located at https://www.uber.com/ suffers from a generated Cross-site Scripting (XSS) vulnerability in the "find a city" input field. 

Reproduction Steps:

Open the latest Chrome web browser

Navigate to the following URL's "find a city input field":
https://www.uber.com/

Type in the following:
<script>alert(1)</script>

Note that the autocomplete result being generated 

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


Description:
The website located at https://www.uber.com/ suffers from a generated Cross-site Scripting (XSS) vulnerability in the "find a city" input field. 

Reproduction Steps:

Open the latest Chrome web browser

Navigate to the following URL's "find a city input field":
https://www.uber.com/

Type in the following:
<script>alert(1)</script>

Note that the autocomplete result being generated from the server side is raw javascript and payload was fired.

I’ve tested this in the latest Chrome. Attached to this report are screenshots of this issue occurring in chrome.

</details>

---
*Analysed by Claude on 2026-05-24*
