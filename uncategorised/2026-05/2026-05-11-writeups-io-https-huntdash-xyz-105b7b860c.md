# HuntDash - Bug Bounty Scope Monitoring Dashboard

## Metadata
- **Source:** writeups.io
- **Date:** 
- **Author:** Various
- **Program:** Multiple (Stripe, Spotify, MercadoLibre, Circle, Mozilla, pixiv, Remitly)
- **Bounty:** Varies by program
- **Severity:** unknown
- **Vuln types:** See writeup
- **Category:** uncategorised
- **Writeup:** https://huntdash.xyz/

## Summary
HuntDash is a security scope monitoring dashboard tracking recent changes across 55 targets in bug bounty programs. The dashboard displays newly added and updated scope entries including URLs, downloadable executables, and source code repositories with severity classifications.

## Attack scenario (step by step)
1. Attacker monitors HuntDash for newly added scope entries to identify fresh attack surface
2. Attacker identifies that Stripe's MCP server endpoint (mcp.stripe.com) was recently added and uses Dynamic Client Registration without pre-registration requirements
3. Attacker creates a malicious MCP-compatible client tool or exploits OAuth consent phishing vulnerabilities to obtain user credentials/tokens
4. Attacker targets newly exposed Remitly payment infrastructure domains (45 new domains added) for reconnaissance and exploitation
5. Attacker analyzes Circle's GitHub repository for remote signer vulnerabilities that could compromise transaction signing
6. Attacker leverages the staging environment (relay.allizom.org) to test Mozilla Relay API endpoints without detection

## Root cause
This appears to be a scope tracking tool rather than a specific vulnerability. However, the underlying issue is that recently added scope entries expose new attack surface immediately upon publication, and attackers can use public scope monitoring to prioritize reconnaissance efforts on fresh targets.

## Attacker mindset
Opportunistic - leverage publicly available scope information to identify newly exposed infrastructure before organizations fully harden defenses. Focus on low-hanging fruit on newly added domains and recent code repositories.

## Defensive takeaways
- Implement staged scope rollout - don't expose all new assets simultaneously to reduce reconnaissance window
- Monitor for automated scope scanning activity patterns against newly added entries
- Implement rate limiting and WAF rules specifically targeting reconnaissance behavior on new scope assets
- Require explicit security review before publicly listing new scope entries
- Implement canary tokens or honeypot endpoints within newly added scopes to detect automated enumeration
- Stagger scope publication across multiple time periods to avoid concentrating attack surface visibility

## Variant hunting
Search for similar public scope tracking dashboards or RSS feeds from other bug bounty platforms; investigate if scope changes can be predicted through GitHub repository updates or DNS zone file monitoring; analyze if attacker infrastructure queries newly registered domains shortly after scope publication.

## MITRE ATT&CK
- T1592 - Gather Victim Host Information
- T1592.004 - Client Configurations
- T1598.004 - Phishing - Credential Exposure
- T1595 - Active Scanning
- T1589 - Gather Victim Identity Information
- T1590 - Gather Victim Network Information

## Notes
This is a scope monitoring dashboard aggregating public bug bounty program scope changes. The 'vulnerability' is not in any single program but in the information disclosure of newly exposed attack surface. Stripe's MCP server entry explicitly discusses OAuth consent phishing as an accepted risk model. Remitly's addition of 45 new domains suggests infrastructure expansion. Mozilla's staging environment reference indicates controlled testing scope. This tool would be valuable for both defensive security teams and threat actors tracking emerging opportunities.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-11*
