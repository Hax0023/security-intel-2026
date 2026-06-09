# Live Hacking like a MVH – A walkthrough on methodology and strategies to win big

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-09
- **Author:** Various
- **Program:** Multiple (Uber, Salesforce, Zenefits, Shopify, Oath, Mapbox)
- **Bounty:** Variable (MVH competition winnings)
- **Severity:** Informational
- **Vuln types:** Submitted by:quas
- **Category:** uncategorised
- **Writeup:** https://speakerdeck.com/fransrosen/live-hacking-like-a-mvh-a-walkthrough-on-methodology-and-strategies-to-win-big

## Summary
This is a presentation by Frans Rosén from BountyCon 2019 discussing methodologies and strategies for successful bug bounty hunting and competitive hacking events. Rather than describing a specific vulnerability, it outlines the approach and mindset needed to win major vulnerability hunting (MVH) competitions and maximize bug bounty earnings.

## Attack scenario (step by step)
1. Researcher identifies target programs with high-value vulnerabilities
2. Applies systematic methodology to discover novel attack vectors
3. Tests across multiple attack surfaces (web, API, OAuth flows, format injection)
4. Develops proof-of-concept exploits demonstrating impact
5. Documents findings for submission to bug bounty programs
6. Iterates on methodology based on results to improve hit rate

## Root cause
N/A - This is a methodology presentation, not a specific vulnerability writeup

## Attacker mindset
Persistent, methodical researcher focused on understanding attack surface comprehensively rather than opportunistic vulnerability hunting. Emphasis on strategy, systematic exploration, and learning from each engagement to refine techniques and maximize success in competitive environments.

## Defensive takeaways
- Implement comprehensive input validation across all attack surfaces (web, API, OAuth)
- Review authentication and authorization flows for 'dirty dancing' and token manipulation
- Audit serialization and deserialization mechanisms for format injection vulnerabilities
- Conduct regular security assessments using fuzzing and information disclosure techniques
- Monitor for X-correlation injections and server-side context breaks
- Establish robust code review processes for modern web technologies
- Maintain updated patch management for dependency vulnerabilities
- Deploy information disclosure protections and error handling hardening

## Variant hunting
Look for similar attack patterns in: OAuth flow implementations across different platforms, format injection in custom serialization protocols, memory dumping techniques in other applications, dependency vulnerabilities in build tools (hot jar swapping patterns), server-side template injection variants, and authentication bypass techniques in sign-in flows.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1056 - Input Capture
- T1110 - Brute Force
- T1040 - Traffic Sniffing
- T1557 - Man-in-the-Middle
- T1539 - Steal Web Session Cookie
- T1528 - Steal Application Access Token

## Notes
This is a presentation deck from a competitive hacking event rather than a traditional bug bounty writeup. Content focuses on high-level strategies for winning MVH competitions. Frans Rosén is ranked #6 on HackerOne all-time leaderboard, indicating expertise in diverse vulnerability classes. Referenced talks hint at advanced techniques: X-Correlation Injections, RCE via dependency manipulation (Apple hot jar), OAuth account hijacking, fuzzing methodologies, format injection with memory dumping, and AEM (Adobe Experience Manager) vulnerabilities.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-09*
