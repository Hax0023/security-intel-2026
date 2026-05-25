# Nested Deserialization Leading to XXE in Magento (CVE-2024-34102)

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-25
- **Author:** Various
- **Program:** Adobe Magento / Adobe Commerce
- **Bounty:** Not specified
- **Severity:** critical
- **Vuln types:** XML External Entity (XXE) Injection, Unsafe Deserialization, Local File Inclusion
- **Category:** web-api
- **Writeup:** https://www.assetnote.io/resources/research/why-nested-deserialization-is-harmful-magento-xxe-cve-2024-34102

## Summary
CVE-2024-34102 is a pre-authentication XXE vulnerability in Magento stemming from unsafe deserialization that instantiates SimpleXMLElement with controllable parameters, allowing attackers to exfiltrate sensitive files including app/etc/env.php containing JWT cryptographic keys. The vulnerability can be chained with PHP filter chains (CVE-2024-2961) to achieve remote code execution on affected Magento installations.

## Attack scenario (step by step)
1. Attacker identifies a deserialization gadget chain in Magento that leads to SimpleXMLElement instantiation with controllable arguments
2. Attacker crafts malicious serialized PHP object with XXE payload containing external entity references targeting app/etc/env.php
3. Attacker sends crafted payload via POST request to vulnerable Magento endpoint without authentication
4. Deserialization process instantiates SimpleXMLElement with dataIsURL parameter set to true, loading external XML entity
5. Server exfiltrates file contents via out-of-band channel or error messages, revealing JWT cryptographic key
6. Attacker uses extracted key to forge administrator JWT tokens and abuse Magento APIs with elevated privileges, optionally chaining to RCE

## Root cause
Magento's deserialization process unsafely instantiates SimpleXMLElement class with user-controlled parameters. The dataIsURL parameter allows loading XML from external sources, and the sourceData parameter can be manipulated to trigger XXE conditions. Initial mitigations only blocked dataIsURL keyword, but the vulnerability remained exploitable through alternative code paths.

## Attacker mindset
Sophisticated adversary targeting high-value e-commerce infrastructure. Recognized that while public advisory existed without PoC, the CVSS 9.8 rating indicated pre-authentication RCE potential. Leveraged publicly available mitigation bypass information to develop working exploit, demonstrating that incomplete patches create false sense of security.

## Defensive takeaways
- Never use SimpleXMLElement or XML parsing functions with user-controlled data, especially with dataIsURL/external entity loading enabled
- Implement strict input validation on all deserialization entry points, not just keyword blacklisting
- Disable XXE processing globally at the XML parser level (libxml_disable_entity_loader) rather than application-level filtering
- Require authentication for deserialization endpoints whenever possible
- Implement peer review process for emergency security patches before release to catch bypass vectors
- Consider using JSON instead of serialized PHP objects for data transmission
- Monitor for suspicious deserialization patterns in application logs
- Keep cryptographic keys separate from application configuration files and use secrets management solutions

## Variant hunting
Look for other Magento gadget chains leading to different object instantiations with external resource loading capabilities. Search for similar nested deserialization patterns in other PHP frameworks (Symfony, Laravel, WordPress plugins). Investigate whether similar XXE patterns exist in other Adobe products. Test whether initial mitigation patches in competing e-commerce platforms (WooCommerce, Shopify) have similar bypass potential through keyword-only filtering approaches.

## MITRE ATT&CK
- T1190
- T1105
- T1040
- T1003
- T1087
- T1078

## Notes
This vulnerability demonstrates the critical importance of technical disclosure for security research peer review. Multiple iterations of patches were required as initial mitigations proved bypassable. The chaining potential with CVE-2024-2961 (PHP filter chains) elevates risk from information disclosure to RCE. The CosmicString designation by SanSec suggests this may be tracked as a known exploit in the wild. Over 140,000 Magento instances globally creates massive attack surface. Researchers properly followed coordinated disclosure before publishing full PoC.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-25*
