# XSS via SVG file

## Metadata
- **Source:** HackerOne
- **Report:** 212253 | https://hackerone.com/reports/212253
- **Submitted:** 2017-03-10
- **Reporter:** 0xspade
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
# Hello Ubuquiti,

# Details
I was able to upload an svg file to [here](https://community.ubnt.com/t5/media/gallerypage/user-id/559584). so i uploaded an SVG file with XSS on its code and if the attacker give the link to his victim he can grab it's victim's cookie.
and regarding to the your Upload image svg file it uploaded even it has an error..

# PoC
[link](https://community.ubnt.com/t5/image/s

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

# Hello Ubuquiti,

# Details
I was able to upload an svg file to [here](https://community.ubnt.com/t5/media/gallerypage/user-id/559584). so i uploaded an SVG file with XSS on its code and if the attacker give the link to his victim he can grab it's victim's cookie.
and regarding to the your Upload image svg file it uploaded even it has an error..

# PoC
[link](https://community.ubnt.com/t5/image/serverpage/image-id/0i9D3EF39FC6246359/image-size/thumb/is-preview/true?v=1.0&px=100)
{F167791}

# Fix

Dont allow to upload an svg file because attacker can put his payload to a SVG files.

</details>

---
*Analysed by Claude on 2026-05-24*
