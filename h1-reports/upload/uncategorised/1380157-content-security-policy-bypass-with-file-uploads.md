# Content-Security Policy bypass with File Uploads in Rocket.Chat

## Metadata
- **Source:** HackerOne
- **Report:** 1380157 | https://hackerone.com/reports/1380157
- **Submitted:** 2021-10-25
- **Reporter:** gronke
- **Program:** Rocket.Chat
- **Bounty:** Not specified in provided content
- **Severity:** High
- **Vuln:** Content Security Policy (CSP) Bypass, Arbitrary File Upload, Cross-Site Scripting (XSS), HTML Injection
- **CVEs:** None
- **Category:** uncategorised

## Summary
Rocket.Chat's default CSP header prevents inline script execution, but this protection can be bypassed by uploading a JavaScript file and including it via script src attribute or iframe srcdoc. The file upload feature accepts JavaScript content-types without validation, allowing attackers to execute arbitrary code despite CSP restrictions.

## Attack scenario
1. Attacker identifies an HTML injection or XSS vulnerability in Rocket.Chat message handling
2. Attacker crafts a malicious JavaScript payload and uploads it via the file upload feature with content-type application/javascript or text/javascript
3. Attacker injects an iframe element with srcdoc attribute containing a script tag referencing the uploaded file: <iframe srcdoc="&#x3c;script src='/file-upload/<UPLOAD_ID>/payload.js?download'></script>">
4. The iframe's srcdoc attribute bypasses script tag filters applied to message content
5. Browser loads and executes the JavaScript payload from the uploaded file
6. Attacker achieves code execution despite CSP restrictions on unsafe-inline scripts

## Root cause
The application implements CSP to prevent inline script execution but fails to restrict the content-types accepted during file uploads. Additionally, message filters that remove script tags do not account for indirect execution vectors like iframe srcdoc attributes. The CSP policy lacks proper script-src directives to restrict script loading to trusted sources only.

## Attacker mindset
An attacker recognizes that while CSP blocks inline scripts, file upload functionality provides an alternative vector. By combining file upload with HTML injection and iframe srcdoc bypass techniques, they circumvent the security boundary. This demonstrates understanding that defense-in-depth failures can chain together, and that filters focusing on one element (script tags) may miss alternative constructs (iframes).

## Defensive takeaways
- Implement strict file type validation on uploads, blocking execution-capable content-types (application/javascript, text/javascript, application/x-javascript, etc.)
- Serve uploaded files with Content-Disposition: attachment and Content-Type: application/octet-stream headers to prevent browser interpretation as executable content
- Enforce CSP script-src directive to explicitly whitelist trusted sources and prevent loading scripts from arbitrary URLs, including user-uploaded file paths
- Filter or sanitize all HTML injection vectors including iframe, embed, object, and other frame-based elements from user-generated content
- Implement proper CSP with script-src 'none' or specific trusted origins rather than relying solely on unsafe-inline restrictions
- Apply multi-layer validation: validate file types at upload, enforce strong CSP headers, and sanitize HTML output comprehensively
- Use a security-focused HTML sanitizer library that understands CSP-bypass techniques and removes dangerous constructs holistically

## Variant hunting
Search for similar patterns: (1) Other applications accepting JavaScript uploads without restriction combined with HTML injection, (2) CSP implementations relying solely on unsafe-inline restrictions without script-src validation, (3) HTML sanitizers that remove script tags but miss iframe/embed/object elements, (4) File download endpoints that serve uploads with executable content-types, (5) Other messaging platforms with file upload + HTML injection combinations

## MITRE ATT&CK
- T1190
- T1059
- T1567
- T1189
- T1204

## Notes
This vulnerability is particularly insidious because it represents a CSP bypass rather than a CSP violation - the policy is technically enforced but circumvented through a separate feature. The use of iframe srcdoc with HTML entity encoding (&#x3c;) to bypass script tag filters demonstrates sophisticated bypass techniques. Affects Rocket.Chat versions 4.0.3 and 3.18.2. The vulnerability requires chaining multiple weaknesses: file upload acceptance of executable types, HTML injection capability, and inadequate iframe/embed filtering.

## Full report
<details><summary>Expand</summary>

## Summary

The current default CSP header in Rocket.Chat prevents inline script execution, which can be bypassed by importing a script file uploaded via the Rocket.Chat file upload.

## Description

The default CSP header blocks execution of inline-scripts. When a HTML injection vulnerability occurs though, that restriction can be bypassed by uploading a JavaScript file via the file-upload feature (with `application/javascript` or `text/javascript` content-type) to include it in a `<script src="<UPLOAD_URL></script>" tag.

It is worth noticing that script tags are removed from message content, but this filter can also be bypassed as following:

```html
<iframe srcdoc="&#x3c;script src='/file-upload/<UPLOAD ID>/payload.js?download'></script>">
```

## Releases Affected:

  * 4.0.3
  * 3.18.2

## Steps To Reproduce (from initial installation to vulnerability):

  1. Upload payload as `payload.js` via File Upload feature
  2. Inject iframe with srcdoc via arbitary XSS

## Suggested mitigation

  * Block script content-types from file-uploads
  * Filter frames from message body

## Impact

The CSP `unsafe-inline` restriction can be bypassed by uploading script payload as File Upload.

</details>

---
*Analysed by Claude on 2026-05-24*
