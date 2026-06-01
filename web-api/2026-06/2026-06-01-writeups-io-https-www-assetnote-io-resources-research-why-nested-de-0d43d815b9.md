# Nested Deserialization Leading to XXE in Magento (CVE-2024-34102)

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-01
- **Author:** Various
- **Program:** Adobe Magento / Adobe Commerce
- **Bounty:** Not specified
- **Severity:** Critical
- **Vuln types:** XML External Entity Injection (XXE), Unsafe Deserialization, Pre-authentication Remote Code Execution
- **Category:** web-api
- **Writeup:** https://www.assetnote.io/resources/research/why-nested-deserialization-is-harmful-magento-xxe-cve-2024-34102

## Summary
CVE-2024-34102 is a critical pre-authentication XXE vulnerability in Magento 2.4.7 and earlier versions that allows unauthenticated attackers to exfiltrate sensitive files like app/etc/env.php containing cryptographic JWT signing keys. The vulnerability stems from unsafe deserialization of user-controlled data that instantiates SimpleXMLElement with the dataIsURL parameter enabled, and can be chained with PHP filter chains (CVE-2024-2961) for remote code execution.

## Attack scenario (step by step)
1. Attacker identifies a Magento instance running version 2.4.7 or earlier through public scanning
2. Attacker crafts a malicious serialized PHP object containing XXE payload that will instantiate SimpleXMLElement with dataIsURL parameter
3. Attacker sends the serialized payload via POST request to an unauthenticated endpoint that deserializes the data
4. During deserialization, SimpleXMLElement is instantiated with attacker-controlled XML containing external entity declarations pointing to local files
5. Attacker exfiltrates app/etc/env.php containing the JWT signing key used for admin authentication
6. Attacker crafts a valid admin JWT token signed with the exfiltrated key and abuses Magento APIs or chains to RCE via PHP filter gadgets

## Root cause
Magento's deserialization process allows instantiation of SimpleXMLElement class with user-controlled arguments without proper validation. The dataIsURL parameter in SimpleXMLElement constructor enables loading XML from external URLs or files, and nested deserialization chains allow traversing through gadget chains to reach this dangerous sink. Insufficient input validation on serialized data and lack of allowlisting for safe classes enabled the exploitation.

## Attacker mindset
An attacker exploiting this vulnerability seeks to gain unauthorized administrative access to high-value e-commerce platforms. With 140,000+ Magento instances running, the attacker views this as a high-impact, unauthenticated attack vector that requires minimal interaction. The ability to chain this with RCE vulnerabilities elevates it from data exfiltration to full system compromise, making it an attractive target for both APT groups and financially-motivated threat actors.

## Defensive takeaways
- Implement strict input validation and sanitization on all deserialization entry points; use allowlisting for permitted classes rather than blocklisting dangerous ones
- Disable dangerous PHP functions and features like SimpleXMLElement with dataIsURL parameter by default; require explicit developer opt-in with security review
- Conduct thorough code review of deserialization gadget chains; use static analysis tools to identify paths from deserialization to dangerous sinks
- Implement rate limiting and authentication requirements on all API endpoints, even those intended for public use
- Rotate and protect sensitive cryptographic material (JWT signing keys) separately from general configuration; consider using key management services
- Apply defense-in-depth: disable XXE at the XML parser level using PHP's libxml options (libxml_disable_entity_loader)
- Establish emergency patching procedures and peer review processes for hotfixes before wide deployment
- Monitor for and block access patterns consistent with XXE exploitation (requests with DOCTYPE declarations, external entity references)

## Variant hunting
Researchers should search for other Magento endpoints accepting POST data that triggers deserialization, alternative gadget chains leading to SimpleXMLElement instantiation, and similar XXE patterns in other PHP frameworks using serialization (Laravel, Symfony, WordPress plugins). Additionally, hunt for other classes with URL-loading capabilities in PHP standard library that could be abused via deserialization chains, and test whether the initial blocklist-based mitigations for dataIsURL and sourceData keywords can be bypassed using encoding or alternative parameter names.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1552 - Unsecured Credentials
- T1552.001 - Credentials In Files
- T1567.002 - Exfiltration Over Web Service
- T1059.007 - PHP
- T1083 - File and Directory Discovery
- T1078.002 - Valid Accounts (via JWT forgery)

## Notes
The research team's contribution was significant: they created the first public PoC before widespread exploitation. The iterative nature of the mitigations (SanSec's initial patch blocked dataIsURL, then Sergey's version added sourceData blocking) demonstrates that XXE via deserialization is subtle and hard to patch comprehensively. The use of diff analysis between patched and unpatched versions was an effective methodology. The potential to chain with CVE-2024-2961 (PHP filter chains) for RCE is particularly concerning. The presence of 140,000+ Magento instances made this a high-impact vulnerability. Notably, the original discoverer Sergey Temnikov did not release full PoC initially, showing responsible disclosure practices, but subsequent community analysis eventually revealed bypass techniques for emergency mitigations.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-01*
