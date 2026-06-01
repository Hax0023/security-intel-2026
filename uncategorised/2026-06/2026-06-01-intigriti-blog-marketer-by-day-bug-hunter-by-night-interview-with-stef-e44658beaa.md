# Marketer by Day, Bug Hunter by Night - Interview with Stefan Goossens

## Metadata
- **Source:** Intigriti Blog
- **Date:** 2026-06-01
- **Author:** Eleanor Barlow
- **Program:** Multiple (Red Bull, Private Programs, Intigriti)
- **Bounty:** Not specified - 3000+ reputation points accumulated
- **Severity:** N/A
- **Vuln types:** Hacker Spotlight
- **Category:** uncategorised
- **Writeup:** https://www.intigriti.com/researchers/blog/hacker-spotlight/marketer-by-day-bug-hunter-by-night-interview-with-stefan-goossens

## Summary
This is an interview with Stefan Goossens (G0053), a part-time bug bounty hunter and marketing professional from the Netherlands. The article discusses his journey into bug bounty hunting, skill development, and methodology rather than a specific vulnerability disclosure.

## Attack scenario (step by step)
1. Not applicable - this is an interview piece, not a vulnerability writeup
2. No specific attack is described
3. No technical exploitation is detailed
4. No proof-of-concept is provided
5. No vulnerability chain is documented
6. Content focuses on career development and methodology

## Root cause
Not applicable - no vulnerability analyzed

## Attacker mindset
Stefan employs a methodical, puzzle-solving approach focusing on business logic vulnerabilities and unexpected user behavior rather than technical exploits. He tests basic payloads first (XSS, SQLi) and examines error messages and application behavior to identify issues.

## Defensive takeaways
- Validate and sanitize all user inputs, including unexpected field combinations
- Implement proper access controls for business logic processes
- Prevent negative value transactions and validate business logic constraints
- Handle error messages carefully to avoid information disclosure
- Test application behavior when users deviate from expected workflows
- Security testing should include non-technical vulnerability discovery

## Variant hunting
Stefan's methodology of testing 'what happens if I do the opposite' and 'can I bypass this process' could be applied to: privilege escalation via workflow manipulation, price/quantity manipulation, state management vulnerabilities, multi-step process circumvention, and authorization bypass scenarios.

## MITRE ATT&CK
- T1190
- T1566
- T1082

## Notes
This is primarily an educational interview highlighting a successful part-time bug bounty hunter's journey and approach. Stefan emphasizes the importance of understanding application behavior, using proper tools (Caido, VPS infrastructure), and maintaining consistent focus on programs of interest. No specific CVE or vulnerability is disclosed in this content.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-01*
