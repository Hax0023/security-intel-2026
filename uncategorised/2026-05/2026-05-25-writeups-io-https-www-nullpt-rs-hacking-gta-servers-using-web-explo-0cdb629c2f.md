# Hacking GTA V RP Servers Using Web Exploitation Techniques

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-25
- **Author:** Various
- **Program:** FiveM GTA V Multiplayer Mod (rcore_radiocar resource)
- **Bounty:** Not specified
- **Severity:** critical
- **Vuln types:** Cross-Site Scripting (XSS), Client-Side Code Injection, Unsafe DOM Manipulation, Missing Input Validation
- **Category:** uncategorised
- **Writeup:** https://www.nullpt.rs/hacking-gta-servers-using-web-exploitation

## Summary
A critical XSS vulnerability exists in the rcore_radiocar FiveM resource that allows attackers to execute arbitrary JavaScript on players' machines by injecting malicious URLs into the music player functionality. The vulnerability stems from unsafe DOM manipulation using jQuery's append() function without proper input sanitization, enabling remote code execution on connected players.

## Attack scenario (step by step)
1. Attacker identifies the rcore_radiocar resource on a FiveM roleplay server through the public server list
2. Attacker crafts an XSS payload disguised as a music URL using an erroneous img tag with onerror handler
3. Attacker joins the server and uses the radio car feature to broadcast the malicious payload URL
4. The JavaScript code fails to extract a YouTube ID, treating the payload as a generic audio source
5. The vulnerable code appends the unsanitized URL directly to the DOM using jQuery append()
6. The onerror event triggers on other players' clients, executing the attacker's JavaScript payload and potentially stealing credentials or IP addresses

## Root cause
The rcore_radiocar resource uses jQuery's append() function to inject user-supplied URLs directly into the DOM without sanitization. When URL parsing fails (non-YouTube/SoundCloud sources), the raw user input is concatenated into an HTML string and appended to the page, allowing injection of arbitrary HTML/JavaScript. The developer failed to validate, encode, or sanitize user-controlled input before DOM manipulation.

## Attacker mindset
Opportunistic attacker leveraging public FiveM server infrastructure to identify vulnerable resources. The attacker performed reconnaissance through the CEF Remote Debugging interface (localhost:13172) to understand client-side implementation and identify input vectors. The motivation evolved from initial IP leakage interest to demonstrating arbitrary JavaScript execution, indicating a progression toward potential account compromise or malware distribution to the gaming community.

## Defensive takeaways
- Never use string concatenation for HTML construction; use textContent instead of innerHTML/append for user input
- Implement strict input validation and URL whitelisting for music service integrations (YouTube, SoundCloud only)
- Use Content Security Policy (CSP) headers to restrict script execution origins and inline scripts
- Sanitize all user input using established libraries (DOMPurify, xss package) before any DOM insertion
- Disable or restrict CEF Remote Debugging in production environments (localhost:13172)
- Implement server-side URL validation and proxy requests through trusted services rather than direct client-side loading
- Code review paid/closed-source resources for security vulnerabilities before deployment
- Use templating engines with automatic escaping (Vue.js template syntax) instead of raw jQuery DOM manipulation
- Implement security headers and consider running FiveM resources in sandboxed contexts with limited API access

## Variant hunting
Look for similar vulnerabilities in other FiveM resources that: (1) accept user-supplied URLs for audio/video playback, (2) perform dynamic DOM manipulation with jQuery/vanilla JavaScript without sanitization, (3) use getYoutubeUrlId() or similar fallback patterns, (4) render user input in NUI callbacks, (5) lack CSP headers, (6) process user-supplied file paths or URLs in custom UIs, (7) use eval() or Function() constructors with user data, (8) implement custom music/media players without proper input validation. Common patterns in roleplay resources like item systems, vehicle customization, or streaming features may have similar vulnerabilities.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1059 - Command and Scripting Interpreter (JavaScript)
- T1203 - Exploitation for Client Execution
- T1566 - Phishing (social engineering to get players to use malicious URLs)
- T1598 - Phishing for Information (IP harvesting via onerror requests)
- T1539 - Steal Web Session Cookie
- T1005 - Data from Local System (memory/session data access)

## Notes
The vulnerability was discovered through methodical server enumeration and CEF debugging exploitation. The author demonstrated excellent reconnaissance methodology by using the public FiveM server list and built-in debugging features. The presentation suggests the full exploit likely included credential harvesting or further payload delivery mechanisms not detailed in this excerpt. The widespread adoption of FiveM and popularity of roleplay servers creates significant attack surface. Similar class of vulnerabilities likely affects other paid/proprietary FiveM resources with closed source code. The localhost CEF debugging exposure is particularly dangerous as it allows unauthenticated inspection of resource code without server-side access, enabling vulnerability discovery in paid resources.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-25*
