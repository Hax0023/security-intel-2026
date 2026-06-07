# Stored XSS in Administrator Panel via MarkupSafe Misuse

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-07
- **Author:** Various
- **Program:** pass Culture Bug Bounty (Private)
- **Bounty:** Not disclosed
- **Severity:** HIGH
- **Vuln types:** Stored XSS, Improper Output Encoding, Template Injection
- **Category:** web-api
- **Writeup:** https://www.aeth.cc/public/Article-Pass-Culture/stored-xss-article-en.html

## Summary
A stored XSS vulnerability was discovered in the pass Culture administrator panel due to misuse of the MarkupSafe library. Developers used f-string formatting before applying Markup(), negating the protection mechanism. The vulnerability became exploitable when user-controlled offerer names were rendered without proper escaping in administrative UI links.

## Attack scenario (step by step)
1. Attacker creates a professional account on pass Culture platform
2. Attacker registers a new offerer/vendor with a malicious name containing XSS payload (e.g., '<img src=x onerror="alert(1)">')
3. Offerer name is stored in the database without sanitization
4. Administrator views the fraud validation panel containing the offerer link formatter
5. The _offerer_link() function renders the malicious name using Markup(f'...{text}...') pattern
6. XSS payload executes in administrator's browser context, potentially stealing session tokens or admin credentials

## Root cause
Developers misunderstood MarkupSafe's protection model by applying f-string variable interpolation before passing to Markup(). This caused variables to be embedded in the string before any HTML escaping occurred. The Markup() call only marked the final string as safe, bypassing all escaping of user-controlled content that was already baked into the string.

## Attacker mindset
Patient, methodical researcher who conducted routine code reviews and tracked commit history to identify when safe code became vulnerable. Waited for the specific commit that introduced user-controlled data into a previously safe formatter pattern, then immediately recognized the exploitation path.

## Defensive takeaways
- Never interpolate user input before HTML escaping functions; always escape first, then embed
- Use templating engines (Jinja2) with auto-escaping enabled rather than manual Markup() calls
- Substitute f-strings with parameterized string operations: Markup('<a href="{url}">{text}</a>').format(url=escape(url), text=escape(text))
- Implement mandatory code review checklist specifically for XSS patterns in admin panels
- Add security-focused unit tests that inject malicious strings into all admin formatters
- Monitor template/formatter functions during code review for anti-pattern: Markup(f'...{var}...')
- Establish secure coding guidelines documenting correct MarkupSafe usage with examples
- Use static analysis tools configured to detect f-string usage within security-sensitive functions

## Variant hunting
Search codebase for: (1) All Markup() calls containing f-strings or .format() with external variables, (2) Other flask_admin custom formatters using similar patterns, (3) User-controlled fields recently added to database models that feed into existing formatters, (4) Comments or TODOs near template/formatter functions suggesting planned user input integration

## MITRE ATT&CK
- T1190
- T1059.007
- T1592

## Notes
Researcher demonstrated excellent bug hunting discipline by establishing a weekly code review routine and tracking commit history. The vulnerability transitioned from low-risk code smell (misuse of MarkupSafe without exploitable input) to critical when developers committed changes injecting real user data. Initial non-exploitable finding became valuable once attacker recognized the injection point would be user-controllable via professional account offerer names. Disclosure was coordinated post-patch in private program. Open source codebase significantly aided analysis and reproduction.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-07*
