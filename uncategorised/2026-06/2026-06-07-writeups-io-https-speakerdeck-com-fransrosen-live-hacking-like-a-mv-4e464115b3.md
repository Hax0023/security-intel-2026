# Live Hacking like a MVH – A walkthrough on methodology and strategies to win big

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-07
- **Author:** Various
- **Program:** Multiple (Facebook, Google, Uber, Shopify, Oath, Dropbox, Mapbox, Salesforce, Zenefits)
- **Bounty:** Multiple winners of major bug bounty competitions (MVH awards)
- **Severity:** Educational/Methodology
- **Vuln types:** Multiple vulnerability classes, Server-side injection, OAuth flow manipulation, Remote code execution, Information disclosure, Format injection
- **Category:** uncategorised
- **Writeup:** https://speakerdeck.com/fransrosen/live-hacking-like-a-mvh-a-walkthrough-on-methodology-and-strategies-to-win-big

## Summary
Frans Rosén presents a comprehensive methodology talk from BountyCon 2019 covering strategies and techniques for successful bug bounty hunting at scale. The presentation references multiple award-winning vulnerability discoveries including RCE, OAuth attacks, injection flaws, and information disclosure techniques. This is a methodology-focused educational presentation rather than a single vulnerability writeup.

## Attack scenario (step by step)
1. Identify target scope and potential attack vectors across large-scale applications
2. Apply systematic reconnaissance and fuzzing methodologies to uncover vulnerabilities
3. Discover server-side injection points, OAuth flow weaknesses, or format injection opportunities
4. Develop proof-of-concept exploits demonstrating impact (RCE, account hijacking, data exfiltration)
5. Chain vulnerabilities together for maximum impact and bounty awards
6. Document findings with clear methodology demonstrating reproducibility and severity

## Root cause
Systemic security gaps in modern web technologies including improper input validation, inadequate OAuth flow protections, insecure deserialization, and insufficient access controls across multiple platforms

## Attacker mindset
Methodical, scalable approach to vulnerability research with focus on high-impact findings. Prioritizes understanding application architecture and business logic to identify critical vulnerabilities. Combines passive reconnaissance with active fuzzing and testing frameworks to maximize discovery efficiency.

## Defensive takeaways
- Implement strict input validation and context-aware output encoding across all user input processing
- Secure OAuth implementations with proper state validation and token handling
- Audit serialization/deserialization mechanisms for unsafe object handling
- Establish comprehensive logging and monitoring for suspicious patterns
- Conduct regular security assessments using active fuzzing and penetration testing
- Implement defense-in-depth with multiple layers of validation
- Review format handling and parsing logic for injection vulnerabilities
- Maintain secure coding practices for third-party library management

## Variant hunting
['Search for similar injection patterns in other request processing pipelines', 'Test OAuth implementations across different platforms for state validation bypasses', 'Fuzz file format handlers and parsers for memory corruption', 'Analyze dependency chains for hot-swap or dynamic code loading vulnerabilities', 'Test API endpoints for information disclosure through error messages', 'Examine server-side context handling in templating engines', 'Probe authentication flows for dirty dancing attacks in multi-step processes']

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1556 - Modify Authentication Process
- T1048 - Exfiltration Over Alternative Protocol
- T1083 - File and Directory Discovery
- T1592 - Gather Victim Host Information
- T1598 - Phishing for Information
- T1566 - Phishing
- T1199 - Trusted Relationship

## Notes
This is a presentation on methodology and strategies rather than a single vulnerability disclosure. Frans Rosén is a highly accomplished bug bounty researcher with multiple MVH (Most Valuable Hacker) awards. The deck references several distinct vulnerability classes discovered across major platforms. The actual technical details of individual vulnerabilities are referenced in other presentations (X-Correlation Injections, RCE on Apple via JAR swapping, OAuth dirty dancing, AEM vulnerabilities). This talk emphasizes the importance of systematic methodology, proper scoping, and chainable vulnerability discovery for maximum impact in competitive bug bounty environments.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-07*
