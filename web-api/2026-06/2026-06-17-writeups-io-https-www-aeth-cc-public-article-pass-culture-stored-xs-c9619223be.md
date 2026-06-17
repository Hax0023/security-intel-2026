# Stored XSS in Administrator Panel due to MarkupSafe Misuse

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-17
- **Author:** Various
- **Program:** pass Culture Bug Bounty
- **Bounty:** Not disclosed
- **Severity:** High
- **Vuln types:** Stored Cross-Site Scripting (XSS), Improper Use of Security Library, Template Injection
- **Category:** web-api
- **Writeup:** https://www.aeth.cc/public/Article-Pass-Culture/stored-xss-article-en.html

## Summary
A stored XSS vulnerability was discovered in the pass Culture administrator panel resulting from improper use of the MarkupSafe library. The vulnerability allowed attackers to inject malicious JavaScript through user-controlled input (offerer names) that was formatted using f-strings before being wrapped in Markup(), negating the intended HTML escaping protection.

## Attack scenario (step by step)
1. Attacker creates a professional account on pass Culture platform
2. Attacker sets the offerer/vendor name to a malicious XSS payload (e.g., '<img src=x onerror="alert(document.cookie)">')
3. Attacker creates or modifies offers associated with the malicious offerer account
4. Administrator accesses the admin panel to review offers for fraud validation
5. The offerer name field renders in the _offerer_link() formatter without proper HTML escaping
6. Malicious JavaScript executes in the administrator's browser session, potentially stealing admin credentials or performing unauthorized actions

## Root cause
The code used f-string interpolation before passing the result to Markup(). The MarkupSafe.Markup() class expects unescaped strings as input and escapes them internally. However, by using f-strings first, the user-controlled data (offerer.name) was already embedded as a raw string literal before Markup could escape it, rendering the protection ineffective.

## Attacker mindset
An attacker would recognize that while initial code had this anti-pattern, it wasn't exploitable until user-controlled data was introduced into the template. By monitoring code commits weekly, the attacker could identify when injectable user input was added to a previously non-vulnerable formatter. This demonstrates patience and opportunistic exploitation triggered by code changes rather than initial discovery.

## Defensive takeaways
- Use parameterized templating languages (Jinja2) instead of f-strings for HTML output - Jinja2 auto-escapes by default
- Pass unescaped user input directly to Markup escaping functions, never pre-format with f-strings or string concatenation
- Implement Content Security Policy (CSP) headers to mitigate XSS impact
- Maintain security code review routines, especially for admin panels with elevated privileges
- Use static analysis tools to detect MarkupSafe misuse patterns
- Establish security unit tests that verify escaping behavior for admin panel formatters
- Monitor code commits for patterns that change from non-injectable to injectable contexts

## Variant hunting
['Search for other formatter functions in flask_admin using similar f-string + Markup patterns', 'Audit all user-controlled fields (names, descriptions, emails) that flow through formatting functions', 'Check for similar issues in other Markup-using Python codebases where f-strings precede Markup()', 'Investigate other Flask extensions for similar templating misuse patterns', 'Review any bulk import functionality that might allow CSV injection into formatted fields']

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1598 - Phishing - Spearphishing Link (to admin panel)
- T1562 - Impair Defenses - Disable or Modify Security Tools (CSP bypass via XSS)
- T1539 - Steal Web Session Cookie (via XSS in admin context)
- T1566 - Phishing - Spearphishing Attachment (malicious offerer data import)

## Notes
This vulnerability demonstrates the importance of understanding library semantics. MarkupSafe is designed to escape HTML, but only when receiving raw input - preprocessing with f-strings bypasses this protection entirely. The researcher's disciplined code review routine was key to discovering this vulnerability. The fact that the vulnerability only became exploitable after a specific code commit shows the value of continuous security monitoring. The attack surface is limited to professional accounts, but the impact is severe due to admin panel access. Pass Culture's open-source nature and good testing practices made vulnerability research accessible and the disclosure process appeared collaborative.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-17*
