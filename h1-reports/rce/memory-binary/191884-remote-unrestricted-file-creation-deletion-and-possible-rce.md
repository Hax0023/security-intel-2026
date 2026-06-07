# Remote Unrestricted File Creation/Deletion and Possible RCE on Reverb.twitter.com

## Metadata
- **Source:** HackerOne
- **Report:** 191884 | https://hackerone.com/reports/191884
- **Submitted:** 2016-12-17
- **Reporter:** zigoo0
- **Program:** Twitter Bug Bounty Program
- **Bounty:** Not specified in report
- **Severity:** CRITICAL
- **Vuln:** Unrestricted File Upload, Path Traversal/Directory Traversal, Arbitrary File Write, Missing Authentication, Missing Input Validation, Denial of Service
- **CVEs:** None
- **Category:** memory-binary

## Summary
The saveImage.php API endpoint on reverb.twitter.com lacks authentication and input validation, allowing unauthenticated attackers to create arbitrary files with controlled names and extensions anywhere on the web root. By combining directory traversal sequences with PHP extension, attackers can achieve arbitrary file write leading to potential RCE, file overwrite, and DoS via disk space exhaustion.

## Attack scenario
1. Attacker identifies the unauthenticated saveImage.php API endpoint that accepts image, filename, and extension parameters
2. Attacker crafts a POST request with directory traversal payload in filename parameter (e.g., /../../zigoo) and php extension
3. Backend concatenates 'preview-' prefix but fails to sanitize path traversal, resulting in file creation outside intended directory
4. Attacker accesses created PHP file at predictable web-accessible path and executes arbitrary code
5. Attacker exploits file overwrite capability to modify critical application files (twitterLogin.php, .htaccess) causing defacement or DoS
6. Attacker submits repeated requests with large payloads to exhaust server disk space and trigger Denial of Service

## Root cause
Multiple layers of insufficient input validation and missing security controls: (1) No authentication/authorization check on API endpoint, (2) No filename sanitization to remove path traversal characters, (3) No extension whitelist restriction, (4) No file size limits enforced, (5) Predictable output directory structure, (6) Unsafe concatenation of user input with file paths

## Attacker mindset
Opportunistic but sophisticated researcher who methodically identified an administrative API endpoint, reverse-engineered the backend logic through normal operation analysis, and systematically tested input parameters to exploit path traversal. The attacker recognized the severity of storing authentication tokens and the potential for cascading damage through file overwrite attacks.

## Defensive takeaways
- Implement mandatory authentication and authorization checks on all API endpoints, especially administrative functions
- Use whitelist-based validation for file extensions (e.g., only allow '.png')
- Sanitize and validate all user input for special characters and path traversal sequences (../, .., etc.)
- Generate random, unpredictable filenames server-side rather than trusting user input
- Implement strict file size limits per upload and aggregate disk usage limits
- Store uploaded files outside web root or in a non-executable directory
- Use security headers like X-Content-Type-Options: nosniff to prevent script execution
- Implement file integrity monitoring for critical application files
- Apply principle of least privilege - ensure web server process runs with minimal permissions
- Regular security audits and SAST scanning for file operation vulnerabilities

## Variant hunting
Search for other endpoints accepting filename/extension parameters across Twitter's infrastructure
Test other image processing APIs for similar path traversal and extension manipulation flaws
Identify other administrative tools that may rely on insecure file operations without proper validation
Audit for similar patterns in social media analysis/visualization tools that handle file uploads
Check for other instances where user-controlled data is concatenated into file system operations

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1104 - Proxy Execution
- T1071 - Application Layer Protocol
- T1567 - Exfiltration Over Web Service
- T1499 - Endpoint Denial of Service
- T1548 - Abuse Elevation Control Mechanism
- T1546 - Event Triggered Execution

## Notes
Critical vulnerability affecting a data visualization tool with access to Twitter user authentication tokens. The combination of missing authentication, path traversal, and arbitrary file write creates multiple attack vectors including RCE, application defacement, and DoS. The researcher demonstrated exceptional analysis by identifying the backend logic pattern and providing detailed exploitation scenarios. Video POC available. Platform appears to be shared between reverb.twitter.com and reverb.guru domains.

## Full report
<details><summary>Expand</summary>

Hello Gents,

During my research on Twitter BBP, I found below domain name: **Reverb.twitter.com**

###Background:
>We worked with Twitter to develop TwitterReverb, an application that reveals how conversations arise and reverberate across the entire Twitter landscape. The custom application allows visitors to reveal patterns in Twitter activities related to keywords, hashtags, topics, people, and individual tweets through the use of a backend administrative tool that dynamically generates a custom data visualization.
>"TheRealPeriscopic" -> https://www.youtube.com/watch?v=bm5eyTeBBDE

###Description:
Reverb.twitter.com (also uses **reverb.guru**) is vulnerable to unauthenticated remote file Creation/Deletion and Possible RCE vulnerability.
Below URL is an API file used to generate png images based on 3 given inputs:
https://reverb.twitter.com/api/actions/saveImage.php

The 3 given inputs are: **image**=SomeContent&**filename**=test&**extension**=png

It was found that the file doesn't require authentication or authorization in order to be able to initiate the API call to generate a new png file. it doesn't even validate the created file name.

In normal scenario, to use the file you have to send a POST request as below:
https://reverb.twitter.com/api/actions/saveImage.php
**POST:**
image=SomeContent&filename=test&extension=png

the a/m example should create a png file named as "preview-test.png" in below directory:
/var/www/html/view/data/image/preview-test.png

**Example of normal file operation output:**
https://go.reverb.guru/view/data/image/preview-069772811858678284.png

Since I've the ability to choose the file name & ext, i've manipulated the file ext to be php and the file name to be /../../zigo (Directory Traversal) which allowed me escape the "preview-" added to the filename and to escape the uploads directory to create a file as below:

https://reverb.twitter.com/api/actions/saveImage.php
**POST:**
image=SomeContent&filename=/../../zigoo&extension=php

**POC:** https://reverb.twitter.com/view/data/zigoo.php
**PATH:** /var/www/html/view/data/zigoo.php

It is noticed that user input under the parameter "image" is passed to some function that would treat it as image stream and convert it as well to a png image. I imagine that backend code that handles the input of parameter "image" looks like:

><?php
 $data = $_POST['image'];
 $im = imagecreatefromstring($data);
 if ($im !== false) {
    imagepng($im);
    imagedestroy($im);
 }
 else {
    exit;
 }
> ?>

I've wrote a python script (Attached as: F144335) to simulate the same scenario, unfortunately i couldn't trigger the RCE. BUT ......

**Vulnerability Consequences:**
1. Since i can control the filename, ext, and file content, the RCE is still possible if given enough time to research and try, but i always thought that FileDescriptor would have reported it if i delayed :D
2. An attacker can submit the same request over and over with large file size, even if the files contents are not understood, it is still consuming the server space which would cause the server to go down (Space Exhaustion, refer to function **DDOS()** in the attached python file)
3. File deletion and defacement is also possible since Directory traversal were found. for example, an attacker can submit the file name as: **../../../../index.php** which will replace the main page of the vulnerable site!
4. The above mentioned scenario could also be used to cause the **TwitterReverb** application to stop working permanently by overwriting the file **"api/twitter/twitterLogin.php"** which is responsible for the authentication of application users.
5. Also directory traversal scenario could be used to create ".htaccess" file at any directory which would cause all the pages inside that directory to stop working!

**How to Fix:**
1. Set proper authentication/authorization on the affected file.
2. Filename, ext & input content should be validated before being submitted to the backend server. for example the file ext should be restricted to '.png' only & filename should never contain dots or other special characters.
3. A filesize limit must be applied on the created files to avoid DDOS attacks via exhausting the server disk space.

Kindly note that the affected server holds large amount of Twitter users authentication tokens for the TwitterRiverb application.

And finally, below is a POC video to demonstrate the vulnerability and how to reproduce it.

**POC:** https://youtu.be/OPlexp-1XxU

Thank you and have a nice day.


</details>

---
*Analysed by Claude on 2026-06-07*
