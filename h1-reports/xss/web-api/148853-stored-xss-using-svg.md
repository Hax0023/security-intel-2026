# Stored XSS using  SVG 

## Metadata
- **Source:** HackerOne
- **Report:** 148853 | https://hackerone.com/reports/148853
- **Submitted:** 2016-07-02
- **Reporter:** abdullah
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
Hi , 

Background 
------------------------------------

I had problem in setup the airship at ubuntu so I tested on your site .  
If you uploads any file thet can use for XSS (HTML,SWF,etc) the content type will change to "text/plain; charset=us-ascii" . But for images it will stay the same . so if you upload SVG with JS content it will work fine ! 

The "Content-Type: image/svg+xml; charset=us-a

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

Hi , 

Background 
------------------------------------

I had problem in setup the airship at ubuntu so I tested on your site .  
If you uploads any file thet can use for XSS (HTML,SWF,etc) the content type will change to "text/plain; charset=us-ascii" . But for images it will stay the same . so if you upload SVG with JS content it will work fine ! 

The "Content-Type: image/svg+xml; charset=us-ascii" header will make this attack works . 

Just upload the svg file to the site . 

PoC
---------------

{F102954}


SVG's  is not good sometimes to view as image and it will be stored in users accounts.

Thanks 

</details>

---
*Analysed by Claude on 2026-05-24*
