# Stored XSS at ██████userprofile.aspx

## Metadata
- **Source:** HackerOne
- **Report:** 901377 | https://hackerone.com/reports/901377
- **Submitted:** 2020-06-18
- **Reporter:** 5050thepiguy
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** high
- **Vuln:** Cross-site Scripting (XSS) - Stored
- **CVEs:** None
- **Category:** web-api

## Summary
**Summary:**
Stored XSS vulnerability exists at ██████████userprofile.aspx under "say something about yourself...". XSS can be used for a variety of attacks. 

## Impact
XSS can be used to steal cookies, password or to run arbitrary code in the victim's browser. 

## Step-by-step Reproduction Instructions

1. Create an account at ███████
2. Go to your profile at ████userprofile.aspx
3. Go to "Say 

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

**Summary:**
Stored XSS vulnerability exists at ██████████userprofile.aspx under "say something about yourself...". XSS can be used for a variety of attacks. 

## Impact
XSS can be used to steal cookies, password or to run arbitrary code in the victim's browser. 

## Step-by-step Reproduction Instructions

1. Create an account at ███████
2. Go to your profile at ████userprofile.aspx
3. Go to "Say something about yourself..." and enter the XSS payload xxx<svg/onload=alert(document.cookie);>xxx
4. Observe that XSS triggers and reload the page to observe that it is stored XSS.

## Product, Version, and Configuration (If applicable)
███userprofile.aspx#

## Suggested Mitigation/Remediation Actions
Use secure coding techniques such as sanitizing input into form fields so attackers cannot inject scripts to perform XSS attacks. XSS vulnerabilities come from a lack of data escaping. 

##References
https://hackerone.com/reports/858255
https://dzone.com/articles/reflected-xss-explained-how-to-prevent-reflected-x
https://www.imperva.com/learn/application-security/reflected-xss-attacks/
https://www.hacksplaining.com/prevention/xss-reflected

## Impact

XSS can be used to steal cookies, password or to run arbitrary code in the victim's browser.

</details>

---
*Analysed by Claude on 2026-05-24*
