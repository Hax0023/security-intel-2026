# CRLF Injection and Stored XSS on ton.twitter.com via Image Upload Manipulation

## Metadata
- **Source:** HackerOne
- **Report:** 191380 | https://hackerone.com/reports/191380
- **Submitted:** 2016-12-15
- **Reporter:** seifelsallamy
- **Program:** Twitter
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** CRLF Injection, Stored XSS, HTTP Response Splitting, Cookie Injection, Path Traversal
- **CVEs:** None
- **Category:** web-api

## Summary
A CRLF injection vulnerability in ton.twitter.com allows attackers to inject arbitrary HTTP headers including cookies via URL parameters. Combined with a stored XSS vulnerability exploitable through image extension manipulation in direct messages, an attacker can inject authentication tokens into victims' browsers and execute malicious JavaScript, leading to phishing attacks and potential CSP bypass.

## Attack scenario
1. Attacker crafts a CRLF injection URL containing URL-encoded newline characters and injects a malicious auth_token cookie targeting the victim's domain
2. Attacker uploads a malicious image file with .jpg extension to Twitter's direct message feature containing JavaScript payload
3. Attacker modifies the image URL by removing the `:large` suffix and appending `%23.html` to trigger HTML/JavaScript rendering instead of image rendering
4. When victim clicks the crafted URL, the CRLF injection sets the attacker's auth_token cookie in the victim's browser via Set-Cookie header
5. The victim's browser now authenticates as the attacker on ton.twitter.com, allowing access to the injected image with XSS payload
6. JavaScript executes in victim's browser context, enabling phishing page injection or malware distribution without requiring mutual follow relationship

## Root cause
Insufficient input validation on URL parameters in ton.twitter.com's file serving endpoint allowing CRLF characters to be passed through to HTTP response headers. Additionally, inadequate file type validation permits HTML/JavaScript execution through image file extension manipulation and URL rewriting bypass.

## Attacker mindset
An attacker identifies that individual vulnerabilities (CRLF alone or XSS alone) have limited impact due to authentication and visibility restrictions. By chaining them together, the attacker overcomes the mutual-follow requirement and leverages CRLF to inject valid authentication credentials, amplifying the XSS impact from self-only to arbitrary victims without relationship constraints.

## Defensive takeaways
- Implement strict input validation and sanitization on all URL parameters, explicitly blocking CRLF characters (\r\n, %0d%0a) before they reach response generation
- Enforce Content-Type headers based on file content (magic bytes) rather than user-supplied extensions or URL parameters
- Implement proper response header filtering to prevent injection of security-sensitive headers like Set-Cookie
- Use X-Content-Type-Options: nosniff header to prevent MIME-type sniffing attacks
- Implement Content Security Policy (CSP) with strict directives and script-src 'none' for user-uploaded content domains
- Validate and sanitize image files server-side; reject files containing embedded scripts or unusual content
- Separate user-generated content to a different domain/subdomain without sensitive cookies
- Implement multi-factor authentication resilience to mitigate cookie injection attacks
- Use HTTPOnly and Secure flags on authentication cookies to limit client-side access

## Variant hunting
Hunt for similar CRLF injection points in other Twitter subdomains and API endpoints handling file uploads/downloads. Investigate other file serving endpoints that perform URL rewriting (`:large`, `:small`, etc.) for extension manipulation bypasses. Search for other authentication token delivery mechanisms that could be exploited via CRLF injection. Test for similar vulnerabilities in other CDN/media serving infrastructure.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1598 - Phishing (via injected phishing page)
- T1185 - Man in the Browser (via cookie injection)
- T1036 - Masquerading (file extension manipulation)
- T1657 - Web Session Cookie (cookie injection)

## Notes
The report demonstrates sophisticated vulnerability chaining, combining two individually low-impact vulnerabilities into a high-impact attack. The attacker's observation that ton.twitter.com lacks valuable cookies is important context - the real value comes from using injected auth_token to bypass access controls on the private message image, enabling XSS delivery. The similarity to report #52042 suggests this may be a variant or incomplete previous fix. The CSP bypass potential on twitter.com domain indicates potential for escalation beyond ton.twitter.com's own limited functionality.

## Full report
<details><summary>Expand</summary>

Hey,

###[1] CRLF:
It's similar to #52042 but weaker
to reproduce go to:
https://ton.twitter.com/1.1/ton/data/dm/x/%E5%98%8A%E5%98%8Dset-cookie%3A%20test%3Dtest%3B%20Domain%3D.twitter.com%3B%20Path%3D%2F%3B%20Expires%3DSat%2C%2015-Dec-2018%2009%3A45%3A55%20UTC

you will find that `test` cookie with the value `test` has been added to your cookies

###[2] XSS:
XSS can occur by injecting a `.jpg` image 
and uploading it to twitter
then changing the extension from `.jpg` to `.html`
to reproduce open messages and start a conversation 
upload this image F143743 and send it in the conversation 
open the image source url it will look alike 

https://ton.twitter.com/i/ton/data/dm/123456789/987654321/AbCdEf.jpg:large

remove the last part `:large`
and put `%23.html`
XSS popup box will popup

however this image can only appear to you and to the one who you send it to because it is a private message
and to send the message you have to follow the victim and the victim has to follow you in most cases
and ton.twitter.com has no valuable cookies at all 
so the impact will be a phishing page or let the victim downloading a malicious software after sending the injected image on a message 

###CRLF + XSS:
both bugs separately are too weak 
but by joining them together the impact will be much more powerful
ton.twitter.com showing the image to the one who has a valid `auth_token` cookie with a value that has the right to see the injected image 
as example the attackers' `auth_token` is valid and has the right to see the injected image
so if the attacker injected his own `auth_token` to the victim by CRLF
the injected image will appear to the victim even if the victim not following you
causing a XSS to occur 
the following URL will:
[1] change auth_token value to my own `auth_token` value to make the injected image appear in your pc
[2] will redirect you to the injected imaged
[3] Javascript will be executed causing attacker's phishing page to appear
https://ton.twitter.com/1.1/ton/data/dm/809353163740483587/809353151434330112/O5hEYiOt.jpg%2523.html%E5%98%8A%E5%98%8Dset-cookie%3A%20auth_token%3Db2868e3d5fd901a1cf4819afd147ee893f331294%3B%20Domain%3D.twitter.com%3B%20Path%3D%2F%3B%20Expires%3DSat%2C%2015-Dec-2018%2009%3A45%3A55%20UTC%3BSecure%3BHTTPOnly

###Impacts
[1] phishing
[2] crlf injection (cookie injection &  DOS may occur & cache poisoning )
[3] under certain circumstances it may lead to bypassing CSP in https://twitter.com 

###POCS
F143759
F143760
F143761

Thank you!

</details>

---
*Analysed by Claude on 2026-05-12*
