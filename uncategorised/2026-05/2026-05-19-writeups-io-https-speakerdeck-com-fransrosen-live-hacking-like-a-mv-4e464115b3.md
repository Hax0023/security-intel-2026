# Live Hacking like a MVH – A walkthrough on methodology and strategies to win big

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-19
- **Author:** Various
- **Program:** Multiple (Uber, Salesforce, Zenefits, Shopify, Oath, Mapbox, Dropbox)
- **Bounty:** Not specified in source material
- **Severity:** N/A
- **Vuln types:** Submitted by:quas
- **Category:** uncategorised
- **Writeup:** https://speakerdeck.com/fransrosen/live-hacking-like-a-mvh-a-walkthrough-on-methodology-and-strategies-to-win-big

## Summary
This is a methodology and strategy presentation by Frans Rosén delivered at BountyCon 2019, focusing on approaches to identify and exploit vulnerabilities in major technology companies. The presentation documents his experience winning multiple bug bounty competitions (MVH - Most Valuable Hacker) across various platforms and companies.

## Attack scenario (step by step)
1. Identify target scope and reconnaissance objectives within authorized bug bounty programs
2. Apply systematic methodology to discover vulnerability classes (RCE, OAuth flaws, format injection, information disclosure)
3. Leverage fuzzing techniques and targeted testing strategies to trigger edge cases
4. Document and validate findings before responsible disclosure
5. Compete in live hacking events to demonstrate exploitation techniques under time constraints
6. Refine approach based on results to maximize impact and bounty rewards

## Root cause
Presentation material does not detail specific vulnerabilities - focuses on methodology rather than root causes of particular bugs

## Attacker mindset
Systematic, research-driven approach prioritizing high-impact vulnerabilities; competitive motivation evident through MVH tournament wins; emphasis on replicable methodology over one-off exploits; focus on novel attack vectors (OAuth flows, format injection, hot jar swapping, XPath/X-Correlation injection)

## Defensive takeaways
- Implement comprehensive input validation and output encoding across all tiers
- Secure OAuth implementation with proper state management and token handling
- Monitor and restrict deserialization of untrusted data
- Conduct regular fuzzing and edge-case testing in development
- Establish structured vulnerability disclosure programs and take researcher reports seriously
- Implement defense-in-depth for information disclosure vectors
- Review third-party dependencies (hot jar context suggests JAR/dependency risks)

## Variant hunting
Search for similar presentations and write-ups by Frans Rosén on Detectify Labs covering X-Correlation Injections, Apple RCE through hot jar swapping, OAuth account hijacking, and AEM vulnerabilities; examine other MVH competition winning submissions from 2017-2018 timeframe

## MITRE ATT&CK
- T1190
- T1528
- T1552
- T1518
- T1589
- T1598

## Notes
This is a methodology presentation rather than a specific bug writeup. The actual technical details of individual vulnerabilities are referenced through other Detectify Labs presentations by the same author. The presentation emphasizes competitive bug bounty hunting strategy and winning approaches at live hacking events (MVH tournaments). Key vulnerability classes mentioned include RCE, OAuth flow attacks, format injection, and information disclosure vulnerabilities.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-19*
