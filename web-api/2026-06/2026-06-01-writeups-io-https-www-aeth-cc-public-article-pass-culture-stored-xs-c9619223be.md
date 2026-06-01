# Stored XSS in Pass Culture Administrator Panel via MarkupSafe Misuse

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-01
- **Author:** Various
- **Program:** Pass Culture Bug Bounty (Private/Invitation-only via YesWeHack)
- **Bounty:** Not disclosed
- **Severity:** high
- **Vuln types:** Stored Cross-Site Scripting (XSS), Improper Input Validation, Template Injection
- **Category:** web-api
- **Writeup:** https://www.aeth.cc/public/Article-Pass-Culture/stored-xss-article-en.html

## Summary
A Stored XSS vulnerability was discovered in the Pass Culture administrator panel due to incorrect usage of the MarkupSafe library. Developers used f-string formatting before applying Markup protection, causing HTML escaping to be bypassed. An attacker with a professional account could inject malicious JavaScript through the offerer/vendor name field, which would execute when administrators viewed offer validation pages.

## Attack scenario (step by step)
1. Attacker creates or takes over a professional account on Pass Culture platform
2. Attacker modifies the offerer/vendor organization name to include XSS payload (e.g., '<img src=x onerror=alert(1)>')
3. Attacker creates offers under the malicious offerer account to trigger fraud detection review workflow
4. Administrator opens the offer validation/fraud detection page in the admin panel
5. The _offerer_link formatter renders the attacker's payload within an HTML anchor tag without proper escaping
6. Malicious JavaScript executes in administrator's browser session, allowing session hijacking or account takeover

## Root cause
Misuse of MarkupSafe library protection mechanism. The code applied f-string variable interpolation before calling Markup(), which meant user input was embedded into the string before HTML escaping occurred. MarkupSafe only escapes content passed directly to its constructor, not pre-formatted strings. The pattern `Markup(f'<a href="{url}">{text}</a>')` is vulnerable because `text` containing user input gets interpolated first, bypassing protection.

## Attacker mindset
Opportunistic privilege escalation targeting administrative accounts through a known weak pattern in framework usage. The attacker demonstrated patience by monitoring code commits weekly, waiting for injectable user input to be added to a previously-safe code pattern, transforming a latent architectural flaw into an exploitable vulnerability.

## Defensive takeaways
- Never use f-strings or string concatenation before applying HTML escaping libraries like MarkupSafe - pass raw variables directly to the protection function
- Use templating engines (Jinja2) with auto-escaping enabled by default rather than manual Markup wrapping
- Implement strict input validation on all user-controllable fields like organization names with character whitelisting
- Apply security code review patterns specifically checking for XSS escape function misuse
- Implement Content Security Policy (CSP) headers on admin panels to mitigate XSS impact even if injection occurs
- Use automated security scanning tools (bandit, semgrep) with custom rules to detect MarkupSafe misuse patterns
- Restrict admin panel access to VPN/whitelisted IPs and require additional authentication factors
- Monitor and log administrative account activities for suspicious JavaScript execution

## Variant hunting
Search for similar patterns across codebase: regex for `Markup\(.*f['\"].*{.*}` to find all f-string+Markup combinations. Check other template formatters in flask_admin custom formatters for identical vulnerability. Investigate if other template rendering libraries (Jinja2, Mako) have user input flowing through unescaped channels. Look for user-controlled fields in model names, descriptions, metadata that flow to HTML rendering.

## MITRE ATT&CK
- T1190
- T1598
- T1566
- T1137

## Notes
This vulnerability exemplifies the importance of understanding security library semantics. MarkupSafe is a safety tool but requires correct usage patterns. The researcher's methodology was exemplary: source code review, local deployment for testing, monitoring code evolution, and patience waiting for exploitable conditions. The vulnerability only became actionable after new features introduced user-controllable data into previously-safe code. Pass Culture's open-source codebase and Docker deployment significantly facilitated vulnerability discovery. The attack requires legitimate professional account access, making it a mid-privileged escalation to admin-level compromise.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-01*
