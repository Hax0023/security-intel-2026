# Stored XSS in pass Culture Administrator Panel via MarkupSafe Misuse

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-19
- **Author:** Various
- **Program:** pass Culture Bug Bounty (Private, YesWeHack)
- **Bounty:** Not specified in writeup
- **Severity:** high
- **Vuln types:** Stored Cross-Site Scripting (XSS), Improper Neutralization of Input During Web Page Generation, Unsafe Use of Security Library
- **Category:** web-api
- **Writeup:** https://www.aeth.cc/public/Article-Pass-Culture/stored-xss-article-en.html

## Summary
A stored XSS vulnerability was discovered in the pass Culture administrator panel due to misuse of MarkupSafe's Markup class. Developers used f-string formatting before passing data to Markup(), allowing HTML injection to occur before escaping, rather than after. The vulnerability was exploitable when a professional user's offerer name (injectable user input) was incorporated into administrative panel markup without proper sanitization.

## Attack scenario (step by step)
1. Attacker creates a professional account on pass Culture and registers as an Offerer
2. Attacker sets their offerer/vendor name to include malicious XSS payload (e.g., '<img src=x onerror="alert(1)">')
3. Attacker creates or uploads offers under this malicious offerer account, triggering fraud detection workflow
4. Administrator accesses the admin panel's offer validation page to review flagged offers for fraud
5. The _offerer_link() formatter processes the offerer name through f-string interpolation before Markup escaping
6. XSS payload executes in administrator's browser session, allowing session hijacking or account compromise

## Root cause
Developers misunderstood MarkupSafe's protection model. The library only escapes values passed as function arguments to Markup(), not values already interpolated into strings via f-strings. By using f'<a href="{url}">{text}</a>' inside Markup(), the text variable was concatenated before Markup could escape it, defeating the intended protection mechanism.

## Attacker mindset
Patient reconnaissance and code review discipline. The attacker initially found the anti-pattern but recognized it was not immediately exploitable without injectable input. By maintaining a weekly code review routine and monitoring commits, they discovered when user-controlled data (offerer names) was incorporated into the vulnerable formatter, creating an actual exploitation path. This demonstrates strategic thinking: identifying latent vulnerabilities and waiting for conditions to make them exploitable.

## Defensive takeaways
- Never interpolate user input into strings before passing to security libraries; pass user data as function arguments to allow proper escaping
- Use templating engines with auto-escaping enabled (Jinja2 with autoescape=True) instead of manual formatting functions
- Implement strict Content Security Policy (CSP) headers in admin panels to mitigate XSS impact
- Establish code review practices that specifically audit usage of security libraries like MarkupSafe
- Create unit tests validating that user-controlled strings in admin formatters cannot introduce HTML/JavaScript
- Use linting rules or AST analysis to detect f-strings containing HTML markup combined with user variables
- Implement input validation and sanitization at the data model level for user-facing fields like offerer names

## Variant hunting
['Search codebase for all uses of Markup() combined with f-strings or .format() containing user input', 'Audit other formatter functions in flask_admin integration for similar anti-patterns', 'Check if venue names, offer titles, or other professional user inputs follow same vulnerable pattern', 'Review all admin panel pages displaying user-generated content for similar injection points', "Examine any field marked as 'injectable user input' that flows through custom formatters", 'Hunt for similar anti-patterns with other escaping libraries (e.g., bleach, markupsafe.escape used incorrectly)']

## MITRE ATT&CK
- T1190
- T1598
- T1566
- T1557
- T1187

## Notes
This is an excellent example of security library misuse being equally dangerous as complete lack of protection. The writeup demonstrates sophisticated bug bounty methodology: source code review discipline, pattern recognition (identifying the anti-pattern before it was exploitable), patience, and automated monitoring of codebase evolution. The public disclosure was made only after vendor patch was deployed. Pass Culture's open-source nature and available local deployment via docker-compose significantly aided the researcher's ability to discover and validate the vulnerability. The vulnerability specifically targets administrative accounts, the highest privilege level in the application, making it particularly valuable for attackers.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-19*
