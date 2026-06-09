# UZ Leuven Bug Bounty Program Scope Analysis - IP Whitelisting & Geo-Restriction Bypass Potential

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-09
- **Author:** Various
- **Program:** Intigriti - UZ Leuven
- **Bounty:** Variable (HIGH, MEDIUM, LOW based on target tier)
- **Severity:** HIGH
- **Vuln types:** IP Whitelisting Bypass, Geo-Restriction Bypass, Host Header Injection, Reverse Proxy Misconfiguration, Access Control Bypass
- **Category:** uncategorised
- **Writeup:** https://huntdash.xyz/

## Summary
UZ Leuven's bug bounty scope reveals critical IP whitelisting and geo-restriction controls across multiple high-value targets including APIs, medical systems (ECRF, PCR Studio), and file sharing services. The program explicitly documents that /api/ endpoints should only be accessible from Belgian or Dutch IPs, and several applications enforce 403 HTTP responses for out-of-scope geographic locations. Host header handling determines bounty tier classification, creating potential for header manipulation attacks.

## Attack scenario (step by step)
1. Attacker identifies HIGH severity targets with explicit IP whitelisting requirements (e.g., prddsplunkhf.uzleuven.be, ecrf.uzleuven.be, liquidfiles.uzleuven.be)
2. Attacker proxies requests through compromised or rented Belgian/Dutch IP addresses, or manipulates X-Forwarded-For, CF-Connecting-IP, or similar headers to spoof location
3. Attacker crafts requests with malicious Host headers pointing to tier 1/2 targets while routing through reverse proxy IPs (193.58.149.x range), potentially triggering tier mismatch
4. Attacker bypasses API access restrictions by chaining header injection with Host header manipulation to access /api/ endpoints from non-whitelisted geographies
5. Attacker exploits the 'default to Tier 2' policy when Host header is not properly validated, escalating impact of vulnerabilities on lower-tier targets
6. Attacker targets medical/sensitive systems (ECRF, CardsonLine, PCR Studio) with geo-bypass to extract patient data or sensitive research information

## Root cause
The program documentation reveals trust in network-layer geofencing without apparent application-layer validation. The explicit mention of 'Host header determines bounty tier' and 'default to Tier 2' suggests inconsistent header validation across different applications. Reliance on reverse proxy IP ranges and X-Forwarded-For headers creates multiple bypass vectors if proper validation is not implemented at the application level.

## Attacker mindset
A skilled attacker would recognize this as a mature organization with documented security controls, making it attractive for targeted research. The explicit scope documentation inadvertently highlights which systems have the strictest controls (HIGH severity = tighter restrictions = more interesting bypasses). Medical/healthcare targets (ECRF, CardsonLine) indicate high-value data. The Host header note suggests some systems may not properly validate headers, creating a specific attack vector to research.

## Defensive takeaways
- Implement application-layer IP validation rather than relying solely on reverse proxy headers; verify source IP through multiple independent methods
- Normalize and strictly validate Host headers against a whitelist before using for tier/feature determination; never accept arbitrary Host header values
- Use consistent header validation logic across all applications; avoid 'default to lower tier' policies that create exploitation incentives
- Implement proper X-Forwarded-For/CF-Connecting-IP validation to prevent header spoofing; limit trust chain depth
- For sensitive systems (medical data), implement additional factors beyond IP geo-location (mutual TLS, API keys, device fingerprinting)
- Conduct regular security audits specifically targeting header injection and geo-restriction bypass techniques
- Document internal Host header expectations but avoid publishing specific validation logic or tier mapping details in public scope
- Implement rate limiting and anomaly detection for requests with mismatched Host headers or geographic patterns

## Variant hunting
Research similar patterns in other healthcare organization bug bounty programs, particularly those with medical record systems (ECRF, patient portals). Hunt for applications using liquidfiles.uzleuven.be style file-sharing systems with geo-restrictions. Investigate other organizations using 'reverse proxy IP ranges' in scope documentation - this pattern indicates potential header validation weaknesses. Look for programs mentioning 'Host header determines feature access' as this suggests tier/feature gating based on headers. Search for CardsonLine or similar healthcare transaction systems with documented IP whitelisting. Examine programs with wildcard scopes (*.uzleuven.be) where tier 3 creates incentive to bypass higher tiers.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1598 - Phishing: Spearphishing Link (if combined with social engineering for IP access)
- T1557 - Man-in-the-Middle: Adversary-in-the-Middle
- T1040 - Traffic Redirection
- T1021.001 - Remote Services: Remote Service Session Hijacking (via header manipulation)
- T1078 - Valid Accounts (if escalating from tier 3 access to tier 1)
- T1110 - Brute Force (bypass attempts)
- T1526 - Reconnaissance (active scanning of reverse proxy IPs)

## Notes
This is not a traditional vulnerability writeup but rather an analysis of a bug bounty scope document. The 'vulnerability' is the potential for IP whitelisting/geo-restriction bypass based on how the scope is written. The mention of 'should return http 403' and explicit IP ranges creates a roadmap for attackers. The reverse proxy IP range disclosure (193.58.149.x) is particularly notable as these are specific targets for header manipulation research. High-value targets include medical systems (ECRF = Electronic Case Report Form for clinical trials, PCR Studio, CardsonLine for healthcare transactions). This appears to be from HuntDash, a scope tracking tool, suggesting the information was publicly visible or leaked. Organizations should be cautious about what they publish in bug bounty scope documentation.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-09*
