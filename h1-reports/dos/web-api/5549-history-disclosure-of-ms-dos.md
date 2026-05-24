# History Disclosure of MS-DOS

## Metadata
- **Source:** HackerOne
- **Report:** 5549 | https://hackerone.com/reports/5549
- **Submitted:** 2014-04-01
- **Reporter:** siddiki
- **Program:** Unknown/Unclear
- **Bounty:** Unknown
- **Severity:** informational
- **Vuln:** information_disclosure, public_information
- **CVEs:** None
- **Category:** web-api

## Summary
Researcher discovered that publicly available Wikipedia article about MS-DOS contains historical information, designer names, and technical details about the operating system. The submission appears to be either a misunderstanding of what constitutes a vulnerability or a test of the bug bounty program's triage process.

## Attack scenario
1. Attacker performs search engine query for 'MS-DOS bugs'
2. Search results include Wikipedia article about MS-DOS history
3. Attacker accesses publicly available Wikipedia page
4. Page contains historical information about MS-DOS development
5. Attacker reviews designer names and technical information
6. Attacker concludes this is sensitive information disclosure

## Root cause
Misunderstanding of vulnerability definition; public encyclopedic sources are not security vulnerabilities or confidential disclosures

## Attacker mindset
Possibly well-intentioned but uninformed researcher attempting to identify security issues by searching for technical information and misinterpreting publicly available historical documentation as a breach

## Defensive takeaways
- Establish clear guidelines distinguishing between public information and actual security vulnerabilities
- Document what constitutes valid bug submissions in program scope
- Provide security researcher education on vulnerability taxonomy
- Screen submissions for obvious non-issues before triage

## Variant hunting
Similar low-quality submissions linking to public databases, historical archives, or encyclopedic sources and claiming information disclosure

## MITRE ATT&CK


## Notes
This report (HackerOne #5549) is an example of a non-vulnerability submission. Wikipedia articles are intentionally public historical references, not confidential system disclosures. No actual security impact exists. The submission may serve as a training example for bug bounty programs on handling scope clarification and researcher education.

## Full report
<details><summary>Expand</summary>

I was searching for MS-Dos bugs in search engines.Suddenly I got a surprising result.That result discloses the history of MS-Dos,designers names,and many other secret information.
Here is the POC:
http://en.wikipedia.org/wiki/MS-DOS


</details>

---
*Analysed by Claude on 2026-05-24*
