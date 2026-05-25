# Live Hacking like a MVH – A walkthrough on methodology and strategies to win big

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-25
- **Author:** Various
- **Program:** Multiple (Uber, Shopify, Salesforce, Zenefits, Oath, Mapbox, Dropbox)
- **Bounty:** Multiple MVH (Most Valuable Hacker) awards and significant bug bounty winnings
- **Severity:** Informational
- **Vuln types:** Submitted by:quas
- **Category:** uncategorised
- **Writeup:** https://speakerdeck.com/fransrosen/live-hacking-like-a-mvh-a-walkthrough-on-methodology-and-strategies-to-win-big

## Summary
This is a presentation on bug bounty hunting methodology and strategies by Frans Rosén, a top-ranked security researcher on HackerOne. The deck outlines approaches and techniques for identifying high-impact vulnerabilities across major technology companies, based on his experience winning multiple MVH competitions and securing significant bounties.

## Attack scenario (step by step)
1. Researcher identifies target companies with active bug bounty programs
2. Conducts reconnaissance and information gathering on target application architecture
3. Applies systematic fuzzing, format injection, and context-breaking techniques
4. Discovers vulnerabilities through OAuth flows, hot jar swapping, and memory disclosure methods
5. Documents findings and submits to bug bounty program for validation
6. Collaborates with program teams to remediate while earning MVH recognition and bounty rewards

## Root cause
The presentation itself is not a vulnerability writeup but rather a methodology guide. The referenced vulnerabilities stem from insufficient input validation, insecure deserialization, OAuth implementation flaws, and inadequate separation of security contexts in web applications.

## Attacker mindset
Systematic, methodical researcher focused on discovering high-impact vulnerabilities through structured testing rather than random fuzzing. Emphasizes understanding application architecture, using advanced techniques like format injection and memory dumping, and testing edge cases in authentication flows. Mindset is collaborative within bug bounty ecosystem while maintaining offensive security research techniques.

## Defensive takeaways
- Implement rigorous input validation and sanitization across all entry points
- Secure OAuth implementations with proper state validation and PKCE
- Prevent deserialization of untrusted data and implement integrity checks
- Establish proper security context isolation between administrative and user contexts
- Conduct regular security testing including fuzzing and format injection attacks
- Implement memory safety protections and prevent information disclosure through detailed error messages
- Maintain active bug bounty programs with clear scope and responsive triage processes

## Variant hunting
Search for similar vulnerabilities in: OAuth implementations across platforms, hot swapping/dynamic code loading mechanisms, memory disclosure through side-channels, format string and format injection in various parsers, privilege escalation through context confusion, and information disclosure in administrative interfaces.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1550.001 - Use Alternate Authentication Material (OAuth token theft)
- T1552 - Unsecured Credentials
- T1056 - Input Capture
- T1548 - Abuse Elevation Control Mechanism
- T1592 - Gather Victim Identity Information

## Notes
This is a presentation on methodology rather than a specific vulnerability disclosure. Frans Rosén is a recognized elite bug bounty hunter with multiple MVH awards. The slides reference several attack categories (X-Correlation Injections, hot jar swapping RCE, OAuth account hijacking, format injection, AEM vulnerabilities) that suggest focus on advanced attack vectors. The presentation was delivered at BountyCon 2019, a competitive security research event hosted by Facebook and Google.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-25*
