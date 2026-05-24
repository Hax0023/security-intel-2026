# Reflected XSS in Pastebin-view

## Metadata
- **Source:** HackerOne
- **Report:** 17540 | https://hackerone.com/reports/17540
- **Submitted:** 2014-06-26
- **Reporter:** pseudochu
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
The paste ID passed in via the URL in the Pastebin-view is inserted between `<script>` tags unsanitised. This leads to reflected XSS that bypasses all major XSS protection software (Chrome, IE...).

Normal request: https://www.irccloud.com/pastebin/nhm4f6pB
Proof-of-concept: https://www.irccloud.com/pastebin/";alert(0);%2F%2F

I've never used **HackerOne** before so please let me know if my r

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

The paste ID passed in via the URL in the Pastebin-view is inserted between `<script>` tags unsanitised. This leads to reflected XSS that bypasses all major XSS protection software (Chrome, IE...).

Normal request: https://www.irccloud.com/pastebin/nhm4f6pB
Proof-of-concept: https://www.irccloud.com/pastebin/";alert(0);%2F%2F

I've never used **HackerOne** before so please let me know if my report is missing something important!

</details>

---
*Analysed by Claude on 2026-05-24*
