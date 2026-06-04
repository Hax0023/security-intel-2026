# Live Hacking like a MVH – A walkthrough on methodology and strategies to win big

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-04
- **Author:** Various
- **Program:** Multiple (Uber, Shopify, Salesforce, Oath, Dropbox, Mapbox, Zenefits)
- **Bounty:** N/A - Methodology/Training Presentation
- **Severity:** N/A
- **Vuln types:** Submitted by:quas
- **Category:** uncategorised
- **Writeup:** https://speakerdeck.com/fransrosen/live-hacking-like-a-mvh-a-walkthrough-on-methodology-and-strategies-to-win-big

## Summary
This is a presentation deck from Frans Rosén delivered at BountyCon 2019 covering methodology and strategies for successful bug bounty hunting at scale. Rather than a specific vulnerability writeup, it serves as a guide for researchers to systematically identify and exploit security issues across multiple programs to achieve competitive advantage in live hacking competitions.

## Attack scenario (step by step)
1. Establish reconnaissance and information gathering across target applications
2. Identify attack surface expansion through lesser-known endpoints and features
3. Apply systematic fuzzing and format injection techniques to uncover information disclosure
4. Chain multiple findings together to escalate impact (e.g., OAuth flows, context injection)
5. Prioritize high-value targets and focus on novel attack vectors others overlook
6. Document and report findings strategically to maximize reputation and bounty earnings

## Root cause
No specific vulnerability - presentation focuses on attacker methodology rather than a single root cause. Covers broad categories including OAuth implementation flaws, context injection, format injection, and information disclosure vulnerabilities.

## Attacker mindset
Competitive researcher mindset focused on efficiency, scalability, and high-impact findings. Prioritizes methodology over luck, employs systematic approach to vulnerability discovery, seeks novel attack vectors that others miss, aims to maximize both reputation and financial reward through strategic targeting of multiple high-value programs simultaneously.

## Defensive takeaways
- Implement comprehensive input validation and output encoding across all contexts (HTML, JavaScript, URL, CSS)
- Secure OAuth implementations by validating all parameters and preventing state manipulation
- Apply defense-in-depth to prevent information disclosure through fuzzing or format injection
- Monitor and restrict exposure of debug endpoints, error messages, and verbose logging
- Conduct regular security assessments focusing on lesser-known features and endpoints
- Establish consistent security testing across all application layers and technologies
- Implement rate limiting and anomaly detection for fuzzing-based reconnaissance attempts

## Variant hunting
Researchers should explore: (1) Similar OAuth implementations in other applications for 'dirty dancing' account hijacking patterns; (2) Format injection vulnerabilities in different serialization formats (JSON, XML, YAML); (3) Context injection across various server-side template engines and execution contexts; (4) Hot jar/dependency swapping in Java applications and other managed runtime environments; (5) Information disclosure through passive aggressive configuration in content management systems like AEM

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1598 - Phishing - Spearphishing Link (OAuth context)
- T1040 - Network Sniffing
- T1592 - Gather Victim Host Information
- T1526 - Enumerate External Cloud Assets
- T1057 - Process Discovery
- T1518 - Software Discovery
- T1538 - Cloud Service Discovery
- T1552 - Unsecured Credentials

## Notes
This is a presentation/methodology guide rather than a specific vulnerability writeup. Frans Rosén is a highly accomplished bug bounty researcher (#6 all-time on HackerOne) who has won multiple competitive hacking events. The presentation emphasizes systematic methodology for discovering and exploiting multiple vulnerability classes rather than detailing a single critical finding. Related presentations cover specific techniques: X-Correlation Injections, Apple RCE via jar swapping, OAuth account hijacking, AEM security issues, and web format injection. The content is valuable for understanding how elite researchers approach systematic vulnerability hunting at scale.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-04*
