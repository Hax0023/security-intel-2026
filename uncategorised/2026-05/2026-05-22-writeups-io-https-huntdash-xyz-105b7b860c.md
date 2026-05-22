# Bug Bounty Program Scope Analysis - Multiple Organizations

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-22
- **Author:** Various
- **Program:** Multiple (Intigriti: UZ Leuven/AZDiest, HackerOne: Stripe, Spotify, MercadoLibre, Circle, Mozilla)
- **Bounty:** Varies by program (CRITICAL to LOW)
- **Severity:** INFORMATIONAL
- **Vuln types:** Scope Information Disclosure, Target Enumeration, Configuration Information Exposure
- **Category:** uncategorised
- **Writeup:** https://huntdash.xyz/

## Summary
This is a public-facing bug bounty dashboard that aggregates and displays detailed scope information, asset listings, and recent changes across multiple active bug bounty programs. The exposure of this granular reconnaissance data could enable threat actors to prioritize targets and understand security testing scope constraints.

## Attack scenario (step by step)
1. Attacker visits huntdash.xyz and observes publicly listed bug bounty program scopes
2. Attacker identifies high-value targets (Stripe MCP endpoint, Mozilla Relay, Spotify CLI) and their tier levels
3. Attacker notes specific restrictions (IP whitelisting on UZ Leuven assets, geographic constraints on wp5-truststroke)
4. Attacker uses scope intelligence to identify which assets are actively being tested vs overlooked
5. Attacker targets overlapping infrastructure or similar assets outside bounty scope to avoid detection
6. Attacker leverages MCP Dynamic Client Registration details to craft targeted phishing campaigns against Stripe users

## Root cause
Public aggregation and display of confidential bug bounty program scope information, including target URIs, asset types, severity tiers, recent modifications, and security testing constraints without access controls.

## Attacker mindset
Reconnaissance opportunist seeking to understand organizational security posture, identify lower-hanging fruit outside bounty scope, and discover which infrastructure has active security monitoring vs passive assets. The detailed scope information enables threat actors to avoid honeypots and focus on realistic attack surfaces.

## Defensive takeaways
- Implement strict access controls on bug bounty scope dashboards - restrict visibility to authorized researchers only
- Avoid publishing specific asset hostnames, IP ranges, and security constraints in public or semi-public interfaces
- Consider using content delivery that requires authentication or operates behind VPNs for scope information
- Monitor for unauthorized aggregation and republication of scope data across multiple programs
- Implement rate limiting and bot detection on scope tracking platforms
- Use HTTP headers (X-Robots-Tag: noindex) to prevent search engine indexing of scope information
- Implement audit logging for scope data access and publication
- Educate organizations about risks of shared/centralized scope tracking systems

## Variant hunting
['Search for other public bug bounty dashboards or scope aggregators (similar platforms to huntdash.xyz)', 'Check GitHub for accidentally committed .env files containing bug bounty scope information', 'Hunt for cached versions of scope pages in search engine archives (Wayback Machine, Google Cache)', 'Look for scope data exposed via API endpoints without authentication on bounty platforms', 'Monitor pastebin-like services for dumps of bounty scope configurations', 'Check for scope information disclosed in git history or public repositories', 'Search for Shodan/Censys queries targeting known bounty infrastructure', 'Investigate whether scope changes trigger webhook notifications to unauthenticated endpoints']

## MITRE ATT&CK
- T1598.003 - Phishing: Spearphishing Link (targeting Stripe OAuth phishing with MCP context)
- T1592.004 - Gather Victim Org Info: Identify Personnel (finding security researchers and bounty hunters)
- T1589.001 - Gather Victim Org Info: Credentials (understanding auth mechanisms from scope details)
- T1592.002 - Gather Victim Identity Info: Domain Registration (asset enumeration via scope)
- T1526 - Passive Scanning (asset discovery from public scope listings)
- T1580 - Cloud Infrastructure Discovery (identifying cloud targets like Stripe via scope)
- T1538 - Cloud Service Discovery (reconnaissance of exposed endpoints)

## Notes
This appears to be the 'HuntDash' tool - a third-party service aggregating public bug bounty scope information. The critical risk is meta-level reconnaissance: exposing which targets are actively being tested, their tier levels, and security constraints enables threat actors to identify overlooked infrastructure and optimize attack timing. The Stripe MCP disclosure about unauthenticated Dynamic Client Registration combined with OAuth phishing risk is particularly concerning when correlated with this public scope visibility. Organizations should consider whether their scope information should ever be published in centralized, public dashboards regardless of the tool's convenience.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-22*
