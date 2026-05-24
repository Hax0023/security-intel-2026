# Stored XSS Using Media

## Metadata
- **Source:** HackerOne
- **Report:** 275386 | https://hackerone.com/reports/275386
- **Submitted:** 2017-10-07
- **Reporter:** dyoon
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Cross-site Scripting (XSS) - Stored
- **CVEs:** None
- **Category:** web-api

## Summary
Hi,

Summary:
This exploits an XSS vulnerability on polldaddy.com

Steps to Reproduce:
1. Create a multiple-choice question quiz on Polldaddy
2. Insert stored XSS payload into Media Embed such that it matches the shortcode format
   Payload: [<img src="http://url.to.file.which/not.exist" onerror=alert("Hello!");>]
3. When someone goes on the quiz page through the quiz share link, the payload will 

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

Hi,

Summary:
This exploits an XSS vulnerability on polldaddy.com

Steps to Reproduce:
1. Create a multiple-choice question quiz on Polldaddy
2. Insert stored XSS payload into Media Embed such that it matches the shortcode format
   Payload: [<img src="http://url.to.file.which/not.exist" onerror=alert("Hello!");>]
3. When someone goes on the quiz page through the quiz share link, the payload will execute. 

Proof of Concept (30-second video):
https://drive.google.com/file/d/0B_lsH7QMy9DkQnV5a3hHa05lSmM/view

</details>

---
*Analysed by Claude on 2026-05-24*
