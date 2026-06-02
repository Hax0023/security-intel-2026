# Live Hacking like a MVH – A walkthrough on methodology and strategies to win big

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-02
- **Author:** Various
- **Program:** Multiple (Uber, Salesforce, Zenefits, Shopify, Oath, Mapbox, Dropbox, Apple)
- **Bounty:** Multiple MVH (Most Valuable Hacker) awards and significant bounties (exact amounts not disclosed in available content)
- **Severity:** N/A
- **Vuln types:** Submitted by:quas
- **Category:** uncategorised
- **Writeup:** https://speakerdeck.com/fransrosen/live-hacking-like-a-mvh-a-walkthrough-on-methodology-and-strategies-to-win-big

## Summary
This is a methodology and strategy presentation by Frans Rosén, a top-ranked HackerOne researcher, delivered at BountyCon 2019. The talk covers approaches, techniques, and mindset for successful vulnerability research and bug bounty hunting at scale. The presentation includes case studies and lessons learned from winning multiple major bug bounty competitions and awards.

## Attack scenario (step by step)
1. Identify high-value targets and programs with track records of awarding significant bounties
2. Develop comprehensive reconnaissance and information gathering strategies across target attack surface
3. Apply fuzzing, format injection, and data disclosure techniques to uncover vulnerabilities
4. Analyze modern web technologies and OAuth flows for authentication bypass opportunities
5. Leverage server-side context manipulation and configuration weaknesses (e.g., AEM misconfigurations)
6. Document findings thoroughly and report strategically to maximize impact and bounty awards

## Root cause
This is a methodology presentation rather than a specific vulnerability writeup. The underlying root causes vary across vulnerabilities discussed, including: improper OAuth flow implementations, insecure deserialization/hot jar swapping, information disclosure leading to RCE chains, AEM misconfiguration, and inadequate input validation in modern frameworks.

## Attacker mindset
Systematic, methodology-driven approach to vulnerability research. Emphasis on understanding target technologies deeply, applying varied attack techniques across large attack surfaces, competing effectively in bug bounty competitions, and maximizing value through proper documentation and reporting strategy. Focus on reusable techniques and frameworks applicable across multiple targets.

## Defensive takeaways
- Implement comprehensive input validation and output encoding across all contexts (HTML, JavaScript, URL, CSS, etc.)
- Secure OAuth implementations with proper state management, PKCE enforcement, and redirect URI validation
- Apply secure deserialization practices and restrict dynamic code loading mechanisms
- Harden configuration management for complex platforms (e.g., AEM) with principle of least privilege
- Conduct regular fuzzing and automated security testing against modern web frameworks
- Implement defense-in-depth strategies recognizing that single-layer protections fail
- Monitor for information disclosure that could chain into higher-impact vulnerabilities
- Establish threat modeling practices specific to modern web technologies and architectural patterns

## Variant hunting
Look for OAuth implementation flaws across other platforms; investigate deserialization attacks in Java-based applications; audit CMS and enterprise platform configurations (AEM-like systems); examine format injection opportunities in modern template engines; search for information disclosure in API responses and error messages that could enable RCE chains.

## MITRE ATT&CK
- T1190
- T1204
- T1566
- T1598
- T1592
- T1589
- T1590
- T1591
- T1199
- T1621
- T1040
- T1557
- T1556
- T1111
- T1539
- T1087
- T1010
- T1110
- T1555
- T1187
- T1200
- T1543
- T1546
- T1547
- T1547.001

## Notes
This is a methodology and strategy presentation from BountyCon 2019 by Frans Rosén (@fransrosen), ranked #6 on HackerOne all-time leaderboard. The actual vulnerability details are contained in referenced talks: X-Correlation Injections, RCE on Apple via hot jar swapping, OAuth account hijacking, format injection attacks, and AEM misconfiguration exploitation. The presentation emphasizes systematic approaches to vulnerability research rather than specific technical exploits. Detailed vulnerability information would require accessing the individual referenced slide decks.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-02*
