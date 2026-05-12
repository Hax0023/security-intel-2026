# XSS and Cache Poisoning via Unknown File Type Upload on upload.twitter.com

## Metadata
- **Source:** HackerOne
- **Report:** 84601 | https://hackerone.com/reports/84601
- **Submitted:** 2015-08-25
- **Reporter:** filedescriptor
- **Program:** Twitter
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Cross-Site Scripting (XSS), Cache Poisoning, Content-Type Sniffing, File Upload Validation Bypass, HTML5 AppCache Abuse
- **CVEs:** None
- **Category:** web-api

## Summary
Upload.twitter.com fails to reject files with unknown extensions (e.g., .test), allowing attackers to upload HTML/JavaScript content. The server omits Content-Type headers for unrecognized file types, causing browsers to sniff the content as HTML and execute embedded scripts. Attackers can escalate this to cache poisoning by uploading AppCache manifests to persistently control victim browser caches across ton.twitter.com.

## Attack scenario
1. Attacker accesses Twitter Ads audience manager and initiates file upload
2. Attacker intercepts upload request and modifies file extension from recognized type to unknown extension (e.g., .test)
3. Attacker injects XSS payload (e.g., <script>alert(1)</script>) into file content
4. Server accepts file lacking Content-Type header validation, stores malicious file
5. Attacker generates signed OAuth requests to make uploaded file accessible to victims
6. When victim accesses signed URL, browser sniffs content-type, executes HTML/JavaScript, and can cache malicious AppCache manifests affecting entire domain

## Root cause
Insufficient file type validation combined with missing Content-Type headers in responses. The whitelist-based rejection only checked known dangerous extensions (.html) but failed to handle unknown extensions. When Content-Type header is absent, browsers perform MIME-type sniffing, treating unrecognized content as HTML if it contains HTML tags. Additionally, no Content-Security-Policy or X-Content-Type-Options headers were implemented to prevent sniffing.

## Attacker mindset
Adversary identified a gap in upload validation logic that rejects known dangerous types but accepts unknown extensions as a fallback. Recognizing browser content-sniffing behavior as a feature rather than security mechanism, attacker realized HTML content in unknown-extension files would execute. The escalation to AppCache demonstrated sophisticated understanding of web caching mechanisms to achieve persistent, domain-wide poisoning affecting all users.

## Defensive takeaways
- Implement whitelist-based file extension validation with explicit rejection of unknown types rather than accepting unknown extensions
- Always set explicit Content-Type headers based on validated file types; never rely on browser sniffing
- Deploy X-Content-Type-Options: nosniff header to disable MIME-type sniffing
- Implement Content-Security-Policy headers to restrict script execution origins
- Validate file content signatures/magic bytes, not just extensions
- Store user uploads on separate domain isolated from application domains to prevent XSS impact
- Restrict or disable HTML5 AppCache functionality or validate cache manifests strictly
- Implement strict same-origin policies for signed requests and validate request legitimacy

## Variant hunting
Test other upload endpoints with various unknown extensions (.xyz, .foo, .tmp)
Attempt double extension bypasses (file.html.test, file.test.html)
Test null-byte injection in filenames (file.html%00.test)
Check if other file upload features share same validation logic
Test service worker registration via unknown-extension uploads for persistent control
Attempt SVG uploads with embedded JavaScript as alternative to HTML sniffing
Check if API endpoints have different validation than web UI uploads
Test with case variations (.HTML, .Test, .HtMl)

## MITRE ATT&CK
- T1190
- T1566
- T1598
- T1204
- T1105

## Notes
Report demonstrates sophisticated chaining of multiple web vulnerabilities: upload bypass → content-type sniffing → XSS → cache poisoning. The escalation to AppCache manifests shows deep understanding of browser caching mechanisms. The use of signed OAuth requests to force victim access is a critical escalation factor converting self-XSS to stored XSS. PoC included video demonstration clearly showing cache poisoning effects on ton.twitter.com content replacement.

## Full report
<details><summary>Expand</summary>

Hi,
I would like to report an issue where attackers can bypass the upload restriction on upload.twitter.com to cause XSS on ton.twitter.com and cache poisoning.

##Detail
When using upload.twitter.com to upload audience data, it checks if the file type is allowed and rejects any harmful files (e.g. .html). However it fails to reject files with unknown file type. For example, ```foobar.html``` is rejected while ```foobar.test``` is passed. Since the server does not recognize the file type, it outputs the file without sending the ```Content-Type``` header in the response. The lack of such header results in browser sniffing for the document type. In this case, attackers can insert HTML to perform XSS. Normally the file uploaded is only accessible to the uploader which makes it a self-XSS, but with signed requests attackers can force victims to be able to view the file, thus triggering XSS on behalf of the victim.

###Cache poisoning
Attackers can take this attack further and perform cache poisoning on victim's browser. Since it allows uploading files, attackers can upload a cache manifest file (HTML5 AppCache) to control the cache behaviors over ton.twitter.com. There are two things the attacker can achieve:

1. Attacker can force victim's browser to cache the XSS file. That means it creates a persistent XSS on victim's browser even if the XSS file on the server is removed. 
2. Attacker can control all returning contents on the domain. For example, attacker can replace contents of any file on ton.twitter.com (in victim's perspective)

##Repo step
1. Go to Twitter Ads > Tools > Audience manager > Create new list audience
2. Upload a normal file under "Upload your data file." and intercept the request
3. Change the parameter *blobstore_url* with an unknown suffix (e.g. 1440354519600.txt => 1440354519600.test)
4. Replace the parameter *content* with any XSS vector (e.g. <script>alert(1)</script>)
5. The uploaded file now contains XSS
6. To make it accessible to others, sign it with OAuth token

##PoC
You may also visit http://innerht.ml/pocs/twitter-upload-xss to see the attack in action.

Video demo: https://vimeo.com/137155736 (password: appcache)

The PoC demonstrates the XSS. It also shows how it can influence contents of other pages (poisoning http://ton.twitter.com/).

</details>

---
*Analysed by Claude on 2026-05-12*
