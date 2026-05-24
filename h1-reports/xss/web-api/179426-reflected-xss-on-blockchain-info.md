# Reflected XSS on blockchain.info

## Metadata
- **Source:** HackerOne
- **Report:** 179426 | https://hackerone.com/reports/179426
- **Submitted:** 2016-11-01
- **Reporter:** kasperkarlsson
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
The application at https://blockchain.info is vulnerable to reflected XSS/HTML injection through the URL at the block-index page.

Proof of concept
===
The following PoC contains the payload `"><h1>XSS here` which displays the text in heading size.
https://blockchain.info/en/block-index/1160457/%22%3E%3Ch1%3EXSS%20here
Another example with some scrolling text `"><marquee>XSS here`:
https://blockch

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

The application at https://blockchain.info is vulnerable to reflected XSS/HTML injection through the URL at the block-index page.

Proof of concept
===
The following PoC contains the payload `"><h1>XSS here` which displays the text in heading size.
https://blockchain.info/en/block-index/1160457/%22%3E%3Ch1%3EXSS%20here
Another example with some scrolling text `"><marquee>XSS here`:
https://blockchain.info/en/block-index/1160457/%22%3E%3Cmarquee%3EXSS%20here

Print screens from the two PoCs above are attached to this report. This was tested using Mozilla Firefox 49.0.2 and Google Chrome 54.0.2840.71.

Due to the strict Content Security Policy which even blocks 'self', arbitrary javascript cannot be executed through this vulnerability without some CSP bypass. Great! :)

Recommended solution
===
Make sure to properly encode the last part of the URL before printing it to the page. Another possible solution is to make sure the URL matches a strict whitelist regexp, so that this part of the URL is not put on the page at all if it looks fishy.

</details>

---
*Analysed by Claude on 2026-05-24*
