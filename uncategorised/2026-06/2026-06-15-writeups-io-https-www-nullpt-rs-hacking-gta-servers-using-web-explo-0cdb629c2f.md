# Hacking GTA V RP Servers Using Web Exploitation Techniques

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-15
- **Author:** Various
- **Program:** FiveM (GTA V multiplayer mod)
- **Bounty:** Not specified
- **Severity:** Critical
- **Vuln types:** Cross-Site Scripting (XSS), Unsafe DOM Manipulation, Client-Side Code Injection, Insufficient Input Validation
- **Category:** uncategorised
- **Writeup:** https://www.nullpt.rs/hacking-gta-servers-using-web-exploitation

## Summary
The rcore_radiocar FiveM resource contains a reflected XSS vulnerability where user-supplied URLs are directly appended to the DOM without sanitization. An attacker can craft malicious URLs containing JavaScript payloads that execute arbitrary code on players' machines when the music player attempts to process them.

## Attack scenario (step by step)
1. Attacker discovers the rcore_radiocar resource on a FiveM roleplay server via the server browser
2. Attacker crafts a malicious URL containing an XSS payload (e.g., using img onerror or other DOM-based vectors)
3. Attacker shares the malicious URL or tricks a player into using it as a music source in their car
4. Player enters the URL into the music player interface, triggering the NUI callback
5. The JavaScript code fails YouTube URL extraction and treats it as an unknown audio source
6. The URL is directly appended to the DOM via jQuery append() without sanitization, executing the injected JavaScript payload on the player's client

## Root cause
The SoundPlayer.js create() function directly appends unsanitized user input (this.getUrlSound()) to the DOM using jQuery's append() method without any HTML encoding or input validation. The application assumes only valid audio URLs will be provided but fails to sanitize malicious payloads.

## Attacker mindset
Security researcher identifying low-hanging fruit in popular third-party game modifications. The attacker leverages the fact that paid resources are often less scrutinized, uses debugging tools exposed by FiveM (CEF Remote Debugging on localhost:13172), and recognizes the classic XSS pattern of unsanitized user input being directly inserted into the DOM.

## Defensive takeaways
- Never use jQuery append(), innerHTML, or similar methods with user-supplied data; use textContent or createElement() instead
- Implement strict input validation: validate URLs against expected formats (protocol, domain whitelist) before processing
- Sanitize all user input before DOM insertion using DOMPurify or similar libraries
- Use Content Security Policy (CSP) headers to restrict inline script execution
- Implement output encoding/HTML entity escaping for any user-controlled data rendered in HTML contexts
- Disable or restrict CEF Remote Debugging in production environments to prevent resource inspection
- Conduct security code reviews for third-party resources, especially paid ones
- Use a URL parser library to extract video IDs rather than regex, reducing parsing bypass opportunities

## Variant hunting
Search for similar patterns in other FiveM resources: (1) Other audio/media players that accept user URLs without sanitization, (2) Resources using jQuery append/html with user input, (3) Resources with CEF debugging enabled in production, (4) Custom UI resources handling any user-supplied data in DOM operations, (5) NUI callbacks that relay unvalidated parameters to the frontend

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1059.007 - Command and Scripting Interpreter: JavaScript
- T1657 - Exploitation of Vulnerability in Browser Extensions
- T1598 - Phishing - Link
- T1204.001 - User Execution: Malicious Link

## Notes
The vulnerability is particularly dangerous in a multiplayer gaming context where social engineering is trivial. The researcher demonstrated impressive methodology by identifying the attack surface through public server listings, using built-in debugging tools to reverse-engineer paid resources, and recognizing a classic XSS pattern. The CEF Remote Debugging interface exposure on localhost:13172 is a significant operational security issue. The use of eval() in conjunction with DOM-based XSS amplifies severity. Client-side code execution in FiveM could potentially lead to credential theft, account hijacking, or lateral movement on the player's machine.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-15*
