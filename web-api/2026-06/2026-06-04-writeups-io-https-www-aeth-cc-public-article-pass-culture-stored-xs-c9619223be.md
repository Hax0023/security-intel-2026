# Stored XSS in Administrator Panel via MarkupSafe Misuse in pass Culture

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-04
- **Author:** Various
- **Program:** pass Culture Bug Bounty (Private, YesWeHack)
- **Bounty:** Not publicly disclosed
- **Severity:** high
- **Vuln types:** Stored XSS, Improper Input Validation, Template Injection
- **Category:** web-api
- **Writeup:** https://www.aeth.cc/public/Article-Pass-Culture/stored-xss-article-en.html

## Summary
A stored XSS vulnerability existed in the pass Culture administrator panel due to improper use of MarkupSafe's Markup() function. User-controlled data (offerer/vendor names) were formatted into HTML strings using f-strings before being wrapped in Markup(), causing the protection mechanism to be bypassed. An authenticated professional account could inject malicious JavaScript that would execute in the administrator's browser when reviewing flagged offers.

## Attack scenario (step by step)
1. Attacker creates or compromises a professional account (vendor/offerer account) on pass Culture
2. Attacker modifies their offerer/vendor organization name to include XSS payload (e.g., '<img src=x onerror=alert(1)>')
3. Attacker creates or submits offers under this malicious account, potentially flagging them for fraud review
4. Administrator accesses the admin panel to review flagged offers, which displays a list including the offerer names
5. The malicious offerer name is rendered unescaped in the admin panel due to the f-string pre-formatting before Markup()
6. JavaScript payload executes in administrator's browser with their session privileges, allowing session hijacking, data theft, or further privilege escalation

## Root cause
The developers used f-string formatting to inject user-controlled data into HTML strings, then wrapped the entire result in Markup(). The correct pattern requires wrapping individual values in Markup() after escaping, not formatting them into raw strings first. The code used `Markup(f'<a href="{url}">{text}</a>')` where `text` contained unescaped user input, instead of `Markup('<a href="{url}">{text}</a>').format(url=url, text=Markup.escape(text))`.

## Attacker mindset
The researcher demonstrates patient, methodical approach: initial code review identified the anti-pattern before any actual vulnerability existed, then weekly monitoring of commits caught the exact moment user input was introduced into the vulnerable code path. This shows understanding of temporal windows in security (code review, commit monitoring, early detection). The attacker mentality would recognize the admin panel as high-value target and understand that professional accounts are easier to control than beneficiary accounts.

## Defensive takeaways
- Never use string formatting (f-strings, .format(), %) to inject data into HTML before escaping - always escape values first
- Use templating engines with auto-escaping enabled by default (Jinja2 with autoescape=True) rather than manual Markup() calls
- Security tools should flag patterns like Markup(f'...{variable}...') as anti-patterns
- Implement code review processes specifically for template/HTML rendering code
- Maintain automated scanning for stored XSS patterns in admin panels where multiple user types feed data
- Add integration tests that verify XSS payloads cannot be stored through each account type
- Use security-focused linting rules to detect dangerous MarkupSafe usage patterns

## Variant hunting
["Search for similar Markup(f'...{') patterns across entire codebase - likely multiple instances of same anti-pattern", 'Check all custom flask_admin formatters for manual HTML construction', 'Review any field that accepts user input from lower-privilege accounts (professionals, vendors, offerers) and flows to higher-privilege views (admin panels)', 'Test all vendor/offerer/professional account metadata fields (name, description, address, contact info) for XSS injection', 'Audit historical commits for introduction of user-controlled data into previously safe code paths', 'Check for similar vulnerabilities in other Django/Flask admin customizations using third-party libraries', 'Review any location where professional account data is displayed to administrators']

## MITRE ATT&CK
- T1190
- T1566
- T1195
- T1204

## Notes
This is an excellent example of vulnerability discovery through proactive code review and temporal monitoring. The researcher correctly identified the anti-pattern before exploitation was possible, then monitored for the specific condition (user input injection) that would make it exploitable. The disclosure was responsible and coordinated with the program. The vulnerability required two privilege levels (professional account for injection + admin account for execution), reducing immediate impact but still critical for administrative security. The open-source nature and local Docker deployment enabled thorough analysis. This represents a common real-world pattern where security libraries (MarkupSafe) are misused due to developer misunderstanding of when escaping occurs.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-04*
