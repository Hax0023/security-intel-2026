# Why Nested Deserialization is Harmful: Magento XXE (CVE-2024-34102)

## Metadata
- **Source:** writeups.io
- **Date:** 
- **Author:** Various
- **Program:** Magento
- **Bounty:** Unknown
- **Severity:** high
- **Vuln types:** XML External Entity (XXE) Injection, Unsafe Deserialization, Information Disclosure
- **Category:** web-api
- **Writeup:** https://www.assetnote.io/resources/research/why-nested-deserialization-is-harmful-magento-xxe-cve-2024-34102

## Summary
A XXE vulnerability in Magento was discovered through nested deserialization of untrusted XML data, allowing attackers to read sensitive files and perform information disclosure attacks. The vulnerability stems from improper handling of XML deserialization in Magento's core functionality without adequate XXE protections.

## Attack scenario (step by step)
1. Attacker identifies a Magento endpoint that accepts serialized data or XML input
2. Attacker crafts a malicious XML payload containing external entity definitions (XXE payload)
3. The payload is sent to the vulnerable deserialization function in Magento
4. Nested deserialization processes the XML without proper validation or XXE filtering
5. External entities are resolved, allowing file read operations (e.g., /etc/passwd, config files)
6. Attacker exfiltrates sensitive information from the server filesystem

## Root cause
Magento's deserialization mechanism does not properly disable XML external entity processing when handling nested or layered deserialized data structures. The vulnerability occurs when serialized data containing XML is deserialized multiple times without sanitization at each layer.

## Attacker mindset
An attacker would leverage this to perform reconnaissance, extract configuration files containing database credentials, API keys, or other sensitive data. The nested deserialization aspect is particularly attractive as it may bypass basic XXE protections applied only at the outermost layer.

## Defensive takeaways
- Disable XML external entity processing globally in XML parsers (libxml_disable_entity_loader, LIBXML_NOENT flags)
- Validate and sanitize data at each deserialization layer, not just the first level
- Implement allowlist-based deserialization to only permit expected object types
- Use secure alternatives to PHP serialization (JSON) where possible
- Apply XXE protections consistently across all XML processing functions
- Implement Web Application Firewall (WAF) rules to detect XXE payloads
- Regular security audits of serialization/deserialization code paths

## Variant hunting
['Search for other instances of nested deserialization in Magento extensions and plugins', 'Analyze SOAP/XML-RPC endpoints that may perform multiple deserialization passes', 'Review any code paths where serialized data is processed before final deserialization', 'Examine third-party libraries integrated with Magento for similar nested patterns', 'Check for XXE vulnerabilities in other e-commerce platforms using similar architecture']

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1083 - File and Directory Discovery
- T1005 - Data from Local System
- T1040 - Network Sniffing

## Notes
The research emphasizes how nested deserialization creates layers of processing that can bypass single-point XXE protections. This is particularly relevant for complex applications like Magento that may deserialize data multiple times across different processing stages. The CVE highlights a common architectural weakness in handling untrusted data transformations.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-11*
