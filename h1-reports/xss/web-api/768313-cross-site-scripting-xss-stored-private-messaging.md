# Cross Site Scripting (XSS) Stored - Private messaging

## Metadata
- **Source:** HackerOne
- **Report:** 768313 | https://hackerone.com/reports/768313
- **Submitted:** 2020-01-05
- **Reporter:** javakhishvili
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** low
- **Vuln:** Cross-site Scripting (XSS) - Stored
- **CVEs:** None
- **Category:** web-api

## Summary
• Title: concrete5-8.5.2 Cross Site Scripting (XSS) Stored - Private messaging
• Keyword: crayons
• Software : concrete5
• Product Version: 8.5.2
• Vulnerability : Cross Site Scripting (XSS) Stored
• Vulnerable component: Private messaging

concrete5 latest version 8.5.2  suffer from persistent (Stored) cross site scripting and html injection vulnerabilities.
Insufficient validation of user input 

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

• Title: concrete5-8.5.2 Cross Site Scripting (XSS) Stored - Private messaging
• Keyword: crayons
• Software : concrete5
• Product Version: 8.5.2
• Vulnerability : Cross Site Scripting (XSS) Stored
• Vulnerable component: Private messaging

concrete5 latest version 8.5.2  suffer from persistent (Stored) cross site scripting and html injection vulnerabilities.
Insufficient validation of user input on the authenticated part of the concrete5 application exposes the application to persistent cross site scripting (XSS) vulnerabilities.
These vulnerabilities enable potentially dangerous input from the user to be accepted by the application and then embedded back in the HTML response of the page returned by the web server.
It is possible for lowest privileged user with access to private messaging to send private message to Administrator with malicious XSS payload.

 -  Steps to Reproduce:
Login as basic user and visit private messages, and if there is message from admin you can just reply to it and insert the XSS payload into the body area and submit. Then login as Admin user who would have received the message and when the admin checks the messages there will be message body where admin will hover over the mouse on message body, and either admin will be automatically redirected to malicious site or the XSS payload will render in the browser. Both payloads are provided below:

- Two Attack vector:

               • <input><img src=a onmouseover=window.location.href='https://www.test.com'>
               • <img src=x onmouseover=alert('XSS-Stored')>Bar

- Vulnerable parameter: msgBody

See four screenshots below illustrating both injection part and the part where the payload renders in the browser

## Impact

It is possible for lowest privileged user with access to private messaging to send private message to Administrator with malicious XSS payload.
Cross-site scripting is a flaw that allows users to inject HTML or JavaScript code into a page enabling arbitrary input. Stored XSS allows an attacker to embed a malicious script into a vulnerable page, which is then executed when a victim views the page in this case Admin

</details>

---
*Analysed by Claude on 2026-05-24*
