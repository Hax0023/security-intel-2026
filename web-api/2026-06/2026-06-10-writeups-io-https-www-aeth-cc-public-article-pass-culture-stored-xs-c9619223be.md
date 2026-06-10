# Stored XSS in Pass Culture Administrator Panel via MarkupSafe Misuse

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-10
- **Author:** Various
- **Program:** Pass Culture Bug Bounty (Private Program via YesWeHack)
- **Bounty:** Not specified in writeup
- **Severity:** high
- **Vuln types:** Stored Cross-Site Scripting (XSS), Improper Input Neutralization, Template Injection
- **Category:** web-api
- **Writeup:** https://www.aeth.cc/public/Article-Pass-Culture/stored-xss-article-en.html

## Summary
A Stored XSS vulnerability was discovered in the Pass Culture administrator panel due to misuse of the MarkupSafe library. Developers used f-string formatting before applying Markup protection, rendering the HTML escaping ineffective. An attacker with a professional account could inject malicious JavaScript through the offerer name field, which would execute in the admin panel when reviewing offers.

## Attack scenario (step by step)
1. Attacker creates a professional account on Pass Culture platform
2. Attacker registers an offerer/venue with a malicious JavaScript payload embedded in the offerer name field (e.g., '<img src=x onerror="alert(1)">')
3. Attacker creates or submits offers through their account, triggering fraud detection review process
4. Administrator accesses the offer validation page in flask_admin panel to review suspected fraudulent offers
5. The malicious payload stored in the offerer name field is rendered unsanitized in the HTML link formatter
6. JavaScript payload executes in the administrator's browser session, allowing credential theft or administrative action abuse

## Root cause
The _offerer_link() formatter function used f-string interpolation (f'{text}') before wrapping the result in Markup(). This means user-controlled input was injected into the string BEFORE HTML escaping was applied. The Markup() wrapper only escapes content that hasn't already been converted to a string via f-strings. The correct approach would be to use Markup's escape() method or concatenate already-escaped values.

## Attacker mindset
An attacker recognizes that while Markup appears to provide XSS protection, the implementation is vulnerable to bypass through f-string pre-formatting. They identify that offerer names are user-controllable and will be displayed in a high-privilege administrative interface, making this a valuable target. The attacker exploits the trust administrators place in the admin panel's supposed sanitization.

## Defensive takeaways
- Never use f-strings or string concatenation before applying HTML escaping libraries; always escape first, concatenate after
- Use template engines with automatic escaping enabled by default (Jinja2 autoescape=True)
- Implement strict Content Security Policy (CSP) headers to mitigate XSS impact even if sanitization fails
- Apply output encoding specifically for the context (HTML context requires HTML encoding, not just generic Markup wrapping)
- Use security linters and static analysis tools to detect dangerous patterns like f-strings inside Markup calls
- Implement automated security testing for admin panels with both legitimate and malicious user input
- Conduct regular code reviews specifically targeting template rendering and output encoding functions
- Validate and constrain user input at the source (offerer names) to alphanumeric + safe punctuation only

## Variant hunting
['Search for other formatter functions in flask_admin using f-strings before Markup() calls', 'Look for similar patterns in Jinja2 templates using {{ user_input }} without explicit filters', 'Check for other user-controlled fields rendered in admin interfaces (venue names, offer titles, descriptions)', 'Audit professional account fields for XSS injection points in any admin-facing displays', 'Review all custom Flask-Admin formatters for improper string concatenation patterns', 'Test user profile fields (name, bio, description) in professional accounts for reflected/stored XSS', 'Check if similar vulnerable patterns exist in the professional portal or public-facing interfaces']

## MITRE ATT&CK
- T1190
- T1598
- T1566
- T1204

## Notes
This is a high-quality vulnerability writeup demonstrating excellent bug bounty methodology: persistent code review, understanding of the specific framework's security features, identifying where defenses fail, and waiting for the exploitable condition to emerge. The researcher shows restraint by not reporting a potentially unexploitable issue early, then demonstrating mature judgment by re-evaluating when the attack surface changed. The vulnerability specifically affects administrative users, making it a privilege context-sensitive issue with potentially high impact for a government service. The pass Culture program demonstrates best practices for government bug bounties: open-source code, local deployment capability, and clear scope definition.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-10*
