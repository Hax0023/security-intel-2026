# self cross site scripting

## Metadata
- **Source:** HackerOne
- **Report:** 245762 | https://hackerone.com/reports/245762
- **Submitted:** 2017-07-04
- **Reporter:** tanvi07
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** low
- **Vuln:** Cross-Site Request Forgery (CSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
Vulnerability Exploited : cross site scripting using csrf

Vulnerable URL:https://gratipay.com/search

Vulnerability Explanation :The application is vulnerable with Reflected Cross Site Scripting. Here                                        application fails to validate user supplied inputs due to which an attacker can inject his own JavaScript on your web application.  

Impact :The attacker can 

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

Vulnerability Exploited : cross site scripting using csrf

Vulnerable URL:https://gratipay.com/search

Vulnerability Explanation :The application is vulnerable with Reflected Cross Site Scripting. Here                                        application fails to validate user supplied inputs due to which an attacker can inject his own JavaScript on your web application.  

Impact :The attacker can access the victim's cookies associated with the website using document.domain, send them to his own server, and use them to hijack the session of target user. An attacker can also register a keyboard event listener using addEventListener and then send all of the user's keystrokes to his own server, potentially recording sensitive information such as passwords and credit card numbers. 

Payload : <script>alert(document.domain>

severity: high

step to reproduce:
1) login the URL https://gratipay.com.
2) go to search button.
3)use the proxy like burp suit.and intercept the request of search box.
4)generate the csrf code ,then after write in search to above payload.
5) csrf text file run in the browser 
6) you can see that cross site scripting.







</details>

---
*Analysed by Claude on 2026-05-24*
