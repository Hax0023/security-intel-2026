# Remote Code Execution via CVE-2017-1000486 in PrimeFaces 5.3.6

## Metadata
- **Source:** HackerOne
- **Report:** 874924 | https://hackerone.com/reports/874924
- **Submitted:** 2020-05-15
- **Reporter:** pwn1um
- **Program:** U.S. Department of Defense
- **Bounty:** Not specified in report
- **Severity:** CRITICAL
- **Vuln:** Weak Encryption, Insecure Deserialization, Remote Code Execution, Cryptographic Weakness
- **CVEs:** CVE-2017-1000486
- **Category:** memory-binary

## Summary
A DoD website was found running an outdated version of PrimeFaces 5.3.6, which is vulnerable to CVE-2017-1000486 due to weak encryption in the serialization mechanism. The vulnerability allows unauthenticated attackers to execute arbitrary code on the server by crafting malicious serialized objects. The researcher successfully demonstrated RCE by executing the 'whoami' command.

## Attack scenario
1. Attacker identifies target website running vulnerable PrimeFaces 5.x version
2. Attacker crafts malicious serialized Java object exploiting weak encryption in PrimeFaces serialization
3. Attacker sends crafted payload to vulnerable endpoint (typically ViewState parameter)
4. Server deserializes the object without proper validation due to weak encryption key
5. Malicious payload executes arbitrary code with application server privileges
6. Attacker gains remote code execution and can exfiltrate data or establish persistence

## Root cause
PrimeFaces 5.x uses weak encryption (hardcoded or easily guessable keys) to protect serialized objects. The deserialization process trusts the encrypted objects without sufficient validation, allowing attackers to decrypt, modify, and re-encrypt malicious payloads that execute code upon deserialization.

## Attacker mindset
An attacker would target government websites running outdated frameworks, knowing that legacy systems often lag in patching. The publicly available exploit lowers the barrier to entry, making this attractive for opportunistic or sophisticated adversaries targeting critical infrastructure.

## Defensive takeaways
- Maintain an up-to-date inventory of all third-party dependencies and frameworks
- Implement continuous vulnerability scanning to detect outdated library versions
- Apply security patches within defined SLAs, prioritizing critical/high severity vulnerabilities
- Use strong, unique encryption keys for serialization mechanisms
- Implement input validation and deserialization safeguards (e.g., FilteringObjectInputStream)
- Deploy Web Application Firewalls to detect and block exploitation attempts
- Conduct regular security assessments of government-facing applications
- Consider disabling dangerous Java deserialization features when possible

## Variant hunting
Search for other framework versions with similar weak encryption in serialization (Liferay, Spring, Struts). Audit custom serialization implementations in-house. Check for similar CVEs affecting other UI component libraries (e.g., Mojarra, OpenFaces). Review Java deserialization gadget chains across dependencies.

## MITRE ATT&CK
- T1190
- T1203
- T1059
- T1570
- T1195
- T1648

## Notes
The report lacks details on bounty amount and specific endpoint exploitation. The researcher's responsible disclosure appears minimal (only 'whoami' PoC). CVE-2017-1000486 has been known since 2017; the fact that a DoD website was still vulnerable indicates significant patching deficiencies. The public exploit availability increases risk significantly for all affected systems.

## Full report
<details><summary>Expand</summary>

**Summary:**
The targeted website is vulnerable to CVE-2017-1000486, by only running command was (whoami) to prove that the RCE exist has been run successfully on the target
**Description:**
The target uses a vulnerable version of primefaces : Primetek Primefaces 5.x, that is vulnerable to a weak encryption flaw resulting in remote code execution
## Impact
Critical
## Step-by-step Reproduction Instructions
Using the following exploit : https://github.com/pimps/CVE-2017-1000486
1. python primefaces.py████████/

## Product, Version, and Configuration (If applicable)
Primefaces 5.3.6
## Suggested Mitigation/Remediation Actions
Primefaces has to be updated to a newer version

## Impact

An attacker could execute remote codes on the target system, that could impact all of the CIA triad

</details>

---
*Analysed by Claude on 2026-05-12*
