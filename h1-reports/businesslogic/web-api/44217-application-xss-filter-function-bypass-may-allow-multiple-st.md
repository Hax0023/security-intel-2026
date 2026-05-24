# Application XSS filter function Bypass may allow Multiple stored XSS

## Metadata
- **Source:** HackerOne
- **Report:** 44217 | https://hackerone.com/reports/44217
- **Submitted:** 2015-01-18
- **Reporter:** securityidiots
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
Hi,

As i analysed the application behavior and the security structure, i found out that the application is using "Greedy XSS Regex filter" against XSS and removes any the whole string from '<' to '>'. So i tried some basic bypass which allowed me to insert tags and other characters into the string.

Here is the the payload:
<%0crameset%20src=''> 

Now if we see the whole application is usi

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

As i analysed the application behavior and the security structure, i found out that the application is using "Greedy XSS Regex filter" against XSS and removes any the whole string from '<' to '>'. So i tried some basic bypass which allowed me to insert tags and other characters into the string.

Here is the the payload:
<%0crameset%20src=''> 

Now if we see the whole application is using same filter against XSS which makes this bypass to be universally working on nearly all the input fields, which means we can say an attacker can successfully bypass and enter XSS payload in database but when the string prints in the frontend there is another filter, which encode all html entities before printing.

Nice but now enough as many of the inputs could in the below condition will end up with a successful XSS exploitation.
1. Input under javascript.
2. Any string not properly encoded before printing.
3. JSON output with HTML headers.

I have already reported some issues in vimeo where input injected directly into javascript and do not need any html characters, another issue of JSON output with HTML headers. 

Below you can see both reports:
https://hackerone.com/reports/43934
https://hackerone.com/reports/44215

In the first screenshot you can see profile update request where i updates my profile and injected those HTML characters, in second screenshot you can see it injected in the response as stored XSS.

</details>

---
*Analysed by Claude on 2026-05-24*
