# Stored XSS in pass Culture Administrator Panel via MarkupSafe Misuse

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-28
- **Author:** Various
- **Program:** pass Culture Bug Bounty (private, invitation-only via YesWeHack)
- **Bounty:** Not specified in writeup
- **Severity:** high
- **Vuln types:** Stored XSS, Template Injection, Improper Output Encoding
- **Category:** web-api
- **Writeup:** https://www.aeth.cc/public/Article-Pass-Culture/stored-xss-article-en.html

## Summary
A stored XSS vulnerability was discovered in the pass Culture administrator panel due to improper use of MarkupSafe's Markup class. User-controlled input (offerer/vendor names) was embedded in f-strings before being wrapped with Markup(), negating the escaping protection and allowing HTML/JavaScript injection. This vulnerability required a professional account to inject malicious vendor names that would execute in the admin panel when reviewing flagged offers.

## Attack scenario (step by step)
1. Attacker creates a professional account on pass Culture to manage a venue/structure
2. Attacker sets the offerer/vendor name to contain XSS payload, e.g., '<img src=x onerror="alert(1)">
3. Attacker creates or flags offers under this malicious vendor name
4. Administrator accesses the offer review/validation panel in flask_admin
5. The _offerer_link() formatter renders the vendor name using the vulnerable Markup pattern
6. JavaScript payload executes in administrator's browser with full admin privileges, enabling account takeover or data exfiltration

## Root cause
Misuse of MarkupSafe library through f-string interpolation before Markup() wrapping. The code performed string interpolation with f-strings first (unescaped), then wrapped the already-interpolated string with Markup(), which assumes the input is already safe. Correct usage requires passing raw values to Markup and letting it handle escaping, or using jinja2 template auto-escaping.

## Attacker mindset
Patient, methodical researcher who discovered a bad security practice (f-strings + Markup misuse) in code review, then monitored weekly commits waiting for user-controlled input to be introduced into the vulnerable pattern. The attacker recognized the privilege escalation opportunity: using a low-privilege professional account to compromise high-privilege administrator accounts.

## Defensive takeaways
- Never use f-strings or string concatenation before passing to Markup(); pass raw values only
- Use template engines with automatic escaping (Jinja2) instead of manual Markup handling when possible
- Implement Content Security Policy (CSP) headers to mitigate XSS execution in admin panels
- Enforce input validation on user-provided fields like business/vendor names; restrict special characters where appropriate
- Perform security code reviews when adding user-controlled data to admin panels or privileged contexts
- Establish automated scanning for common MarkupSafe antipatterns in CI/CD pipelines
- Implement output encoding at display time rather than relying on single-point library usage

## Variant hunting
['Search for other f-string + Markup() patterns in flask_admin formatters across the codebase', 'Audit all custom formatter functions in admin panel for unsafe concatenation patterns', 'Review all professional/user-controlled fields rendered in admin dashboards for similar misuse', 'Check for similar patterns with other escaping libraries (markupsafe, bleach, etc.) in Flask applications', 'Inspect offer creation workflows for other injectable fields (descriptions, tags, categories)', 'Test venue-related fields, store descriptions, and category names for XSS in admin context', 'Look for HTML rendering in notification/email templates that may use similar patterns']

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1598: Phishing - Spearphishing Link (potential secondary impact)
- T1539: Steal Web Session Cookie (admin session hijacking)
- T1567: Exfiltration Over Web Service (data theft from admin panel)

## Notes
This is a high-quality writeup demonstrating persistence and methodology. Key strengths: (1) clear explanation of MarkupSafe misuse with concrete code examples, (2) weekly monitoring of commits to catch when user input entered vulnerable code path, (3) privilege escalation chain from professional to admin account, (4) responsible disclosure with legal context. The researcher initially found the antipattern but correctly identified it as non-exploitable until user input was introduced—showing mature vulnerability assessment. Open source code availability and local docker-compose deployment enabled thorough analysis. The vulnerability highlights how security libraries provide false sense of protection when misused.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-28*
