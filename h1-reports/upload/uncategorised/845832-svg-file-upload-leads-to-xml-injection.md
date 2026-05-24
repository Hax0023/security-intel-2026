# SVG File Upload Leads to XML Injection (XXE/SSRF)

## Metadata
- **Source:** HackerOne
- **Report:** 845832 | https://hackerone.com/reports/845832
- **Submitted:** 2020-04-10
- **Reporter:** tushr
- **Program:** Topcoder
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** XML External Entity (XXE) Injection, Server-Side Request Forgery (SSRF), Local File Inclusion (LFI), Denial of Service (Billion Laugh Attack), Improper File Upload Validation
- **CVEs:** None
- **Category:** uncategorised

## Summary
The avatar upload functionality accepts SVG files (image/svg+xml MIME type) without proper validation, allowing attackers to upload malicious XML-based SVG files. This enables XXE injection attacks to read local files, perform SSRF to external systems, and potentially cause denial of service through billion laugh attacks.

## Attack scenario
1. Attacker calls photoUploadUrl API endpoint with contentType set to 'image/svg+xml' to obtain a pre-signed S3 URL
2. Attacker crafts malicious SVG file containing XXE payload with external entity definitions (e.g., file:// or http:// references)
3. Attacker uploads crafted SVG via PUT request to pre-signed S3 URL with Content-Type header set to image/svg+xml
4. Server or client-side parser processes uploaded SVG file and resolves external XML entities
5. Attacker retrieves sensitive files from server filesystem or triggers requests to internal/external systems via SSRF
6. Alternative: Attacker uses billion laugh attack payload to exhaust server resources and cause denial of service

## Root cause
The application accepts SVG uploads based on MIME type validation alone without parsing or sanitizing SVG file contents. SVG is XML-based and supports dangerous features like external entity declarations and xlink:href attributes that can reference local files or external URLs. No XXE-specific protections were implemented during file processing.

## Attacker mindset
An attacker recognizes that SVG files are commonly allowed in image upload filters but are actually XML documents. They exploit this discrepancy by crafting SVG payloads with XXE declarations to bypass file restrictions and access sensitive data, lateral resources, or degrade service availability. The SSRF vector is particularly valuable for accessing internal services behind firewalls.

## Defensive takeaways
- Implement strict file type validation beyond MIME type checking - use magic bytes or file signature analysis
- Disable XML external entities (XXE) globally via parser configuration (e.g., FEATURE_SECURE_PROCESSING, XMLConstants.ACCESS_EXTERNAL_DTD set to empty string)
- If SVG support is required, use dedicated SVG sanitization libraries that strip dangerous elements (script tags, event handlers, external references)
- Implement Content Security Policy (CSP) headers to mitigate XSS from stored SVG files
- Use allowlist-based approach: only permit specific safe SVG elements and attributes
- Disable DTD processing in XML parsers: setFeature('http://apache.org/xml/features/disallow-doctype-decl', true)
- Implement resource limits on XML parsing to prevent billion laugh DoS attacks
- Store uploaded files outside web root and serve via download handler rather than direct browser access
- Scan uploaded files with security tools (e.g., ClamAV, custom XXE scanners) before acceptance

## Variant hunting
Search for similar issues in: PDF upload functionality (PDF supports XML/XXE), Word document uploads (DOCX/XLSX are ZIP archives with XML), image metadata processing, XML-based configuration file uploads, document conversion services, and any file type that wraps or contains XML structures. Check for XXE vulnerabilities in image processing libraries (ImageMagick, GhostScript) when handling SVG or vector formats.

## MITRE ATT&CK
- T1190
- T1083
- T1057
- T1005
- T1046
- T1499

## Notes
The XXE SSRF variant (fetching external resources via xlink:href) was successfully demonstrated by the researcher connecting to their own server, confirming the vulnerability is exploitable. The LFI variant references another user's uploaded file path, showing potential for user data exfiltration. The report properly notes that stored XSS via SVG script tags was not exploitable in this context due to use of <img> tag rather than <svg> tag for rendering, but remains a potential variant. Billion laugh attack potential was identified but not fully tested by the researcher.

## Full report
<details><summary>Expand</summary>

## Summary:
Upload Avatar option allows the user to upload image/* . Thus enabling the upload of many file formats including SVG files (MIME type: image/svg+xml) 
SVG files are XML based graphics files in 2D images. Thus, this opens up an attack vector to upload specially crafted malicious SVG files. 
The attacks that are possible using SVG files are:

1. XSS attack: Stored XSS can be performed by including a "<script>alert(1)</script>" payload inside the XML code of the SVG file can make the browser execute the javascript when the file is rendered. However, only possible when using an <svg> tag to call the file. In this case, <img> tag is used thus not exploitable.
2. XXE attack: Injecting malicious XML code inside the SVG file thus executing once the server parses the SVG. [Follow steps to reproduce for this]
3. DOS attack: Billion laugh attack is an application-level DOS and can lead to resource exhaustion making the server slow down or crash. I have not tried this but found the below resource about it:
                            https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/XXE%20Injection#billion-laugh-attack

## Steps to reproduce
  1. I observed that when uploading a user avatar picture, the first request was sent to 
       https://api.topcoder.com/v3/members/oldsoul/photoUploadUrl
       with a POST parameter "contentType" telling the type of file being uploaded. I changed the value to "image/svg+xml".  
       Now, the response had a preSignedURL variable pointing to the valid S3 object creation URL, and a token variable which gives a random number which is added to the file name which is being uploaded.
                                     F781757
  
  2. Second request is a PUT request to https://api.topcoder.com/v3/members/oldsoul/photo
       with a token variable which is same as the token variable which we received in the first request. Also a variable "contentType" which is used in determining the extension of the file being uploaded. I changed the value to "image/svg+xml"
                                     F781767
  
  3. Now, I sent a PUT request to the "preSignedURL" that we got from the first request with HTTP header "Content-Type: image/svg+xml". The body of this request contains the SVG file data to be uploaded.    F781788


----------------------------------------------------XXE SSRF------------------------------------------------
   1. For Fetching External resources from a remote server, 
   upload SVG with <image xlink:href="http://159.65.151.4:81/svg" /> to the SVG file [observed connection to my server when listening via netcat on port 81]  =>   F781770

<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg
   xmlns:svg="http://www.w3.org/2000/svg"
   xmlns="http://www.w3.org/2000/svg"
   xmlns:xlink="http://www.w3.org/1999/xlink"
   style="overflow: hidden; position: relative;"
   width="300"
   height="200">
  <image x="10" y="10" width="276" height="110" xlink:href="http://159.65.151.4:81/svg" stroke-width="1" id="image3204" />
  <rect x="0" y="150" height="10" width="300" style="fill: black"/>
</svg>

(This is the IP of my personal server. You can include a public resource like http://images.google.com/intl/es_ALL/images/logos/images_logo_lg.gif)  =>  F781773

   2. For fetching local files from the server itself (LFI),

I created another user named testing68 and uploaded an avatar picture for it. Added the picture link for testing68 user to the XML payload  =>  F781779

  <image x="10" y="10" width="276" height="110" xlink:href="/member/profile/testing68-1586481096585.png" stroke-width="1" id="image3204" />


## Supporting Material/References:
SImilar Reports: 
https://hackerone.com/reports/97501
https://hackerone.com/reports/142709

Reference material:
https://qy.sg/x-ctf-finals-2016-john-slick-web-25/
https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/XXE%20Injection#xxe-inside-svg


Thanks

## Impact

Exploiting an XXE attack, allows an attacker to interfere with an application's processing of XML data. It often allows an attacker to view files on the application server filesystem, and to interact with any backend or external systems that the application itself can access.

Exploiting the billion laugh DOS attack can mess with the availability of the server and since it is an application level DOS network level filters will not be effective to stop such attack.

</details>

---
*Analysed by Claude on 2026-05-24*
