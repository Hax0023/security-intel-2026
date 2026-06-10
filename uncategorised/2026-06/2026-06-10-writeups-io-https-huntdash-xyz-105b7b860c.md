# UZ Leuven Intigriti Bug Bounty Program Scope Analysis

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-10
- **Author:** Various
- **Program:** Intigriti - UZ Leuven
- **Bounty:** Variable (HIGH/MEDIUM/LOW tier based on target)
- **Severity:** INFORMATIONAL
- **Vuln types:** Scope Documentation, IP Whitelisting Bypass, Host Header Validation
- **Category:** uncategorised
- **Writeup:** https://huntdash.xyz/

## Summary
This is a bug bounty program scope document for UZ Leuven medical institution listing 22 in-scope targets across multiple subdomains and IP ranges. The scope includes explicit geo-blocking requirements (BE/NL IPs only for /api/) and IP whitelisting expectations for certain web applications. Several targets are marked as HIGH severity, indicating critical infrastructure exposure.

## Attack scenario (step by step)
1. Attacker identifies HIGH severity targets like prddsplunkhf.uzleuven.be, sts.uzleuven.be, and extranet.uzleuven.be within the scope
2. Attacker bypasses geographical IP restrictions using VPN/proxy services claiming BE or NL origin to access /api/ endpoints
3. Attacker probes IP whitelisting on cardsonline.azdiest.be and cardsonlinetst.azdiest.be which should return HTTP 403 but may return content
4. Attacker exploits Host header manipulation using reverse proxy IPs (193.58.149.x range) to access tier-3 wildcard *.uzleuven.be targets
5. Attacker targets medical/sensitive systems (ECRF, liquidfiles, extranet-asa, pcrstudiorzb) for data exfiltration or privilege escalation
6. Attacker reports findings with proper Host header context to claim higher bounty tier classification

## Root cause
Multiple security misconfigurations in UZ Leuven infrastructure: (1) Insufficient IP whitelisting enforcement allowing bypass, (2) Host header reliance without proper validation, (3) Exposure of internal/test systems (teststs, liquidfilestest) in production environment, (4) Reverse proxy IP ranges disclosed in scope documentation enabling Host header spoofing, (5) Geo-blocking relying on client-provided IP information rather than network-level enforcement

## Attacker mindset
Medical institutions are high-value targets with sensitive patient data (ECRF = Electronic Case Report Form), financial systems (cardsOnline), and administrative access (extranet). The explicit documentation of security controls (IP whitelisting, geo-blocking) actually reveals the attack surface. The reverse proxy IPs and Host header dependency are security implementation details that can be leveraged. Test/staging systems often have weaker controls. The tiered bounty system incentivizes finding higher-severity targets.

## Defensive takeaways
- Never publicly disclose IP ranges, reverse proxy details, or security control mechanisms in scope documentation
- Implement network-level geo-blocking instead of relying on IP header validation (can be spoofed)
- Remove staging/test systems from production or properly segment them with different credentials
- Validate Host headers server-side and implement strict hostname whitelisting independent of reverse proxy configuration
- Separate sensitive systems (medical records, financial) from public-facing infrastructure with additional authentication
- Audit all wildcard scope definitions (*.uzleuven.be) for unintended exposure of subdomains
- Document security requirements internally only; public scope should reference controls without revealing implementation details
- Implement rate limiting and anomaly detection for accessing geo-restricted or whitelisted systems
- Consider tiering bounties based on impact rather than infrastructure tier to avoid incentivizing lower-tier target enumeration

## Variant hunting
['Search for other medical institutions using similar reverse proxy setups with exposed IP ranges in public documentation', 'Look for organizations publishing Host header dependencies without proper validation in their scope documents', 'Identify other *.uzleuven.be subdomains not listed in tier 1-2 that fall under tier 3 wildcard coverage', 'Find other Intigriti programs with explicit IP whitelisting documented alongside reverse proxy IPs', 'Search for test/staging domain variants (teststs, liquidfilestest pattern) in healthcare organization scope documents', 'Look for ECRF or electronic health record systems exposed in public bug bounty scopes', 'Find organizations mentioning specific IP ranges (193.58.x.x) in public security documentation']

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application (targeting exposed medical/admin systems)
- T1598 - Phishing (targeting healthcare staff accessing extranet systems)
- T1040 - Traffic Redirection/Proxy (leveraging reverse proxy IP ranges for Host header attacks)
- T1562 - Impair Defenses (bypassing IP whitelisting/geo-blocking)
- T1556 - Modify Authentication Process (exploiting Host header validation)
- T1526 - Enumerate External System/Infrastructure (mapping scope targets)
- T1592 - Gather Victim Network Information (using disclosed IP ranges and hostnames)

## Notes
This document is a program scope disclosure rather than a vulnerability report, but reveals significant reconnaissance value for attackers. The explicit mention that reports submitted without proper Host header context default to Tier 2 bounties suggests prior exploitation. The medical focus (ECRF, cardsOnline payment systems) indicates HIPAA/data protection compliance concerns. The 22 scope changes over 30 days suggests active testing environment changes. Test systems (teststs.uzleuven.be, liquidfilestest.uzleuven.be) presence in scope indicates weaker internal controls. The reverse proxy architecture suggests DDoS protection (Cloudflare-like) or load balancing that may introduce additional bypass vectors.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-10*
