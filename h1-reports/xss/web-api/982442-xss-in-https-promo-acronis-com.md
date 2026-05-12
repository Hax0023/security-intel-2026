# DOM-based XSS via document.referrer in https://promo.acronis.com/GL-Trial-MassTransit.html

## Metadata
- **Source:** HackerOne
- **Report:** 982442 | https://hackerone.com/reports/982442
- **Submitted:** 2020-09-15
- **Reporter:** yash_
- **Program:** Acronis
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** DOM-based XSS, Insecure use of document.referrer, Unsafe document.write with unsanitized input
- **CVEs:** None
- **Category:** web-api

## Summary
A DOM-based XSS vulnerability exists in the GL-Trial-MassTransit.html page where user-controlled document.referrer is used unsafely in document.write() statements to dynamically load scripts. An attacker can create a malicious page that loads the vulnerable Acronis page in an iframe, allowing arbitrary JavaScript execution in the context of promo.acronis.com.

## Attack scenario
1. Attacker creates a malicious webpage containing an iframe that loads https://promo.acronis.com/GL-Trial-MassTransit.html
2. When a victim visits the attacker's page, the iframe loads the vulnerable Acronis page with the attacker's domain as the referrer
3. The vulnerable JavaScript code executes document.write() using the unsanitized document.referrer value
4. The code attempts to load `/marketo/common.js` from the attacker's domain instead of the intended location
5. The attacker-controlled script executes with full privileges in the victim's browser within the promo.acronis.com context
6. Attacker can steal session tokens, redirect to phishing sites, perform account takeover, or inject malware

## Root cause
The application uses document.referrer directly in document.write() statements without sanitization or validation. The referrer header is user-controlled via the Referer HTTP header and can be manipulated by an attacker through HTML/JavaScript.

## Attacker mindset
An attacker recognizes that document.referrer is an attacker-controllable DOM source when the page is loaded via iframe from a malicious origin. The attacker leverages the trusted domain (promo.acronis.com) to execute arbitrary code by controlling the script path loaded via document.write().

## Defensive takeaways
- Never use document.referrer or other user-controllable sources directly in document.write(), innerHTML, or eval()
- Implement Content Security Policy (CSP) to restrict script sources and prevent inline script execution
- Use strict input validation and sanitization for any dynamic script loading
- Replace document.write() with safer alternatives like appendChild() and use proper DOM APIs
- Implement Subresource Integrity (SRI) for external scripts to prevent tampering
- Use X-Frame-Options header to prevent clickjacking and limit iframe embedding
- Apply output encoding appropriate to context (HTML, JavaScript, URL)
- Conduct security code reviews focusing on DOM-based vulnerabilities

## Variant hunting
Search for all instances of document.write() in codebase and audit their inputs
Identify all uses of document.referrer, document.URL, window.location, and other DOM sources
Review JavaScript files for dynamic script/iframe creation using unsanitized values
Check for similar patterns on other Acronis subdomains (*.acronis.com)
Test other pages with HTML forms or redirects that could manipulate referrer
Audit Marketo integration implementations across Acronis properties

## MITRE ATT&CK
- T1190
- T1598
- T1566

## Notes
This is a straightforward DOM XSS via document.referrer exploitation. The vulnerability is particularly dangerous because it leverages a trusted domain and could be used for credential harvesting or malware distribution. The attacker's proof-of-concept is clear and reproducible using Node.js/Express. The use of try/catch blocks does not provide security, only error handling.

## Full report
<details><summary>Expand</summary>

Hello, 

I found DOM XSS in https://promo.acronis.com/  
Open this URL https://promo.acronis.com/GL-Trial-MassTransit.html and view source.
Search for `document.write` and there will be 4 statements inside try/catch block.  
{F988381}

The last statement loads script from using `document.referrer`. So we can host a page that loads https://promo.acronis.com/GL-Trial-MassTransit.html in iframe. So it will load the script `/marketo/common.js` from our domain.

## Steps To Reproduce
  1. To create server I am using Node.js you can use static files also..  If you are using static files server make sure to create `/marketo/common.js` file.
  1. Create a director and copy this file F988371 in it.
  1. Run `npm init -y`
  1. and then `npm i express` to install exprss.
  1. Now run `node index.js` this will start server on 'localhost:5000'
  1. Open http://localhost:5000 and you will see alert.  
   {F988380}

## Impact

Anyone who opens this page, attacker can execute JavaScript code on their device or redirect victims to phishing websites.

</details>

---
*Analysed by Claude on 2026-05-12*
