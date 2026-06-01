# Marketer by day, bug hunter by night. Interview with Stefan Goossens (G0053)

## Metadata
- **Source:** Intigriti Blog
- **Date:** 2026-06-01
- **Author:** Eleanor Barlow
- **Program:** Multiple (Red Bull, private programs, Intigriti)
- **Bounty:** Not specified
- **Severity:** N/A
- **Vuln types:** Business Insights
- **Category:** uncategorised
- **Writeup:** https://www.intigriti.com/blog/business-insights/marketer-by-day-bug-hunter-by-night-interview-with-stefan-goossens-g0053

## Summary
This is an interview article with Stefan Goossens (G0053), a Dutch security researcher and bug bounty hunter who maintains a dual career as a marketer and web developer. The article discusses his journey into bug bounty hunting, skill development approaches, and methodology for finding vulnerabilities through business logic testing rather than technical exploits.

## Attack scenario (step by step)
1. Stefan began his bug hunting journey by watching educational cybersecurity content from STÖK on YouTube
2. He researched legal aspects of bug bounty hunting and started with Intigriti as a trusted European platform
3. His first bug was a basic Cross-Site Scripting (XSS) vulnerability found on a Red Bull program by testing input fields with HTML tags
4. He progressed from simple injection attacks to more complex business logic vulnerabilities by studying PortSwigger Academy and YouTube tutorials
5. He developed a methodology focusing on application behavior analysis, error message inspection, and testing unexpected inputs to identify logic flaws
6. He discovered vulnerabilities by questioning normal user workflows and attempting unauthorized actions (e.g., ordering with negative values)

## Root cause
No specific vulnerability root causes discussed; article focuses on methodology and reconnaissance techniques rather than technical exploitation details.

## Attacker mindset
Stefan demonstrates a puzzle-solving mindset with curiosity about application behavior and business logic. He approaches testing by asking 'what if I do the opposite?' and systematically probes boundaries. His background in web development provides legitimate context for understanding how applications should behave, enabling him to identify deviations. He maintains consistency with tools and workflows to support continuous learning and idea capture.

## Defensive takeaways
- Validate all user inputs and implement strict input validation beyond basic HTML/script filtering
- Test business logic flows for unauthorized state transitions and boundary conditions
- Implement proper authorization checks for all operations, including edge cases like negative values or reverse operations
- Monitor and sanitize error messages to avoid information disclosure
- Design workflows to prevent users from executing operations in unintended sequences
- Conduct threat modeling focusing on business logic rather than only technical vulnerabilities
- Use application behavior testing to identify unexpected state changes and data flows

## Variant hunting
Researchers should hunt for similar business logic vulnerabilities across different application workflows: negative value transactions, reversed operations, skipped authorization steps, unauthorized state transitions, process circumvention through parameter manipulation, and error-based information disclosure. Focus on applications with multi-step processes and state management.

## MITRE ATT&CK
- T1190
- T1566
- T1598

## Notes
This is a biographical/interview article rather than a technical vulnerability writeup. No specific CVEs, exploits, or detailed technical vulnerabilities are documented. The article emphasizes methodology and soft skills in bug bounty hunting. Stefan's approach prioritizes business logic testing over technical depth, making it accessible for security researchers with web development backgrounds but limited deep technical hacking experience. The article mentions he has 3000+ reputation points primarily from private program testing.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-01*
