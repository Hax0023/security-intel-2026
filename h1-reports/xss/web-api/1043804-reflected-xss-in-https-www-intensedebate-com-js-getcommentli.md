# Reflected DOM XSS in getCommentLink.php via posttitle Parameter

## Metadata
- **Source:** HackerOne
- **Report:** 1043804 | https://hackerone.com/reports/1043804
- **Submitted:** 2020-11-26
- **Reporter:** sudi
- **Program:** Intense Debate
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Cross-Site Scripting (XSS), Reflected XSS, DOM-based XSS
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected DOM XSS vulnerability exists in the posttitle parameter of intensedebate.com/js/getCommentLink.php that allows unauthenticated attackers to inject arbitrary JavaScript code. An attacker can craft a malicious URL and trick users into clicking it to execute JavaScript in their browser context, potentially leading to account compromise, session hijacking, or automated account deletion.

## Attack scenario
1. Attacker identifies that the posttitle parameter in getCommentLink.php is not properly sanitized or escaped
2. Attacker crafts a malicious URL containing JavaScript payload in the posttitle parameter (e.g., "><img src=x onerror=alert(1)>)
3. Attacker sends the crafted URL to a victim via phishing email, social media, or forum post
4. Victim clicks the link and the malicious URL is loaded in their browser
5. JavaScript code executes in the victim's browser under the context of intensedebate.com domain
6. Attacker can steal session cookies, perform actions on behalf of the user (delete account via document.getElementById('frm2').submit()), or redirect to malicious sites

## Root cause
The posttitle parameter is reflected in the DOM without proper HTML encoding or output escaping. The application fails to sanitize user input before including it in the JavaScript response, allowing attackers to break out of the intended context and inject arbitrary HTML/JavaScript.

## Attacker mindset
An opportunistic attacker seeking to compromise user accounts on a popular commenting platform. The attacker demonstrates awareness of the application's data export and account closure functionality, suggesting potential intent for account takeover, data theft, or account sabotage. The use of common XSS payloads indicates familiarity with web security testing.

## Defensive takeaways
- Implement strict input validation and whitelist acceptable characters for the posttitle parameter
- Apply proper HTML entity encoding/escaping to all user-controlled input before reflecting it in responses
- Use Content Security Policy (CSP) headers to prevent inline script execution and reduce XSS impact
- Implement output encoding appropriate to the context (HTML encoding for HTML context, JavaScript encoding for JavaScript context)
- Use templating engines with automatic escaping enabled by default
- Implement HTTPOnly and Secure flags on session cookies to mitigate session hijacking
- Require CSRF tokens for sensitive actions like account deletion or data export
- Conduct regular security code reviews focusing on user input handling in URL parameters

## Variant hunting
Look for similar patterns in other PHP endpoints that accept URL parameters (postid, posturl, acct). Test other comment-related endpoints for XSS vulnerabilities. Check if similar sanitization bypasses exist in other widgets or embeddable components. Investigate if other parameters are also vulnerable. Test for stored XSS if these parameters are cached or stored in databases.

## MITRE ATT&CK
- T1190
- T1598
- T1566
- T1539

## Notes
This is a classic reflected XSS vulnerability with straightforward exploitation. The reporter provides clear proof-of-concept and demonstrates awareness of business impact by identifying potential for automated account deletion. The vulnerability affects a JavaScript endpoint commonly embedded across third-party websites, amplifying the attack surface. The report lacks explicit bounty amount, suggesting it may have been reported before public disclosure or handled through a different process.

## Full report
<details><summary>Expand</summary>

Hey there,
I have found a reflected dom xss vulnerability in your website www.intensedebate.com, the *posttitle* parameter is vulnerable.

---------------------------------------------------------------------------------------------------------------------------------------------------


**Full url:** https://www.intensedebate.com/js/getCommentLink.php?acct=c90a61ed51fd7b64001f1361a7a71191&postid=https://web.archive.org/web/20170820134008/https://mronline.org/2010/12/08/jobs-liberty-and-the-bottom-line/&posturl=https://web.archive.org/web/20170820134008/https://mronline.org/2010/12/08/jobs-liberty-and-the-bottom-line/&posttitle=xss
**Parameter:** posttitle
**XSS Payload:** "><img src=x onerror=alert(1)>

---------------------------------------------------------------------------------------------------------------------------------------------------


**Steps to reproduce:**
Just load this url in your browser and you will get the xss popup

https://www.intensedebate.com/js/getCommentLink.php?acct=c90a61ed51fd7b64001f1361a7a71191&postid=https://web.archive.org/web/20170820134008/https://mronline.org/2010/12/08/jobs-liberty-and-the-bottom-line/&posturl=https://web.archive.org/web/20170820134008/https://mronline.org/2010/12/08/jobs-liberty-and-the-bottom-line/&posttitle=%3Cimg%20src=x%20onerror=alert(document.domain)%3E

---------------------------------------------------------------------------------------------------------------------------------------------------

**POC:**

{F1094491}

-----------------------------------------------------------------------------------------------------------------------------------------------------

## Impact

An attacker steal cookies of logged in users just by sending the url with the xss-payload, can redirect users to another websites,virtual defacement,etc.
Also Looking at the page: https://www.intensedebate.com/your-information, there are two actions available *Account Closure*, *Data export* with the xss we can perform this action on behalf of the user for eg:

```javascript
 document.getElementById('frm2').submit();
```
With a js code like this we can auto submit this  form so that when the user visits the url, his/her account will automatically will be deleted. 


Thankyou
Kind Regards
Sudhanshu

</details>

---
*Analysed by Claude on 2026-05-12*
