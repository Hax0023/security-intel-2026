# Drag Drop XSS in Google Docs Drawing Module

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-17
- **Author:** Various
- **Program:** Google Bug Bounty (Google Docs/Sheets/Drawing/Presentation)
- **Bounty:** Not specified in writeup
- **Severity:** High
- **Vuln types:** Stored XSS, Input Validation Bypass, Improper File Upload Handling
- **Category:** web-api
- **Writeup:** https://blog.yappare.com/2016/04/drag-drop-xss-in-google.html

## Summary
A stored XSS vulnerability was discovered in Google Docs/Sheets drawing module through drag-and-drop functionality. By crafting an HTML file containing an image tag with an onerror XSS payload and dragging it into the drawing module, the malicious script would execute when the broken image triggered the error handler. The vulnerability bypassed validation by leveraging local file paths that would be inaccessible in the Google environment, causing the image to fail loading and execute the payload.

## Attack scenario (step by step)
1. Attacker creates an HTML file containing <img src=nonvalid.jpg onerror=alert(0)> or similar payload
2. Attacker uses a valid local image path (e.g., C:\Users\Public\Pictures\Sample Pictures) that exists on Windows systems but is inaccessible from Google's servers
3. Victim opens the HTML file locally and drags it into Google Docs/Sheets drawing module
4. Google's drawing module accepts the file and processes the image tag without proper sanitization
5. When Google attempts to load the image source, it fails (broken image)
6. The onerror event handler executes, delivering the XSS payload to the victim's browser

## Root cause
The drawing module implemented insufficient HTML sanitization when processing drag-dropped files. It validated the presence of valid image sources but failed to strip or sanitize event handlers (onerror, onload, etc.) from image tags. The validation logic accepted any image tag structure without removing dangerous attributes, and the reliance on image loading failures to trigger error handlers was not anticipated.

## Attacker mindset
The attacker recognized that different file formats (OpenOffice, HTML) could be leveraged through drag-drop mechanisms. By understanding that Google's module would attempt to load any referenced image, the attacker deliberately used paths that would fail in the Google environment, ensuring the onerror handler would execute. This demonstrates creative exploitation of the gap between local file accessibility and web-based execution contexts.

## Defensive takeaways
- Implement strict HTML sanitization on all user-supplied content, including drag-dropped files
- Strip or disable all event handler attributes (onerror, onload, onmouseover, etc.) from HTML elements
- Use allowlists rather than denylists for permissible HTML tags and attributes in rich content editors
- Validate file MIME types and content on the server side, not just client side
- Sandbox drag-drop processing in contexts that prevent script execution
- Apply Content Security Policy (CSP) headers to mitigate XSS impact
- Test drag-drop functionality with malicious payloads as part of security testing
- Educate users about the risks of dragging untrusted files into web applications

## Variant hunting
Similar vulnerabilities likely exist in other Google products with rich editors (Gmail, Google Sites). Other web-based drawing/design tools and collaborative platforms may have identical issues. Research drag-drop handling in other office suites (Microsoft 365, Notion, Figma). Test any paste/import functionality that processes HTML or rich content without proper sanitization. Investigate whether other event handlers (onload, onmouseover, onmouseenter) can be exploited through similar broken resource scenarios.

## MITRE ATT&CK
- T1190
- T1566.002
- T1589.001

## Notes
The researcher noted this was later submitted as a duplicate by another researcher, but in a different Google product (Google Images vs. Google Docs). The vulnerability chain is subtle: it depends on the convergence of three factors - drag-drop acceptance, inadequate HTML sanitization, and reliance on error handlers for execution. The use of local file paths as a trigger mechanism is particularly clever, as it bypasses server-side image verification while ensuring failure in the victim's browser context.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-17*
