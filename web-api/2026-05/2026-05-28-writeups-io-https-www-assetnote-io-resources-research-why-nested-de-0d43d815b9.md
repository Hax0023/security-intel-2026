# Nested Deserialization Leading to XXE in Magento (CVE-2024-34102)

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-28
- **Author:** Various
- **Program:** Adobe Magento / Adobe Commerce
- **Bounty:** Not specified in writeup
- **Severity:** critical
- **Vuln types:** XML External Entity Injection (XXE), Unsafe Deserialization, Pre-authentication Remote Code Execution
- **Category:** web-api
- **Writeup:** https://www.assetnote.io/resources/research/why-nested-deserialization-is-harmful-magento-xxe-cve-2024-34102

## Summary
CVE-2024-34102 is a critical pre-authentication XXE vulnerability in Magento 2 caused by unsafe deserialization of user-supplied data leading to SimpleXMLElement instantiation with attacker-controlled arguments. The vulnerability enables exfiltration of sensitive files including app/etc/env.php containing JWT cryptographic keys, authentication bypass, and potential RCE when chained with PHP filter exploits.

## Attack scenario (step by step)
1. Attacker sends a crafted HTTP POST request with XML payload to a Magento endpoint that processes deserialized data
2. The payload contains nested serialized objects designed to instantiate SimpleXMLElement with the dataIsURL parameter set to true
3. The deserialization gadget chain is traversed during PHP object deserialization, eventually calling SimpleXMLElement constructor
4. SimpleXMLElement loads external XML from attacker-controlled URL or local file path via XXE, exfiltrating contents to attacker server
5. Attacker obtains JWT cryptographic key from env.php and forges admin authentication tokens
6. Attacker uses admin tokens to access Magento APIs and escalate privileges, or chains with CVE-2024-2961 PHP filters for RCE

## Root cause
Magento's deserialization process unsafely instantiates SimpleXMLElement objects with user-controlled constructor arguments passed through the 'sourceData' parameter. The absence of input validation on deserialized data allows attackers to trigger XXE by controlling the dataIsURL parameter during object instantiation, enabling external entity loading and file exfiltration.

## Attacker mindset
Attacker seeks pre-authentication access to critical systems. By identifying a deserialization gadget chain, they can bypass authentication entirely and extract cryptographic material for token forgery. The chaining capability with existing PHP exploits demonstrates opportunistic thinking to compound initial access into full system compromise.

## Defensive takeaways
- Implement strict input validation and sanitization on all deserialized data; never trust user-supplied serialized objects
- Disable XXE processing in XML parsers by setting appropriate flags (LIBXML_NOENT, LIBXML_NONET, etc.)
- Avoid passing user-controlled data as constructor arguments to dangerous classes like SimpleXMLElement
- Use allowlisting rather than blocklisting when mitigating deserialization issues; the keyword blocking approach ('dataIsURL', 'sourceData') proved insufficient
- Implement peer review and iterative testing of security patches before deployment
- Monitor for chaining opportunities between vulnerabilities; fix root causes rather than symptoms
- Maintain cryptographic keys outside serializable objects and implement key rotation policies
- Apply principle of least privilege; restrict deserialization to only necessary data types

## Variant hunting
Search for other Magento endpoints accepting serialized data or XML input. Hunt for other PHP gadget chains invoking SimpleXMLElement or similar dangerous constructors (DOMDocument, etc.). Examine custom extensions using unserialize() on user input. Test for similar patterns in other PHP frameworks using serialization (Symfony, Laravel). Investigate whether 'sourceData' parameter appears in other deserialization contexts. Look for wrapper functions around SimpleXMLElement that might bypass keyword-based filters.

## MITRE ATT&CK
- T1190
- T1083
- T1087
- T1566
- T1105
- T1021
- T1548

## Notes
The vulnerability gained notoriety as 'CosmicString' by SanSec. Original discoverer Sergey Temnikov published limited details without PoC. Multiple iterations of emergency patches were required, with initial mitigations being bypassable. This case demonstrates the value of public disclosure and peer review in security patching. The ability to chain with CVE-2024-2961 PHP filter chains amplifies impact to RCE. Over 140,000 Magento instances were potentially affected. The CVSS 9.8 rating reflects pre-authentication access, confidentiality/integrity compromise, and authentication bypass potential.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-28*
