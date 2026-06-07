# Nested Deserialization Harmful: Magento XXE (CVE-2024-34102)

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-07
- **Author:** Various
- **Program:** Adobe Commerce / Magento
- **Bounty:** Not specified
- **Severity:** critical
- **Vuln types:** XML External Entity (XXE) Injection, Unsafe Deserialization, Local File Inclusion, Pre-authentication Remote Code Execution
- **Category:** web-api
- **Writeup:** https://www.assetnote.io/resources/research/why-nested-deserialization-is-harmful-magento-xxe-cve-2024-34102

## Summary
CVE-2024-34102 is a critical pre-authentication XXE vulnerability in Magento 2 (CVSS 9.8) that allows attackers to exfiltrate sensitive files including the JWT signing key from app/etc/env.php. The vulnerability stems from unsafe deserialization of user-controlled data that instantiates SimpleXMLElement with the dataIsURL parameter enabled, allowing external XML loading and entity expansion attacks.

## Attack scenario (step by step)
1. Attacker crafts malicious serialized PHP object containing nested SimpleXMLElement instantiation with dataIsURL=true
2. Attacker sends POST request with XXE payload to vulnerable Magento endpoint before authentication
3. Magento deserializes attacker's object, triggering SimpleXMLElement constructor with external entity reference
4. SimpleXMLElement loads and parses attacker-controlled XML containing references to local files like app/etc/env.php
5. Attacker exfiltrates JWT signing key from env.php file or chains with PHP filter chains (CVE-2024-2961) for RCE
6. Attacker forges admin JWT token and abuses Magento APIs with administrative privileges

## Root cause
Magento deserializes untrusted user input without proper validation, and the deserialization gadget chain allows instantiation of SimpleXMLElement with controllable arguments. The dataIsURL parameter was not blocked in initial hotfixes, enabling XXE via external entity loading. The vulnerability is rooted in nested deserialization patterns where internal library functions receive attacker-controlled objects as parameters.

## Attacker mindset
Attackers exploited the widespread deployment of Magento (140,000+ instances) to target high-value e-commerce platforms. The pre-authentication nature made it universally exploitable without credentials. Chaining with known PHP filter gadgets for RCE demonstrated sophisticated attack stacking. The attacker recognized that JWT signing keys in env.php would grant admin access, escalating XXE from information disclosure to complete account takeover.

## Defensive takeaways
- Never deserialize untrusted user input; use JSON instead of PHP serialization
- Implement strict input validation and type checking on deserialized objects before instantiation
- Block dangerous parameters like dataIsURL and sourceData in deserialization contexts
- Disable XML external entity loading globally via libxml2 configuration (libxml_disable_entity_loader)
- Conduct thorough peer review of emergency hotfixes before deployment; initial mitigations may be bypassable
- Perform gadget chain analysis to identify all deserialization code paths that could instantiate dangerous classes
- Implement network segmentation to limit exfiltration of sensitive files like env.php
- Monitor for suspicious deserialization patterns in logs and WAF rules

## Variant hunting
Search for other deserialization gadget chains in Magento and similar PHP frameworks that instantiate dangerous classes with attacker-controlled parameters. Investigate other SimpleXMLElement constructor calls accepting user input. Hunt for nested object instantiation patterns where inner objects receive parameters from outer objects. Review other PHP serialization libraries for similar vulnerabilities where constructor arguments bypass security checks.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1528 - Steal Application Access Token
- T1005 - Data from Local System
- T1041 - Exfiltration Over C2 Channel
- T1059 - Command and Scripting Interpreter
- T1036 - Masquerading

## Notes
The research highlighted the importance of technical vulnerability disclosure for peer review; both SanSec and Sergey Temnikov's initial hotfix mitigations were bypassable, demonstrating that transparency aids the broader security community. The development of a PoC before public exploitation was critical for customer risk assessment. The chaining potential with CVE-2024-2961 PHP filter chains elevates this from XXE to RCE, making it exceptionally severe. Debugging with XDebug in a containerized Magento environment proved essential for discovering the gadget chain.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-07*
