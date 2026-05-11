# Hacking GTA V RP Servers Using Web Exploitation Techniques

## Metadata
- **Source:** writeups.io
- **Date:** 
- **Author:** Various
- **Program:** FiveM (GTA V Multiplayer Mod)
- **Bounty:** Not specified
- **Severity:** critical
- **Vuln types:** Cross-Site Scripting (XSS), Unsafe DOM Manipulation, Insufficient Input Validation, Client-Side Code Injection
- **Category:** uncategorised
- **Writeup:** https://www.nullpt.rs/hacking-gta-servers-using-web-exploitation

## Summary
A critical XSS vulnerability was discovered in the rcore_radiocar FiveM resource that allows attackers to execute arbitrary JavaScript on players' machines by injecting malicious URLs into the music player. The vulnerability stems from unsanitized user input being directly appended to the DOM using jQuery's append() function without validation or encoding.

## Attack scenario (step by step)
1. Attacker identifies the rcore_radiocar resource used on popular FiveM roleplay servers
2. Attacker gains access to the CEF Remote Debugging interface or observes the client-side code through normal gameplay
3. Attacker crafts an XSS payload disguised as a music URL (e.g., a crafted img tag with onerror handler)
4. Attacker submits the malicious URL through the radiocar music broadcast feature
5. The vulnerable code fails to validate the URL and appends it directly to DOM via jQuery append()
6. JavaScript onerror handler executes, fetching and eval'ing a larger payload to compromise the player's machine

## Root cause
The SoundPlayer.js create() function performs insufficient input validation on user-supplied URLs. When a URL cannot be identified as a YouTube link, it is treated as an audio file and appended to the DOM using jQuery's append() without sanitization. The code: `$('body').append("<div id='" + this.div_id + "' style='display:none'>" + this.getUrlSound() + "</div>")` directly concatenates user input into HTML without encoding special characters or validating the URL format.

## Attacker mindset
An attacker would recognize this as a straightforward client-side security bypass opportunity. By leveraging the CEF Remote Debugging interface accessibility and observing the unsanitized append() operation, they could craft polyglot payloads that bypass basic YouTube ID regex checks. The attacker mindset involves exploring publicly available FiveM servers, identifying popular resources, and fuzzing input fields to discover DOM-based XSS vulnerabilities that lead to arbitrary code execution on victim machines.

## Defensive takeaways
- Always sanitize and validate user input before DOM manipulation; use textContent instead of innerHTML/append for untrusted data
- Implement a whitelist of allowed URL schemes (https only) and validate against known music platforms before processing
- Use DOMPurify or similar libraries to sanitize any user-controlled content before DOM insertion
- Implement Content Security Policy (CSP) headers to restrict script execution sources and prevent inline script execution
- Disable or properly authenticate CEF Remote Debugging in production environments to prevent code inspection by attackers
- Apply principle of least privilege: resources should only communicate necessary data through NUI callbacks and validate all callback parameters
- Conduct security code reviews for paid/closed-source resources before deployment on public servers
- Implement server-side URL validation and proxy music requests rather than allowing direct client-side resource loading

## Variant hunting
['Search for other FiveM resources that use jQuery append(), innerHTML, or insertAdjacentHTML with unsanitized user input', 'Examine NUI callback handlers that accept URLs or file paths without validation', 'Look for resources using Howler.js or other audio libraries with improper input handling', 'Identify resources with CEF debugging enabled that expose sensitive functionality', 'Check for stored XSS variants where malicious URLs are saved to server database and broadcast to multiple players', 'Investigate other broadcast/streaming features (custom maps, vehicle spawns, custom interiors) for similar injection patterns', "Search for iframe-based resources that don't properly isolate content from untrusted sources"]

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1059.007 - Command and Scripting Interpreter: JavaScript
- T1564.006 - Hide Artifacts: Run Virtual Instance
- T1199 - Trusted Relationship
- T1566.002 - Phishing: Spearphishing Link
- T1204.001 - User Execution: Malicious Link

## Notes
The vulnerability demonstrates the security risks of third-party modded game servers where resources lack proper security review. The CEF Remote Debugging interface being accessible allows attackers to directly inspect and analyze resource code. This is a supply chain vulnerability where a single compromised or vulnerable resource can affect all players on a server. The impact extends beyond individual machines to potential lateral movement within gaming communities and networks. The researcher discovered this through methodical reconnaissance: identifying popular resources, accessing debugging interfaces, and analyzing code for common web vulnerabilities adapted to game mod context.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-11*
