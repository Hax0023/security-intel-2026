# Live Hacking like a MVH – A walkthrough on methodology and strategies to win big

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-22
- **Author:** Various
- **Program:** Multiple (Uber, Salesforce, Zenefits, Shopify, Oath, Mapbox, Dropbox)
- **Bounty:** Variable (multiple MVH competition wins)
- **Severity:** N/A
- **Vuln types:** Submitted by:quas
- **Category:** uncategorised
- **Writeup:** https://speakerdeck.com/fransrosen/live-hacking-like-a-mvh-a-walkthrough-on-methodology-and-strategies-to-win-big

## Summary
This is a presentation deck from Frans Rosén at BountyCon 2019 detailing his methodology and strategies for successful bug bounty hunting. Rather than describing a specific vulnerability, it serves as a meta-analysis of techniques and approaches that have enabled the author to win multiple Most Valuable Hacker awards across major platforms.

## Attack scenario (step by step)
1. Reconnaissance phase: Enumerate and map target infrastructure, APIs, and endpoints systematically
2. Analysis phase: Apply structured methodology to identify classes of vulnerabilities across scope
3. Exploitation phase: Test discovered weaknesses with consideration for impact and severity
4. Validation phase: Confirm reproducibility and gather evidence of the vulnerability
5. Documentation phase: Create clear, detailed reports demonstrating the exploit chain
6. Submission phase: Present findings strategically to maximize bounty and reputation gains

## Root cause
Not applicable - presentation is educational content on bug bounty methodology rather than analysis of a specific vulnerability root cause

## Attacker mindset
Methodical, strategic approach to vulnerability research with emphasis on scalability and consistency. Focus on understanding patterns across multiple programs, leveraging reputation metrics, and optimizing for both financial returns and competitive standing in the bug bounty community.

## Defensive takeaways
- Implement systematic security testing across all infrastructure and endpoints to prevent structured enumeration
- Establish clear scope definitions and responsible disclosure processes for bug bounty programs
- Create layered authentication and authorization controls to prevent common exploitation chains
- Develop rapid patching procedures to minimize window between disclosure and remediation
- Monitor and log suspicious reconnaissance activity that may precede focused vulnerability testing
- Conduct regular security assessments using similar methodology to identify issues before bounty hunters

## Variant hunting
Search for other presentations or writeups by Frans Rosén on specific vulnerability classes (X-Correlation Injections, RCE chains, OAuth attacks, format injection, AEM vulnerabilities). Cross-reference HackerOne disclosed reports from this researcher to understand applied methodology.

## MITRE ATT&CK
- T1592
- T1589
- T1590
- T1526
- T1518
- T1087
- T1190

## Notes
Source material is a presentation deck without detailed technical writeup. The actual vulnerability details and methodologies are contained within the presentation slides which are not fully transcribed in the provided content. This represents meta-level bug bounty knowledge rather than specific vulnerability analysis. Referenced other research topics suggest focus on injection attacks, authentication bypass, RCE chains, and memory disclosure techniques.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-22*
