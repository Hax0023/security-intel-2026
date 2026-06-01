# Hacking GTA V RP Servers Using Web Exploitation Techniques

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-01
- **Author:** Various
- **Program:** FiveM (GTA V multiplayer mod) - rcore_radiocar resource
- **Bounty:** Not specified
- **Severity:** critical
- **Vuln types:** Cross-Site Scripting (XSS), Improper Input Validation, Unsafe DOM Manipulation, Client-Side Code Injection
- **Category:** uncategorised
- **Writeup:** https://www.nullpt.rs/hacking-gta-servers-using-web-exploitation

## Summary
The rcore_radiocar FiveM resource contains a reflected XSS vulnerability in its music URL handling mechanism. User-supplied URLs are appended directly to the DOM without sanitization, allowing attackers to inject malicious JavaScript payloads that execute in players' browsers with full client access.

## Attack scenario (step by step)
1. Attacker identifies the rcore_radiocar resource on a public FiveM server via the server listing
2. Attacker uses CEF Remote Debugging (localhost:13172) to inspect the resource's client-side code and identifies unsanitized URL handling in SoundPlayer.js
3. Attacker crafts an XSS payload embedding JavaScript code in a malicious URL (e.g., using img onerror attribute)
4. Attacker joins the FiveM server and triggers the music player feature with the malicious URL
5. The resource fails to extract a YouTube ID, treats the URL as a direct audio source, and appends it unsanitized to the DOM via jQuery.append()
6. The XSS payload executes in the player's browser context, allowing arbitrary code execution and potential account compromise

## Root cause
The create() function in SoundPlayer.js uses jQuery's append() method to insert user-controlled URLs directly into the DOM without sanitization or encoding. The application only validates YouTube URLs but fails to sanitize non-YouTube URLs, assuming they are safe audio sources. No Content Security Policy (CSP) or input validation is implemented for arbitrary URLs.

## Attacker mindset
An attacker seeking to compromise GTA RP server players would recognize that paid resources have limited source code visibility but that CEF Remote Debugging provides a backdoor to inspect client-side logic. The attacker leverages this debugging capability to reverse-engineer the vulnerable code, then exploits the obvious XSS vulnerability through a feature (music URL specification) that is regularly used by players.

## Defensive takeaways
- Implement strict input validation and sanitization for all user-supplied URLs before DOM insertion
- Use textContent or createElement instead of innerHTML/append for dynamic content when possible
- Apply DOMPurify or similar library to sanitize any HTML content before insertion
- Implement Content Security Policy (CSP) headers to restrict inline script execution
- Disable or restrict CEF Remote Debugging in production FiveM environments
- Validate URLs against a whitelist of allowed domains (YouTube, SoundCloud only)
- Perform security code reviews of third-party FiveM resources before deployment
- Use URL encoding/escaping for any user input rendered in HTML context

## Variant hunting
Similar XSS vulnerabilities likely exist in other FiveM resources that accept user input for URLs, file paths, or custom content (vehicle skins, map modifications, UI customizations). Resources handling streaming content, custom notifications, or player-generated media are high-risk targets. The same CEF debugging technique can be used to audit other paid resources for similar DOM manipulation vulnerabilities.

## MITRE ATT&CK
- T1190
- T1203
- T1059.007
- T1566.002
- T1204.001
- T1563.001

## Notes
The writeup demonstrates a practical attack chain against gaming infrastructure. The availability of CEF Remote Debugging on localhost:13172 is a significant security oversight that enables reverse-engineering of paid, proprietary resources. This vulnerability class is particularly dangerous in gaming contexts where players trust server-provided content. The attack requires no special privileges and can be executed by any player who joins the server.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-01*
