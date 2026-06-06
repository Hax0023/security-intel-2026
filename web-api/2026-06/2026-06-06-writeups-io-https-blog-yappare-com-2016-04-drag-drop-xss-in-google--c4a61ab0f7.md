# Drag Drop XSS in Google Docs Drawing Module

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-06
- **Author:** Various
- **Program:** Google Bug Bounty
- **Bounty:** Not specified in writeup
- **Severity:** High
- **Vuln types:** Stored XSS, Improper Input Validation, Client-side Code Injection
- **Category:** web-api
- **Writeup:** https://blog.yappare.com/2016/04/drag-drop-xss-in-google.html

## Summary
A stored XSS vulnerability was discovered in Google Docs/Sheets/Drawing/Presentation modules where users could drag and drop malicious HTML files containing XSS payloads. The vulnerability exploited improper validation of dropped content and the onerror event handler on broken image sources to execute arbitrary JavaScript.

## Attack scenario (step by step)
1. Attacker crafts an HTML file containing an img tag with a valid image source initially loaded in the user's system (e.g., from C:\Users\Public\Pictures\Sample Pictures)
2. Attacker hosts or provides this HTML file to the victim
3. Victim's browser initially loads the image successfully, establishing trust
4. Victim drags and drops the HTML file into Google Docs Drawing module
5. Google Docs processes the dropped content and attempts to embed the image, but the source becomes invalid/broken in the new context
6. The onerror event handler executes, triggering the malicious JavaScript payload (e.g., alert(0) or more serious attacks)

## Root cause
The drawing module only validated that content appeared to be a valid image without properly sanitizing HTML event handlers. The validation failed to account for: (1) images that would be broken after being imported into Google's environment, (2) embedded event handlers like onerror in img tags, and (3) the execution context of dropped content from local file systems.

## Attacker mindset
The attacker demonstrated sophisticated understanding of browser behavior and file handling mechanics. By leveraging locally available image paths that would initially load but break upon import, they bypassed simple image validation. The choice of onerror over onload/onmouseover showed methodical testing and payload optimization for the specific vulnerability condition.

## Defensive takeaways
- Sanitize all HTML content from user uploads, not just validate file types or image sources
- Strip all event handlers (onerror, onload, onclick, etc.) from img tags and other HTML elements during import
- Implement Content Security Policy (CSP) headers to restrict inline script execution
- Validate image sources comprehensively and handle broken images without executing associated event handlers
- Apply whitelist-based HTML parsing rather than blacklist-based filtering
- Test cross-context behavior where local resources become unavailable in cloud environments
- Implement server-side validation and re-encoding of dropped content

## Variant hunting
Similar drag-drop XSS patterns likely exist in: (1) other Google products with document import features (Slides, Forms), (2) other cloud office suites (Microsoft 365, Zoho), (3) embedded media handling in wikis and collaboration tools, (4) using different event handlers (ontouchstart, onwheel, onscroll), (5) other HTML tags accepting src attributes (script, iframe, source), (6) SVG elements with embedded event handlers

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1587: Develop Capabilities - Malware/Payload Development
- T1566: Phishing - Spearphishing Attachment

## Notes
The vulnerability was partially duplicated but the researcher found it existed in Google Images when initial findings were in Drawing module. The write-up highlights creative payload engineering using system resource availability to bypass validation checks. This is a good example of understanding application behavior differences between local and cloud contexts.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-06*
