# Hacking GTA V RP Servers Using Web Exploitation Techniques

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-28
- **Author:** Various
- **Program:** FiveM (GTA V Multiplayer Mod)
- **Bounty:** Not specified
- **Severity:** Critical
- **Vuln types:** Cross-Site Scripting (XSS), Unsafe DOM Manipulation, Client-Side Code Injection, Improper Input Validation
- **Category:** uncategorised
- **Writeup:** https://www.nullpt.rs/hacking-gta-servers-using-web-exploitation

## Summary
A critical XSS vulnerability was discovered in the rcore_radiocar resource on FiveM servers, where user-supplied URLs for music playback are directly appended to the DOM without sanitization. An attacker can craft malicious URLs containing JavaScript payloads to execute arbitrary code on connected players' machines. This allows for account compromise, credential theft, and further system exploitation.

## Attack scenario (step by step)
1. Attacker identifies a FiveM server running the vulnerable rcore_radiocar resource via the public server list
2. Attacker joins the server and accesses the music broadcast feature
3. Attacker crafts a malicious URL containing an XSS payload (e.g., using img onerror handler) instead of a legitimate YouTube/SoundCloud link
4. Attacker broadcasts the malicious URL, which is stored server-side and transmitted to nearby players
5. Victim players' clients receive the URL and append it directly to DOM via vulnerable jQuery append()
6. Attacker's JavaScript payload executes in victim's context with full client-side access, enabling credential harvesting, account takeover, or further exploitation

## Root cause
The rcore_radiocar resource fails to validate and sanitize user-supplied URLs before appending them directly to the DOM using jQuery's append() function. The code path for non-YouTube URLs treats the input as trusted data without any HTML encoding or Content Security Policy protection.

## Attacker mindset
An attacker exploiting this vulnerability would seek to compromise FiveM players for credential theft, account hijacking, or lateral movement into gaming accounts/communities. The public nature of server lists makes this vulnerability easily discoverable and weaponizable at scale across multiple servers.

## Defensive takeaways
- Always validate and sanitize user input before DOM manipulation; use textContent instead of append() for user-supplied data
- Implement URL validation using allowlist approaches for media sources (e.g., only permit specific domains)
- Use HTML encoding functions or frameworks with auto-escaping to prevent XSS
- Implement Content Security Policy (CSP) headers to restrict script execution
- Use security linters and static analysis tools to detect unsafe DOM operations during development
- For third-party resources, implement sandboxing and permission models to limit attack surface
- Conduct security code reviews for community-created game mods before deployment
- Disable or restrict CEF Remote Debugging interface in production environments

## Variant hunting
Search for other FiveM resources that accept user-supplied URLs for media playback, streaming, or image display. Investigate any resource that dynamically constructs HTML or URLs from player input. Look for similar patterns in other game modding frameworks (Garry's Mod, Roblox, Minecraft servers) that expose web-based UI layers to user input.

## MITRE ATT&CK
- T1190
- T1203
- T1059
- T1059.007
- T1566
- T1566.002

## Notes
This vulnerability demonstrates the risks of combining web technologies (JavaScript, DOM APIs) with gaming platforms. The attacker leveraged CEF Remote Debugging (localhost:13172) to inspect client-side source code of paid resources, showing how even closed-source mods can be analyzed. The attack is particularly dangerous because it operates at the application level below traditional game anti-cheat systems. FiveM's architecture of isolated iframes per resource provides some segmentation but does not protect against DOM-based XSS within a resource's context.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-28*
