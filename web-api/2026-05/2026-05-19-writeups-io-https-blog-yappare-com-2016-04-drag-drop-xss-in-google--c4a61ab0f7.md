# Drag Drop XSS in Google Docs Drawing Module

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-19
- **Author:** Various
- **Program:** Google Bug Bounty (Google Docs/Sheets/Drawing/Presentation)
- **Bounty:** Not specified in writeup
- **Severity:** High
- **Vuln types:** Stored XSS, Improper Input Validation, Client-side Code Execution
- **Category:** web-api
- **Writeup:** https://blog.yappare.com/2016/04/drag-drop-xss-in-google.html

## Summary
A stored XSS vulnerability was discovered in Google Docs' Drawing module that allowed attackers to execute arbitrary JavaScript by dragging and dropping specially crafted HTML files containing image tags with onerror event handlers. The vulnerability exploited improper HTML validation when processing drag-and-drop content, specifically when images failed to load from invalid or inaccessible sources.

## Attack scenario (step by step)
1. Attacker creates an HTML file containing a malicious img tag with onerror handler: <img src=nonvalid.jpg onerror=alert(0)>
2. Attacker crafts the payload to reference a valid image path (e.g., C:\Users\Public\Pictures\Sample Pictures) that exists locally but cannot be accessed by the web context
3. Victim opens Google Docs and accesses the Drawing module
4. Attacker tricks victim into dragging and dropping the malicious HTML file into the Drawing canvas
5. Google Docs accepts the payload as an image element, but the image fails to load due to invalid source
6. The onerror event handler executes, triggering arbitrary JavaScript in the victim's Google Docs session

## Root cause
The Drawing module in Google Docs/Sheets/Presentation failed to properly validate and sanitize HTML content when processing drag-and-drop operations. The application parsed img tags without removing dangerous event handlers (onerror, onload, onmouseover), and the validation logic only checked for valid image sources rather than sanitizing the HTML markup itself. This allowed event handlers to execute when images failed to load.

## Attacker mindset
The researcher demonstrated sophisticated payload engineering by understanding that only onerror handlers would execute (not onload or onmouseover), and then creatively leveraged Windows system image paths that would be valid file references but inaccessible in the web context, causing the image to fail and trigger the error handler.

## Defensive takeaways
- Sanitize all HTML content from user input by removing event handlers (onclick, onerror, onload, onmouseover, etc.) regardless of origin
- Implement strict Content Security Policy (CSP) to prevent inline script execution and event handler execution
- Use allowlist-based validation for drag-and-drop operations, accepting only specific file types and MIME types
- Parse and validate images server-side before returning them to clients; never embed user-supplied HTML directly
- Apply HTML entity encoding or use DOM APIs that don't interpret HTML (textContent instead of innerHTML)
- Implement comprehensive input validation on both client and server side
- Use library functions designed for safe HTML parsing and sanitization (DOMPurify, etc.)

## Variant hunting
Similar vulnerabilities could exist in other Google products (Gmail, Blogger, Sites) that support drag-drop rich content insertion. Other collaborative editing platforms (Microsoft Office 365, Notion, Confluence) should be tested for similar drag-drop XSS vectors. The technique of using event handlers with invalid image sources could apply to any system that processes HTML from untrusted sources without proper sanitization.

## MITRE ATT&CK
- T1190
- T1566
- T1566.002

## Notes
This vulnerability was discovered in late 2015, with a similar issue previously found by Harry in Google Docs (resolved). The researcher's submission was marked as a duplicate of another researcher's finding but in a different Google product (not Google Images). The vulnerability demonstrates the importance of comprehensive sanitization across all features of a product, as similar issues can persist in different modules despite being patched in one area.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-19*
