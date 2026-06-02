# Hacking GTA V RP Servers Using Web Exploitation Techniques

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-02
- **Author:** Various
- **Program:** FiveM/rcore_radiocar resource (GTA V RP servers)
- **Bounty:** Not specified
- **Severity:** critical
- **Vuln types:** Cross-Site Scripting (XSS), Improper Input Validation, DOM-based XSS, Arbitrary Code Execution
- **Category:** uncategorised
- **Writeup:** https://www.nullpt.rs/hacking-gta-servers-using-web-exploitation

## Summary
The rcore_radiocar FiveM resource fails to sanitize user-supplied audio URLs before appending them to the DOM, enabling DOM-based XSS attacks. Attackers can inject malicious payloads through crafted URLs that execute arbitrary JavaScript in the context of connected players' browsers, potentially leading to account compromise, credential theft, and lateral movement across FiveM servers.

## Attack scenario (step by step)
1. Attacker identifies rcore_radiocar resource on a target FiveM roleplay server via the public server listing
2. Attacker connects to the server and accesses the music broadcast feature that accepts YouTube/SoundCloud/arbitrary audio URLs
3. Attacker crafts a malicious URL payload containing a non-YouTube link with embedded JavaScript (e.g., using img onerror attribute) designed to evade YouTube ID extraction
4. The vulnerable code fails to validate/sanitize the URL and appends it directly to DOM via jQuery append(), triggering XSS execution
5. Malicious JavaScript executes in player's CEF context with access to NUI callbacks, allowing exfiltration of game data, player IPs, or execution of further exploits
6. Attacker can establish persistence or escalate to compromise the FiveM server infrastructure or player accounts

## Root cause
The SoundPlayer.js create() function performs insufficient URL validation by only attempting YouTube ID extraction. Non-YouTube URLs bypass validation and are directly concatenated into DOM via jQuery's append() method without HTML encoding, sanitization, or Content Security Policy enforcement. The CEF debugging interface also exposed resource source code to local inspection.

## Attacker mindset
Researcher systematically enumerated public FiveM servers seeking resources with user input handling, identified a paid resource through public listings, and leveraged CEF remote debugging (exposed on localhost:13172) to reverse-engineer source code without authorization. Recognized DOM append pattern as classic XSS vector and crafted polyglot payloads to bypass basic YouTube URL detection.

## Defensive takeaways
- Implement strict URL validation using URL parsing APIs rather than regex; whitelist only approved domains or use iframe sandboxing with restrictive CSP
- Sanitize all user input before DOM insertion using textContent instead of innerHTML/append, or use DOMPurify/similar libraries
- Enforce Content Security Policy headers to prevent inline script execution and restrict script sources
- Disable CEF remote debugging in production environments or restrict access to authorized users only
- Apply defense-in-depth: validate on both client and server-side; use server-side URL verification before serving to clients
- Implement security review process for user-facing resources, especially paid/popular ones with high exposure
- Use automated AST analysis or SAST tooling to detect dangerous patterns like unsanitized append() calls
- Consider using a resource signing/verification mechanism to prevent tampering with resource code

## Variant hunting
Search for similar patterns in FiveM resources: (1) Other audio/streaming resources (music players, radio, jukebox) accepting user URLs, (2) Resources displaying user-generated content (chat systems, billboards, neon signs), (3) Any resource using jQuery append/html with user input without sanitization, (4) Resources with URL parameters in iframe src attributes, (5) Resources accepting player-supplied media links for thumbnails/images, (6) Custom UI frameworks in FiveM resources that mirror vulnerable patterns

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1047: Windows Management Instrumentation
- T1566.002: Phishing - Spearphishing Link
- T1204.001: User Execution - Malicious Link
- T1059.007: Command and Scripting Interpreter - JavaScript
- T1083: File and Directory Discovery
- T1040: Traffic Sniffing
- T1557.001: Man-in-the-Middle - ARP Cache Poisoning

## Notes
The vulnerability chain demonstrates risks in gaming mod ecosystems where resources are user-developed, often proprietary (paid), and leverage embedded browser engines (CEF) with insufficient isolation. The public CEF debugging interface significantly lowered the barrier to reverse-engineering paid resources. FiveM's NUI callback architecture creates additional risk surface for cross-context exploitation. Real-world impact includes player IP leakage (noted in initial reconnaissance), credential theft via phishing redirects, malware distribution, and potential server compromise if resources have elevated privileges. The research highlights need for ecosystem-wide security guidelines and automated scanning of resource marketplaces.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-02*
