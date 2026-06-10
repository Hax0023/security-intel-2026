# Hacking GTA V RP Servers Using Web Exploitation Techniques

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-10
- **Author:** Various
- **Program:** FiveM/GTA V RP Servers (Bug Bounty Program Unknown)
- **Bounty:** Unknown
- **Severity:** Critical
- **Vuln types:** Cross-Site Scripting (XSS), Insecure Direct Object References, Client-Side Code Injection, Improper Input Validation, DOM-based XSS
- **Category:** uncategorised
- **Writeup:** https://www.nullpt.rs/hacking-gta-servers-using-web-exploitation

## Summary
A critical DOM-based XSS vulnerability was discovered in the rcore_radiocar FiveM resource that allows players to execute arbitrary JavaScript on other players' machines by providing malicious URLs to audio playback functionality. The vulnerability exists because user-supplied URLs are directly appended to the DOM without sanitization, bypassing YouTube URL validation checks.

## Attack scenario (step by step)
1. Attacker identifies the rcore_radiocar resource on a popular FiveM roleplay server via the public server list
2. Attacker uses CEF Remote Debugging (localhost:13172) to inspect the resource's client-side code and identify the XSS vulnerability in SoundPlayer.js
3. Attacker crafts a malicious URL containing JavaScript payload wrapped in an img tag onerror handler (e.g., non-existent URL that triggers onerror)
4. Attacker joins the server and uses the radio car UI to specify the crafted XSS payload as an audio URL
5. When other players load the malicious audio link, the JavaScript executes in their browser context with access to sensitive data
6. Attacker can harvest player IPs, perform keylogging, steal credentials, or establish persistence on compromised machines

## Root cause
The rcore_radiocar resource fails to sanitize user-supplied URL inputs before appending them to the DOM. The code checks for YouTube URLs and extracts IDs, but non-YouTube URLs are directly passed to jQuery's append() function without HTML encoding or content validation, allowing arbitrary HTML/JavaScript injection.

## Attacker mindset
Opportunistic security researcher exploiting a widely-deployed third-party FiveM resource. The attacker demonstrates methodical reconnaissance by discovering the resource through public server lists, leveraging exposed debugging interfaces to analyze code, and crafting proof-of-concept exploits. The focus on IP leakage suggests interest in doxing or targeting specific players.

## Defensive takeaways
- Implement strict input validation and sanitization for all user-supplied URLs before DOM manipulation
- Use textContent or createElement() instead of append() when handling user input to prevent XSS
- Apply HTML entity encoding to user-controlled data before inserting into DOM
- Implement Content Security Policy (CSP) headers to restrict script execution origins
- Disable or restrict CEF Remote Debugging in production environments (only enable for localhost in development)
- Perform code reviews on third-party FiveM resources, especially paid ones with widespread deployment
- Use a DOM-safe library like DOMPurify to sanitize HTML before insertion
- Validate URL schemes (whitelist http/https, reject data: URIs and javascript: protocols)
- Implement server-side validation for resource loads and enforce code signing for resources
- Monitor and alert on suspicious CEF debugging access attempts

## Variant hunting
Search for similar vulnerable patterns in other FiveM resources that handle user-supplied URLs: (1) look for resources that render custom UI with media playback (chat systems, streaming, etc.), (2) search for improper use of jQuery append/html with user input, (3) examine other paid resources that may have less scrutiny, (4) check for NUI callback handlers that pass data directly to DOM without sanitization, (5) investigate if similar XSS chains exist in vehicle customization or inventory systems, (6) test streaming/media resources like rcore_music, rcore_livery, or custom radio mods

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1204 - User Execution
- T1059 - Command and Scripting Interpreter
- T1056 - Input Capture
- T1083 - File and Directory Discovery
- T1113 - Screen Capture
- T1005 - Data from Local System
- T1041 - Exfiltration Over C2 Channel

## Notes
The vulnerability is particularly dangerous due to FiveM's architecture: (1) CEF Remote Debugging is exposed on localhost allowing local code inspection, (2) Resources are loaded into separate iframes but share network context, (3) NUI callbacks allow bidirectional communication between Lua and JavaScript, (4) Player IP leakage was achievable simply through URL fetching, (5) The rcore_radiocar resource was paid software, suggesting less community code review, (6) No evidence of patch or responsible disclosure process mentioned. This demonstrates how third-party game modifications introduce attack surface and the importance of vetting community-developed extensions. The attacker's methodology of using debugging tools to analyze obfuscated/proprietary code is highly transferable to other game mod ecosystems.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-10*
