# Magento XXE via Nested Deserialization (CVE-2024-34102)

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-22
- **Author:** Various
- **Program:** Adobe Commerce / Magento
- **Bounty:** Not specified
- **Severity:** Critical
- **Vuln types:** XML External Entity Injection (XXE), Insecure Deserialization, Local File Inclusion, Pre-authentication Remote Code Execution
- **Category:** web-api
- **Writeup:** https://www.assetnote.io/resources/research/why-nested-deserialization-is-harmful-magento-xxe-cve-2024-34102

## Summary
CVE-2024-34102 is a critical pre-authentication XXE vulnerability in Magento 2.4.7 that exploits unsafe deserialization leading to instantiation of SimpleXMLElement with controllable arguments. The vulnerability enables attackers to exfiltrate sensitive files including app/etc/env.php (containing JWT signing keys) and can be chained with PHP filter exploits (CVE-2024-2961) for remote code execution.

## Attack scenario (step by step)
1. Attacker identifies Magento instance and locates a deserialization gadget chain that instantiates SimpleXMLElement with user-controlled parameters
2. Attacker crafts malicious serialized PHP object containing XXE payload with dataIsURL parameter set to load external XML
3. Attacker sends POST request with crafted serialized payload to vulnerable Magento endpoint (pre-authentication)
4. Magento deserializes the payload and instantiates SimpleXMLElement with attacker-controlled XML source pointing to local file (app/etc/env.php)
5. XXE vulnerability allows XML parser to read and exfiltrate the contents of env.php containing database credentials and JWT signing key
6. Attacker uses extracted JWT key to forge administrator authentication tokens and abuse Magento APIs, or chains with CVE-2024-2961 for RCE

## Root cause
Magento's deserialization process lacks sufficient input validation when instantiating SimpleXMLElement objects. The vulnerability chain allows attackers to reach the SimpleXMLElement constructor with controllable arguments, specifically the dataIsURL parameter which permits loading XML from external/local sources. The nested deserialization mechanism compounds this by providing multiple gadget chain paths to reach unsafe object instantiation.

## Attacker mindset
Reconnaissance-focused: Attacker analyzes public vulnerability advisories and diffs between patched/unpatched versions to identify root cause. Persistence-oriented: Attacker develops working POC and chains multiple CVEs together. Opportunistic: Pre-authentication nature means widespread exploitation potential against 140,000+ Magento instances without requiring valid credentials.

## Defensive takeaways
- Implement strict input validation and sanitization on all deserialization operations, not just blocking specific keywords like dataIsURL or sourceData
- Use allowlist-based approach for deserialization rather than blocklist, as attackers can find alternative paths (as seen with SanSec's bypassed mitigations)
- Avoid deserializing untrusted user input; consider using safer serialization formats (JSON) instead of PHP serialization
- Conduct peer review of security patches and hotfixes before deployment to identify bypasses
- Monitor for XXE-related gadget chains in popular libraries and frameworks
- Implement network-level controls to prevent XXE exfiltration (block outbound entity resolution)
- Disable XML external entity processing at the parser level where possible
- Regularly audit deserialization gadget chains in dependency libraries using tools like phpggc

## Variant hunting
Search for other Magento deserialization points that instantiate objects with external data loading capability (DOM, SimpleXML alternatives). Examine other PHP frameworks using similar nested deserialization patterns. Look for XXE gadget chains in popular PHP libraries (Symfony, Laravel, Doctrine) that may instantiate XML parsers through object deserialization. Test other e-commerce platforms with PHP/serialization-based architectures.

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1566: Phishing (for initial access in advanced scenarios)
- T1552: Unsecured Credentials (exfiltration of env.php)
- T1005: Data from Local System
- T1041: Exfiltration Over C2 Channel
- T1027: Obfuscation of Files or Information (serialized gadget chains)
- T1078: Valid Accounts (JWT token forgery for lateral movement)

## Notes
The vulnerability was discovered by Sergey Temnikov and dubbed 'CosmicString' by SanSec. The research demonstrates the critical importance of: (1) understanding how patch diffs reveal vulnerability mechanics, (2) setting up proper debugging environments for complex deserialization issues, (3) iterative security patching as initial mitigations (blocking dataIsURL) proved bypassable. Multiple bypass iterations of emergency hotfixes show that keyword blocking is insufficient and comprehensive input validation is required. The XXE can be chained with CVE-2024-2961 PHP filter chains for RCE, significantly amplifying impact from data exfiltration to code execution.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-22*
