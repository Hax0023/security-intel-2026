# Stored XSS in Administrator Panel due to MarkupSafe Misuse in pass Culture

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-06
- **Author:** Various
- **Program:** pass Culture Bug Bounty (Private Program via YesWeHack)
- **Bounty:** Not disclosed
- **Severity:** High
- **Vuln types:** Stored Cross-Site Scripting (XSS), Improper Output Encoding, Template Injection
- **Category:** web-api
- **Writeup:** https://www.aeth.cc/public/Article-Pass-Culture/stored-xss-article-en.html

## Summary
A stored XSS vulnerability was discovered in the pass Culture administrator panel due to misuse of MarkupSafe protection. The vulnerability arises from using Python f-string formatting before applying Markup(), allowing injection of unsanitized user input (offerer/vendor names) into HTML output. An attacker with a professional account can inject malicious JavaScript that executes in the administrator's browser when reviewing fraud reports.

## Attack scenario (step by step)
1. Attacker creates or compromises a professional (vendor) account on pass Culture
2. Attacker sets the offerer/vendor organization name to a malicious XSS payload (e.g., '<img src=x onerror=alert(1)>')
3. Attacker creates offers or triggers fraud detection to ensure the offerer record appears in the admin panel
4. Administrator accesses the fraud validation page in the admin panel to review suspicious offers
5. The malicious payload in the offerer name is rendered without proper escaping due to f-string pre-processing before Markup()
6. JavaScript payload executes in administrator's browser context, enabling session hijacking, credential theft, or privilege escalation

## Root cause
The code uses Python f-string formatting to inject variables into HTML before passing the result to Markup(). The pattern `Markup(f'<a>{user_input}</a>')` evaluates the f-string first (unescaped), then wraps it in Markup() which marks it as safe HTML. MarkupSafe only escapes values passed directly to its constructor as arguments, not pre-formatted strings. Correct usage would be: `Markup('<a>{}</a>').format(escape(user_input))` or `Markup('<a>{text}</a>', text=user_input)`.

## Attacker mindset
The researcher demonstrated excellent persistence and code review discipline by implementing a weekly review routine. Rather than dismissing the initial finding as non-exploitable, they anticipated potential code evolution and monitored commits. This proactive approach revealed the vulnerability when a new feature (offerer names in admin display) provided an injection vector. The attacker would likely use this to compromise administrator accounts and gain platform-wide control.

## Defensive takeaways
- Never use f-strings or string concatenation before passing to template escaping functions; pass variables as separate arguments
- Implement automated linting rules to detect dangerous patterns like Markup(f'...{var}...') in CI/CD pipelines
- Use templating engines properly with context-aware auto-escaping enabled by default
- Conduct regular security training on MarkupSafe/Jinja2 best practices for Python/Flask developers
- Require security review of formatter functions in admin panels as they frequently handle sensitive data
- Implement Content Security Policy (CSP) headers to mitigate XSS impact in admin interfaces
- Add output encoding tests for all user-controllable data rendered in administrative views
- Monitor admin panel access logs for suspicious activity that may indicate compromise

## Variant hunting
['Search for all uses of Markup() with f-strings or format() operations across the codebase', 'Identify other formatter functions in flask_admin implementations that may have similar patterns', 'Review all professional account editable fields (name, description, metadata) for similar injection points in user-facing templates', 'Check for stored user input rendered in other administrative panels or reporting interfaces', 'Audit database import/export functionality where user data might flow into templates', 'Examine email templates or PDF generation that incorporates offerer/venue data', 'Test other Markup-wrapped content that incorporates model relationships (venue, offerer, offer names)']

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1059 - Command and Scripting Interpreter (JavaScript execution)
- T1566 - Phishing (if used to distribute malicious content)
- T1547 - Boot or Logon Autostart Execution (XSS payload persistence in admin context)
- T1071 - Application Layer Protocol (HTTP/HTML delivery)
- T1020 - Automated Exfiltration (via XSS to steal admin session tokens)

## Notes
This is an exemplary bug bounty report demonstrating excellent security research methodology. The researcher: (1) reviewed open-source code thoroughly, (2) recognized a subtle anti-pattern in security controls, (3) established monitoring for code evolution, (4) pursued the vulnerability when conditions changed, and (5) documented findings comprehensively. The vulnerability is a classic example of how security controls can create false confidence when misused. MarkupSafe requires proper API usage; wrapping already-formatted strings provides no protection. The attack surface is limited to professional accounts, reducing impact scope but not severity given administrative access compromise potential. The patch likely involved correcting the Markup() usage pattern across all formatter functions. Pass Culture's open-source approach and responsive patching are commendable for a public service application.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-06*
