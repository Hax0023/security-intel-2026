# Nested Deserialization Leading to XXE in Magento (CVE-2024-34102)

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-02
- **Author:** Various
- **Program:** Adobe Commerce / Magento
- **Bounty:** Not specified
- **Severity:** Critical
- **Vuln types:** XML External Entity (XXE) Injection, Insecure Deserialization, Pre-authentication Remote Code Execution (via chaining)
- **Category:** web-api
- **Writeup:** https://www.assetnote.io/resources/research/why-nested-deserialization-is-harmful-magento-xxe-cve-2024-34102

## Summary
CVE-2024-34102 is a critical pre-authentication XXE vulnerability in Magento 2 that allows attackers to exfiltrate sensitive files including app/etc/env.php containing JWT cryptographic keys. The vulnerability stems from unsafe deserialization gadget chains that instantiate SimpleXMLElement with attacker-controlled arguments, enabling external entity loading and file disclosure.

## Attack scenario (step by step)
1. Attacker identifies Magento installation and sends POST request containing serialized PHP object with malicious deserialization gadget chain
2. Gadget chain triggers instantiation of SimpleXMLElement with controlled parameters including XXE payload
3. SimpleXMLElement constructor loads external XML entity or file reference specified via dataIsURL or direct file path
4. Attacker exfiltrates app/etc/env.php containing JWT signing keys and database credentials
5. Attacker uses extracted JWT key to forge administrative authentication tokens
6. Attacker abuses Magento APIs as administrator to execute further attacks or chains with CVE-2024-2961 PHP filter chains for RCE

## Root cause
Magento's deserialization process uses unsafe gadget chains that eventually instantiate SimpleXMLElement with user-controlled serialized data. The SimpleXMLElement constructor accepts dataIsURL parameter enabling external entity resolution. Insufficient input validation and nested deserialization without type checking allows attackers to craft malicious serialized payloads that traverse the gadget chain to reach the XXE-vulnerable SimpleXMLElement instantiation.

## Attacker mindset
Methodical vulnerability researcher discovering complex deserialization chains through code diffing, documentation analysis, and systematic gadget chain hunting. Attacker recognizes that bypassing initial patches requires understanding the root cause rather than surface-level mitigations, enabling rapid pivot to alternative exploitation paths.

## Defensive takeaways
- Avoid deserializing untrusted data or implement strict input validation before deserialization
- Disable external entity resolution in XML parsers (XXE prevention via libxml_disable_entity_loader or similar)
- Remove or restrict access to dangerous deserialization gadget chains through class whitelisting
- Implement comprehensive input sanitization to block gadget chain trigger keywords recursively (not just simple string blocking)
- Apply defense-in-depth: use allowlists for expected serialized object types and validate object properties after deserialization
- Peer review emergency hotfixes and security patches rigorously before deployment
- Monitor and restrict access to sensitive configuration files like env.php through file permissions and security groups
- Implement JWT key rotation and avoid embedding keys in plaintext configuration files
- Apply principle of least privilege to API endpoints and authentication mechanisms

## Variant hunting
Search for other PHP applications using SimpleXMLElement with user-controlled input. Examine deserialization entry points in frameworks like Laravel, Symfony, and WordPress plugins. Hunt for gadget chains in popular PHP libraries (Symfony DependencyInjection, Laravel Serialization, Monolog) that could chain to XXE-vulnerable XML operations. Test alternative bypasses to XXE mitigations (e.g., wrapper protocols like php://, file:// with null bytes, CDATA sections).

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1566 - Phishing (social engineering to identify Magento instances)
- T1005 - Data from Local System (file exfiltration via XXE)
- T1041 - Exfiltration Over C2 Channel (XXE data exfiltration)
- T1027 - Obfuscated Files or Information (serialized gadget chains)
- T1140 - Deobfuscate/Decode Files or Information (PHP deserialization analysis)
- T1621 - Multi-Stage Channels (XXE to RCE via CVE-2024-2961 chaining)

## Notes
The vulnerability is particularly severe due to the ability to extract JWT signing keys enabling authenticated privilege escalation without credentials. The research demonstrates the importance of peer review in emergency patches - initial mitigations blocking 'dataIsURL' proved bypassable. SanSec and Sergey Temnikov iterated multiple times before reaching a robust fix blocking 'sourceData'. This CVE exemplifies modern complex deserialization vulnerabilities requiring gadget chain analysis and deep framework knowledge. The ProofOfConcept was developed before public disclosure, suggesting advanced adversaries likely weaponized this during the advisory window. Estimated 140,000+ vulnerable Magento instances represents significant attack surface.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-02*
