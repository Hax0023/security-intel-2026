# Nested Deserialization Leading to XXE in Magento (CVE-2024-34102)

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-10
- **Author:** Various
- **Program:** Adobe Magento/Adobe Commerce
- **Bounty:** Not specified in writeup
- **Severity:** critical
- **Vuln types:** XML External Entity (XXE) Injection, Unsafe Deserialization, Object Instantiation via Gadget Chain, Pre-authentication Remote Code Execution
- **Category:** web-api
- **Writeup:** https://www.assetnote.io/resources/research/why-nested-deserialization-is-harmful-magento-xxe-cve-2024-34102

## Summary
CVE-2024-34102 is a critical pre-authentication XXE vulnerability in Magento 2 that exploits unsafe deserialization of SimpleXMLElement objects through a gadget chain. The vulnerability allows attackers to exfiltrate sensitive files including app/etc/env.php containing cryptographic keys, which can be chained with PHP filter exploits (CVE-2024-2961) for remote code execution. The flaw stems from Magento's deserialization process accepting user-controlled arguments to instantiate SimpleXMLElement with dataIsURL parameters.

## Attack scenario (step by step)
1. Attacker identifies Magento endpoint that deserializes user-supplied PHP objects without validation
2. Attacker crafts malicious serialized payload containing a gadget chain leading to SimpleXMLElement instantiation with dataIsURL parameter
3. Attacker sends payload via POST request to trigger deserialization process
4. SimpleXMLElement is instantiated with attacker-controlled URL/XML data containing XXE payloads
5. XXE payload references external DTD or local file entities to exfiltrate app/etc/env.php
6. Attacker retrieves JWT signing key from env.php and forges admin authentication tokens for API abuse or chains with PHP filters for RCE

## Root cause
Magento's deserialization process accepts nested object instantiation without proper validation of constructor arguments. The SimpleXMLElement class constructor accepts a dataIsURL parameter that enables loading XML from external sources, creating an XXE gadget point. The vulnerability exists because: (1) user input flows through deserialization without sanitization, (2) no blocklist or allowlist of instantiable classes exists, (3) SimpleXMLElement constructor is exploitable via nested deserialization.

## Attacker mindset
An attacker targeting e-commerce platforms recognizes that Magento powers 140,000+ instances and represents high-value targets. Pre-authentication exploitation is attractive as it requires no initial access. The attacker seeks to either steal JWT keys for admin impersonation or achieve direct RCE through chained exploits. The gadget chain approach is methodical - finding legitimate classes that when instantiated with attacker-controlled arguments lead to XXE.

## Defensive takeaways
- Implement strict deserialization controls: use allowlists of safe classes, never deserialize untrusted data, or avoid PHP's unserialize() on user input entirely
- Disable XXE-vulnerable XML parsing features: set libxml_disable_entity_loader(true), use XMLReader with proper DTD restrictions, disable LIBXML_NOENT and LIBXML_DTDLOAD flags
- Validate all constructor arguments before instantiation: ensure SimpleXMLElement and similar XML classes receive only safe, validated input
- Apply input validation at deserialization boundaries: sanitize or reject payloads containing suspicious keywords like 'dataIsURL' and 'sourceData' before processing
- Use wrapper validation: block specific gadget chain patterns through WAF rules or application-layer checks before deserialization
- Implement comprehensive testing: fuzzing deserialization endpoints, reviewing diff patches for similar vulnerabilities, and peer-reviewing security patches
- Defense-in-depth layering: combine blocklists (dataIsURL, sourceData) with type restrictions and sandboxing
- Monitor for bypass techniques: as SanSec and Sergey Temnikov discovered, initial patches were bypassable; continuous monitoring of bypass research is essential

## Variant hunting
Search for: (1) Other PHP classes with constructor parameters enabling XXE or RCE (SimpleXML, DOMDocument, Twig templates), (2) Alternative gadget chains to SimpleXMLElement instantiation in Magento codebase, (3) Similar nested deserialization vulnerabilities in other PHP frameworks (Laravel, Symfony, Yii), (4) Variations of XXE gadgets in commonly used libraries (Monolog, Guzzle, PHPMailer), (5) PHP filter chains that can be chained with XXE for information disclosure/RCE without needing CVE-2024-2961, (6) Other Adobe products using similar unsafe deserialization patterns

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1611 - Escape to Host
- T1083 - File and Directory Discovery
- T1005 - Data from Local System
- T1041 - Exfiltration Over C2 Channel
- T1078 - Valid Accounts
- T1550.004 - Use Alternate Authentication Material: Web Session Cookie

## Notes
This vulnerability is particularly dangerous because: (1) it requires no authentication, (2) Magento's widespread deployment creates massive attack surface, (3) compromised JWT keys enable persistent admin-level access, (4) chaining with CVE-2024-2961 enables RCE without alternative PHP filter chains needed, (5) initial emergency patches by SanSec and Sergey Temnikov were bypassable, demonstrating that blocklist-based mitigations are fragile. The discovery methodology - using diff analysis between patched/unpatched versions combined with code review - is highly effective for reverse-engineering vulnerabilities from patches. This case study demonstrates why full technical disclosure post-patch is valuable: iterative community review identified bypass techniques and strengthened mitigations. The vulnerability exemplifies how modern application vulnerabilities often chain deserialization flaws with class-specific gadgets (XXE) and follow-up exploitation vectors (RCE via PHP filters) into multi-stage attacks.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-10*
