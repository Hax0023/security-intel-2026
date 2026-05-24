# Information Disclosure

## Metadata
- **Source:** HackerOne
- **Report:** 143064 | https://hackerone.com/reports/143064
- **Submitted:** 2016-06-04
- **Reporter:** mugeesahmed
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Information Disclosure
- **CVEs:** None
- **Category:** web-api

## Summary
Hey, 

I found Following Security issue on your site.

Information Disclosure :-

your Wordpress installation in Disclosing its version Number in https://drchrono.com/blog/readme.html 
This can a hacker in speeding up the process or information gathering though discovering your wordpress version number a attacker could use specific exploits made just for your version.

Missing Best Practice :- 

T

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

Hey, 

I found Following Security issue on your site.

Information Disclosure :-

your Wordpress installation in Disclosing its version Number in https://drchrono.com/blog/readme.html 
This can a hacker in speeding up the process or information gathering though discovering your wordpress version number a attacker could use specific exploits made just for your version.

Missing Best Practice :- 

There are Two outdated plugins in your Wordpress site

                 1.  Wordpress-importer
                  2.  Wufoo-shortcode

This could Serve as a Potential Thread to your site because outdated plugins are often Vulnerable to attacks 
and could also be vulnerable to 0days 

The Website Plugins Should be update regularly to prevent your site from getting attacked.

Prove of Concept :-

https://drchrono.com/blog/wp-content/plugins/wufoo-shortcode/readme.txt
https://drchrono.com/blog/wp-content/plugins/wordpress-importer/readme.txt



</details>

---
*Analysed by Claude on 2026-05-24*
