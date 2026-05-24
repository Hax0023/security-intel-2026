# Stored Cross-Site scripting in the infographics using Data Objects links

## Metadata
- **Source:** HackerOne
- **Report:** 280503 | https://hackerone.com/reports/280503
- **Submitted:** 2017-10-19
- **Reporter:** sp1d3rs
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Cross-site Scripting (XSS) - Stored
- **CVEs:** None
- **Category:** web-api

## Summary
##Description
Hello. This stored XSScase is different from early reported #280495, but has a very similar root cause and reproduction steps.

Upon pasting the link to the Text Object (not in the `Add Media` section, like in previous report), we can intercept the request, and change the link source to the malicious - which will result to the Stored XSS
{F230787}

##POC
https://infogram.com/step-by-

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

##Description
Hello. This stored XSScase is different from early reported #280495, but has a very similar root cause and reproduction steps.

Upon pasting the link to the Text Object (not in the `Add Media` section, like in previous report), we can intercept the request, and change the link source to the malicious - which will result to the Stored XSS
{F230787}

##POC
https://infogram.com/step-by-step-chartsgreaterlesssvg-onloadalert1greater-1ggk2694e7dj2n0
Click on the text in the block `2. Question`
{F230788}
You will be XSSed.

##Reproduction steps
1. Create some infographic
2. Use some text object and add the link to it, for example, `http://google.com`:
{F230789}
3. Start web debugger, and enable interception mode.
4. Insert the link
5. Catch the request to the 
```
https://infogram.com/api/infographics/update/[_your_project_id]
```
and change 
```
http://google.com
```
to the
```
javascript:alert(document.domain)
```
{F230790}
6. Execute the request, and make infographic Public
7. Visit it and click the text object to ensure that XSS works.

##Suggested fix
Check the inserted links on the server side - they must start with the pattern `http[s]://`

</details>

---
*Analysed by Claude on 2026-05-24*
