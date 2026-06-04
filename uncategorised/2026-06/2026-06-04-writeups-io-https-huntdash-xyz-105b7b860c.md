# HuntDash - Bug Bounty Program Scope Dashboard Analysis

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-04
- **Author:** Various
- **Program:** Multiple (UZ Leuven/Intigriti, Stripe/HackerOne, Spotify/HackerOne, MercadoLibre/HackerOne, Circle/HackerOne, Mozilla/HackerOne, pixiv/HackerOne)
- **Bounty:** Varies by program and severity tier
- **Severity:** INFORMATIONAL
- **Vuln types:** Submitted by:quas
- **Category:** uncategorised
- **Writeup:** https://huntdash.xyz/

## Summary
This is a scope aggregation dashboard showing active bug bounty programs and their targets across multiple platforms (Intigriti, HackerOne). The dashboard displays 138 recent scope changes across 10 targets, including critical assets like Stripe's MCP server, Mozilla Relay, and various enterprise targets. No specific vulnerability is disclosed; this appears to be a reconnaissance tool aggregating publicly available scope information.

## Attack scenario (step by step)
1. Attacker identifies multiple high-value targets through the HuntDash aggregation dashboard
2. Attacker focuses on assets marked CRITICAL severity (Stripe MCP, Stripe CLI, Circle's remote-signer, Mozilla Relay)
3. Attacker reviews scope notes and constraints (e.g., IP whitelisting, region restrictions, Host header requirements)
4. Attacker prioritizes targets with complex configurations (reverse proxies, tier-based rewards) for potential misconfigurations
5. Attacker cross-references scope changes to identify newly exposed assets or recently modified endpoints
6. Attacker targets OAuth consent phishing and interoperability weaknesses noted in Stripe MCP description

## Root cause
Not a vulnerability writeup. This is a publicly accessible dashboard aggregating bug bounty scope information. The tool enables centralized reconnaissance of multiple programs, potentially revealing attack surface across different platforms and reducing research time for attackers.

## Attacker mindset
An attacker would use this dashboard to efficiently map high-value targets across multiple bug bounty platforms, prioritize critical assets, and identify scope misconfigurations or newly added targets. The aggregation reduces reconnaissance overhead and provides competitive intelligence on bounty program coverage.

## Defensive takeaways
- Limit public disclosure of detailed scope information including tier levels and asset categorization
- Avoid publishing constraints like IP whitelisting, region restrictions, or header validation requirements that hint at bypass techniques
- Be cautious with OAuth implementations and consent phishing risks in open MCP/API ecosystems
- Monitor scope change logs and rate-limit rapid scope queries from automated tools
- Use scope obfuscation or require authentication to view detailed bounty program targets
- Implement stricter staging/production isolation and avoid exposing testing infrastructure details

## Variant hunting
Search for similar scope aggregation tools; investigate if HuntDash has a public API; examine other bug bounty meta-sites (BugBounty.jp, Yeswehack dashboards); check for exposed scope databases or program metadata leaks on GitHub or pastebin; monitor for scope information in web archives or cached pages.

## MITRE ATT&CK
- T1592 - Gather Victim Identity Information
- T1589 - Gather Victim Organization Information
- T1592.004 - Gather Victim Identity Information: Client Configurations
- T1598 - Phishing for Information
- T1598.001 - Spearphishing Link
- T1190 - Exploit Public-Facing Application

## Notes
This appears to be HuntDash.xyz, a legitimate bug bounty scope aggregator. While not itself a vulnerability, it demonstrates information disclosure risks in bug bounty programs. The dashboard exposes: program targets, severity tiers, scope notes revealing security architecture (reverse proxies, IP whitelisting, geo-restrictions), recent scope changes indicating newly exposed assets, and detailed constraints that could hint at bypass techniques. Organizations should be cautious about overly detailed scope documentation.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-04*
