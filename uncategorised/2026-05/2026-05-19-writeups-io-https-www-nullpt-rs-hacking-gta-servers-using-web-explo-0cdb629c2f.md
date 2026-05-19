# Hacking GTA V RP Servers Using Web Exploitation Techniques

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-19
- **Author:** Various
- **Program:** FiveM (GTA V Multiplayer Mod) / rcore_radiocar Resource
- **Bounty:** Not specified
- **Severity:** CRITICAL
- **Vuln types:** Cross-Site Scripting (XSS), Insufficient Input Validation, Unsafe DOM Manipulation, Remote Code Execution
- **Category:** uncategorised
- **Writeup:** https://www.nullpt.rs/hacking-gta-servers-using-web-exploitation

## Summary
A critical DOM-based XSS vulnerability exists in the rcore_radiocar FiveM resource which allows players to inject malicious JavaScript through specially crafted audio URLs. The vulnerability stems from unsanitized user input being directly appended to the DOM via jQuery's append() function, enabling arbitrary code execution on connected players' machines.

## Attack scenario (step by step)
1. Attacker joins a FiveM roleplay server running the vulnerable rcore_radiocar resource
2. Attacker crafts a malicious URL payload containing XSS JavaScript code disguised as an audio source
3. Attacker submits the crafted URL through the radiocar music feature interface
4. Server-side validation fails to sanitize the URL input before passing it to the client
5. Client-side JavaScript appends the unsanitized URL directly into the DOM using jQuery append()
6. Malicious JavaScript payload executes in the context of all players viewing the radiocar, allowing IP exfiltration, credential theft, or further exploitation

## Root cause
The rcore_radiocar resource fails to properly validate and sanitize user-supplied audio URLs before rendering them in the DOM. The vulnerable code path uses jQuery's append() function to directly insert user input without escaping special characters or validating URL structure, allowing injection of HTML/JavaScript. The fallback mechanism that treats non-YouTube URLs as raw audio sources compounds this by passing untrusted input directly to DOM manipulation functions.

## Attacker mindset
The attacker methodically discovered vulnerability through server reconnaissance, identified interesting resources with client-side input handling, and leveraged debugging tools (CEF Remote Debugging) to inspect client-side code. They recognized DOM manipulation vulnerabilities and crafted proof-of-concept payloads using standard XSS techniques (img tag onerror handlers with eval). This demonstrates opportunistic reconnaissance of public server infrastructure combined with web exploitation methodology.

## Defensive takeaways
- Implement strict server-side URL validation and whitelist only known audio hosting domains (YouTube, SoundCloud)
- Sanitize all user input using contextual encoding before DOM insertion - use textContent instead of innerHTML/append for untrusted data
- Disable CEF Remote Debugging in production FiveM environments to prevent attackers from inspecting client-side code
- Implement Content Security Policy (CSP) headers to restrict inline script execution and external resource loading
- Apply output encoding appropriate to context (HTML entity encoding for DOM insertion)
- Regular security audits of paid/closed-source FiveM resources for input validation flaws
- Use modern JavaScript frameworks with built-in XSS protection (Vue.js, React) rather than jQuery string concatenation

## Variant hunting
['Search for other FiveM resources using jQuery append/html/text with user input (music players, chat systems, notification systems)', 'Identify resources accepting URLs or text input without validation (spawn systems, vehicle customizers, UI frameworks)', 'Test CEF debugging on other resources to identify similar DOM-based XSS patterns', 'Audit resources handling player-supplied configuration data or cosmetic customizations', 'Review resources with NUI callback handlers that process string data without sanitization', 'Check for similar vulnerabilities in C#-based resources that may reflection-execute code']

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1059 - Command and Scripting Interpreter (JavaScript)
- T1566 - Phishing (social engineering to click malicious link)
- T1104 - Ingress Tool Transfer (payload delivery via eval)
- T1040 - Traffic Capture or Redirection (IP exfiltration)
- T1592 - Gather Victim Host Information

## Notes
The writeup demonstrates practical security research methodology applied to gaming infrastructure. The ability to access CEF Remote Debugging on localhost was crucial for discovering the vulnerability - this represents a significant security risk in FiveM's architecture. The vulnerability impacts not just the individual attacker but all players on the server who load the compromised content. The ease of discovering and exploiting this vulnerability highlights the security risks of user-generated content in multiplayer gaming platforms. Attribution to 'veritasecurity' indicates this is from a legitimate security researcher documenting findings rather than malicious disclosure.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-19*
