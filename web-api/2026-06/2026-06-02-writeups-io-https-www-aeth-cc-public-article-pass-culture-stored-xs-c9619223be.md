# Stored XSS in pass Culture Administrator Panel via MarkupSafe Misuse

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-02
- **Author:** Various
- **Program:** pass Culture Bug Bounty (private program via YesWeHack)
- **Bounty:** Not disclosed
- **Severity:** high
- **Vuln types:** Stored Cross-Site Scripting (XSS), Improper Output Encoding, Template Injection
- **Category:** web-api
- **Writeup:** https://www.aeth.cc/public/Article-Pass-Culture/stored-xss-article-en.html

## Summary
A stored XSS vulnerability was discovered in the pass Culture administrator panel caused by incorrect use of MarkupSafe's Markup class. The vulnerability leverages f-string formatting that occurs before Markup application, allowing HTML/JavaScript injection through the offerer name field. An authenticated professional account can inject malicious scripts that execute when administrators view the fraud validation panel.

## Attack scenario (step by step)
1. Researcher identifies MarkupSafe misuse pattern in flask_admin custom formatters where f-strings are evaluated before Markup() wrapping
2. Researcher creates or takes control of a professional account (offerer) on pass Culture platform
3. Researcher sets the offerer/vendor name to malicious payload: '<img src=x onerror="alert('XSS')" />' or similar XSS vector
4. Researcher creates offers that trigger fraud detection flags, causing admin review workflow to activate
5. Administrator navigates to fraud validation panel in admin interface which renders the _offerer_link formatter
6. Malicious payload stored in offerer name executes in administrator's browser with full admin privileges

## Root cause
The _offerer_link() and similar formatter functions use Python f-strings to interpolate user-controlled data (offerer name) directly into HTML strings before passing to Markup(). MarkupSafe's Markup() function does not escape content that was pre-formatted with f-strings; it only prevents re-escaping. The pattern `Markup(f'<a href="{url}">{user_input}</a>')` is vulnerable because user_input is evaluated before Markup() can protect it.

## Attacker mindset
An attacker with professional account access monitors code commits looking for security regressions. Upon discovering that user-controllable data (offerer name) enters an unsafe formatter function, they exploit the deployment window to inject XSS payloads. The attack targets high-value admin accounts to gain administrative access or steal session tokens, knowing admins regularly audit fraud cases.

## Defensive takeaways
- Never use f-string or format() interpolation before passing to escaping functions like MarkupSafe.Markup(); apply escaping first or use template systems with automatic context-aware escaping
- Use Markup.escape() on untrusted data before wrapping with Markup() constructor, or better: leverage Jinja2 autoescaping in Flask templates
- Implement strict code review processes checking for MarkupSafe anti-patterns; flag any f-string usage in admin/template formatters
- Enforce Content Security Policy (CSP) headers in admin panels to mitigate XSS blast radius even if output encoding fails
- Conduct security training on framework-specific escaping semantics; developers often misunderstand that Markup() is not a sanitizer
- Add integration tests validating that special characters in user-controlled fields (names, descriptions) render as escaped HTML in admin UI

## Variant hunting
['Search codebase for all Markup() or Markup.format() calls containing f-strings, .format(), or % string formatting with variables', 'Audit flask_admin custom column formatters in admin route definitions for similar unsafe patterns', 'Check other template rendering contexts in Flask views for premature string interpolation before auto-escape application', 'Review other user-controllable fields used in admin panels: descriptions, titles, addresses that may flow through similar formatters', 'Test other professional account fields for injection: venue names, offer titles, category names', 'Search for uses of jinja2.Markup in non-template contexts where escaping responsibility shifts to developer']

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1598: Phishing for Information (social engineering to get admin to click malicious link)
- T1539: Steal Web Session Cookie (XSS cookie theft)
- T1021: Remote Services (lateral movement from admin compromise)
- T1199: Trusted Relationship (leveraging trusted admin account compromise)

## Notes
This is a excellent example of second-order vulnerability discovery through continuous code review monitoring. The researcher initially found the anti-pattern but correctly identified it wasn't exploitable without user input. By establishing a Sunday review ritual of recent commits, they caught the exact commit introducing user-controlled data into the unsafe formatter. Pass Culture's public open-source codebase and docker-compose deployment dramatically reduced barrier to entry. The vulnerability demonstrates that security libraries like MarkupSafe provide false sense of security when misused—developers must understand escaping semantics. Notably, the researcher exercised responsible disclosure and legal compliance by operating within the private bug bounty agreement.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-02*
