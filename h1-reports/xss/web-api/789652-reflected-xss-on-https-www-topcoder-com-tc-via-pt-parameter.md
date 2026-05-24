# Reflected-XSS on https://www.topcoder.com/tc via pt parameter

## Metadata
- **Source:** HackerOne
- **Report:** 789652 | https://hackerone.com/reports/789652
- **Submitted:** 2020-02-05
- **Reporter:** laz0rde
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Cross-site Scripting (XSS) - Reflected
- **CVEs:** None
- **Category:** web-api

## Summary
##Summary:
I Found an XSS(Reflected) at the URL mentioned 
and the injected parameter is: pt
Steps To Reproduce:
1-go to this URL [https://www.topcoder.com/tc?module=ReviewBoard&pt=1]
$$you will recognize that is parameter (pt) is reflecting its value into the page
2- try injecting this parameter with HTML tags or XSS payloads 
the payloads I used 
1-for HTML Injection = <a+href="https://bing.com"

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

##Summary:
I Found an XSS(Reflected) at the URL mentioned 
and the injected parameter is: pt
Steps To Reproduce:
1-go to this URL [https://www.topcoder.com/tc?module=ReviewBoard&pt=1]
$$you will recognize that is parameter (pt) is reflecting its value into the page
2- try injecting this parameter with HTML tags or XSS payloads 
the payloads I used 
1-for HTML Injection = <a+href="https://bing.com">LINK</a>
2-for XSS = <script>confirm(1)</script>

## Impact

XSS can be used for :
1- Cookie stealing 
2- Pishing attacks
3- URL redirection 
etc....

</details>

---
*Analysed by Claude on 2026-05-24*
