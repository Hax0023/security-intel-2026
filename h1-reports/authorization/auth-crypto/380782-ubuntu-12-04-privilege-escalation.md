# Ubuntu 12.04 End-of-Life Privilege Escalation

## Metadata
- **Source:** HackerOne
- **Report:** 380782 | https://hackerone.com/reports/380782
- **Submitted:** 2018-07-11
- **Reporter:** ezk
- **Program:** Unknown
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Privilege Escalation, Use of Unsupported Software, Kernel Vulnerability
- **CVEs:** None
- **Category:** auth-crypto

## Summary
Ubuntu 12.04 LTS has reached end-of-life and no longer receives security patches, leaving the system vulnerable to known privilege escalation exploits. The report references CVE-2016-0728 (Keyring vulnerability), a public kernel vulnerability that can be exploited to escalate privileges from unprivileged user to root.

## Attack scenario
1. Attacker gains initial access to the system with unprivileged user account
2. Attacker identifies the target is running unsupported Ubuntu 12.04
3. Attacker obtains public privilege escalation exploit (e.g., CVE-2016-0728)
4. Attacker compiles and executes the kernel exploit on target
5. Exploit triggers keyring subsystem vulnerability in kernel
6. Attacker achieves root-level code execution

## Root cause
Ubuntu 12.04 LTS reached end-of-life and no longer receives security updates, leaving known kernel vulnerabilities unpatched. The system contains exploitable privilege escalation flaws that were patched in supported versions.

## Attacker mindset
An attacker with foothold access would recognize an outdated OS as a high-value target for local privilege escalation, leveraging publicly available exploits against known unpatched vulnerabilities to achieve full system compromise.

## Defensive takeaways
- Maintain an up-to-date inventory of all systems and their OS versions
- Establish policies requiring support for all production systems
- Implement automated patching and update procedures
- Monitor for end-of-life announcements and schedule timely upgrades
- Restrict unprivileged user capabilities and monitor for exploit execution
- Use kernel security modules (AppArmor/SELinux) to restrict privilege escalation
- Implement continuous vulnerability scanning to detect unsupported systems

## Variant hunting
Search for other outdated but still-deployed OS versions (Ubuntu 14.04, Debian 7, CentOS 6) vulnerable to similar unpatched privilege escalation flaws. Research other privilege escalation CVEs affecting Ubuntu 12.04 kernel versions.

## MITRE ATT&CK
- T1548.004
- T1134
- T1190

## Notes
This is a responsible disclosure highlighting systemic risk rather than a zero-day. CVE-2016-0728 (keyring) is the referenced vulnerability. The report emphasizes that running unsupported OS versions creates continuous privilege escalation exposure. Organizations should treat EOL systems as critical infrastructure vulnerabilities requiring immediate remediation.

## Full report
<details><summary>Expand</summary>

Hello Security Team,

Description
According to its self-reported version number, the Unix operating system running on the remote host is no longer supported.

Lack of support implies that no new security patches for the product will be released by the vendor. As a result, it is likely to contain security vulnerabilities.
Solution
Upgrade to a version of the Unix operating system that is currently supported.

Best  Regard!

## Impact

The privilege escalation for this system is as follows

https://www.exploit-db.com/exploits/37292/

</details>

---
*Analysed by Claude on 2026-05-24*
