# Reflected XSS in Username Parameter - Registration Form

## Metadata
- **Source:** HackerOne
- **Report:** 2356104 | https://hackerone.com/reports/2356104
- **Submitted:** 2024-02-05
- **Reporter:** chor4o
- **Program:** Undisclosed (Redacted)
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Cross-Site Scripting (XSS) - Reflected, Improper Input Validation, Improper Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability exists in the username parameter of a registration form endpoint (/testweb/aeon.dll/css/Aeon.dll). An attacker can inject arbitrary JavaScript code via the Username POST parameter which is reflected in the response without proper sanitization or encoding. This allows theft of sensitive data from users who click a malicious link containing the XSS payload.

## Attack scenario
1. Attacker identifies the registration form endpoint accepts POST requests with a Username parameter
2. Attacker crafts a malicious URL or HTML form containing XSS payload in the Username field (e.g., '<ScRiPt>alert(233)</ScRiPt>')
3. Attacker sends the malicious link to target users via phishing, social engineering, or embeds in a webpage
4. Victim clicks the link and submits the form, triggering the XSS payload execution in their browser
5. Malicious JavaScript executes in victim's session context, allowing theft of session cookies, authentication tokens, or other sensitive data
6. Attacker exfiltrates stolen credentials or data to their server

## Root cause
The application fails to properly validate and encode user-supplied input in the Username parameter before reflecting it in HTTP responses. The payload '<ScRiPt>alert(233)</ScRiPt>' is not filtered or HTML-encoded, allowing script execution in the victim's browser context.

## Attacker mindset
The attacker is performing reconnaissance on the application to identify input validation weaknesses. They systematically tested form parameters using Burp Suite to find injection points, demonstrating methodical vulnerability discovery. The goal is to establish a reliable XSS vector for credential harvesting or session hijacking attacks.

## Defensive takeaways
- Implement strict input validation on all user-supplied parameters - whitelist acceptable characters and reject or sanitize special characters
- Apply context-appropriate output encoding (HTML entity encoding) to all user input reflected in HTTP responses
- Use a Web Application Firewall (WAF) with rules to detect and block common XSS patterns
- Implement Content Security Policy (CSP) headers to prevent inline script execution
- Use security-focused template engines that auto-escape output by default
- Conduct regular security testing including manual code review and penetration testing of all input points
- Apply principle of least privilege to limit potential damage from XSS execution
- Educate developers on secure coding practices for input handling and output encoding

## Variant hunting
Test other form parameters (FirstName, LastName, Address, etc.) for similar XSS vulnerabilities
Test for Stored XSS if username values are persisted in user profiles or displayed to other users
Test for DOM-based XSS if JavaScript processes the username parameter on the client side
Test various XSS encoding bypasses: case variation, HTML entities, Unicode encoding, tag attributes
Test for Blind XSS by injecting callbacks to external domains in various parameters
Test other HTTP methods (GET, PUT, DELETE) on the same endpoint
Test POST parameters with Content-Type variations (JSON, XML, multipart)

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1566.002 - Phishing: Spearphishing Link
- T1203 - Exploitation for Client Execution
- T1005 - Data from Local System
- T1041 - Exfiltration Over C2 Channel
- T1056.004 - Interaction Recording (session capture via XSS)

## Notes
The report lacks clarity and complete details (significant redactions present). The researcher demonstrates understanding of the vulnerability through video POCs but provides minimal technical detail in written form. The Burp request shows conversion from GET to POST method as an attack vector variation. Proper remediation and mitigation suggestions are completely absent from the submission. The writeup would benefit from clearer payload documentation and explicit impact description beyond generic 'data theft' claims.

## Full report
<details><summary>Expand</summary>

Hi teams,

Burp - Request

█████

In the first video, I demonstrate via burp the capture of get and then I modify it to post and copy the code that I sent in the other reports and send the xss.

Dod-1.mkv

In the video dod-2.mkv I am sending the xss via "POC" poc-dod.html

## Impact

The attacker can steal data from whoever checks the report.

## System Host(s)
█████

## Affected Product(s) and Version(s)


## CVE Numbers


## Steps to Reproduce
Burp Request

POST /testweb/aeon.dll/css/Aeon.dll HTTP/1.1
Host: ███
Sec-Ch-Ua: "Chromium";v="121", "Not A(Brand";v="99"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Windows"
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.85 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Sec-Fetch-Site: none
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Accept-Encoding: gzip, deflate, br
Accept-Language: pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7
Priority: u=0, i
Connection: close
Content-Type: application/x-www-form-urlencoded
Content-Length: 597

Address=███████&Address2=█████&AeonForm=Registration&City=██████&Country=████&Department=Candidate&EMailAddress=█████████&FORMSTATE=1&FirstName=ghovjnjv&ID=1&IDType=1&LastName=ghovjnjv&NotificationMethod=Email&Password1=u]H[ww6KrA9F.x-F&Password2=u]H[ww6KrA9F.x-F&Phone=███&SAddress=██████&SAddress2=█████████&SCity=██████&SCountry=AF&SState=N/A&SZip=██████████&State=N/A&Status=USMA&SubmitButton=Submit%20Information&Username=ghovjnjv'"()%26%25<zzz><ScRiPt>alert(233)</ScRiPt>&Zip=██████████

## Suggested Mitigation/Remediation Actions




</details>

---
*Analysed by Claude on 2026-05-12*
