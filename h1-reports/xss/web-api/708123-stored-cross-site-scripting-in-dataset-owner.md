# Stored cross-site scripting in dataset owner.

## Metadata
- **Source:** HackerOne
- **Report:** 708123 | https://hackerone.com/reports/708123
- **Submitted:** 2019-10-05
- **Reporter:** irisrumtub
- **Program:** Unknown
- **Bounty:** $1,925
- **Severity:** none
- **Vuln:** Cross-site Scripting (XSS) - Stored
- **CVEs:** None
- **Category:** web-api

## Summary
Hi again. Another XSS this time.
**Summary:** Unescaped chars in 'dataset owner' could be abused to store arbitrary javascript.

**Description:** There is a 'dataset owner' field in new 'custom dataset dashboard' which contains unsanitized output. If attacker would modify his name, like first name '<img src=x' and last name 
'onerror=alert(1)>', the field would hold a script. While for most users 

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

Hi again. Another XSS this time.
**Summary:** Unescaped chars in 'dataset owner' could be abused to store arbitrary javascript.

**Description:** There is a 'dataset owner' field in new 'custom dataset dashboard' which contains unsanitized output. If attacker would modify his name, like first name '<img src=x' and last name 
'onerror=alert(1)>', the field would hold a script. While for most users this is a case of self-xss, for enterprise users (for which, as i understand. this field was introduced in the first place), it can lead to executing arbitrary javascript.

**Steps To Reproduce:**

  1. Put the payload in name and/or surname
 *(first name '<img src=x' and last name 
'onerror=alert(1)>')*
  2. Navigate to custom datasets. 


**Test account information**

tvburis+hackerone@gmail.com

## Impact

Executing arbitrary javascript, stealing other users' algos as demonstrated in previous reports with XSS on quantopian domain.

</details>

---
*Analysed by Claude on 2026-05-24*
