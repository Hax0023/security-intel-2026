# XSS in topics because of bandcamp preview engine vulnerability

## Metadata
- **Source:** HackerOne
- **Report:** 197443 | https://hackerone.com/reports/197443
- **Submitted:** 2017-01-11
- **Reporter:** skavans
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** high
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
1. Load http://try.discourse.org
2. Click "New topic"
3. Enter this payload https://89.223.28.48/bandcamp.com/album/index.html?XSSa2 to field with placeholder "Type title or paste a link here"
4. Wait for the preview engine to parse the link
4. XSS will fire

{F151439}

You should sanitize external data in this engine and replace *matches_regexp* from
`^https?:\/\/.*bandcamp\.com\/album\/`
to
`^ht

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

1. Load http://try.discourse.org
2. Click "New topic"
3. Enter this payload https://89.223.28.48/bandcamp.com/album/index.html?XSSa2 to field with placeholder "Type title or paste a link here"
4. Wait for the preview engine to parse the link
4. XSS will fire

{F151439}

You should sanitize external data in this engine and replace *matches_regexp* from
`^https?:\/\/.*bandcamp\.com\/album\/`
to
`^https?:\/\/.*\.bandcamp\.com\/album\/`
to fix the issue.

</details>

---
*Analysed by Claude on 2026-05-24*
