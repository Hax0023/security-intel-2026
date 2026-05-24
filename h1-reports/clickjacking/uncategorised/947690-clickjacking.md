# Clickjacking Vulnerability on Acronis Website

## Metadata
- **Source:** HackerOne
- **Report:** 947690 | https://hackerone.com/reports/947690
- **Submitted:** 2020-07-30
- **Reporter:** salna_kuruvi
- **Program:** Acronis
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Clickjacking, UI Redressing, Missing X-Frame-Options Header
- **CVEs:** None
- **Category:** uncategorised

## Summary
The Acronis website (https://www.acronis.com/en-in/) lacks proper X-Frame-Options headers, allowing the site to be embedded in iframes on attacker-controlled pages. This enables clickjacking attacks where users can be tricked into performing unintended actions by clicking on invisible or disguised elements overlaid on legitimate content.

## Attack scenario
1. Attacker creates a malicious HTML page and embeds the Acronis website within an iframe
2. Attacker overlays transparent or visually hidden interactive elements (buttons, links) on top of the framed Acronis content
3. Attacker tricks users into visiting the malicious page through social engineering or advertising
4. User unknowingly clicks on attacker-controlled overlay elements while believing they are interacting with Acronis
5. User performs unintended actions such as initiating transfers, changing account settings, or installing malware
6. Attacker gains unauthorized access to user accounts, credentials, or sensitive information

## Root cause
The application does not implement the X-Frame-Options HTTP response header or equivalent Content Security Policy (CSP) directives to prevent embedding in frames. This allows any website to embed the application in an iframe without restriction.

## Attacker mindset
An attacker would recognize that the lack of frame-busting mechanisms creates an opportunity for UI redressing attacks. By layering legitimate-looking content from Acronis beneath attacker-controlled UI elements, they can manipulate user behavior and steal credentials, perform unauthorized actions, or facilitate further attacks.

## Defensive takeaways
- Implement X-Frame-Options header with DENY or SAMEORIGIN value to prevent framing attacks
- Use Content-Security-Policy frame-ancestors directive as a modern alternative to X-Frame-Options
- Implement client-side frame-busting JavaScript code to detect and break out of frames
- Regularly test for clickjacking vulnerabilities as part of security assessment processes
- Apply security headers consistently across all endpoints and pages
- Educate users about the risks of clicking on suspicious links or content from untrusted sources

## Variant hunting
Check for partial X-Frame-Options implementation (e.g., SAMEORIGIN that may be bypassable with subdomain attacks)
Test other endpoints and subdomains for missing or inconsistent frame-options headers
Verify CSP frame-ancestors policy is properly configured if X-Frame-Options is deprecated
Test for dangling iframes or XSLT that might bypass frame protections
Look for similar clickjacking vulnerabilities on other Acronis properties and partner websites

## MITRE ATT&CK
- T1189
- T1566
- T1598

## Notes
This is a straightforward clickjacking vulnerability report. The write-up is basic and lacks detail on actual proof of impact beyond embedding. The researcher correctly identifies the vulnerability and recommended fix. The severity is typically rated as medium to high depending on the sensitivity of actions users can perform on the framed site. Acronis handles sensitive backup and security software, making credential theft or unauthorized account actions particularly impactful.

## Full report
<details><summary>Expand</summary>

I have found the vulnerability called Clickjacking.

Please find the details below:

Description     

Clickjacking is an exploit in which malicious coding is hidden beneath apparently legitimate buttons or other clickable content on a website.

  OWASP Benchmark   A6- Security Misconfiguration  


Steps to Reproduce   

1.Craft an HTML page and add the following 
( https://www.acronis.com/en-in/ ) of the application within an iframe.

2.Save the file as *.html and run the file.

3.Open the HTML page in a browser.

4.The following attached screenshot shows webiste is in frame.

Please find the attached screenshot for your reference. 

High Level Fix Recommendation

Clickjacking attacks can be avoided by setting the X-Frame-Options header or by using frame busting code which check if the current web page is the top web page (not within a frame).

## Impact

Impact 

Multitude of attacks including key logging and stealing user credentials.

</details>

---
*Analysed by Claude on 2026-05-24*
