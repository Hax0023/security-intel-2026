# HuntDash Bug Bounty Program Scope Analysis

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-19
- **Author:** Various
- **Program:** Multiple programs (UZ Leuven/Intigriti, Stripe/HackerOne, Spotify/HackerOne, MercadoLibre/HackerOne, Circle/HackerOne, Mozilla/HackerOne)
- **Bounty:** Variable by program and severity tier
- **Severity:** INFORMATIONAL
- **Vuln types:** Submitted by:quas
- **Category:** uncategorised
- **Writeup:** https://huntdash.xyz/

## Summary
This is a bug bounty scope dashboard aggregating active targets across multiple programs rather than a specific vulnerability writeup. The dashboard displays 47 targets across 6 programs with tiered severity levels (CRITICAL, HIGH, MEDIUM, LOW). Notable scope items include UZ Leuven healthcare infrastructure, Stripe's MCP server, Spotify CLI, and Mozilla's Relay service.

## Attack scenario (step by step)
1. Researcher reviews HuntDash dashboard to identify high-value targets
2. Researcher selects target based on criticality rating and scope tier
3. Researcher tests target according to program-specific rules (e.g., reverse proxy IP whitelisting for UZ Leuven)
4. Researcher identifies vulnerability and documents with proper Host headers and context
5. Researcher submits report to appropriate program platform (Intigriti/HackerOne)
6. Program security team reviews and awards bounty based on severity and asset tier

## Root cause
Not applicable - this is a scope aggregation dashboard, not a vulnerability disclosure

## Attacker mindset
Bug bounty researchers using centralized dashboard to efficiently identify and target high-value assets across multiple programs, focusing on resources marked CRITICAL or HIGH severity

## Defensive takeaways
- Implement strict IP whitelisting for sensitive infrastructure (noted in cardsonline.azdiest.be scope)
- Enforce Host header validation in reverse proxy configurations (UZ Leuven reverse proxy IP ranges: 193.58.149.x)
- Require authentication at API registration endpoints rather than relying on open ecosystem interoperability (Stripe MCP response)
- Implement OAuth consent warnings and user education for authorization phishing risks
- Use staging/sandboxed instances for security testing rather than production (Mozilla Relay: relay.allizom.org)
- Apply request headers for security testing identification (Mozilla X-HackerOne-Research header requirement)
- Tier scope items appropriately with clear severity classifications to guide researcher effort

## Variant hunting
['Host header injection across UZ Leuven infrastructure despite reverse proxy configuration', 'IP whitelisting bypass techniques on cardsonline.azdiest.be and cardsonlinetst.azdiest.be', 'Geographic IP restriction bypass on wp5-truststroke.uzleuven.be (BE/NL only /api/ access)', 'OAuth consent phishing attacks against Stripe MCP and other OAuth implementations', 'Dynamic client registration vulnerabilities in MCP ecosystem clients', 'Supply chain attacks through Spotify CLI distribution channel']

## MITRE ATT&CK
- T1190
- T1598.003
- T1199
- T1021.004
- T1556.001
- T1566.002
- T1091

## Notes
This appears to be a screenshot/data export from HuntDash.xyz, a third-party bug bounty scope aggregation tool. The dashboard does not describe an actual vulnerability but rather aggregates live scope data from multiple bug bounty platforms. Key observations: (1) UZ Leuven healthcare program emphasizes reverse proxy validation and IP whitelisting as security controls; (2) Stripe explicitly rejects OAuth consent phishing as vulnerability due to user responsibility model; (3) Multiple CRITICAL tier targets indicate aggressive program recruitment; (4) Geographic and network-level restrictions common in healthcare/financial sector scopes; (5) Staging instance testing requirement (Mozilla) is security best practice. This tool is valuable for researchers but highlights the distributed nature of modern bug bounty programs.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-19*
