# Live Hacking like a MVH – A walkthrough on methodology and strategies to win big

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-17
- **Author:** Various
- **Program:** Multiple (Uber, Salesforce, Zenefits, Shopify, Oath, Mapbox, Dropbox)
- **Bounty:** Not specified in content
- **Severity:** Informational
- **Vuln types:** Submitted by:quas
- **Category:** uncategorised
- **Writeup:** https://speakerdeck.com/fransrosen/live-hacking-like-a-mvh-a-walkthrough-on-methodology-and-strategies-to-win-big

## Summary
This is a presentation deck from Frans Rosén delivered at BountyCon 2019 covering methodologies and strategies for successful bug bounty hunting. Rather than detailing specific vulnerabilities, it serves as a meta-discussion of approaches that have led to multiple MVH (Most Valuable Hacker) awards across major platforms. The presentation emphasizes systematic methodology over individual vulnerability types.

## Attack scenario (step by step)
1. Researcher identifies target scope through bug bounty program offerings
2. Applies structured reconnaissance and information gathering methodologies
3. Maps application architecture and trust boundaries systematically
4. Develops hypothesis-driven testing strategies based on gathered intelligence
5. Executes targeted exploitation focusing on high-impact vulnerability classes
6. Documents findings with clear impact assessment for submission and awards

## Root cause
Not applicable - this is a methodology presentation rather than a specific vulnerability writeup. The deck discusses strategies for identifying vulnerabilities systematically rather than analyzing root causes of particular flaws.

## Attacker mindset
Competitive, methodology-focused researcher seeking to maximize impact and recognition within bug bounty ecosystems. Emphasis on systematic approaches, team collaboration (multiple team entries), and focusing effort on high-reward targets. Demonstrates persistence across multiple programs and events with evolving strategies.

## Defensive takeaways
- Implement comprehensive threat modeling covering architectural boundaries and trust zones
- Establish structured security testing frameworks beyond common OWASP categories
- Develop detection capabilities for systematic reconnaissance and enumeration activities
- Create security culture emphasizing continuous assessment against evolving methodologies
- Implement application-level logging for unusual information disclosure patterns
- Establish rapid response processes for high-impact vulnerability classes

## Variant hunting
Look for presentations and materials from other MVH winners discussing similar methodology-driven approaches; examine Detectify research blogs for specific vulnerability classes; review Frans Rosén's other decks (X-Correlation Injections, OAuth account hijacking, RCE via hot jar swapping) for concrete exploitation patterns.

## MITRE ATT&CK
- T1592 - Gather Victim Host Information
- T1589 - Gather Victim Identity Information
- T1598 - Phishing for Information
- T1526 - Exposure of Cloud Service Credentials
- T1046 - Network Service Discovery
- T1087 - Account Discovery

## Notes
This is a meta-level security presentation about bug bounty methodology rather than a specific vulnerability writeup. The value lies in understanding the systematic approaches of elite researchers. Content appears truncated in the provided source. Primary insight is that consistent MVH wins correlate with methodology, team collaboration, and deep understanding of target architectures rather than single-technique exploitation. Frans Rosén's track record across multiple platforms suggests versatility and adaptability in reconnaissance and exploitation approaches.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-17*
