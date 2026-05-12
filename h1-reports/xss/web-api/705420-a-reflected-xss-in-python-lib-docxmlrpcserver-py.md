# Reflected XSS in python/Lib/DocXMLRPCServer.py

## Metadata
- **Source:** HackerOne
- **Report:** 705420 | https://hackerone.com/reports/705420
- **Submitted:** 2019-10-01
- **Reporter:** longwenzhang
- **Program:** Python
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Cross-Site Scripting (XSS), Reflected XSS, Input Validation Failure
- **CVEs:** CVE-2019-16935
- **Category:** web-api

## Summary
A reflected XSS vulnerability was discovered in Python's DocXMLRPCServer.py library where user-controlled input was not properly sanitized before being reflected in HTML responses. This allowed attackers to inject arbitrary JavaScript code that would execute in the context of users' browsers when accessing malicious XMLRPC documentation pages.

## Attack scenario
1. Attacker crafts a malicious URL containing JavaScript payload targeting the XMLRPC server's documentation endpoint
2. Attacker sends the link to a victim user (via email, chat, social media, etc.)
3. Victim clicks the link while authenticated or in a session with the XMLRPC server
4. The vulnerable server reflects the unescaped payload in the HTML response
5. Victim's browser parses and executes the injected JavaScript code
6. Attacker gains ability to steal session tokens, perform actions on behalf of user, or harvest credentials

## Root cause
The DocXMLRPCServer.py library failed to properly HTML-encode or sanitize user-supplied input (likely from URL parameters or request paths) before including it in dynamically generated HTML documentation pages. The server trusted user input and directly embedded it into HTML without using appropriate escaping functions.

## Attacker mindset
An attacker would target this vulnerability to gain unauthorized access to XMLRPC server functionality, steal authenticated user sessions, or perform malicious actions on behalf of legitimate users. The reflected nature makes it easy to deliver via social engineering.

## Defensive takeaways
- Always HTML-encode user input before rendering in HTML context using language-appropriate escaping functions
- Implement Content Security Policy (CSP) headers to restrict script execution origins
- Use templating engines that auto-escape output by default
- Validate and sanitize all user inputs on the server side
- Apply whitelist validation for expected input formats
- Use security testing frameworks to scan for XSS vulnerabilities in generated content
- Implement HTTP security headers (X-XSS-Protection, X-Content-Type-Options)
- Conduct code review of dynamic HTML generation, especially in built-in libraries

## Variant hunting
Check other Python standard library modules that generate HTML for similar reflection vulnerabilities
Review SimpleXMLRPCServer and other RPC implementations for unescaped output
Audit Django, Flask, and other frameworks' auto-generated admin/documentation pages
Test CGI, wsgiref, and other HTTP handling modules for reflected XSS in error pages
Search for uses of string concatenation in HTML generation rather than proper templating
Look for functions that accept user input and pass directly to response.write() or print()

## MITRE ATT&CK
- T1190
- T1566.002
- T1598.002

## Notes
The vulnerability was formally reported to Python Security Response Team (PSRT), assigned CVE-2019-16935, and tracked in Python bug tracker as issue #38243. The write-up itself is minimal but references the official disclosure channels, indicating responsible disclosure was followed. This vulnerability affects all Python versions with the vulnerable DocXMLRPCServer.py code path.

## Full report
<details><summary>Expand</summary>

I have report this issue to PSRT and it has been resolved now.
Details about this issue is at https://bugs.python.org/issue38243 and http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2019-16935

## Impact

It's the same with other xss.

</details>

---
*Analysed by Claude on 2026-05-12*
