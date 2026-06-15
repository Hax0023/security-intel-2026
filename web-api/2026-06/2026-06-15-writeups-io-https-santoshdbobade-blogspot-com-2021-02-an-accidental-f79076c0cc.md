# Accidental XSS on uu.nl via UUID Parameter

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-15
- **Author:** Various
- **Program:** uu.nl (Utrecht University)
- **Bounty:** Not specified
- **Severity:** High
- **Vuln types:** Reflected Cross-Site Scripting (XSS), Improper Input Validation, Insufficient Output Encoding
- **Category:** web-api
- **Writeup:** https://santoshdbobade.blogspot.com/2021/02/an-accidental-xss-onuunl.html

## Summary
A reflected XSS vulnerability was discovered on a uu.nl subdomain through a UUID parameter that reflected unsanitized user input within the HTML title tag. The attacker successfully injected a script payload by closing the title tag and executing arbitrary JavaScript in the victim's browser context.

## Attack scenario (step by step)
1. Attacker performs subdomain enumeration on uu.nl using tools like subfinder/amass
2. Attacker collects historical URLs using waybackurls to identify parameter patterns
3. Attacker identifies the vulnerable endpoint with a UUID parameter that reflects in the title tag
4. Attacker crafts XSS payload: test</title><script>alert(document.domain)</script>
5. Attacker sends crafted URL to victim via phishing or social engineering
6. Victim's browser executes the injected script, confirming XSS and accessing document.domain

## Root cause
The application failed to properly validate and encode user-supplied input (UUID parameter) before inserting it into the HTML title tag. No Context-aware output encoding was implemented, allowing tag breakout attacks.

## Attacker mindset
Systematic reconnaissance-driven approach: enumerate subdomains, collect historical data via Wayback Machine, identify parameter injection points, test for reflection, and exploit tag-based context escapes. The 'accidental' nature suggests discovery during routine security testing rather than targeted exploitation.

## Defensive takeaways
- Implement context-aware output encoding (HTML entity encoding for HTML context)
- Use Content Security Policy (CSP) headers to restrict inline script execution
- Validate and sanitize all user inputs against whitelists of allowed characters
- Apply input length restrictions on parameters like UUID
- Use template engines with automatic escaping enabled
- Implement HTTPOnly and Secure flags on sensitive cookies
- Perform security code reviews focusing on output encoding in all contexts
- Implement automated scanning for reflected XSS in CI/CD pipeline

## Variant hunting
['Test other URL parameters for reflection in different HTML contexts (attributes, script, style)', 'Check other uu.nl subdomains for identical or similar vulnerable endpoints', 'Attempt DOM-based XSS variants using JavaScript event handlers', 'Test for stored XSS if UUID values are persisted and displayed elsewhere', 'Investigate SVG/XML contexts for namespace-based XSS vectors', 'Check for bypass techniques using HTML5 attributes or encoding variations']

## MITRE ATT&CK
- T1190
- T1566.002
- T1204.001

## Notes
The writeup lacks specific details about the program name (uu.nl subdomain redacted), bounty amount, and disclosure timeline. The vulnerability appears straightforward but highlights importance of systematic reconnaissance and parameter testing. 'Accidental' discovery suggests this may have been found during routine testing rather than active exploitation. No information provided on responsible disclosure process or remediation timeline.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-15*
