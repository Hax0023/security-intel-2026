# Live Hacking like a MVH – A walkthrough on methodology and strategies to win big

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-01
- **Author:** Various
- **Program:** Multiple (Uber, Salesforce, Zenefits, Shopify, Oath, Mapbox, Dropbox)
- **Bounty:** Not specified in content
- **Severity:** N/A
- **Vuln types:** Submitted by:quas
- **Category:** uncategorised
- **Writeup:** https://speakerdeck.com/fransrosen/live-hacking-like-a-mvh-a-walkthrough-on-methodology-and-strategies-to-win-big

## Summary
This is a presentation deck from BountyCon 2019 by Frans Rosén, a top-ranked security researcher, outlining methodology and strategies for successful bug bounty hunting and live hacking competitions. The talk documents approaches used to win multiple major bug bounty tournament events (MVH) across major technology companies.

## Attack scenario (step by step)
1. Identify target scope and potential vulnerability classes based on application architecture
2. Apply systematic reconnaissance and information gathering techniques
3. Develop custom testing methodology tailored to discovered attack surface
4. Execute targeted exploitation using identified vulnerability patterns
5. Document findings and prepare comprehensive write-ups for bounty submission
6. Iterate and refine techniques based on results to maximize impact and rewards

## Root cause
Not detailed in available content - presentation focuses on methodology rather than specific vulnerabilities

## Attacker mindset
Strategic approach to vulnerability research emphasizing systematic methodology, reusable techniques across programs, and focus on high-impact findings. Demonstrates competitive mindset in bug bounty tournaments with emphasis on both technical excellence and efficient resource allocation to maximize earnings and reputation.

## Defensive takeaways
- Implement comprehensive security testing across all architectural layers
- Establish proactive threat modeling based on common attack patterns used by skilled researchers
- Develop robust input validation and output encoding practices
- Conduct regular security assessments using adversarial methodologies
- Monitor for information disclosure vulnerabilities that enable reconnaissance
- Create bug bounty programs with clear scope and reasonable reward structures

## Variant hunting
Look for similar vulnerability patterns across different applications in the same technology stack; investigate architectural similarities in systems built by same vendors; examine edge cases in APIs and authentication mechanisms; test for information disclosure in error handling and debug endpoints

## MITRE ATT&CK
- T1592 - Gather Victim Host Information
- T1589 - Gather Victim Identity Information
- T1598 - Phishing for Information
- T1566 - Phishing
- T1190 - Exploit Public-Facing Application
- T1190 - Web Application Exploitation

## Notes
This is a methodology presentation rather than a detailed vulnerability writeup. Content focuses on Frans Rosén's background as #6 HackerOne researcher and multiple MVH competition wins. Actual technical vulnerabilities and specific exploitation techniques are referenced but not detailed in the available transcript. The presentation appears to cover attack methodology, reconnaissance strategies, and tournament-winning approaches rather than specific CVEs or vulnerability types.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-01*
