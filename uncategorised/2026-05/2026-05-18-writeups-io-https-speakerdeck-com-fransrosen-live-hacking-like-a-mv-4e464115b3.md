# Live Hacking like a MVH – A walkthrough on methodology and strategies to win big

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-18
- **Author:** Various
- **Program:** Multiple (Uber, Salesforce, Zenefits, Shopify, Oath, Mapbox, Dropbox)
- **Bounty:** Not specified in document
- **Severity:** N/A
- **Vuln types:** Submitted by:quas
- **Category:** uncategorised
- **Writeup:** https://speakerdeck.com/fransrosen/live-hacking-like-a-mvh-a-walkthrough-on-methodology-and-strategies-to-win-big

## Summary
This is a methodology and strategy presentation by Frans Rosén from BountyCon 2019 focusing on approaches to identify and exploit vulnerabilities at scale in bug bounty programs. The presentation covers frameworks for finding high-impact bugs rather than detailing specific vulnerability types.

## Attack scenario (step by step)
1. Develop systematic methodology for vulnerability discovery across target applications
2. Apply reconnaissance and information gathering techniques to identify attack surfaces
3. Execute targeted testing strategies based on application architecture and technology stack
4. Document and validate findings through proof-of-concept demonstrations
5. Prioritize high-impact vulnerabilities based on scope and business logic
6. Report findings through coordinated disclosure processes

## Root cause
Not applicable - presentation focuses on methodology rather than specific technical flaws

## Attacker mindset
Professional bug bounty researcher adopting structured, systematic approaches to vulnerability discovery at scale. Emphasizes methodological thinking, strategic target selection, and optimization of research efforts to identify high-value findings in competitive bounty environments.

## Defensive takeaways
- Implement comprehensive input validation across all application layers
- Establish secure API design principles with proper authentication and authorization
- Conduct regular security assessments using systematic methodologies similar to attacker approaches
- Maintain threat modeling aligned with attacker research strategies
- Deploy automated security testing alongside manual code review
- Monitor for patterns of systematic reconnaissance activities

## Variant hunting
Apply Frans Rosén's documented methodologies to: X-Correlation Injections in server-side contexts; hot jar swapping for RCE chains; OAuth flow manipulation; format injection techniques; AEM misconfiguration patterns; modern web technology attack surfaces

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1592 - Gather Victim Host Information
- T1589 - Gather Victim Identity Information
- T1598 - Phishing for Information
- T1526 - Acquire Infrastructure

## Notes
Presentation deck without full transcript; lacks specific technical details. Author is highly accomplished bug bounty researcher with consistent MVH (Most Valuable Hacker) wins. Presentation emphasizes methodology over specific vulnerabilities, suggesting focus on foundational approaches to systematic security research and competitive bug bounty hunting strategies.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-18*
