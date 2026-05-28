# Sandbox iframe XSS Challenge - CSP Bypass via Redirect and Parent Window Access

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-28
- **Author:** Various
- **Program:** Private/Educational CTF Challenge
- **Bounty:** N/A - Educational challenge
- **Severity:** high
- **Vuln types:** Content Security Policy Bypass, Cross-Site Scripting (XSS), Sandbox Escape, Open Redirect
- **Category:** web-api
- **Writeup:** https://joaxcar.com/blog/2024/05/16/sandbox-iframe-xss-challenge-solution/

## Summary
A sandboxed iframe XSS challenge was solved by exploiting a CSP redirect loophole to load arbitrary JavaScript from CDN, then accessing the parent window's hash fragment through a fetch('') technique. The challenge combined three security mechanisms (CSP, iframe sandbox, and hash-based flag storage) that were defeated through understanding browser CSP specification edge cases and sandbox behavior.

## Attack scenario (step by step)
1. Attacker base64-encodes malicious HTML containing a script tag with redirect URL parameter
2. Encoded payload is injected into the xss search parameter on the challenge page
3. Malicious HTML is loaded into sandboxed iframe via srcdoc attribute, inheriting parent CSP
4. Script tag references /redirect endpoint (allowed by 'self' in CSP) which redirects to CDN resource
5. Browser loads arbitrary JavaScript from CDN after redirect, only validating base domain per CSP spec
6. Loaded JavaScript (HTMX or Angular) executes XSS payload; attacker then performs fetch('') or similar to access parent window hash containing flag

## Root cause
CSP specification allows redirects from allowed sources to load content from any path on the destination domain without strict path validation. Combined with srcdoc iframe inheritance of parent CSP and sandbox permissions allowing scripts with allow-modals, this creates an exploitable bypass chain. The fetch('') behavior in sandboxed context provides cross-origin access to parent resources.

## Attacker mindset
Attacker deeply understands CSP specification nuances, particularly W3C documented redirect behavior (CVE-adjacent edge case). Knowledge that CSP path restrictions don't apply post-redirect is crucial. Recognizes that common CDN libraries (HTMX, Angular) can serve as XSS gadgets. Understands iframe sandbox origin handling and srcdoc behavior as distinct from src-loaded resources.

## Defensive takeaways
- Avoid CSP directives with full paths that can be abused via open redirects; use hash-based integrity checks instead
- Remove 'unsafe-eval' from CSP if not absolutely necessary
- Do not use open redirects on the same origin as sensitive content
- Consider using frame-ancestors directive in addition to iframe sandbox attributes
- Understand that srcdoc iframe inherits parent CSP unlike src-loaded external frames
- Avoid storing sensitive data (flags/tokens) in URL fragments accessible to sandboxed contexts
- Regularly audit which external dependencies and gadgets are accessible via CSP-allowed sources
- Test CSP bypass scenarios including redirect chains during security review

## Variant hunting
Look for similar patterns: any strict CSP with allowed domains + open redirects on same origin; srcdoc iframes with allow-scripts inheriting parent CSP; hash-stored secrets in applications with iframe injection points; other CDN-hosted libraries with dangerous auto-executing code (jQuery with plugins, legacy frameworks); fetch('') behavior in other sandbox configurations; postMessage communication from sandboxed iframes to parent

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application (CSP bypass via redirect)
- T1059 - Command and Scripting Interpreter (JavaScript execution in iframe)
- T1021 - Remote Services (iframe sandbox escape)
- T1005 - Data from Local System (hash fragment access)

## Notes
This is an educational CTF writeup demonstrating sophisticated security bypass techniques. The CSP redirect loophole is documented in W3C spec but frequently overlooked by developers. The attack requires chaining multiple weaknesses: unsanitized input → CSP bypass → sandbox escape → flag exfiltration. The fetch('') technique hint suggests Relative URL Navigation behavior in sandboxed contexts. This represents realistic attack patterns seen in real-world applications with similar architectural flaws.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-28*
