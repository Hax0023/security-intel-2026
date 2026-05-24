# XSS - Gallery Search Listing

## Metadata
- **Source:** HackerOne
- **Report:** 76713 | https://hackerone.com/reports/76713
- **Submitted:** 2015-07-19
- **Reporter:** bugs3ra
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
HI.
If you upload video having title with XSS payload. and search for the video, the dropdown listing will execute the payload.

https://www.zaption.com/gallery/search?q=%3E%3Cimg

I need not to upload the payload, I utilized already uploaded videos.


You can also execute the payload by just start typing into the search box with
"><img

That's it, XSS will be executed.

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

HI.
If you upload video having title with XSS payload. and search for the video, the dropdown listing will execute the payload.

https://www.zaption.com/gallery/search?q=%3E%3Cimg

I need not to upload the payload, I utilized already uploaded videos.


You can also execute the payload by just start typing into the search box with
"><img

That's it, XSS will be executed.

</details>

---
*Analysed by Claude on 2026-05-24*
