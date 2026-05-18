# HuntDash Security Scope Analysis - Multiple Programs

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-18
- **Author:** Various
- **Program:** Multiple (UZ Leuven/Intigriti, Stripe/HackerOne, Spotify/HackerOne, MercadoLibre/HackerOne, Circle/HackerOne, Mozilla/HackerOne)
- **Bounty:** Varies by program and tier (LOW to CRITICAL)
- **Severity:** CRITICAL
- **Vuln types:** IP Whitelisting Bypass, Host Header Injection, Geographic Restriction Bypass, OAuth Consent Phishing, Unauthorized API Access
- **Category:** uncategorised
- **Writeup:** https://huntdash.xyz/

## Summary
HuntDash displays a consolidated bug bounty scope tracker showing recent changes across multiple enterprise programs, primarily highlighting UZ Leuven's healthcare infrastructure with critical IP-based access controls and Stripe's open OAuth MCP implementation. The dashboard reveals several high-value targets with documented security boundaries including IP whitelisting, geographic restrictions, and authentication mechanisms that represent significant attack surfaces.

## Attack scenario (step by step)
1. Attacker identifies wp5-truststroke.uzleuven.be with documented restriction: '/api/ only accessible from BE/NL IPs'
2. Attacker uses VPN/proxy infrastructure to spoof Belgian or Dutch IP address by routing traffic through reverse proxy IP range (193.58.149.0/24)
3. Attacker crafts HTTP request with Host header manipulation to claim tier-3 subdomain, escalating bounty tier from 2 to higher classification
4. Attacker bypasses geographic IP whitelisting by manipulating Host header and X-Forwarded-For headers through the organization's documented reverse proxy infrastructure
5. Attacker accesses restricted /api/ endpoints and extracts sensitive healthcare data or achieves RCE on medical infrastructure
6. Attacker reports findings with proper Host header documentation, qualifying for HIGH/MEDIUM tier bounty rather than default tier-2

## Root cause
IP-based access control reliance without compensating controls such as mutual TLS, request signing, or cryptographic validation. Host header trust in tier determination creates incentive misalignment. Geographic restrictions implemented at perimeter only, not application layer. Open OAuth model in Stripe MCP prioritizes ecosystem interoperability over account takeover prevention.

## Attacker mindset
Target-rich reconnaissance - the dashboard itself leaks critical scope intelligence including IP ranges, specific subdomain restrictions, geographic limitations, and bounty tier information. Attackers view this as a roadmap for prioritizing high-impact targets. OAuth phishing attacks become lucrative if users can be social-engineered during consent flow. Healthcare data in UZ Leuven scope represents high-value exfiltration target.

## Defensive takeaways
- Never expose reverse proxy IP ranges or internal infrastructure details in public scope documentation
- Implement application-layer authentication independent of IP whitelisting; use mutual TLS or cryptographic request validation
- Do not trust Host headers for security decisions; validate against allowlist before tier determination
- Segregate API endpoints from user-facing endpoints at network level rather than relying on path-based restrictions
- Implement geographic restrictions at application layer with device fingerprinting and behavioral analysis, not just IP geotagging
- For OAuth systems, implement additional signals (device trust, risk scoring, CAPTCHA) before showing consent screen to prevent automated phishing
- Do not document security boundaries (IP ranges, geographic limitations, tier escalation paths) in public bug bounty scopes
- Use scope platform's private notes for technical restrictions; only publish asset names in scope

## Variant hunting
Search for other organizations exposing reverse proxy IP ranges in scope documentation. Hunt for bug bounty programs using Host header for tier determination. Identify healthcare/financial programs with documented geographic restrictions that may implement only IP-based controls. Search GitHub for accidentally committed scope files or internal documentation listing IP whitelist ranges. Monitor for OAuth implementations copying Stripe's open registration model without additional account security measures.

## MITRE ATT&CK
- T1190
- T1598.003
- T1606.002
- T1491.001
- T1589.002
- T1040
- T1562.008
- T1550.003

## Notes
This appears to be a legitimate bug bounty scope tracking dashboard rather than a specific vulnerability writeup. The content represents reconnaissance-level intelligence leakage - organizations should never publicly document IP ranges, geographic restrictions, or tier-escalation mechanics. The UZ Leuven scope is particularly sensitive given healthcare data involvement. Stripe's MCP documentation explicitly acknowledges OAuth phishing risk but accepts it as inherent to open ecosystems - this is a policy decision rather than technical vulnerability but represents attack surface. The 'UPDATED' timestamps and 'CRITICAL' severity tags on Stripe MCP suggest active research interest in these targets.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-18*
