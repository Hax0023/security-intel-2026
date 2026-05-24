# Information Disclosure through .DS_Store in ██████████

## Metadata
- **Source:** HackerOne
- **Report:** 142549 | https://hackerone.com/reports/142549
- **Submitted:** 2016-06-01
- **Reporter:** lewerkun
- **Program:** Unknown
- **Bounty:** $560
- **Severity:** unknown
- **Vuln:** Information Disclosure
- **CVEs:** None
- **Category:** web-api

## Summary
Hello!

Description:
The website located at █████████ suffers from an information disclosure through ".DS_Store" file, accessible to unauthorised external users.
In the Apple OS X operating system, .DS_Store is a file that stores custom attributes of its containing folder.

Reproduction Steps:
Guide for installing DS_Store parser - https://digi.ninja/projects/fdb.php

First link: (See pic 0 and 1)

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

Hello!

Description:
The website located at █████████ suffers from an information disclosure through ".DS_Store" file, accessible to unauthorised external users.
In the Apple OS X operating system, .DS_Store is a file that stores custom attributes of its containing folder.

Reproduction Steps:
Guide for installing DS_Store parser - https://digi.ninja/projects/fdb.php

First link: (See pic 0 and 1)
███████.DS_Store

Second link: (See pic 2 and 3)
████Packages/.DS_Store
This directory contain tons of packages for MacOS
Including licence keys (See pic 4 and 5) 
██████████Packages/█████████
██████████Packages/████
and etc
Certificate for WIFI (See pic 6)
█████████Packages/█████
Twitter Root certificate (See pic 8)
█████████Packages/███████
And other juicy stuff which is intended only for Twitter employees

Third link (See pic 7)
██████████Scripts/.DS_Store
This directory contain tons of scripts for installation and configuring corporate computers.

In one case the attacker can just use Twitter licenses and etc (for obvious reasons, I didn't check whether this licences is still active ), in other this information can be useful for future attacks.

Please let me know if you need some extra information.
Thanks in advance!










</details>

---
*Analysed by Claude on 2026-05-24*
