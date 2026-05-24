# Runtime manipulation iOS app breaking the PIN

## Metadata
- **Source:** HackerOne
- **Report:** 80512 | https://hackerone.com/reports/80512
- **Submitted:** 2015-08-04
- **Reporter:** kaleemgiet
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Violation of Secure Design Principles
- **CVEs:** None
- **Category:** uncategorised

## Summary
I was able to bypass your pin protection by doing runtime manipulation in iOS app

1.Installed the snoop it in device
2.By going snoop it tool settings choose the coinbase app
3.I already set the the pin in coinbase app
4.Open the coinbase app it is asking for PIN
5.Now browsing the snoopit controlled window from the browser 
6.Go to the Objective C-Classes in snoop it window
7.By directly

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

I was able to bypass your pin protection by doing runtime manipulation in iOS app

1.Installed the snoop it in device
2.By going snoop it tool settings choose the coinbase app
3.I already set the the pin in coinbase app
4.Open the coinbase app it is asking for PIN
5.Now browsing the snoopit controlled window from the browser 
6.Go to the Objective C-Classes in snoop it window
7.By directly invoking the userAutheticated method from the coinbase.CBPINViewController I was able to break the PIN protection
8. userAuthenticated method is not taking any arguments just invoking this method bypassed the scree

Please see the POC video
https://www.dropbox.com/s/acvr4g7lv63tti5/runtime%20manipulation%20coinbase.mov?dl=0

You can prevent run time manipulation by do not attaching a debugger to app process
you see here how to prevent

http://resources.infosecinstitute.com/ios-application-security-part-23-defending-runtime-analysis-manipulation/



</details>

---
*Analysed by Claude on 2026-05-24*
