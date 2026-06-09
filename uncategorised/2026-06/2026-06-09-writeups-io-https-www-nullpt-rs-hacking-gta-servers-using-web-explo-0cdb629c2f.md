# Hacking GTA V RP Servers Using Web Exploitation Techniques

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-09
- **Author:** Various
- **Program:** FiveM (Grand Theft Auto V Multiplayer Mod)
- **Bounty:** Not specified
- **Severity:** Critical
- **Vuln types:** Cross-Site Scripting (XSS), Unsafe DOM Manipulation, Client-Side Code Injection, Insufficient Input Validation
- **Category:** uncategorised
- **Writeup:** https://www.nullpt.rs/hacking-gta-servers-using-web-exploitation

## Summary
A critical XSS vulnerability was discovered in the rcore_radiocar FiveM resource that allows attackers to execute arbitrary JavaScript on players' machines by injecting malicious URLs into the music player interface. The vulnerability stems from unsafe DOM manipulation using jQuery's append() function without proper input sanitization or encoding. This enables full client-side compromise of GTA V RP server players.

## Attack scenario (step by step)
1. Attacker identifies the rcore_radiocar resource on a public FiveM server using the server list aggregator
2. Attacker crafts a malicious URL containing XSS payload (e.g., img tag with onerror event handler) instead of a valid YouTube or audio URL
3. Attacker specifies this payload URL in the music player interface to broadcast 'music' from their car
4. When other players connect or are within range, the resource attempts to parse the URL and fails to extract a YouTube ID
5. The vulnerable code appends the unescaped URL directly to the DOM using jQuery append(), triggering the onerror event handler
6. Arbitrary JavaScript payload executes in the victim player's browser context, potentially exfiltrating data, stealing credentials, or compromising the game client

## Root cause
The rcore_radiocar resource fails to sanitize or escape user-supplied URL input before inserting it into the DOM. Specifically, the code: `$('#' + this.div_id).append('<div>'+this.getUrlSound()+'</div>')` directly concatenates unsanitized user input into HTML without using safe DOM construction methods or encoding special characters. No Content Security Policy or input validation is implemented.

## Attacker mindset
Opportunistic attacker targeting widespread gaming infrastructure; recognizes that user-generated content in game mods often lacks security review; leverages CEF remote debugging to reverse-engineer paid resources without authorization; understands that players trust curated server resources and will be highly susceptible to client-side attacks; aims to compromise player accounts, steal credentials, or inject malware into gaming communities.

## Defensive takeaways
- Implement strict input validation on all user-supplied URLs - whitelist expected URL patterns and reject suspicious inputs
- Use safe DOM manipulation methods (e.g., textContent, createElement) instead of string concatenation with append()
- Always HTML-encode or escape special characters when inserting user input into HTML context
- Implement Content Security Policy (CSP) headers to prevent inline script execution and restrict script sources
- Conduct security code reviews for all user-facing resources, especially those handling external content
- Disable or restrict CEF remote debugging in production environments to prevent resource reverse-engineering
- Implement server-side validation and URL parsing before sending content to clients
- Use security-focused templating engines that escape output by default (Vue.js has some protections but manual DOM manipulation bypasses them)
- Educate server administrators about resource security vetting before deployment

## Variant hunting
['Search for other FiveM resources using jQuery append() or similar unsafe DOM manipulation with user-controlled data (NUI callbacks, form inputs, server data)', 'Identify resources handling URLs, file uploads, or external content without proper sanitization', 'Test audio/media player resources that accept user input for XSS vulnerabilities', 'Examine resources with CEF remote debugging enabled for data exfiltration or credential theft capabilities', 'Review chat systems, nickname handlers, and other player-controlled text fields for reflected/stored XSS', 'Analyze resources communicating with third-party APIs for Server-Side Request Forgery (SSRF) or injection attacks', 'Test for vulnerabilities in resource loading mechanisms that could allow malicious resource installation']

## MITRE ATT&CK
- T1190
- T1071
- T1059
- T1566
- T1204

## Notes
The researcher discovered this vulnerability through methodical resource enumeration on public FiveM servers. The CEF remote debugging interface on localhost:13172 was instrumental in reverse-engineering the paid resource without source code access. This demonstrates how gaming platforms with custom scripting engines can become attractive targets for web-exploitation techniques traditionally associated with web applications. The vulnerability has widespread impact due to the popularity of roleplay servers and the trusted nature of curated server resources. No evidence of formal bug bounty program is mentioned, suggesting this may be a vulnerability disclosure without official coordination.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-09*
