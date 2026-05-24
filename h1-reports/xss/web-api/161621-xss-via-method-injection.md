# XSS Via Method injection

## Metadata
- **Source:** HackerOne
- **Report:** 161621 | https://hackerone.com/reports/161621
- **Submitted:** 2016-08-20
- **Reporter:** exception
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** none
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
Hi guys

i found a low risk vuln , when you request a page on gratipay.com with uncommon Method , the server responds with error message .

Invalid Method 'Invalid HTTP method:TTEGETTT
with out escaping chars 

so when you inject an html element with method you can trigger an XSS .


Steps to reproduce  
- make an http request with a method  like this 
<img|src='3'|onerror=alert(3)/>



Fix :
you 

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

Hi guys

i found a low risk vuln , when you request a page on gratipay.com with uncommon Method , the server responds with error message .

Invalid Method 'Invalid HTTP method:TTEGETTT
with out escaping chars 

so when you inject an html element with method you can trigger an XSS .


Steps to reproduce  
- make an http request with a method  like this 
<img|src='3'|onerror=alert(3)/>



Fix :
you should validate the method value before printing it back in responses 


</details>

---
*Analysed by Claude on 2026-05-24*
