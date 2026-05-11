# Live Hacking like a MVH – A walkthrough on methodology and strategies to win big

## Metadata
- **Source:** writeups.io
- **Date:** 
- **Author:** Various
- **Program:** Multiple (Facebook, Google, Uber, Shopify, Salesforce, Zenefits, Oath, Mapbox, Dropbox)
- **Bounty:** Multiple MVH wins (exact amounts not specified in available content)
- **Severity:** unknown
- **Vuln types:** See writeup
- **Category:** uncategorised
- **Writeup:** https://speakerdeck.com/fransrosen/live-hacking-like-a-mvh-a-walkthrough-on-methodology-and-strategies-to-win-big

## Summary
This is a presentation deck from BountyCon 2019 by Frans Rosén, a top-ranked bug bounty hunter (#6 on HackerOne all-time leaderboard), discussing methodology and strategies for winning major bug bounty competitions (MVH events). The presentation covers tactics and approaches used to identify and report high-impact vulnerabilities across multiple major technology companies.

## Attack scenario (step by step)
1. Reconnaissance and scoping of target applications within MVH competition parameters
2. Systematic methodology application to identify classes of vulnerabilities across targets
3. Prioritization of high-impact bugs based on severity and business criticality
4. Efficient exploitation and proof-of-concept development to demonstrate impact
5. Strategic reporting and disclosure coordination during time-limited competition
6. Collaboration with team members to maximize coverage and earnings

## Root cause
Not disclosed - presentation focuses on methodology rather than specific vulnerability analysis

## Attacker mindset
Strategic, methodical approach to bug bounty hunting as competitive sport; focus on scalable vulnerability discovery techniques; emphasis on understanding business context and impact; competitive team-based hunting mentality

## Defensive takeaways
- Implement comprehensive security testing methodologies similar to professional bug hunters
- Prioritize vulnerability classes that sophisticated hunters target systematically
- Establish robust vulnerability disclosure programs with clear scoping
- Monitor for patterns in high-impact bug discoveries to identify systemic weaknesses
- Consider continuous red team assessments using MVH-style comprehensive approaches

## Variant hunting
Presentation suggests systematic fuzzing, context-specific injection attacks (X-Correlation Injections), OAuth flow manipulation, format injection vulnerabilities, and memory disclosure techniques based on referenced talks

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1566 - Phishing
- T1557 - Man-in-the-Middle
- T1621 - Multi-Factor Authentication Interception
- T1040 - Traffic Capture or Redirection

## Notes
Source is a presentation deck with limited technical details visible in transcript. Full vulnerability specifics not disclosed in available content. Referenced related talks suggest expertise in OAuth attacks, injection attacks, and memory disclosure. Frans Rosén is highly credentialed professional bug bounty hunter with multiple MVH victories.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-11*
