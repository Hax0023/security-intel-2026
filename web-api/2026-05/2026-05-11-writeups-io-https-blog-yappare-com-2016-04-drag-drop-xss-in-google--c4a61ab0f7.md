# Drag-and-Drop XSS in Google Docs Drawing Module via Broken Image onerror Handler

## Metadata
- **Source:** writeups.io
- **Date:** 
- **Author:** Various
- **Program:** Google (Google Docs/Sheets/Drawing/Presentations)
- **Bounty:** Unknown (marked as duplicate)
- **Severity:** high
- **Vuln types:** Stored XSS, Improper Input Validation, File Upload Vulnerability
- **Category:** web-api
- **Writeup:** https://blog.yappare.com/2016/04/drag-drop-xss-in-google.html

## Summary
A stored XSS vulnerability was discovered in Google's Drawing module (part of Docs/Sheets/Presentations) that allowed attackers to execute arbitrary JavaScript by drag-and-dropping HTML files containing malicious image tags. The vulnerability exploited improper HTML validation combined with the onerror event handler of broken image references, enabling XSS execution when images failed to load.

## Attack scenario (step by step)
1. Attacker creates an HTML file containing an img tag with a non-existent image source and JavaScript payload in the onerror handler: <img src=nonvalid.jpg onerror=alert(0)>
2. Attacker crafts the payload to reference a valid image from a common location (e.g., C:\Users\Public\Pictures\Sample Pictures) that exists on victim's system but becomes inaccessible when uploaded to Google's servers
3. Victim receives the malicious HTML file and drags it into the Google Drawing module
4. Google's Drawing module processes the drag-and-drop input without properly sanitizing HTML content
5. The image reference breaks when Google attempts to load the non-existent or inaccessible image source
6. The onerror event handler triggers, executing the embedded JavaScript payload in the victim's browser context

## Root cause
The Drawing module implementation failed to properly sanitize and validate HTML content during drag-and-drop operations. While Google's validation checked for valid images, it did not account for broken image references with event handlers, allowing onerror attributes to execute arbitrary code. The module's server-side validation only verified image validity without stripping dangerous HTML event handlers.

## Attacker mindset
The researcher demonstrated creative exploitation by recognizing that while drag-and-drop XSS was partially patched in Google Docs proper, the Drawing submodule was overlooked. They leveraged the onerror handler as an alternative to previously-patched event handlers (onload, onmouseover) and used local file system knowledge (Windows Sample Pictures directory) to ensure images would fail to load after upload, triggering the malicious payload.

## Defensive takeaways
- Implement comprehensive HTML sanitization using allowlist-based approaches (not blacklist) for all drag-and-drop file handling
- Strip all event handler attributes (onerror, onload, onmouseover, etc.) from user-supplied HTML content, not just common ones
- Apply consistent security policies across all modules and submodules; partially patched vulnerabilities in one module often exist in related modules
- Perform server-side validation of uploaded content to detect and remove or escape potentially dangerous HTML patterns
- Use Content Security Policy (CSP) headers to prevent inline script execution as a defense-in-depth measure
- Test drag-and-drop functionality with payloads targeting all event handlers, not just image-specific ones
- Maintain a shared security review process across feature teams to prevent similar vulnerabilities in parallel implementations

## Variant hunting
['Test drag-and-drop in other Google products (Google Slides, Google Forms) for similar HTML validation bypasses', 'Attempt other event handlers on different HTML tags (svg, object, embed tags with various handlers)', 'Test drag-and-drop with malformed/polyglot files that could bypass file type validation', 'Investigate whether similar bypasses exist in collaborative editing features where content is shared between users', 'Check if the vulnerability persists when dragging content from external sources vs. local files', 'Test whether the vulnerability affects different browser contexts (iframes, shadow DOM, etc.)']

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1598 - Phishing for Information
- T1566 - Phishing
- T1204 - User Execution

## Notes
This vulnerability is notable for its creative exploitation technique: identifying that while the primary XSS vector was patched, alternative event handlers and the drawing submodule were overlooked. The researcher's insight about using local system images to cause predictable failures demonstrates sophisticated attack planning. The submission was reportedly marked as a duplicate, suggesting another researcher may have independently discovered the same or similar issue. The vulnerability demonstrates the difficulty of achieving complete security when patching related issues across multiple modules and features.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-11*
