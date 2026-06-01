# XSS Attacks and Defense: A Multi-Level Analysis

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-01
- **Author:** Various
- **Program:** Educational/General Security
- **Bounty:** N/A - Educational Article
- **Severity:** high
- **Vuln types:** Stored XSS, Reflected XSS, DOM-based XSS, HTML Injection, Attribute-based XSS, JavaScript Protocol XSS
- **Category:** web-api
- **Writeup:** https://blog.huli.tw/2021/06/19/en/xss-attack-and-defense/

## Summary
Comprehensive analysis of XSS vulnerabilities across three defense levels: preventing code injection, implementing CSP policies, and minimizing damage post-exploitation. The article emphasizes that escaping must be context-aware (HTML content vs attributes vs JavaScript vs URLs) and that single escaping strategies are insufficient against sophisticated attacks.

## Attack scenario (step by step)
1. Attacker identifies a user input field (e.g., nickname) that is rendered without proper validation
2. Attacker injects payload like '<script>alert(1)</script>' which executes directly when page is viewed
3. If basic HTML escaping exists, attacker uses attribute-based bypass like '" onload="alert(1)' in alt attribute
4. If attribute escaping exists, attacker exploits protocol handlers like 'javascript:alert(1)' in href attributes
5. If input validation succeeds, attacker may use stored XSS across multiple pages or reflected XSS in URLs
6. If first-level defenses succeed, attacker attempts CSP bypass through inline script execution or form submission hijacking

## Root cause
Context-agnostic escaping and validation strategies that fail to account for different rendering contexts (HTML content, HTML attributes, JavaScript strings, URL protocols). Developers often implement single escaping methods without understanding that different output contexts require different sanitization approaches.

## Attacker mindset
Methodical exploration of defense layers. Attackers first probe for basic input validation failures, then layer bypass techniques (attribute manipulation, protocol handlers, JavaScript contexts) when primary vectors fail. They understand that defense is multi-layered and look for weak points in the chain.

## Defensive takeaways
- Implement context-aware escaping: HTML entities for content, attribute escaping for attributes, JavaScript escaping for scripts, URL encoding for URLs
- Never trust user input regardless of source or claimed validation
- Use whitelist validation rather than blacklist when possible
- Implement Content Security Policy (CSP) as second-level defense to prevent inline script execution
- Assume XSS may occur and implement third-level defenses: minimize sensitive operations, require re-authentication for critical actions, implement CSRF tokens
- Use security-focused templating engines that auto-escape by default based on context
- Regular security testing including payload testing across different injection points
- Educate developers on the nuanced differences between escaping contexts

## Variant hunting
Test for: (1) Stored XSS in user profiles, comments, metadata fields; (2) Reflected XSS in search, filters, error messages; (3) DOM-based XSS in client-side template rendering; (4) Protocol-based XSS in href/src/action attributes; (5) Event handler XSS in event attributes; (6) JavaScript string breakout attacks; (7) SVG/XML-based XSS; (8) CSS injection via style attributes; (9) Mutation XSS with browser parser inconsistencies; (10) CSP bypass through scriptless attacks

## MITRE ATT&CK
- T1190
- T1598
- T1566
- T1203
- T1041

## Notes
This is an educational writeup rather than a specific bug bounty submission. It provides valuable framework for understanding XSS as layered defense problem. Key insight is that developers must understand context-specific escaping requirements; a single 'escape everything' approach is insufficient. The article effectively demonstrates real-world examples (img alt attributes, href attributes) showing why generic escaping fails. Particularly valuable for junior security researchers learning to think systematically about XSS variants and their corresponding defenses.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-01*
