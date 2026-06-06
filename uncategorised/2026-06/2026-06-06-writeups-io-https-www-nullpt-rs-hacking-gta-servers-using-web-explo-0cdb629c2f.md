# Hacking GTA V RP Servers Using Web Exploitation Techniques

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-06
- **Author:** Various
- **Program:** FiveM/GTA V RP Servers (Bug Bounty Context Unclear)
- **Bounty:** Not specified
- **Severity:** critical
- **Vuln types:** Cross-Site Scripting (XSS), Improper Input Validation, Code Injection, Unsafe DOM Manipulation
- **Category:** uncategorised
- **Writeup:** https://www.nullpt.rs/hacking-gta-servers-using-web-exploitation

## Summary
A critical reflected XSS vulnerability was discovered in the rcore_radiocar FiveM resource that allows players to specify arbitrary URLs for music playback. The resource fails to sanitize user-supplied URLs before appending them to the DOM, enabling attackers to inject malicious JavaScript payloads that execute in the context of other players' browsers. This vulnerability enables remote code execution on victim machines through crafted malicious URLs.

## Attack scenario (step by step)
1. Attacker identifies the rcore_radiocar resource on a public FiveM server that allows custom music URLs
2. Attacker analyzes the resource code using CEF Remote Debugging interface exposed on localhost:13172
3. Attacker discovers the SoundPlayer.js create() function uses jQuery append() without sanitization on user-controlled URL input
4. Attacker crafts an XSS payload using malformed img tag with onerror handler (e.g., <img src=x onerror="fetch and eval malicious script">)
5. Attacker shares the malicious URL with victims or broadcasts it on the server's music system
6. Victim's browser executes the injected JavaScript, granting attacker code execution capabilities on victim's machine

## Root cause
The resource implements unsafe DOM manipulation by directly appending unsanitized user input to the DOM using jQuery's append() method. The developer relied on URL parsing to identify YouTube links but failed to properly sanitize alternative URLs before treating them as safe content, violating the principle of input validation and output encoding.

## Attacker mindset
An attacker could exploit this vulnerability to steal player credentials, capture network traffic, perform credential harvesting, inject malware, hijack game accounts, or use compromised machines as part of a botnet. The attack surface is particularly attractive because it targets a large player base with minimal technical knowledge of web security.

## Defensive takeaways
- Always sanitize and validate user input before DOM manipulation; use textContent instead of append() for untrusted data
- Implement Content Security Policy (CSP) headers to restrict script execution sources
- Use established sanitization libraries (DOMPurify, OWASP HTML Sanitizer) rather than custom validation logic
- Apply allowlist-based validation for URLs; only permit whitelisted domains (YouTube, SoundCloud) rather than accepting arbitrary URLs
- Encode output appropriately for the context (HTML encoding, JavaScript encoding, URL encoding)
- Implement subresource integrity (SRI) checks for external resources
- Regular security audits of third-party resources and paid scripts with source code review
- Use iframe sandboxing to limit blast radius of compromised resources

## Variant hunting
Search for similar patterns in other FiveM resources: (1) Any resource accepting user URLs without validation, (2) DOM manipulation using append/innerHTML with unsanitized input, (3) Audio/media players that accept arbitrary sources, (4) Custom UI frameworks in FiveM that handle user-controlled data, (5) Other paid resources from the same developer, (6) Resources handling embeds, links, or user-generated content

## MITRE ATT&CK
- T1190
- T1203
- T1566
- T1204
- T1059

## Notes
This writeup demonstrates a real-world vulnerability in gaming infrastructure. The exposure of CEF Remote Debugging interface was critical to discovering the vulnerability. The attack is particularly dangerous because FiveM players may not expect web-based vulnerabilities in a game context. The vulnerability affects not just the attacker's own client but can propagate to other players through the shared music broadcast mechanic, making it a network-amplified attack vector.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-06*
