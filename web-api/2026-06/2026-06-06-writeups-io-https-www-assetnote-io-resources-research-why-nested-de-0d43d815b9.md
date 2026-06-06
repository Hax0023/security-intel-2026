# Nested Deserialization Leading to XXE in Magento (CVE-2024-34102)

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-06
- **Author:** Various
- **Program:** Adobe Commerce / Magento
- **Bounty:** Not specified
- **Severity:** critical
- **Vuln types:** XML External Entity Injection (XXE), Unsafe Deserialization, Object Injection, Local File Inclusion
- **Category:** web-api
- **Writeup:** https://www.assetnote.io/resources/research/why-nested-deserialization-is-harmful-magento-xxe-cve-2024-34102

## Summary
CVE-2024-34102 is a pre-authentication XXE vulnerability in Magento 2 caused by unsafe deserialization of SimpleXMLElement objects with controllable parameters. Attackers can exfiltrate sensitive files like app/etc/env.php containing cryptographic JWT signing keys, enabling unauthorized admin access. The vulnerability is chainable with PHP filter chain exploits (CVE-2024-2961) for potential RCE.

## Attack scenario (step by step)
1. Attacker identifies Magento installation vulnerable to CVE-2024-34102 via HTTP probing
2. Attacker crafts malicious serialized PHP object containing SimpleXMLElement instantiation with XXE payload
3. Attacker sends POST request with crafted object to exploitable Magento endpoint (pre-authentication)
4. Magento deserializes the malicious object, triggering SimpleXMLElement constructor with attacker-controlled arguments including external entity references
5. XXE parser processes entity declarations and exfiltrates app/etc/env.php file containing JWT signing key
6. Attacker uses extracted key to forge admin JWT tokens and compromise application or chain with CVE-2024-2961 for RCE

## Root cause
Magento's deserialization process instantiates SimpleXMLElement with user-controlled arguments without proper validation. PHP's SimpleXMLElement constructor accepts a 'dataIsURL' parameter that enables loading XML from remote sources and processes entity declarations by default, enabling XXE attacks. The vulnerability stems from nested deserialization gadgets that reach SimpleXMLElement instantiation without sanitization.

## Attacker mindset
An attacker would recognize that Magento's complex object deserialization chain presents a promising attack surface. By analyzing public diffs and emergency patches, they can reverse-engineer the vulnerability mechanics. The pre-authentication nature and access to sensitive cryptographic material makes this highly attractive for lateral movement and privilege escalation in compromised infrastructure.

## Defensive takeaways
- Never deserialize untrusted data; use JSON or other explicitly structured formats
- When deserialization is necessary, implement strict allowlists of permitted classes
- Disable XXE processing in XML parsers by default (libxml_disable_entity_loader, LIBXML_NOENT flags)
- Validate and sanitize all parameters passed to object constructors in deserialization chains
- Implement defense-in-depth: limit access to deserialization endpoints, require authentication where possible
- Monitor for suspicious object instantiation patterns in logs and runtime monitoring
- Conduct thorough code review when patching deserialization vulnerabilities; multiple iterations were required here
- Rotate cryptographic keys stored in configuration files (app/etc/env.php) regularly
- Use principle of least privilege for JWT signing keys and sensitive credentials

## Variant hunting
Look for other PHP applications using SimpleXMLElement deserialization chains; search for gadgets leading to DOMDocument or SimpleXML instantiation; examine other serialization libraries (YAML, msgpack) in frameworks for similar nested deserialization chains; test file inclusion gadgets that reach filesystem operations; identify XXE-enabling XML parsers in dependency chains with libxml2 configurations

## MITRE ATT&CK
- T1190
- T1105
- T1565
- T1552
- T1070
- T1068
- T1548

## Notes
This vulnerability is particularly severe due to: (1) pre-authentication exploitability requiring no credentials, (2) direct access to JWT signing keys enabling admin account takeover, (3) chainability with other vulnerabilities for RCE, (4) widespread deployment (140k+ instances). The research demonstrates the value of analyzing patch diffs and peer review in security fixes - initial hotfixes were bypassable, requiring iterative improvements. The discovery methodology (debugging with XDebug, analyzing deserialization gadget chains) is methodical and reproducible for similar vulnerabilities in other systems.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-06*
