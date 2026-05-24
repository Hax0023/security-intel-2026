# XSS on added name album on videos.

## Metadata
- **Source:** HackerOne
- **Report:** 65324 | https://hackerone.com/reports/65324
- **Submitted:** 2015-06-01
- **Reporter:** ruisilva
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
Hi

Steps to reproduce:

First go to :  https://vk.com/video
Next click on Add a Video
After add a video from youtube and on title Field Insert TEST XSS
And click save.
Next after this go to https://vk.com/video again and you will see video  with the name TEST XSS
Click above TEST XSS and you will for https://vk.com/video?z=video307088553_171482428%2Falbum307088553 
Now scroll and you wi

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

Hi

Steps to reproduce:

First go to :  https://vk.com/video
Next click on Add a Video
After add a video from youtube and on title Field Insert TEST XSS
And click save.
Next after this go to https://vk.com/video again and you will see video  with the name TEST XSS
Click above TEST XSS and you will for https://vk.com/video?z=video307088553_171482428%2Falbum307088553 
Now scroll and you will see word : Added with a right , put mouse above this and create album 

In folder name field insert this xss payload:

"><img src=x onerror=prompt(1)>
And click save.
Now video will be added to this album
Now go with the mouse above added word and click on added word.
And xss will be executed.
Ty :)

Works on google chrome :  43.0.2357.81 m



</details>

---
*Analysed by Claude on 2026-05-24*
