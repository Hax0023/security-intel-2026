# Hacking GTA V RP Servers Using Web Exploitation - FiveM CEF XSS Vulnerability

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-19
- **Author:** Various
- **Program:** FiveM (Third-party GTA V multiplayer mod)
- **Bounty:** Not specified
- **Severity:** critical
- **Vuln types:** Cross-Site Scripting (XSS), Unsafe DOM Manipulation, Client-Side Code Injection, CEF Remote Debugging Exposure
- **Category:** uncategorised
- **Writeup:** https://www.nullpt.rs/hacking-gta-servers-using-web-exploitation

## Summary
FiveM's rcore_radiocar resource is vulnerable to stored XSS through improper sanitization of user-supplied URLs. Attackers can inject malicious JavaScript payloads via crafted music URLs, which are unsafely appended to the DOM using jQuery's append() function without sanitization. This allows arbitrary code execution on connected players' machines with access to sensitive game and system data.

## Attack scenario (step by step)
1. Attacker identifies rcore_radiocar resource on a FiveM roleplay server via the public server list
2. Attacker crafts a malicious XSS payload using an img tag with onerror handler, disguised as a music URL
3. Attacker or another player submits the payload URL to the resource's music broadcast feature
4. The vulnerable create() function extracts the URL and appends it directly to the DOM via jQuery without sanitization
5. The onerror event triggers, executing the attacker's JavaScript payload in the victim player's context
6. Attacker gains arbitrary code execution capability to exfiltrate player IPs, account data, or perform further attacks

## Root cause
The rcore_radiocar resource fails to sanitize user-supplied URLs before inserting them into the DOM. Specifically, the line `$('body').append('<div id="' + this.div_id + '" style="display:none">' + this.getUrlSound() + '</div>')` directly concatenates unsanitized user input into HTML, bypassing XSS protections. The fallback logic for non-YouTube URLs trusts the input implicitly.

## Attacker mindset
An attacker discovers that user-controlled input (music URLs) is reflected in the DOM without validation. Recognizing the common pattern of unsafe string concatenation in jQuery, they craft a proof-of-concept XSS payload using an img tag's onerror handler, which is a well-known bypass technique for catching injection points. The attacker leverages the public nature of FiveM servers and resource introspection via CEF debugging to identify vulnerable resources at scale.

## Defensive takeaways
- Always sanitize and validate user input before DOM insertion; use textContent or innerText instead of innerHTML/append with raw strings
- Implement Content Security Policy (CSP) headers to restrict script execution sources
- Use URL parsing and validation libraries (e.g., URL constructor) to validate music URLs against whitelisted domains (YouTube, SoundCloud only)
- Employ parameterized DOM methods: use createElement() and setAttribute() instead of string concatenation
- Disable or restrict CEF Remote Debugging in production environments (only enable on localhost for development)
- Implement server-side validation and sanitization of all resource inputs
- Apply security audits and code reviews for third-party resources, especially paid ones with wider distribution
- Use security linters and static analysis tools to detect unsafe DOM manipulation patterns

## Variant hunting
Similar XSS vulnerabilities likely exist in other FiveM resources that accept user-supplied URLs or text (job applications, advertisements, custom UI forms). Resources handling player input via NUI callbacks without sanitization are high-risk targets. The CEF debugging interface could expose vulnerable patterns in other resources; scan for jQuery append() calls with unsanitized variables and eval() usage in resource scripts.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1059 - Command and Scripting Interpreter (JavaScript)
- T1005 - Data from Local System
- T1041 - Exfiltration Over C2 Channel
- T1566 - Phishing
- T1204 - User Execution

## Notes
The vulnerability demonstrates the risks of client-side modding ecosystems with inadequate security controls. The attacker's methodology of leveraging public server lists and CEF debugging to identify and exploit resources is systematic and scalable. The initial discovery (IP leakage via URL requests) provided reconnaissance for deeper exploitation. This highlights the importance of securing third-party extension ecosystems and the difficulty of patching distributed, user-installed mods. The writeup is incomplete (ends mid-payload description) but the XSS vulnerability is clearly demonstrated.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-19*
