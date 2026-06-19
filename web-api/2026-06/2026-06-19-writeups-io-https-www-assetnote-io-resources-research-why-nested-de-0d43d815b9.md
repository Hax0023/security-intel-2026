# Nested Deserialization Leading to XXE in Magento (CVE-2024-34102)

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-19
- **Author:** Various
- **Program:** Adobe Commerce/Magento
- **Bounty:** Not specified
- **Severity:** Critical
- **Vuln types:** XML External Entity (XXE) Injection, Unsafe Deserialization, Pre-authentication Remote Code Execution
- **Category:** web-api
- **Writeup:** https://www.assetnote.io/resources/research/why-nested-deserialization-is-harmful-magento-xxe-cve-2024-34102

## Summary
CVE-2024-34102 is a critical pre-authentication XXE vulnerability in Magento 2 (CVSS 9.8) that exploits unsafe nested deserialization of PHP objects containing SimpleXMLElement instantiation with attacker-controlled parameters. The vulnerability allows exfiltration of sensitive files including app/etc/env.php containing JWT cryptographic keys, enabling authentication bypass and admin impersonation. When chained with PHP filter gadgets (CVE-2024-2961), this can lead to remote code execution.

## Attack scenario (step by step)
1. Attacker identifies Magento installation vulnerable to CVE-2024-34102 (versions prior to 2.4.7-p1)
2. Attacker crafts malicious serialized PHP object containing SimpleXMLElement with dataIsURL parameter pointing to local file system or XXE payload
3. Attacker sends POST request with malicious serialized payload to vulnerable deserialization endpoint
4. Magento deserializes the object, instantiating SimpleXMLElement with attacker-controlled parameters, triggering XXE
5. Attacker exfiltrates app/etc/env.php file containing JWT signing key through XXE out-of-band channels or error messages
6. Attacker uses extracted key to forge valid admin JWT tokens and gain administrative access to Magento APIs

## Root cause
Magento's deserialization process allows instantiation of arbitrary PHP objects through gadget chains, ultimately reaching SimpleXMLElement constructor with insufficient validation of the dataIsURL parameter. This parameter enables loading XML from external sources or file system paths, enabling XXE attacks. The vulnerability stems from trusting user-supplied serialized data without proper sanitization before object reconstruction.

## Attacker mindset
Attacker recognizes that PHP deserialization vulnerabilities are powerful entry points if gadget chains exist. By examining public patches and diffs between vulnerable and patched versions, attacker reverse-engineers the vulnerability. The attacker understands that XXE combined with cryptographic key extraction allows lateral movement to admin access without needing direct RCE initially, and that chaining with known PHP gadgets enables full compromise.

## Defensive takeaways
- Never deserialize untrusted user input; use safer alternatives like JSON with strict schema validation
- Implement strict input validation on all serialized data before deserialization, including whitelist-based checks on expected object types
- Disable dangerous PHP features like SimpleXMLElement's dataIsURL parameter when handling external input
- Apply defense-in-depth: even if deserialization occurs, use WAF/IDS rules to detect XXE payloads (DOCTYPE declarations, SYSTEM/PUBLIC keywords)
- Restrict file system and network access at the application level; disable external entity resolution in XML parsers
- Regularly audit and update dependency libraries; implement gadget chain detection tools in CI/CD
- Apply principle of least privilege to service accounts to limit exposure if JWT keys are compromised
- Monitor for suspicious deserialization patterns in logs; implement real-time alerting for XXE detection
- Conduct thorough peer review of security patches; initial mitigations may be bypassed if incomplete

## Variant hunting
Hunters should examine other PHP frameworks and libraries using SimpleXMLElement constructor with user-controllable arguments. Search for deserialization gadget chains in popular packages (Symfony, Laravel, WordPress plugins) that might instantiate XML parsers. Investigate whether other Magento modules or extensions have similar unsafe deserialization patterns. Test whether dataIsURL parameter blocking can be bypassed via encoding, alternative method signatures, or other XML element initialization functions. Look for similar XXE patterns in services accepting serialized Java/Python objects that might support external entity resolution.

## MITRE ATT&CK
- T1190
- T1083
- T1005
- T1040
- T1070
- T1548

## Notes
This vulnerability was originally discovered by Sergey Temnikov and initially dubbed 'CosmicString' by SanSec. The research demonstrates the importance of technical disclosure and peer review for emergency security patches—both SanSec's initial mitigation (blocking dataIsURL) and early versions of Sergey's fix (blocking sourceData keyword) were found to be bypassable. The vulnerability is particularly dangerous due to: (1) pre-authentication exploitability, (2) direct access to cryptographic signing keys enabling admin impersonation, (3) chainability with CVE-2024-2961 PHP filter chains for RCE, and (4) no public POC existed at time of advisory, suggesting widespread unpatched installations. Researchers recommend studying the original CosmicString writeup by Sergey Temnikov for deeper understanding of Magento's deserialization architecture and inherent design flaws.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-19*
