# Drag Drop XSS in Google Docs Drawing Module

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-15
- **Author:** Various
- **Program:** Google (Google Docs/Sheets/Drawing/Presentation)
- **Bounty:** Not specified in writeup
- **Severity:** High
- **Vuln types:** Stored XSS, Input Validation Bypass, Insufficient Sanitization
- **Category:** web-api
- **Writeup:** https://blog.yappare.com/2016/04/drag-drop-xss-in-google.html

## Summary
A stored XSS vulnerability was discovered in Google Docs Drawing module where users could drag and drop HTML files containing XSS payloads. The vulnerability exploited improper validation of image sources by leveraging onerror event handlers on broken image tags that would execute when the image failed to load on the victim's side.

## Attack scenario (step by step)
1. Attacker creates an HTML file containing an img tag with an XSS payload: <img src=nonvalid.jpg onerror=alert(0)>
2. Attacker shares a document with the victim or embeds the payload in a collaborative Google Doc
3. Victim drags and drops the HTML file or content into the Drawing module within Google Docs
4. The Drawing module accepts the payload and uploads it, treating it as a potential image
5. The image source is broken/invalid on the victim's side, triggering the onerror event
6. The JavaScript payload executes in the victim's browser within the Google Docs context

## Root cause
The Drawing module only validated the presence of image-like content but failed to properly sanitize or escape HTML event handlers. The validation logic did not account for onerror handlers being triggered when images fail to load. Additionally, the module did not escape or remove event attributes from image tags before storing and rendering the content.

## Attacker mindset
The researcher demonstrated sophisticated understanding of Google's validation mechanisms by observing different server responses for valid vs. invalid images. Rather than using common event handlers like onload or onmouseover, they specifically identified onerror as the viable vector. The use of Windows Sample Pictures as a legitimate-looking image reference shows tactical thinking to make payloads appear benign initially.

## Defensive takeaways
- Implement strict Content Security Policy (CSP) to prevent inline script execution
- Sanitize all user-uploaded content using allowlist-based HTML parsers (e.g., DOMPurify, Bleach)
- Remove all event handler attributes (on*) from HTML elements regardless of source
- Validate file uploads by magic bytes/file signatures rather than extensions or content inspection alone
- Apply server-side sanitization consistently across all modules, not just primary features
- Implement context-aware encoding for all user-controlled data in DOM operations
- Use iframe sandboxing with restrictive permissions for untrusted content rendering
- Conduct security reviews across all less-tested modules (like Drawing) with same rigor as primary features

## Variant hunting
Look for similar drag-drop functionality in other Google applications (Forms, Slides). Test other event handlers (onload, onmouseover, onmousemove, oninput, onchange, onpaste) in various Google modules. Explore if similar validation bypasses exist in file upload features. Test cross-origin image references and blob URLs to trigger error conditions. Investigate if the vulnerability exists in Google Images, Photos, or Drive's thumbnail generation.

## MITRE ATT&CK
- T1190
- T1598
- T1566

## Notes
The researcher noted that this was a duplicate submission for Google Images but appears to be novel for the Drawing module specifically. The write-up credits Dr. Mario Heiderich's earlier research on copy-paste XSS vectors and Harry's prior Google Docs XSS discovery. The key innovation was identifying that the specific module didn't implement the same fixes as other Google Docs components. The vulnerability demonstrates how feature-specific modules can regress on security compared to main features.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-15*
