# Stored XSS in Pass Culture Administrator Panel via MarkupSafe Misuse

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-15
- **Author:** Various
- **Program:** Pass Culture Bug Bounty (Private, via YesWeHack)
- **Bounty:** Not disclosed in article
- **Severity:** high
- **Vuln types:** Stored Cross-Site Scripting (XSS), Improper Neutralization of Input During Web Page Generation, Misuse of Security Library
- **Category:** web-api
- **Writeup:** https://www.aeth.cc/public/Article-Pass-Culture/stored-xss-article-en.html

## Summary
A Stored XSS vulnerability was discovered in the Pass Culture administrator panel due to misuse of the MarkupSafe library. User-controlled vendor/offerer names were embedded in f-strings before being passed to Markup(), bypassing HTML escaping. This allowed authenticated professionals to inject malicious JavaScript that executes in the admin panel during manual fraud validation.

## Attack scenario (step by step)
1. Attacker creates a professional account with Pass Culture platform
2. Attacker registers a vendor/offerer with a malicious name containing XSS payload (e.g., '<img src=x onerror="alert(1)">')
3. Attacker creates offers through their vendor account to trigger manual fraud validation by administrators
4. Administrator visits the fraud validation page in the admin panel to review suspicious offers
5. The malicious payload in the offerer name is rendered as unsanitized HTML via the _offerer_link() formatter function
6. Administrator's browser executes the injected JavaScript, allowing session hijacking or admin privilege escalation

## Root cause
The developer used f-string interpolation before passing data to Markup(). The correct pattern requires using % or .format() with Markup to ensure escaping happens during interpolation. Instead, the f-string evaluated first (unescaped), then passed to Markup (no-op on already-formatted strings). The vulnerable code was: `Markup(f'<a href="{url}">{text}</a>')` where `text = model.venue.managingOfferer.name` contains user input.

## Attacker mindset
A security researcher with white-hat motivations performing legitimate code review on an open-source application. They systematically identified a bad practice that initially seemed non-exploitable, then monitored code changes until user-controlled input flowed into the vulnerable pattern—demonstrating patience and routine-based vulnerability hunting.

## Defensive takeaways
- Never use f-strings or concatenation before passing to Markup(); instead use Markup with % or .format() for automatic escaping
- Implement Content Security Policy (CSP) headers to mitigate XSS impact in admin panels
- Establish secure coding guidelines specifically for templating libraries and their proper usage patterns
- Add static analysis tooling to detect f-string usage within Markup() calls
- Require code review for any changes introducing user input into rendering functions
- Consider using template engines (Jinja2) instead of manual HTML construction in Python
- Implement output encoding validation in unit tests for admin formatters

## Variant hunting
['Search for all custom flask_admin formatter functions using Markup() with f-strings or concatenation', 'Audit all user-controlled fields (names, descriptions, titles) flowing through admin panel displays', 'Check for similar patterns in other decorators or rendering utilities throughout the codebase', 'Identify other administrative pages with manual validation workflows that display user input', 'Review vendor/offerer creation endpoints for other injectable fields (description, contact info, etc.)', 'Test whether other user roles (professionals) can view admin panels or manipulate displayed data', 'Check if similar vulnerabilities exist in legitimate user-facing pages using MarkupSafe']

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1598 - Phishing - Spearphishing Link (if combined with session hijacking)
- T1040 - Sniffing (potential session theft)
- T1021 - Remote Services (privilege escalation to admin)
- T1021.006 - Remote Services: Direct Cloud Service Access (if credentials exfiltrated)

## Notes
The researcher demonstrated excellent threat hunting methodology by establishing a weekly code review routine and monitoring commits for specific vulnerable patterns. The vulnerability required two conditions: (1) presence of vulnerable code pattern and (2) flow of user-controlled input into it. Initial assessment correctly identified the anti-pattern but acknowledged it was unexploitable without injectable input. The fix deployed in expected commit created the exploitation path. This exemplifies how security best practices evolve and why continuous monitoring matters. The open-source nature of the code enabled thorough analysis. Disclosure was responsible with vendor cooperation before publication.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-15*
