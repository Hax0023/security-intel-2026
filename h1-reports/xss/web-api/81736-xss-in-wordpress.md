# XSS in WordPress 

## Metadata
- **Source:** HackerOne
- **Report:** 81736 | https://hackerone.com/reports/81736
- **Submitted:** 2015-08-11
- **Reporter:** blinkms
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
Hi there  ,

I have identified a WordPress security vulnerability , a potential XSS vulnerability that affects latest version of WordPress .

POC :-

Go to GET *****.wordpress.com/wp-admin/post-new.php

In Text (HTML Field) input , <HTML xmlns: ><audio>
<audio src=wp onerror=alert(0X1)>


Now, Click on Visual Tab , XSS will trigger . (Screenshot attached )

Thanks and please address 

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

Hi there  ,

I have identified a WordPress security vulnerability , a potential XSS vulnerability that affects latest version of WordPress .

POC :-

Go to GET *****.wordpress.com/wp-admin/post-new.php

In Text (HTML Field) input , <HTML xmlns: ><audio>
<audio src=wp onerror=alert(0X1)>


Now, Click on Visual Tab , XSS will trigger . (Screenshot attached )

Thanks and please address this issue .


</details>

---
*Analysed by Claude on 2026-05-31*
