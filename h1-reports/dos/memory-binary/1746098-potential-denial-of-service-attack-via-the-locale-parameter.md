# Denial of Service Attack via Locale Parameter in Django Internationalized URLs

## Metadata
- **Source:** HackerOne
- **Report:** 1746098 | https://hackerone.com/reports/1746098
- **Submitted:** 2022-10-21
- **Reporter:** benjaoming_realone
- **Program:** Django
- **Bounty:** Not specified in writeup
- **Severity:** high
- **Vuln:** Regular Expression Denial of Service (ReDoS), Denial of Service, Input Validation Failure
- **CVEs:** CVE-2022-41323
- **Category:** memory-binary

## Summary
Django versions 3.2 before 3.2.16, 4.0 before 4.0.8, and 4.1 before 4.1.2 were vulnerable to ReDoS attacks through internationalized URL locale parameters. The locale parameter was unsafely processed as a regular expression, allowing attackers to craft malicious regex patterns that consume excessive CPU resources.

## Attack scenario
1. Attacker identifies a vulnerable Django application using internationalized URLs that accepts locale parameters from the URL path
2. Attacker crafts a catastrophic regular expression pattern known to cause excessive backtracking (e.g., nested quantifiers like (a+)+b)
3. Attacker embeds the malicious regex pattern in the locale parameter of a request URL
4. The Django application processes the locale parameter as a regex during URL routing/localization matching
5. The regex engine enters catastrophic backtracking, consuming CPU resources exponentially
6. Legitimate requests are starved of resources, resulting in application unavailability for other users

## Root cause
The locale parameter in Django's internationalized URL handling was directly used in regular expression matching without proper input sanitization or restriction. The code treated user-controlled locale identifiers as regex patterns rather than literal string identifiers, enabling ReDoS attacks.

## Attacker mindset
An attacker with basic knowledge of ReDoS vulnerabilities can craft simple payloads to disable applications. The attack requires no authentication and can be executed remotely via HTTP requests, making it attractive for low-skill attackers seeking to cause service disruption.

## Defensive takeaways
- Never treat user input as regular expression patterns; use literal string matching for locale identifiers instead
- Implement strict input validation and allowlisting for locale parameters (e.g., only permit ISO 639-1 language codes)
- Apply regex timeouts/limits to prevent catastrophic backtracking if regex matching is necessary
- Sanitize and escape user input before using it in any regex context
- Use parameterized/compiled regex patterns instead of dynamic regex construction from user input
- Implement rate limiting and request throttling to mitigate DoS attacks
- Monitor CPU usage and response times for anomalies indicating ReDoS attacks
- Apply patches promptly from Django security advisories

## Variant hunting
Check other Django URL routing mechanisms for similar regex injection patterns
Examine custom URL converters or locale middleware for similar ReDoS vulnerabilities
Search for other user-controlled parameters used directly in regex operations
Analyze third-party i18n packages for comparable locale parameter handling issues
Test GET/POST parameters and headers that might be processed as regex patterns
Review URL rewriting engines and path normalization routines

## MITRE ATT&CK
- T1190
- T1499

## Notes
This is a well-known class of vulnerability (ReDoS) affecting URL routing in Django. The fix involved constraining locale parameter matching to explicit character sets or string literals rather than user-supplied regex patterns. This vulnerability demonstrates the critical importance of avoiding dynamic regex construction from untrusted input.

## Full report
<details><summary>Expand</summary>

In Django 3.2 before 3.2.16, 4.0 before 4.0.8, and 4.1 before 4.1.2, internationalized URLs were subject to a denial of service attack via the locale parameter, which is treated as a regular expression.

## Impact

By crafting a Python regex, a vulnerable site could suffer a DOS attack. The attack was most likely to happen on sites that processes locale IDs from URL parameters.

</details>

---
*Analysed by Claude on 2026-05-24*
