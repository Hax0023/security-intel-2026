# Hacking GTA V RP Servers Using Web Exploitation Techniques

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-07
- **Author:** Various
- **Program:** FiveM (GTA V Multiplayer Mod) - rcore_radiocar Resource
- **Bounty:** Not specified
- **Severity:** critical
- **Vuln types:** Cross-Site Scripting (XSS), Improper Input Validation, Unsafe DOM Manipulation, Client-Side Code Injection
- **Category:** uncategorised
- **Writeup:** https://www.nullpt.rs/hacking-gta-servers-using-web-exploitation

## Summary
The rcore_radiocar FiveM resource contains a reflected XSS vulnerability in its audio URL handling mechanism. User-supplied URLs are appended directly to the DOM without sanitization, allowing attackers to inject arbitrary JavaScript payloads and execute them on connected players' machines.

## Attack scenario (step by step)
1. Attacker identifies rcore_radiocar resource on a FiveM roleplay server via the public server list
2. Attacker accesses CEF Remote Debugging interface on localhost:13172 to analyze resource source code and identify XSS vulnerability in SoundPlayer.js
3. Attacker crafts malicious URL payload using img onerror attribute to bypass YouTube URL detection (e.g., invalid image tag with JavaScript eval in error handler)
4. Attacker broadcasts crafted URL through music feature, causing it to be appended to DOM without sanitization
5. JavaScript payload executes in victim players' browser context with access to NUI callbacks and client data
6. Attacker exfiltrates sensitive data, modifies game state, or establishes persistence on compromised clients

## Root cause
Unsafe use of jQuery's append() function with unsanitized user input. The resource validates for YouTube URLs but fails to validate or sanitize non-YouTube URLs before DOM insertion. No Content Security Policy (CSP) headers are implemented to restrict script execution.

## Attacker mindset
Reconnaissance-focused attacker who systematically explores public server listings, analyzes available resources, leverages exposed debugging interfaces, and weaponizes UI functionality for client-side code execution. Demonstrates understanding of web security principles applied to game modding ecosystem.

## Defensive takeaways
- Implement strict input validation and URL schema whitelisting for all user-supplied URLs
- Use textContent instead of innerHTML/append for untrusted content; sanitize HTML with libraries like DOMPurify
- Implement Content Security Policy (CSP) headers to restrict inline script execution and external resource loading
- Disable or restrict CEF Remote Debugging in production builds or require authentication
- Use URL.parse() and URL.URL constructor to validate URL structure before processing
- Implement server-side validation and sanitization for all resource content
- Apply principle of least privilege to NUI callbacks and client-side script capabilities
- Regular security audits of third-party resources before deployment on public servers
- Implement output encoding when rendering user-controlled data in HTML/JavaScript contexts

## Variant hunting
Search for similar unsafe append/innerHTML patterns in other FiveM resources, particularly those handling user-supplied URLs (streaming services, link sharing, media players). Investigate other NUI callback mechanisms for injection vulnerabilities. Review resources that parse user input for protocol detection (YouTube, Twitch, etc.) as detection bypass is likely.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1059 - Command and Scripting Interpreter
- T1203 - Exploitation for Client Execution
- T1104 - Proxy Execution
- T1047 - Windows Management Instrumentation

## Notes
FiveM's exposed CEF Remote Debugging interface significantly lowers barrier to vulnerability discovery. The vulnerability chain demonstrates how game modding ecosystems inherit web security risks. Paid/obfuscated resources are not inherently safer. This attack vector affects all players connected to compromised servers, creating widespread impact potential.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-07*
