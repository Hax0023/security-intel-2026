# Nested Deserialization Leading to XXE in Magento (CVE-2024-34102)

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-18
- **Author:** Various
- **Program:** Adobe Magento / Adobe Commerce
- **Bounty:** Not specified
- **Severity:** Critical
- **Vuln types:** XML External Entity Injection (XXE), PHP Object Deserialization, Insecure Deserialization
- **Category:** web-api
- **Writeup:** https://www.assetnote.io/resources/research/why-nested-deserialization-is-harmful-magento-xxe-cve-2024-34102

## Summary
A critical pre-authentication XXE vulnerability exists in Magento 2 through unsafe nested deserialization of SimpleXMLElement objects with controllable parameters. The vulnerability allows attackers to exfiltrate sensitive files like app/etc/env.php containing cryptographic keys used for JWT authentication, enabling admin account takeover. When chained with PHP filter gadget chains (CVE-2024-2961), this can lead to remote code execution.

## Attack scenario (step by step)
1. Attacker identifies that Magento's deserialization process accepts serialized objects through public endpoints
2. Attacker crafts a gadget chain using deserialization to instantiate SimpleXMLElement with dataIsURL parameter set to true
3. The SimpleXMLElement constructor is invoked with a controlled XML payload containing XXE directives pointing to local files
4. XXE payload references app/etc/env.php file containing CRYPT_KEY used to sign admin JWTs
5. Attacker exfiltrates file contents through out-of-band channels or error-based XXE techniques
6. Attacker uses leaked CRYPT_KEY to forge admin JWT tokens and authenticate as administrator to abuse Magento APIs

## Root cause
Magento's deserialization mechanism allows arbitrary object instantiation through gadget chains, enabling attackers to reach SimpleXMLElement constructor with attacker-controlled arguments including dataIsURL flag, which enables remote/local XML loading and XXE exploitation.

## Attacker mindset
An attacker would recognize that complex PHP applications with extensive object hierarchies contain deserialization gadget chains. By analyzing public patches and diffs, they identify the vulnerable SimpleXMLElement instantiation pattern and craft serialized payloads to trigger XXE, ultimately targeting high-value credentials (cryptographic keys) for privilege escalation rather than simple file reads.

## Defensive takeaways
- Never deserialize untrusted data or implement strict type checking and allowlisting for deserialization
- Disable XXE in XML parsers by default (LIBXML_NOENT, LIBXML_DTDLOAD, etc.)
- Implement input validation on serialized objects before deserialization
- Review and test emergency security patches thoroughly with peer review before deployment
- Apply defense-in-depth: disable unnecessary XML features, restrict file access permissions, isolate sensitive credentials from application code
- Monitor for attempts to instantiate dangerous classes like SimpleXMLElement with suspicious parameters
- Use allowlists for permitted classes during deserialization operations

## Variant hunting
Search for other PHP applications using nested deserialization with SimpleXMLElement, DOMDocument, or Twig templating. Examine e-commerce platforms (WooCommerce, PrestaShop), CRM systems, and custom frameworks that deserialize user-supplied data. Investigate whether other classes in Magento accept URL-loading parameters during deserialization.

## MITRE ATT&CK
- T1190
- T1083
- T1005
- T1552
- T1078

## Notes
The vulnerability was discovered pre-patch by Sergey Temnikov and independently researched by Assetnote. The research highlights importance of peer review for emergency hotfixes - initial SanSec mitigation (blocking 'dataIsURL') could be bypassed, requiring iterative fixes. The broader XXE impact combined with JWT key exfiltration and RCE chaining via CVE-2024-2961 made this CVSS 9.8 critical. The diff analysis between patched (2.4.7-p1) and unpatched (2.4.7) versions was instrumental in understanding attack surface.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-18*
