# Hacking GTA V RP Servers Using Web Exploitation - FiveM XSS and CEF Debugging

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-18
- **Author:** Various
- **Program:** FiveM (GTA V Multiplayer Mod) / rcore_radiocar resource
- **Bounty:** Unknown/Not specified
- **Severity:** critical
- **Vuln types:** Cross-Site Scripting (XSS), Improper Input Validation, Client-Side Code Injection, Insecure CEF Remote Debugging Exposure
- **Category:** uncategorised
- **Writeup:** https://www.nullpt.rs/hacking-gta-servers-using-web-exploitation

## Summary
A critical XSS vulnerability exists in the rcore_radiocar FiveM resource that allows attackers to execute arbitrary JavaScript on players' machines by crafting malicious URLs. The vulnerability stems from unsanitized user input being directly appended to the DOM via jQuery's append() function without proper escaping or validation.

## Attack scenario (step by step)
1. Attacker identifies the rcore_radiocar resource on a FiveM roleplay server which allows custom audio URLs
2. Attacker crafts a malicious XSS payload disguised as an audio URL containing an img tag with onerror handler
3. Attacker either invites victims to join the server, joins a server where victims are playing, or tricks them into using the malicious URL
4. When the victim's client attempts to load the 'audio' resource, the JavaScript extracts the payload and appends it to the DOM
5. The img tag fails to load, triggering the onerror event handler which fetches and executes attacker-controlled JavaScript via eval()
6. Attacker gains arbitrary code execution on victim's FiveM client, potentially exfiltrating data, stealing credentials, or manipulating game state

## Root cause
The rcore_radiocar resource fails to validate or sanitize user-supplied URLs before directly inserting them into the DOM using jQuery's append() function. The code checks if a URL is a YouTube link but provides no protection for non-YouTube URLs, allowing injection of arbitrary HTML/JavaScript. The SoundPlayer.js create() function concatenates the unsanitized URL directly into a div element without HTML escaping.

## Attacker mindset
An attacker targets widely-used FiveM resources to maximize impact across multiple servers and players. By leveraging the CEF Remote Debugging interface to reverse-engineer paid resources, attackers can identify vulnerable code paths. The use of img onerror tricks to bypass simple filters and eval() to load larger payloads shows sophisticated evasion techniques. The attacker recognizes that FiveM's client-side architecture and reliance on web technologies (JavaScript, HTML, CEF) creates a large attack surface.

## Defensive takeaways
- Always sanitize and validate user input before inserting into the DOM; use textContent or innerText instead of innerHTML/append() for untrusted data
- Implement a strict whitelist of allowed URL schemes (https only) and validate URLs against expected domains
- Use Content Security Policy (CSP) headers to restrict script execution and prevent eval() usage
- Apply HTML escaping/encoding to all user-supplied data before DOM insertion
- Disable or restrict CEF Remote Debugging in production environments (only enable for development with access controls)
- Implement server-side validation and sanitization of resource URLs before sending to clients
- Use parameterized/safe APIs like new URL() to parse URLs rather than regex patterns
- Apply principle of least privilege to resource permissions and restrict what resources can execute
- Regular security audits of third-party resources, especially paid ones with closed source code

## Variant hunting
Similar vulnerabilities likely exist in other FiveM resources that accept user-supplied URLs or external data, particularly those handling music players, image galleries, external links, or API integrations. Resources using direct DOM manipulation (innerHTML, append, insertAdjacentHTML) with user input are high-priority targets. The same XSS pattern could affect resources handling vehicle customization URLs, character customization links, or server configuration parameters. CEF Remote Debugging exposure is a systemic issue affecting all FiveM installations, enabling reconnaissance and reverse-engineering of any resource.

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1566: Phishing
- T1059: Command and Scripting Interpreter
- T1203: Exploitation for Client Execution
- T1548: Abuse Elevation Control Mechanism
- T1041: Exfiltration Over C2 Channel
- T1005: Data from Local System

## Notes
This vulnerability demonstrates how game modding frameworks that rely on web technologies can inherit traditional web security vulnerabilities at scale. The CEF Remote Debugging interface on localhost:13172 is a significant security control bypass that allows attackers to inspect and reverse-engineer any resource. The writeup is incomplete (cuts off mid-payload), but clearly describes a working XSS exploit. The attack is particularly severe in roleplay communities where players may be incentivized to use server-recommended resources. The combination of client-side code execution and access to game state creates risk for account compromise, data theft, and griefing attacks on the game server and other players.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-18*
