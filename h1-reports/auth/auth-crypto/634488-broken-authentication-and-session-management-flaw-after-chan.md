# Broken Authentication and Session Management Flaw After Change Password and Logout

## Metadata
- **Source:** HackerOne
- **Report:** 634488 | https://hackerone.com/reports/634488
- **Submitted:** 2019-07-03
- **Reporter:** root_geek280
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** low
- **Vuln:** Violation of Secure Design Principles
- **CVEs:** None
- **Category:** auth-crypto

## Summary
####Summary
Usually it's happened that when you change password or sign out from one place (or one browser), automatically someone who is open same account will sign out too from another browser. Basically your session destroyed at server side...
But in your site, it still alive..

####PoC
Detail About Vulnerability and PoC on Attachment File

Noted: You can try these vulnerability in another site

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

####Summary
Usually it's happened that when you change password or sign out from one place (or one browser), automatically someone who is open same account will sign out too from another browser. Basically your session destroyed at server side...
But in your site, it still alive..

####PoC
Detail About Vulnerability and PoC on Attachment File

Noted: You can try these vulnerability in another site. (e.g cryptfolio.com, facebook.com, etc). It's not alive when another has changed password and sign out

For More Information about This Vulnerability You can check OWASP Guide

[https://www.owasp.org/index.php?title=Broken_Authentication_and_Session_Management&setlang=en](https://www.owasp.org/index.php?title=Broken_Authentication_and_Session_Management&setlang=en)

####Attachment Video
[https://gofile.io/?c=Vt4m42](https://gofile.io/?c=Vt4m42)

## Impact

Account profile still can be edited even in another browser the account has signedout and changed password

</details>

---
*Analysed by Claude on 2026-05-24*
