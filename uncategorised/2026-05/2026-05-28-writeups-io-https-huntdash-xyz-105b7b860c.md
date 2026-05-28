# Bug Bounty Program Scope Analysis - Multiple Organizations

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-28
- **Author:** Various
- **Program:** Multiple (UZ Leuven/Intigriti, Stripe/HackerOne, Spotify/HackerOne, MercadoLibre/HackerOne, Circle/HackerOne, Mozilla/HackerOne, pixiv/HackerOne)
- **Bounty:** CRITICAL to LOW tier depending on target and vulnerability type
- **Severity:** INFORMATIONAL
- **Vuln types:** Submitted by:quas
- **Category:** uncategorised
- **Writeup:** https://huntdash.xyz/

## Summary
This is a HuntDash scope aggregation dashboard displaying active bug bounty program scopes across multiple organizations and platforms. The content shows recent scope updates, target classifications, and severity tiers but contains no actual vulnerability disclosure or exploitation details.

## Attack scenario (step by step)
1. Researcher reviews HuntDash to identify active bug bounty programs
2. Selects target organization based on severity tier and scope
3. Reviews scope limitations and notes (IP whitelisting, geographic restrictions, API boundaries)
4. Conducts security testing within defined parameters
5. Submits findings with appropriate Host header or context matching scope tier
6. Receives bounty based on vulnerability severity and scope classification

## Root cause
This is not a vulnerability report but rather a public dashboard aggregating bug bounty scope information. No root cause analysis applies.

## Attacker mindset
Bug bounty researchers use this dashboard to identify attractive targets, understand scope boundaries, and prioritize testing efforts based on bounty tier and program maturity.

## Defensive takeaways
- Organizations should regularly audit and update scope definitions to prevent scope creep or unintended coverage
- IP whitelisting, geographic restrictions, and API boundaries must be enforced and monitored
- Host header validation is critical for determining vulnerability impact tier in multi-tenant environments
- Staging environments should be clearly separated from production with distinct identifiers
- Dynamic client registration and OAuth flows require explicit user consent mechanisms and education
- Dependency on user responsibility for OAuth phishing prevention is insufficient without additional controls

## Variant hunting
Review other bug bounty aggregators for scope misconfigurations; examine organizations with HOST header-dependent tier systems for bypass techniques; test IP whitelisting implementations for spoofing or bypass methods; investigate OAuth consent phishing vectors in open ecosystem integrations

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1566 - Phishing (OAuth consent phishing)
- T1190 - Vulnerability in exposed scope

## Notes
This appears to be a screenshot/export of HuntDash.xyz which aggregates public bug bounty scope information. Key observations: (1) UZ Leuven has strict IP geofencing and Host header tier mapping, (2) Stripe's MCP server explicitly accepts unauthenticated Dynamic Client Registration for ecosystem compatibility, (3) Mozilla requires staging-only testing with specific headers, (4) Multiple organizations acknowledge known risks (IP whitelisting, OAuth phishing) as acceptable within their threat model. This is not a vulnerability writeup but rather scope metadata useful for prioritizing testing efforts.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-28*
