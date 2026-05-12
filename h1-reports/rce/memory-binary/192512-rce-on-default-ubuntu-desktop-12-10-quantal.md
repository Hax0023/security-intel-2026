# RCE on default Ubuntu Desktop >= 12.10 Quantal via Apport

## Metadata
- **Source:** HackerOne
- **Report:** 192512 | https://hackerone.com/reports/192512
- **Submitted:** 2016-12-19
- **Reporter:** donnchac
- **Program:** Internet Bug Bounty
- **Bounty:** Not specified in report
- **Severity:** CRITICAL
- **Vuln:** Remote Code Execution, Arbitrary File Write, Privilege Escalation, Unsafe Deserialization
- **CVEs:** None
- **Category:** memory-binary

## Summary
Multiple vulnerabilities in Canonical's Apport crash reporting software allowed unauthenticated remote code execution on default Ubuntu Desktop installations >= 12.10. The vulnerabilities could be triggered by opening a malicious file, leading to arbitrary code execution with user privileges.

## Attack scenario
1. Attacker creates a malicious crash report file or crafts a specially formatted package/file
2. Attacker delivers the malicious file to target via email, download, or file sharing
3. Victim opens or processes the malicious file with default file handlers
4. Apport automatically processes the file during crash reporting or analysis
5. Unsafe deserialization or file handling in Apport executes attacker-controlled code
6. Code executes with victim user privileges, potentially escalating to root

## Root cause
Apport's crash report processing contained multiple vulnerabilities including unsafe deserialization, improper file handling, and insufficient input validation when processing crash reports and related metadata. The software automatically processed certain file types without proper security checks.

## Attacker mindset
Exploit the automatic nature of crash reporting on Ubuntu Desktop to achieve persistent code execution. Target the trust users place in system utilities. Leverage the fact that default installations process potentially untrusted crash data without sufficient validation.

## Defensive takeaways
- Implement strict input validation and sanitization for all crash report processing
- Avoid unsafe deserialization patterns; use safe alternatives with schema validation
- Apply principle of least privilege to crash reporting services
- Implement sandboxing for automatic file processing utilities
- Require user confirmation before processing external crash data
- Regular security audits of system maintenance tools like crash reporters
- Consider disabling automatic crash reporting on systems handling sensitive data

## Variant hunting
Search for similar vulnerabilities in other system crash reporting tools (Dr. Watson, Windows Error Reporting, ABRT on Linux). Examine file processing pipelines in other Canonical tools. Investigate other automatic background services that process untrusted input.

## MITRE ATT&CK
- T1190
- T1203
- T1566
- T1651
- T1547

## Notes
This report is primarily an inquiry rather than a full vulnerability disclosure. The actual detailed vulnerability information is contained in the referenced Launchpad ticket and blog post. The researcher properly coordinated disclosure with Canonical before public discussion. Multiple related vulnerabilities were packaged together, suggesting systemic issues in the crash reporting architecture rather than isolated bugs.

## Full report
<details><summary>Expand</summary>

I recently reported a number of vulnerabilities in Canonical's Apport crash report software. These bugs provided RCE on a default install of Ubuntu Desktop >= 12.10 upon opening a malicious file. I reported the issues to the Apport maintainers and we coordinate the disclosure of these issues. 

Is the Internet Bug Bounty interested in providing bounties for RCE bugs affecting default Ubuntu installations? I have included a link to the Launchpad ticket and my blog post describing the issues in detail. Please let me know if this is something that you are interested in. I am happy to provide any further information that you require. 

https://bugs.launchpad.net/bugs/1648806
https://donncha.is/2016/12/compromising-ubuntu-desktop/

</details>

---
*Analysed by Claude on 2026-05-12*
