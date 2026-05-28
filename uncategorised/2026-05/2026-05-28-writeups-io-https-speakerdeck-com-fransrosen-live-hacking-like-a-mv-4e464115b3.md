# Live Hacking like a MVH – A walkthrough on methodology and strategies to win big

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-28
- **Author:** Various
- **Program:** Multiple (Uber, Salesforce, Zenefits, Shopify, Oath, Mapbox, Dropbox)
- **Bounty:** Multiple MVH winners across HackerOne events
- **Severity:** N/A
- **Vuln types:** Submitted by:quas
- **Category:** uncategorised
- **Writeup:** https://speakerdeck.com/fransrosen/live-hacking-like-a-mvh-a-walkthrough-on-methodology-and-strategies-to-win-big

## Summary
This is a methodology presentation by Frans Rosén from BountyCon 2019 discussing strategies and approaches for winning bug bounty competitions (Most Valuable Hacker events). The deck outlines research methodology, hacking techniques, and competitive strategies rather than detailing specific vulnerabilities.

## Attack scenario (step by step)
1. Establish systematic reconnaissance and information gathering methodology
2. Identify attack surface areas using fuzzing and information disclosure techniques
3. Apply context-aware injection techniques across multiple technologies
4. Leverage OAuth flow manipulation and authentication weaknesses
5. Execute format injection and memory dumping techniques
6. Document and report high-impact vulnerabilities for competitive advantage

## Root cause
Presentation focuses on methodology rather than specific technical root causes. General themes include insufficient input validation, OAuth implementation flaws, format handling vulnerabilities, and inadequate authentication controls.

## Attacker mindset
Competitive bug bounty hunter seeking maximum impact and recognition. Emphasis on systematic methodology, continuous learning from multiple targets, and developing reusable techniques across different technology stacks. Focus on finding novel attack vectors and demonstrating technical sophistication.

## Defensive takeaways
- Implement comprehensive input validation and context-aware output encoding
- Secure OAuth implementations with proper state validation and token handling
- Audit authentication and sign-in flows for account hijacking vulnerabilities
- Establish memory safety practices to prevent disclosure attacks
- Conduct fuzzing campaigns against custom protocols and formats
- Monitor for X-Correlation injection and server-side context manipulation
- Review hot jar swapping and dynamic loading mechanisms for RCE
- Implement strict format validation and prevent format string attacks

## Variant hunting
Search for related presentations by Frans Rosén on specific topics: X-Correlation Injections, hot jar swapping RCE on Apple, OAuth account hijacking, fuzzing methodologies, format injection, and AEM security. Cross-reference MVH winning reports from 2017-2018 timeframe on HackerOne for specific vulnerability details.

## MITRE ATT&CK
- T1190
- T1040
- T1557
- T1040
- T1598
- T1187
- T1566
- T1539

## Notes
This is a presentation deck rather than a detailed vulnerability writeup. It references multiple successful bug discoveries across major platforms but doesn't provide technical exploit details. The presentation emphasizes competitive hacking methodology and strategy. Original source material appears to be slides without full transcript content. Actual vulnerability details would be found in individual reports or Frans Rosén's blog at labs.detectify.com.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-28*
