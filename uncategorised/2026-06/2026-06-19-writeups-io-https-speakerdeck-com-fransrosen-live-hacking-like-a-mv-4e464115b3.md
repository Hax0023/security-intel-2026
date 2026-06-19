# Live Hacking like a MVH – A walkthrough on methodology and strategies to win big

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-19
- **Author:** Various
- **Program:** Multiple (Uber, Salesforce, Zenefits, Shopify, Oath, Mapbox, Dropbox)
- **Bounty:** Not specified in presentation
- **Severity:** N/A
- **Vuln types:** Submitted by:quas
- **Category:** uncategorised
- **Writeup:** https://speakerdeck.com/fransrosen/live-hacking-like-a-mvh-a-walkthrough-on-methodology-and-strategies-to-win-big

## Summary
This is a conference presentation by Frans Rosén at BountyCon 2019 discussing methodology and strategies for successful bug bounty hunting at scale. The slides outline approaches used by a multiple-time MVH (Most Valuable Hacker) winner across major tech companies' bug bounty programs.

## Attack scenario (step by step)
1. Establish systematic reconnaissance methodology rather than random vulnerability scanning
2. Identify high-value targets through program analysis and scope assessment
3. Apply custom research techniques tailored to target technology stacks
4. Execute coordinated team-based hunting strategies during live hacking competitions
5. Document and prioritize findings based on impact and complexity
6. Submit high-quality reports to maximize bounty awards and reputation

## Root cause
Not applicable - this is a methodology presentation, not a specific vulnerability writeup

## Attacker mindset
Professional bug bounty hunter focused on systematic, high-impact vulnerability discovery. Emphasis on methodology, teamwork, and strategic targeting rather than opportunistic hacking. Goal is maximizing both financial rewards and reputation within competitive environments.

## Defensive takeaways
- Implement comprehensive vulnerability disclosure programs with clear scope boundaries
- Establish security review processes for emerging technology integrations
- Monitor and respond to sophisticated, coordinated vulnerability research efforts
- Create incentive structures that reward security researchers for quality findings
- Develop security testing standards that address both common and novel attack vectors
- Maintain updated asset inventories to understand attack surface exposure

## Variant hunting
Presentation discusses researching X-Correlation Injections, RCE through hot jar swapping, OAuth sign-in flow hijacking, format injection attacks, and AEM-based vulnerabilities. Variants would include similar logic flaws in other authentication flows, serialization mechanisms, and template engines.

## MITRE ATT&CK
- T1190
- T1621
- T1556
- T1552
- T1557
- T1040

## Notes
This is a methodology presentation rather than a specific bug writeup. The actual vulnerability details are referenced in other presentations by the same author (X-Correlation Injections, Apple RCE, OAuth account hijacking). The presentation demonstrates that competitive bug bounty success requires systematic research methodology, team coordination, and deep technical knowledge rather than ad-hoc scanning.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-19*
