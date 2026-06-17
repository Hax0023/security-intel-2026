# Magento XXE via Nested Deserialization (CVE-2024-34102)

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-17
- **Author:** Various
- **Program:** Adobe Magento/Adobe Commerce
- **Bounty:** Not specified
- **Severity:** CRITICAL
- **Vuln types:** XML External Entity Injection (XXE), Insecure Deserialization, Local File Disclosure, Pre-authentication RCE (via chaining)
- **Category:** web-api
- **Writeup:** https://www.assetnote.io/resources/research/why-nested-deserialization-is-harmful-magento-xxe-cve-2024-34102

## Summary
A critical pre-authentication XXE vulnerability in Magento 2 allows attackers to exploit unsafe PHP deserialization to instantiate SimpleXMLElement with controllable arguments. The vulnerability enables exfiltration of sensitive files including app/etc/env.php (containing JWT signing keys) and can be chained with PHP filter exploits for remote code execution.

## Attack scenario (step by step)
1. Attacker identifies Magento endpoint that accepts serialized PHP objects in requests
2. Attacker crafts malicious serialized payload containing gadget chain leading to SimpleXMLElement instantiation
3. Payload is submitted with dataIsURL or sourceData parameters pointing to external XXE payloads
4. Deserialization triggers gadget chain, instantiating SimpleXMLElement with attacker-controlled XML
5. XXE payload exfiltrates app/etc/env.php containing JWT signing key via out-of-band channel
6. Attacker uses extracted key to forge admin JWT token and gain administrative API access

## Root cause
Magento's deserialization process uses unsafe gadget chains that allow instantiation of SimpleXMLElement with arbitrary constructor arguments. The application does not properly validate or sanitize deserialized object parameters, allowing XXE exploitation through nested object instantiation. PHP's SimpleXMLElement constructor accepts dataIsURL and sourceData parameters that enable external entity loading.

## Attacker mindset
Methodical vulnerability researcher leveraging public advisory information and binary diffing to reverse-engineer exploitation technique. Attacker recognizes that complex deserialization chains in popular frameworks create attack surface and focuses on chaining XXE with JWT key theft to achieve privilege escalation without authentication.

## Defensive takeaways
- Avoid deserializing untrusted data; use JSON with strict schema validation instead of PHP serialization
- Implement strict input validation on all deserialization gadget chain entry points
- Disable XXE-vulnerable classes (SimpleXMLElement with dataIsURL) or strictly validate their instantiation
- Use allowlists for which classes can be instantiated during deserialization
- Implement defense-in-depth by restricting file access and disabling URL wrappers (allow_url_fopen)
- Rotate cryptographic keys (JWT signing keys) regularly and store separately from application code
- Apply vendor patches immediately for critical deserialization vulnerabilities
- Monitor for bypass attempts when implementing emergency hotfixes through peer review

## Variant hunting
Search for similar nested deserialization patterns in other PHP frameworks. Look for gadget chains instantiating SimpleXMLElement, DOMDocument, or similar XML classes. Examine other parameters beyond dataIsURL (sourceData, etc.) that enable XXE. Check for deserialization entry points in APIs accepting serialized objects. Investigate whether similar JWT key exfiltration patterns exist in other e-commerce platforms.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1083 - File and Directory Discovery
- T1005 - Data from Local System
- T1041 - Exfiltration Over C2 Channel
- T1078 - Valid Accounts (JWT token forgery)
- T1203 - Exploitation for Client Execution
- T1059 - Command and Scripting Interpreter

## Notes
The research demonstrates the importance of technical disclosure for security hardening. Multiple emergency hotfix attempts were bypassed (blocking only dataIsURL, then sourceData), showing that comprehensive mitigations require deep understanding of underlying gadget chains. The vulnerability's CVSS 9.8 rating reflects pre-authentication + critical impact (RCE via chaining). The 140,000+ Magento instances provided massive attack surface. Binary diffing of patched vs unpatched versions was effective reconnaissance technique. Researchers recommend debugger-assisted development environment setup for complex deserialization analysis.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-17*
