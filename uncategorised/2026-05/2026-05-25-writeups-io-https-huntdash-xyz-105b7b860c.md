# HuntDash - Bug Bounty Program Scope Aggregator

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-25
- **Author:** Various
- **Program:** Multiple (UZ Leuven/Intigriti, Stripe/HackerOne, Spotify/HackerOne, MercadoLibre/HackerOne, Circle BBP/HackerOne, Mozilla/HackerOne)
- **Bounty:** Varies by program and severity tier
- **Severity:** INFORMATIONAL
- **Vuln types:** Submitted by:quas
- **Category:** uncategorised
- **Writeup:** https://huntdash.xyz/

## Summary
This is a dashboard aggregating bug bounty program scopes and recent changes across multiple platforms, not a vulnerability writeup. It displays scope information, target assets, and historical changes for various organizations' security testing programs. The content includes program guidelines, tier definitions, and scope clarifications.

## Attack scenario (step by step)


## Root cause
This is not a vulnerability but rather a reference dashboard/tool for bug bounty hunters.

## Attacker mindset
Not applicable - this is a scope reference tool rather than a security finding.

## Defensive takeaways
- Maintain clear scope definitions and host header policies for bug bounty programs
- Document IP whitelisting requirements explicitly to prevent scope confusion
- Specify geographical restrictions (e.g., BE/NL IP requirements) clearly in scope documentation
- Distinguish between tier levels based on vulnerability severity and exploitation difficulty
- Provide staging/testing environments separate from production systems
- Request identifying headers (X-HackerOne-Research) to differentiate authorized testing from malicious activity

## Variant hunting
Researchers can use this scope aggregator to identify common patterns in organization security policies, such as: reverse proxy IP ranges that may indicate architecture, wildcard scope entries suggesting centralized infrastructure, host-header validation as a security control, and geographical IP restrictions indicating data residency requirements.

## MITRE ATT&CK


## Notes
This appears to be the HuntDash.xyz platform itself - a meta-tool for aggregating bug bounty scope information. The 'bug' referenced is not a security vulnerability but rather the tool's purpose: displaying up-to-date scope information from multiple bug bounty platforms. The JSON structure assumes this is submitted as a reference document rather than an actual vulnerability report.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-25*
