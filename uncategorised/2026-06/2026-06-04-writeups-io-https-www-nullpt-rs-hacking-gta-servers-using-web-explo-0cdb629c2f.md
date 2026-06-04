# Hacking GTA V RP Servers Using Web Exploitation - FiveM XSS Vulnerability

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-04
- **Author:** Various
- **Program:** FiveM (GTA V Multiplayer Mod) / rcore_radiocar Resource
- **Bounty:** Not specified
- **Severity:** critical
- **Vuln types:** Cross-Site Scripting (XSS), Improper Input Validation, DOM-based XSS, Unsafe DOM Manipulation
- **Category:** uncategorised
- **Writeup:** https://www.nullpt.rs/hacking-gta-servers-using-web-exploitation

## Summary
The rcore_radiocar FiveM resource contains a DOM-based XSS vulnerability in its music player functionality that fails to sanitize user-supplied URLs before appending them to the DOM. An attacker can inject malicious JavaScript payloads via crafted URLs to achieve arbitrary code execution on connected players' clients. This vulnerability enables complete compromise of player accounts, IP leakage, credential theft, and malware distribution within FiveM servers.

## Attack scenario (step by step)
1. Attacker identifies the rcore_radiocar resource deployed on a popular FiveM roleplay server through the public server listing
2. Attacker discovers the XSS vulnerability by analyzing the client-side code via CEF Remote Debugging interface exposed on localhost:13172
3. Attacker crafts a malicious URL payload using an img tag with onerror handler to execute JavaScript (e.g., attempting to extract YouTube ID from a URL containing XSS payload)
4. Attacker joins the server and uses the music broadcast feature to submit the malicious URL, which gets stored in-game
5. When other players load the music player or interact with the resource, the payload executes in their browser context with full access to FiveM's NUI callbacks
6. Attacker achieves code execution to steal session tokens, leak player IPs, inject malware, or compromise the FiveM installation

## Root cause
The rcore_radiocar resource uses jQuery's append() function to directly insert unsanitized user-supplied URLs into the DOM without any validation, sanitization, or encoding. The code checks for YouTube URLs but treats all other inputs as direct audio sources, concatenating them into HTML without escaping special characters. The vulnerable code pattern: `$('body').append('<div id="' + this.div_id + '" style="display:none">' + this.getUrlSound() + '</div>')` directly interpolates user input into HTML context.

## Attacker mindset
A web exploitation researcher recognizing that client-side multiplayer games often have weaker security postures than traditional web applications. The attacker systematically identified a popular resource, leveraged the exposed debugging interface to reverse-engineer functionality, and identified that user input flows directly into DOM manipulation without sanitization. The motivations could range from demonstrating vulnerability in popular FiveM ecosystems to enabling account hijacking or server disruption.

## Defensive takeaways
- Never append user-supplied input directly to the DOM; use textContent instead of innerHTML/append for untrusted data
- Implement strict URL validation and whitelisting: only allow known protocols (https) and validate against a whitelist of approved domains
- Use Content Security Policy (CSP) headers to prevent inline script execution and restrict script sources
- Sanitize all user input using established libraries like DOMPurify before any DOM manipulation
- Disable or secure CEF Remote Debugging in production environments; restrict to localhost with authentication
- Implement server-side URL validation before allowing resources to process user-submitted links
- Use Vue.js or React's built-in XSS protections instead of manual DOM manipulation with jQuery
- Perform regular security audits of FiveM resources, especially paid resources that may not be open-sourced
- Implement Content Security Policy and subresource integrity checks for third-party JavaScript libraries
- Use parameterized/templated approaches for URL construction rather than string concatenation

## Variant hunting
Look for similar patterns in other FiveM resources that accept URLs as input (streaming resources, custom browsers, media players, link-sharing features). Search for: jQuery append/html with user input, innerHTML assignments, direct DOM node creation from player-submitted data, and resources handling URLs from chat or UI forms. Check for similar vulnerabilities in v-html Vue directives, document.write calls, and any resource accepting external links for media playback or display purposes.

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1059: Command and Scripting Interpreter
- T1203: Exploitation for Client Execution
- T1598: Phishing - Spearphishing Link
- T1566: Phishing
- T1204: User Execution
- T1005: Data from Local System

## Notes
The vulnerability demonstrates how even third-party game mods can introduce critical security risks. The exposure of CEF debugging interfaces significantly facilitated vulnerability discovery and exploitation. FiveM's architecture separating Lua backend from JavaScript frontend through NUI callbacks creates an attack surface if client-side validation is bypassed. This vulnerability likely affects multiple FiveM resources with similar URL-handling patterns. The researcher noted IP leakage was initially achievable through URL requests, indicating additional information disclosure risks beyond XSS.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-04*
