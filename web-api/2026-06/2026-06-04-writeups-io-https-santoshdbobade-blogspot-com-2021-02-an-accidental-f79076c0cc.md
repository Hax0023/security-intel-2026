# Accidental XSS on uu.nl via UUID Parameter

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-04
- **Author:** Various
- **Program:** uu.nl (Utrecht University)
- **Bounty:** Not specified
- **Severity:** high
- **Vuln types:** Cross-Site Scripting (XSS), Reflected XSS
- **Category:** web-api
- **Writeup:** https://santoshdbobade.blogspot.com/2021/02/an-accidental-xss-onuunl.html

## Summary
A reflected XSS vulnerability was discovered in a uu.nl subdomain where user-supplied UUID parameters were reflected unsanitized within HTML title tags. The attacker exploited improper output encoding by closing the title tag and injecting JavaScript code that executes in the victim's browser.

## Attack scenario (step by step)
1. Attacker enumerates subdomains of uu.nl and identifies vulnerable www.*.uu.nl instances
2. Attacker uses waybackurls tool to discover historical URLs and identifies endpoint with UUID query parameter
3. Attacker crafts malicious payload: test</title><script>alert(document.domain)</script> and injects into uuid parameter
4. Victim visits attacker-crafted URL containing the payload
5. Browser parses response and reflects UUID value unsanitized within title tag
6. Title tag is closed prematurely and JavaScript executes with victim's privileges

## Root cause
Insufficient output encoding/sanitization of user input (uuid parameter) before insertion into HTML context. The application failed to properly escape or validate the uuid parameter when rendering it within the HTML title element, allowing tag injection.

## Attacker mindset
Systematic reconnaissance through subdomain enumeration and historical URL discovery to identify low-hanging fruit. Opportunistic testing of obvious injection points (parameters) with basic payload manipulation to achieve code execution.

## Defensive takeaways
- Implement context-aware output encoding for all user-controlled data (HTML encode for HTML context, JavaScript encode for JS context)
- Apply input validation on UUID parameters to enforce expected format and reject suspicious characters
- Use security headers like Content-Security-Policy to restrict script execution sources
- Implement automated security testing in CI/CD pipeline to catch XSS before deployment
- Apply parameterized templating engines that auto-escape by default
- Conduct security code review focusing on all parameter usage in HTML rendering

## Variant hunting
['Search for other parameters reflecting in title, h1, meta, or other HTML tags', 'Test other subdomains following pattern www.*.uu.nl for same vulnerability', 'Attempt DOM-based XSS by checking if uuid parameter is used in client-side JavaScript', 'Test for stored XSS if uuid values are persisted and displayed to other users', "Attempt event handler injection: test' onload='alert(1)' data='", 'Test attribute context escaping: test" onfocus="alert(1)" autofocus="']

## MITRE ATT&CK
- T1190
- T1566.002
- T1204.001

## Notes
Writeup lacks critical details: specific subdomain name redacted, no bounty amount disclosed, no timeline provided, minimal technical depth. UUID parameter typically expected to be in GUID format - lack of input validation compound the XSS risk. 'Accidental' in title suggests findings may have been coincidental rather than systematic security assessment.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-04*
