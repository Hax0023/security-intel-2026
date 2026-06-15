# Magento XXE via Nested Deserialization (CVE-2024-34102)

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-15
- **Author:** Various
- **Program:** Adobe Commerce / Magento
- **Bounty:** Not specified
- **Severity:** critical
- **Vuln types:** XML External Entity Injection (XXE), Unsafe Deserialization, Pre-authentication Remote Code Execution, Local File Inclusion
- **Category:** web-api
- **Writeup:** https://www.assetnote.io/resources/research/why-nested-deserialization-is-harmful-magento-xxe-cve-2024-34102

## Summary
CVE-2024-34102 is a critical pre-authentication XXE vulnerability in Magento 2.4.7 that exploits unsafe deserialization through SimpleXMLElement instantiation. Attackers can exfiltrate sensitive files including app/etc/env.php containing JWT cryptographic keys, enabling authentication bypass and admin impersonation. The vulnerability chains with PHP filter exploits (CVE-2024-2961) to achieve remote code execution.

## Attack scenario (step by step)
1. Attacker crafts a malicious XML payload containing XXE entities targeting the Magento deserialization endpoint
2. Payload is sent to a pre-authentication endpoint that triggers deserialization through a gadget chain
3. The gadget chain instantiates SimpleXMLElement with attacker-controlled arguments including dataIsURL parameter
4. SimpleXMLElement loads external XML containing entity definitions that reference local files (e.g., app/etc/env.php)
5. File contents are exfiltrated via XXE to attacker-controlled server or embedded in error responses
6. Attacker uses extracted JWT cryptographic key to forge administrator tokens for API abuse or chains with PHP filter RCE

## Root cause
Magento's deserialization mechanism allows nested instantiation of PHP objects through gadget chains. When SimpleXMLElement is instantiated during deserialization with user-controlled parameters, the dataIsURL parameter enables loading XML from external sources. The vulnerability stems from insufficient validation of serialized data before deserialization and lack of restrictions on which classes can be instantiated.

## Attacker mindset
An attacker would recognize that Magento's popularity (140,000+ instances) makes it a high-value target. The pre-authentication nature removes barriers to entry. The ability to extract JWT signing keys transforms a data exfiltration bug into complete authentication bypass. Chaining with CVE-2024-2961 provides a path to RCE, making this a complete takeover primitive. The attacker would be motivated by the minimal requirements and maximum impact.

## Defensive takeaways
- Never deserialize untrusted data without strict class whitelisting and object property validation
- Implement input validation before deserialization to detect and reject malicious serialized objects
- Disable or restrict dangerous PHP functions like SimpleXMLElement with dataIsURL in production contexts
- Use security review and peer review for emergency hotfixes - initial mitigations were bypassable
- Segment sensitive files (env.php, keys) from web-accessible contexts and apply defense-in-depth file access controls
- Monitor for XXE patterns in logs and implement Web Application Firewalls to detect entity injection attempts
- Maintain comprehensive deserialization gadget maps and regularly audit codebase for exploitable chains
- Disclose technical details of vulnerabilities to enable industry-wide detection and fix validation

## Variant hunting
Search for other Magento deserialization endpoints and gadget chains. Investigate other PHP applications using SimpleXMLElement in deserialization contexts (Laravel, Symfony, custom frameworks). Look for similar nested object instantiation patterns where constructor arguments are user-controlled. Examine other Adobe products for comparable XXE through deserialization. Hunt for bypass techniques around sourceData filtering and other mitigation approaches.

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1083: File and Directory Discovery
- T1005: Data from Local System
- T1041: Exfiltration Over C2 Channel
- T1078: Valid Accounts
- T1550: Use Alternate Authentication Material
- T1203: Exploitation for Client Execution

## Notes
The vulnerability is particularly dangerous due to: (1) pre-authentication requirement eliminated, (2) direct access to JWT cryptographic material enabling complete authentication bypass, (3) chainable with CVE-2024-2961 for RCE, (4) massive attack surface with 140,000+ Magento instances. The research methodology was sound - using diff analysis to identify patch locations, then leveraging Docker with XDebug for interactive exploitation. The observation that multiple iterations of hotfixes were bypassable demonstrates the critical importance of technical disclosure and peer review in security patches rather than security-through-obscurity approaches.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-15*
