# Flaw in login with twitter to steal Oauth tokens

## Metadata
- **Source:** HackerOne
- **Report:** 44492 | https://hackerone.com/reports/44492
- **Submitted:** 2015-01-21
- **Reporter:** akhil-reni
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Improper Authentication - Generic
- **CVEs:** None
- **Category:** auth-crypto

## Summary
Hey hi,

Steps to reproduce:
=============================================

I have been testing the twitter kit in fabric.
I added login with twitter integration to my application.
I pushed the application to my android phone , clicked login with twitter.
entered my username and password.

Searched my logcat for everything with the word "twitter" in it. 
I found the oauth token getting 

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

Hey hi,

Steps to reproduce:
=============================================

I have been testing the twitter kit in fabric.
I added login with twitter integration to my application.
I pushed the application to my android phone , clicked login with twitter.
entered my username and password.

Searched my logcat for everything with the word "twitter" in it. 
I found the oauth token getting leaked via login with twitter integration on Fabric.
So any app that is using fabric's twitter kit ( login with twitter) is vulnerable to it.
Any other app installed on that particular phone hasaccess to logcat, and can read the logs.
which results in oauth token stealing.

Regards,
karthik
Wesecureapp


</details>

---
*Analysed by Claude on 2026-05-24*
