# Bug Bounty Program Scope Analysis - HuntDash Dashboard

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-02
- **Author:** Various
- **Program:** Multiple (UZ Leuven/Intigriti, Stripe/HackerOne, Spotify/HackerOne, MercadoLibre/HackerOne, Circle/HackerOne, Mozilla/HackerOne)
- **Bounty:** Varies by program and severity tier
- **Severity:** INFORMATIONAL
- **Vuln types:** Submitted by:quas
- **Category:** uncategorised
- **Writeup:** https://huntdash.xyz/

## Summary
This is a bug bounty program scope dashboard aggregating 140 recent scope changes across 11 targets from multiple platforms including Intigriti and HackerOne. The document shows active bounty programs with varying severity tiers and asset types including web applications, IP ranges, mail servers, and downloadable executables.

## Attack scenario (step by step)
1. Attacker reviews HuntDash dashboard to identify newly added or updated high-severity scope items
2. Attacker selects critical assets like mcp.stripe.com or relay.firefox.com based on severity and asset type
3. Attacker performs reconnaissance on selected targets using standard vulnerability assessment techniques
4. Attacker discovers vulnerabilities respecting the defined scope boundaries and Host header requirements
5. Attacker submits findings with proper Host header designation to maximize bounty tier classification
6. Attacker tracks scope changes to identify newly exposed assets before other researchers

## Root cause
This is a scope aggregation tool, not a vulnerability report. It displays current bug bounty program scopes and recent changes across multiple platforms.

## Attacker mindset
Threat actors and security researchers use scope aggregation dashboards to efficiently identify high-value targets, track scope expansions, and prioritize reconnaissance efforts across multiple bug bounty platforms. The emphasis on Host header usage and IP whitelisting suggests attackers analyze submission requirements to maximize bounty payouts.

## Defensive takeaways
- Implement strict Host header validation on all in-scope assets to prevent host header injection attacks
- Maintain rigorous IP whitelisting for sensitive assets like cardsonline.azdiest.be with proper 403 enforcement
- Regularly audit and update scope boundaries to minimize unintended exposure of development/test environments
- Document Host header requirements clearly since submissions without proper headers default to lower tiers
- Use staging environments exclusively for testing (e.g., relay.allizom.org) rather than production systems
- Implement geographic IP restrictions where applicable (e.g., BE/NL only for /api/ paths)
- Require explicit HTTP header markers (X-HackerOne-Research) for identification of authorized security testing traffic
- Monitor scope dashboard for competitive intelligence leakage and sensitive asset exposure

## Variant hunting
Search for Host header injection, HTTP request smuggling, or header-based access control bypasses on listed high-severity assets. Test IP whitelisting bypass techniques on restricted endpoints. Investigate SSRF possibilities through reverse proxy infrastructure. Examine wildcard scope boundaries (*.uzleuven.be, *.playuzleuven.be) for subdomain enumeration and takeover opportunities.

## MITRE ATT&CK
- T1598.001
- T1591.004
- T1190
- T1105
- T1021.005
- T1040

## Notes
This appears to be a screenshot or export from HuntDash (huntdash.xyz), a third-party tool for aggregating bug bounty program scope information. Not a vulnerability writeup but rather program intelligence data. Contains multiple organizations: UZ Leuven (healthcare), Stripe (payments), Spotify (music), MercadoLibre (ecommerce), Circle (blockchain/fintech), and Mozilla (browser). Assets range from CRITICAL to LOW severity. Host header manipulation is highlighted as a critical consideration for bounty tier classification.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-02*
