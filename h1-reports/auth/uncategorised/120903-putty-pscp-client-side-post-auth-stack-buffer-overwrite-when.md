# putty pscp client-side post-auth stack buffer overwrite when processing remote file size 

## Metadata
- **Source:** HackerOne
- **Report:** 120903 | https://hackerone.com/reports/120903
- **Submitted:** 2016-03-06
- **Reporter:** hxd
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Memory Corruption - Generic
- **CVEs:** CVE-2016-2563
- **Category:** uncategorised

## Summary
Not sure if this will qualify but it may impact a pretty broad audience given the fact that putty code is part of many other apps (filezilla, ...) and it is the defacto standalone ssh client for windows administrators (besides openssh cygwin)

putty <= 0.66; affects putty versions dating back ~9 years.

Vulnerability Note: https://github.com/tintinweb/pub/tree/master/pocs/cve-2016-2563
Vendor Secu

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

Not sure if this will qualify but it may impact a pretty broad audience given the fact that putty code is part of many other apps (filezilla, ...) and it is the defacto standalone ssh client for windows administrators (besides openssh cygwin)

putty <= 0.66; affects putty versions dating back ~9 years.

Vulnerability Note: https://github.com/tintinweb/pub/tree/master/pocs/cve-2016-2563
Vendor Security Notification: http://www.chiark.greenend.org.uk/~sgtatham/putty/wishlist/vuln-pscp-sink-sscanf.html

provided patch and PoC to vendor. was resolved within one week (which is very impressive!).

patch/poc will be released later today on this github account.

in total reported:
* mem-corruption/remote code execution via stack buffer overwrite in putty pscp (connect vulnerable putty to poc.py to trigger an EIP=0x41414141 (AAAA) bad instruction.
* DoS condition in the parsing of SSH-Strings (core packet handling) that lead to a nullptr read. (connect putty to poc.py and type x11exploit to trigger one occurrence of a crash)
* DoS condition in the handling of unrequested forwarded-tcpip channels open requests that lead to a nullptr read. (connect putty to poc.py and type forwardedtcpipcrash to trigger crash)

</details>

---
*Analysed by Claude on 2026-05-24*
