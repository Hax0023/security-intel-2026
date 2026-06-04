# Nested Deserialization Leading to XXE in Magento (CVE-2024-34102)

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-04
- **Author:** Various
- **Program:** Adobe Magento / Adobe Commerce
- **Bounty:** Not specified in writeup
- **Severity:** Critical
- **Vuln types:** XML External Entity (XXE) Injection, Unsafe Deserialization, Pre-authentication Remote Code Execution
- **Category:** web-api
- **Writeup:** https://www.assetnote.io/resources/research/why-nested-deserialization-is-harmful-magento-xxe-cve-2024-34102

## Summary
CVE-2024-34102 is a critical pre-authentication XXE vulnerability in Magento 2 that allows attackers to exfiltrate sensitive files including app/etc/env.php containing cryptographic keys used for JWT signing. The vulnerability stems from unsafe deserialization of user-controlled input that instantiates SimpleXMLElement with controllable parameters, enabling XXE attacks and potential RCE when chained with PHP filter gadget chains.

## Attack scenario (step by step)
1. Attacker sends specially crafted XML payload to Magento endpoint with nested deserialization gadgets
2. Payload triggers instantiation of SimpleXMLElement class with dataIsURL or sourceData parameters under attacker control
3. SimpleXMLElement processes external XML entity references, loading remote or local file content
4. Attacker exfiltrates app/etc/env.php file containing JWT cryptographic signing keys
5. Attacker uses extracted keys to forge valid administrator JWT tokens
6. Attacker uses forged admin JWT to call Magento APIs with administrative privileges for further compromise

## Root cause
Magento's deserialization process unsafely instantiates PHP's SimpleXMLElement class with user-controlled parameters derived from POST request bodies. The vulnerability allows specification of dataIsURL or sourceData parameters which enable XXE by loading external XML entities. Multiple layers of nested deserialization gadget chains obscure the vulnerability from initial analysis.

## Attacker mindset
An attacker discovers this vulnerability through diff analysis between patched and unpatched versions, identifying SimpleXMLElement instantiation as the critical sink. They recognize that blocking single parameters (like dataIsURL) is insufficient, and the vulnerability can be exploited through alternative parameters or gadget chain permutations. The attacker views this as a pre-auth RCE opportunity targeting one of the internet's most popular e-commerce platforms with 140k+ instances.

## Defensive takeaways
- Avoid deserialization of untrusted user input entirely; use safe data formats like JSON with strict parsing
- If deserialization is necessary, use allowlists for permitted classes and implement strict input validation
- Disable XML external entity processing at the parser level (libxml_disable_entity_loader) before processing any XML
- Block dangerous parameter names at multiple layers, not just one keyword, as attackers can find alternative parameter names
- Implement peer review and iterative testing of emergency security patches before release
- Monitor for gadget chain exploitation by logging unusual class instantiations during deserialization
- Apply security patches immediately; CVSS 9.8 pre-auth vulnerabilities are actively exploited
- Consider breaking complex deserialization chains by using intermediate safe transformation steps

## Variant hunting
Search for other Magento endpoints accepting XML/serialized data that flow through deserialization handlers. Investigate alternative gadget chains leading to SimpleXMLElement or other XML processors. Test whether XXE filtering can be bypassed through parameter pollution, case variations, or encoding bypasses. Hunt for similar nested deserialization patterns in other Adobe products and PHP frameworks using SimpleXMLElement.

## MITRE ATT&CK
- T1190
- T1083
- T1552
- T1059

## Notes
SanSec's initial mitigation blocking dataIsURL was incomplete; Sergey Temnikov's refined mitigation blocking sourceData was more effective but still required peer review iteration. The vulnerability was dubbed 'CosmicString' by SanSec. The writeup emphasizes importance of technical disclosure for security industry peer review. Chainable with CVE-2024-2961 PHP filter gadget chains for RCE. Research team developed PoC before public exploits emerged despite CVSS 9.8 criticality rating.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-04*
