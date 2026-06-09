# Stored XSS in pass Culture Administrator Panel via MarkupSafe Misuse

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-09
- **Author:** Various
- **Program:** pass Culture Bug Bounty (YesWeHack)
- **Bounty:** Not specified in writeup
- **Severity:** high
- **Vuln types:** Stored XSS, Improper Output Encoding, Template Injection
- **Category:** web-api
- **Writeup:** https://www.aeth.cc/public/Article-Pass-Culture/stored-xss-article-en.html

## Summary
A stored XSS vulnerability was discovered in the pass Culture administrator panel due to misuse of MarkupSafe's HTML escaping in Flask-Admin custom formatters. User-controlled input (offerer/vendor names) was being interpolated via f-strings before being wrapped in Markup(), bypassing HTML escaping protections. This allowed authenticated professionals to inject malicious JavaScript that would execute in administrators' browsers when viewing offer validation pages.

## Attack scenario (step by step)
1. Attacker creates a professional account on pass Culture and creates a venue/structure
2. Attacker modifies the offerer name to include XSS payload (e.g., '<img src=x onerror="alert(1)">')
3. Attacker creates offers associated with this venue to trigger the fraud detection workflow
4. Administrator reviews the suspicious offers in the admin panel, loading the _offerer_link formatter
5. The malicious payload in the offerer name is rendered without proper escaping due to f-string pre-interpolation
6. JavaScript executes in administrator's browser context, allowing session hijacking, credential theft, or further admin account compromise

## Root cause
The code used Python f-string formatting to interpolate user-controlled data before passing it to MarkupSafe's Markup() function. This caused HTML escaping to occur on already-interpolated values rather than on the raw user input. Correct usage would be: Markup(f'<a href="{url}">{Markup.escape(text)}</a>') or using Jinja2 templates with autoescaping enabled.

## Attacker mindset
The researcher demonstrated persistence in code review, waiting for code evolution weekly to identify when user input became injectable in previously identified bad patterns. This shows sophisticated vulnerability hunting by tracking code commits and understanding how refactoring could introduce exploitable paths into unsafe patterns.

## Defensive takeaways
- Never use f-strings or string concatenation before HTML escaping; apply escaping to raw user input first
- Use template engines with autoescaping enabled (Jinja2) instead of manual Markup() calls in Flask
- Implement security code review focusing on data flow: identify user input sources and ensure escaping at the last output point
- Establish static analysis rules to detect f-string usage before Markup() calls
- Provide secure coding guidelines for Flask-Admin formatters; prefer lambda functions with template rendering
- Enforce security testing in CI/CD to catch XSS in admin interfaces via automated scanning
- Regular security audits of admin panels which handle privileged operations and sensitive data

## Variant hunting
Look for similar patterns in Flask applications: (1) Other Flask-Admin formatters using f-strings before Markup, (2) Custom Jinja2 filters that concatenate strings before Markup(), (3) Admin list views with model_formatter functions, (4) Any codebase using MarkupSafe after string interpolation, (5) Professional/vendor profile pages in multi-tenant apps, (6) Admin review workflows handling user-generated content

## MITRE ATT&CK
- T1190
- T1598
- T1566
- T1566.002

## Notes
This is a high-quality writeup demonstrating responsible disclosure and patience-based vulnerability hunting. The researcher correctly identified that the initial code pattern was vulnerable despite having no injectable input, then monitored code changes for when user input would flow through the vulnerable pattern. Pass Culture's open-source nature and good test coverage made the vulnerability harder to find but the researcher's systematic approach succeeded. The vulnerability would have allowed complete admin account compromise through session hijacking via XSS in a government service handling youth access to culture.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-09*
