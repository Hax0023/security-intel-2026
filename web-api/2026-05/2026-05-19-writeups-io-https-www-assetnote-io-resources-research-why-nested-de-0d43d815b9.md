# Nested Deserialization Leading to XXE in Magento (CVE-2024-34102)

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-19
- **Author:** Various
- **Program:** Adobe Commerce / Magento
- **Bounty:** Not specified in writeup
- **Severity:** critical
- **Vuln types:** XML External Entity (XXE) Injection, Unsafe Deserialization, Arbitrary File Read, Pre-authentication RCE (when chained with CVE-2024-2961)
- **Category:** web-api
- **Writeup:** https://www.assetnote.io/resources/research/why-nested-deserialization-is-harmful-magento-xxe-cve-2024-34102

## Summary
CVE-2024-34102 is a critical pre-authentication XXE vulnerability in Magento that exploits unsafe deserialization of SimpleXMLElement objects. Attackers can exfiltrate sensitive files including app/etc/env.php containing JWT signing keys, enabling admin account impersonation and potential RCE when chained with PHP filter chain vulnerabilities.

## Attack scenario (step by step)
1. Attacker discovers Magento deserialization gadget chain that instantiates SimpleXMLElement with controllable parameters
2. Attacker crafts malicious serialized payload embedding XXE payload with dataIsURL or sourceData parameters
3. Payload is sent to unauthenticated endpoint that triggers deserialization of attacker input
4. SimpleXMLElement constructor is invoked with malicious XML containing external entity references
5. Attacker exfiltrates app/etc/env.php containing cryptographic JWT signing key via out-of-band channels
6. Attacker uses extracted key to forge administrator JWT tokens and make authenticated API calls or chains with CVE-2024-2961 for RCE

## Root cause
Magento's deserialization process allows untrusted input to be reconstructed into PHP objects without proper validation. The gadget chain permits instantiation of SimpleXMLElement with user-controlled arguments, and PHP's SimpleXMLElement constructor supports dataIsURL flag enabling XML loading from external sources or local file inclusion via XXE.

## Attacker mindset
Attacker seeks to compromise high-value e-commerce platforms (140K+ Magento instances). The approach involves reverse-engineering from public patches, setting up development environments for gadget chain discovery, and chaining with existing exploits for maximum impact. The attacker recognizes that early PoC development before widespread awareness provides exploitation window.

## Defensive takeaways
- Never deserialize untrusted data directly; implement strict input validation before deserialization
- Disable XML external entity processing at application and system level (libxml_disable_entity_loader, LIBXML_NOENT restrictions)
- Block dangerous keywords in serialized payloads (dataIsURL, sourceData, DOCTYPE declarations)
- Implement allowlist-based object deserialization to restrict which classes can be instantiated
- Use WAF rules to detect XXE patterns and suspicious serialized object prefixes in POST bodies
- Apply defense-in-depth: even if first mitigation bypassed, secondary controls (keyword blocking) should catch variants
- Implement peer review and iterative testing process for emergency hotfixes as shown by SanSec/Sergey bypass cycles
- Monitor for deserialization gadget chains by analyzing third-party library dependencies

## Variant hunting
Search for other Magento/PHP applications that: (1) Accept serialized data from unauthenticated users, (2) Use SimpleXMLElement instantiation in gadget chains, (3) Lack proper XXE prevention controls, (4) Have similar nested deserialization patterns in custom payment processors or API handlers. Check for bypasses to keyword filtering (alternative XXE vectors, encoding tricks). Investigate CVE-2024-2961 PHP filter chain implementations for other dangerous gadget combinations.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1083 - File and Directory Discovery
- T1005 - Data from Local System
- T1041 - Exfiltration Over C2 Channel
- T1047 - Windows Management Instrumentation (or equivalent RCE via CVE-2024-2961)
- T1078 - Valid Accounts (JWT token forgery)
- T1027 - Obfuscated Files or Information (serialized payload encoding)

## Notes
Original discoverer: Sergey Temnikov. Vulnerability branded 'CosmicString' by SanSec. The writeup emphasizes importance of peer review - multiple iterations of hotfixes were bypassed, demonstrating why technical disclosure benefits broader security community. Researchers used docker-based Magento dev environment with XDebug/PhpStorm for gadget chain discovery. CVSS 9.8 rating justified by: (1) pre-authentication access, (2) JWT key extraction enabling admin impersonation, (3) chainability with CVE-2024-2961 for RCE, (4) estimated 140K+ vulnerable instances.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-19*
