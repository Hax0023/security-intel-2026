# HuntDash Bug Bounty Platform - Scope Configuration Analysis

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-01
- **Author:** Various
- **Program:** Multiple (UZ Leuven/Intigriti, Stripe/HackerOne, Spotify/HackerOne, MercadoLibre/HackerOne, Circle/HackerOne, Mozilla/HackerOne)
- **Bounty:** Varies by program and severity tier
- **Severity:** INFORMATIONAL
- **Vuln types:** Submitted by:quas
- **Category:** uncategorised
- **Writeup:** https://huntdash.xyz/

## Summary
This is a bug bounty dashboard aggregation platform showing recent scope changes across multiple security programs. The content displays scope definitions, severity tiers, and program guidelines rather than detailing a specific vulnerability. This appears to be a dashboard interface for tracking bounty program targets rather than a security research writeup.

## Attack scenario (step by step)
1. Attacker reviews the exposed scope dashboard to identify target applications
2. Attacker identifies high-value targets (CRITICAL/HIGH severity) across multiple programs
3. Attacker maps specific endpoints and their tier classifications to understand bounty payouts
4. Attacker identifies scope gaps (wildcard entries with LOW severity) for potential testing
5. Attacker notes infrastructure details (IP ranges, reverse proxies, Host header dependencies)
6. Attacker prioritizes testing based on severity tier and bounty amount

## Root cause
This is not a vulnerability writeup but rather a scope tracking dashboard. If there is a security issue, it would relate to potential information disclosure of bounty program scopes through an accessible dashboard interface.

## Attacker mindset
A security researcher using this platform to efficiently identify and prioritize high-value targets across multiple bug bounty programs. An attacker with malicious intent could use the exposed scope information to map attack surfaces and understand organizational security boundaries.

## Defensive takeaways
- Implement access controls on bug bounty dashboard platforms to restrict scope visibility to authorized testers only
- Avoid exposing sensitive infrastructure details (IP ranges, internal hostnames, reverse proxy configurations) in public-facing scope documents
- Use tier-based filtering to limit information disclosure to appropriate user roles
- Monitor dashboard access logs for suspicious reconnaissance activity
- Implement Host header validation on reverse proxies to prevent header spoofing attacks mentioned in UZ Leuven scope
- Clearly document scope rules and exclusions to reduce ambiguous testing scenarios

## Variant hunting
Similar scope information leakage on other HackerOne/Intigriti dashboards; Host header injection vectors in reverse proxy configurations; IP whitelist bypasses using header manipulation; wildcard scope interpretation differences across programs; testing environment exposure (staging URLs like relay.allizom.org)

## MITRE ATT&CK
- T1592 - Gather Victim Host Information
- T1590 - Gather Victim Network Information
- T1598 - Phishing for Information
- T1200 - Hardware Additions

## Notes
This appears to be a screenshot of HuntDash.xyz, a third-party aggregation tool for tracking bug bounty scope changes. The content is informational rather than a vulnerability report. No actual exploitation or vulnerability details are present. The dashboard aggregates public scope information from multiple platforms (Intigriti, HackerOne) to help security researchers track program updates. Not a traditional bug bounty writeup format.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-01*
