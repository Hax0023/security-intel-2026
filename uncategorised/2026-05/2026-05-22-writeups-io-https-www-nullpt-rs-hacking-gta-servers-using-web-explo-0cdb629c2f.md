# Hacking GTA V RP Servers Using Web Exploitation - FiveM XSS via rcore_radiocar Resource

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-22
- **Author:** Various
- **Program:** FiveM (Grand Theft Auto V Multiplayer Mod)
- **Bounty:** Not specified
- **Severity:** Critical
- **Vuln types:** Cross-Site Scripting (XSS), Improper Input Validation, Unsafe DOM Manipulation, Client-Side Code Injection
- **Category:** uncategorised
- **Writeup:** https://www.nullpt.rs/hacking-gta-servers-using-web-exploitation

## Summary
The rcore_radiocar FiveM resource contains a reflected XSS vulnerability in its music URL handling functionality. User-supplied URLs are directly appended to the DOM without sanitization, allowing attackers to execute arbitrary JavaScript on connected players' machines. This vulnerability can be exploited to compromise player accounts, steal credentials, and execute malicious code.

## Attack scenario (step by step)
1. Attacker identifies the rcore_radiocar resource on a target FiveM server through the public server list
2. Attacker uses CEF Remote Debugging (localhost:13172) to inspect the resource's client-side code and identify the XSS vulnerability in SoundPlayer.js
3. Attacker crafts a malicious XSS payload using an img tag with onerror attribute to fetch and execute arbitrary JavaScript via eval()
4. Attacker connects to the target server and uses the radiocar feature to submit the malicious URL as a music source
5. When the payload is processed, jQuery's append() function injects the unsanitized URL into the DOM, triggering the XSS
6. Arbitrary JavaScript executes in the context of the player's FiveM client, allowing credential theft, account compromise, or further exploitation

## Root cause
The rcore_radiocar resource fails to sanitize user-supplied URLs before appending them directly to the DOM using jQuery's append() function. The code checks if a URL is a YouTube link but treats all non-YouTube URLs as safe audio sources, directly concatenating them into HTML without encoding or validation. The Howler.js library instantiation includes the raw URL, and the subsequent DOM append operation creates an exploitable XSS vector.

## Attacker mindset
An attacker researches popular FiveM resources by browsing public server lists, then uses the exposed CEF Remote Debugging interface to reverse-engineer paid resources without authorization. Recognizing that user-controlled input flows directly into the DOM without sanitization, the attacker weaponizes this into an XSS exploit. The attacker understands that executing code on player clients provides access to sensitive data, account credentials, and further system compromise opportunities.

## Defensive takeaways
- Implement strict input validation and URL schema whitelisting - only allow http/https protocols and validate against known safe domains
- Use textContent instead of append() or use proper DOM APIs (createElement) rather than string concatenation for dynamic content
- Sanitize all user input using a robust HTML sanitization library before any DOM manipulation
- Disable or restrict CEF Remote Debugging in production environments; only expose on localhost with authentication
- Implement Content Security Policy (CSP) headers to prevent inline script execution and restrict resource loading origins
- Apply output encoding when displaying user-supplied data - encode special characters to prevent HTML/JavaScript interpretation
- Conduct security code reviews for client-side scripts, especially those handling user input from networked sources
- Use templating engines with automatic escaping rather than manual string concatenation
- Implement server-side URL validation and provide only verified, server-hosted media sources to clients

## Variant hunting
Search for similar patterns in other FiveM resources: (1) Resources handling user-supplied URLs (music players, streaming, media) - check for unsafe jQuery append/html usage; (2) NUI callbacks that accept URL parameters without sanitization - audit all client-to-server communication boundaries; (3) JavaScript resources using eval() or Function() constructor with user input; (4) CEF-based applications accepting unvalidated input in DOM operations; (5) Other paid resources with similar radio/media functionality that may have identical vulnerabilities; (6) Resources using outdated versions of Howler.js or jQuery without modern security patches

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1059 - Command and Scripting Interpreter (JavaScript)
- T1203 - Exploitation for Client Execution
- T1598 - Phishing - Spearphishing Link (delivery mechanism)
- T1539 - Steal Web Session Cookie (if credential theft is goal)
- T1056 - Keylogging (potential post-exploitation)
- T1040 - Network Sniffing (IP leakage mentioned in writeup)

## Notes
The vulnerability is particularly severe because: (1) FiveM exposes CEF debugging interface allowing attackers to reverse-engineer paid resources; (2) Paid resources may receive less security scrutiny; (3) The attack is reliable and doesn't require server-side vulnerabilities; (4) Client-side code execution in gaming contexts can lead to account takeover via credential theft; (5) The resource is popular on multiple servers, affecting many players; (6) No authentication or CORS protections prevent remote exploitation. The author demonstrated practical exploitation using img onerror technique to bypass eval() restrictions. The writeup demonstrates excellent vulnerability research methodology: reconnaissance, reverse engineering, proof-of-concept development, and clear documentation.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-22*
