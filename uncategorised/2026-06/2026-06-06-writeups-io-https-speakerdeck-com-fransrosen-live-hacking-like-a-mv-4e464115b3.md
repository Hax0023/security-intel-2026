# Live Hacking like a MVH – A walkthrough on methodology and strategies to win big

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-06
- **Author:** Various
- **Program:** Multiple (Uber, Salesforce, Zenefits, Shopify, Oath, Mapbox, Dropbox)
- **Bounty:** Variable - Multiple MVH (Most Valuable Hacker) wins across HackerOne events
- **Severity:** N/A
- **Vuln types:** Submitted by:quas
- **Category:** uncategorised
- **Writeup:** https://speakerdeck.com/fransrosen/live-hacking-like-a-mvh-a-walkthrough-on-methodology-and-strategies-to-win-big

## Summary
Presentation slides from Frans Rosén covering methodology and strategies for successful bug bounty hunting at scale. This is a meta-level educational talk about effective penetration testing approaches demonstrated through the speaker's track record of winning multiple HackerOne bug bounty competitions.

## Attack scenario (step by step)
1. Identify target scope and surface area mapping across multiple programs
2. Apply systematic reconnaissance and enumeration techniques to discover attack vectors
3. Test for common vulnerability classes with focus on high-impact findings
4. Develop exploit chains or proof-of-concepts demonstrating real business impact
5. Document findings comprehensively for bounty submission and potential retest
6. Iterate methodology across multiple targets to maximize earnings and reputation

## Root cause
N/A - This is a presentation about bug bounty methodology rather than a specific vulnerability writeup

## Attacker mindset
Systematic, scalable approach to vulnerability research. Focus on high-impact findings, efficient reconnaissance, and methodical testing across multiple targets. Emphasis on documentation and communication for successful bounty submissions.

## Defensive takeaways
- Implement comprehensive security testing across entire application surface
- Establish robust penetration testing programs and continuous security validation
- Review interconnected components for chaining opportunities that amplify impact
- Maintain active bug bounty programs to identify vulnerabilities before attackers weaponize them
- Document security testing methodologies and ensure consistent application across teams
- Monitor for both individual vulnerabilities and exploit chain patterns

## Variant hunting
Look for similar methodology applications in: OAuth flow vulnerabilities, server-side injection attacks, format injection techniques, memory disclosure via fuzzing, third-party component vulnerabilities (JAR swapping), and context-breaking injection vectors as referenced in related talks by same presenter

## MITRE ATT&CK
- T1190
- T1592
- T1589
- T1598
- T1199

## Notes
This is a methodology/strategy presentation rather than a specific vulnerability disclosure. Speaker is a prolific bug bounty researcher (#6 HackerOne all-time) with multiple MVH wins. Related presentations suggest expertise in OAuth attacks, RCE via dependency injection, injection flaws, and information disclosure techniques. Content appears to be primarily slides without detailed transcript, limiting specific vulnerability analysis.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-06*
