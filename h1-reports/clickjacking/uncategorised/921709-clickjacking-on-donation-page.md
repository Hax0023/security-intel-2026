# Clickjacking on WordPress Foundation Donation Page

## Metadata
- **Source:** HackerOne
- **Report:** 921709 | https://hackerone.com/reports/921709
- **Submitted:** 2020-07-12
- **Reporter:** b0d8e6c576cada9bb87be7b
- **Program:** WordPress Foundation
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Clickjacking/UI Redressing, Missing X-Frame-Options Header, Missing Content-Security-Policy Frame-Ancestors
- **CVEs:** None
- **Category:** uncategorised

## Summary
The WordPress Foundation donation page (wordpressfoundation.org/donate/) lacks clickjacking protection headers, allowing attackers to embed the page in an iframe and overlay malicious content. An attacker can trick victims into performing unintended actions such as donating to the attacker's payment gateway instead of the legitimate charity.

## Attack scenario
1. Attacker creates a malicious webpage with an embedded iframe of the donation page, positioned with opacity manipulation or transparent overlay
2. Attacker overlays deceptive UI elements (buttons, text) that appear to perform one action but actually trigger donation submission to attacker's payment gateway
3. Victim is lured to the malicious page through phishing email, social engineering, or misleading advertisements
4. Victim believes they are interacting with legitimate content but clicks on attacker's overlay button
5. Donation is processed to the attacker's PayPal or payment processor account instead of WordPress Foundation
6. Victim's financial information and trust in the charity organization is compromised

## Root cause
The donation page fails to implement X-Frame-Options header or Content-Security-Policy frame-ancestors directive, allowing unrestricted embedding in iframes on attacker-controlled domains. The server does not restrict where the page can be framed.

## Attacker mindset
Exploit trust in charitable organizations to intercept donations intended for legitimate causes. Leverage the credibility of the WordPress Foundation brand to social engineer victims into donating to attacker-controlled payment accounts. Potential motivation includes financial fraud, demonstrating vulnerability for extortion, or testing social engineering effectiveness.

## Defensive takeaways
- Implement X-Frame-Options: DENY or X-Frame-Options: SAMEORIGIN header on all pages, especially sensitive ones like donation pages
- Deploy Content-Security-Policy with frame-ancestors directive set to 'none' or 'self' depending on business requirements
- Apply clickjacking defenses consistently across all user-facing pages, not just obvious targets
- Conduct regular security testing for clickjacking vulnerabilities as part of standard vulnerability assessments
- Educate users about the risks of clicking on suspicious links and to verify URLs before completing sensitive transactions
- Implement additional UI protections such as user confirmation dialogs for financial transactions
- Monitor for malicious iframes embedding legitimate donation pages as indicators of active attacks

## Variant hunting
Search for similar clickjacking vulnerabilities on other charity/NGO donation pages, government payment portals, banking sites, and e-commerce checkout flows. Test for missing frame-ancestors CSP directives and X-Frame-Options headers on all pages handling sensitive user interactions (login, payment, account modification).

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1566 - Phishing
- T1598 - Phishing for Information
- T1204 - User Execution

## Notes
Reporter demonstrated responsible disclosure by providing proof-of-concept code and recommendations. The vulnerability is particularly critical for donation pages as it directly impacts financial transactions and organizational trust. The reporter explicitly requested removal of their PayPal payment request ID from submitted files, showing ethical consideration during vulnerability testing.

## Full report
<details><summary>Expand</summary>

## Description:

Vulnerable URL: https://wordpressfoundation.org/donate/

Clickjacking on the vulnerable URL allows an attacker to redirect a victim to do a donation at an attacker's page.

## Steps To Reproduce:

1)  To test whether the page is vulnerable to clickjacking or not use this code

<!DOCTYPE HTML>
<html lang="en-US">
<head>
<meta charset="UTF-8">
<meta http-equiv="refresh" content="5">
<title>i Frame</title>
</head>
<body>
<center><h1>THIS PAGE IS VULNERABLE TO CLICKJACKING</h1>
<iframe src="https://wordpressfoundation.org/donate/" frameborder="0 px" height="1200px" width="1920px"></iframe>
</center>
</body>
</html>

2) To test whether an attacker is able to trick the victim to donate money to the attacker's payment gateway
             i) Open the attached page "donation.html "
             ii) Click on the button give once
             iii) The page will be redirected to the attacker's PayPal money request page.

*Sorry for the bad UI and please remove my payment-request id after the vulnerability check from donation.html page.

## Recommendations

To control where your site can be embedded, use the frame-ancestors directive:
Content-Security-Policy: frame-ancestors 'none'  (The page cannot be displayed in a frame, regardless of the site attempting to do so.)
Content-Security-Policy: frame-ancestors 'self' (The page can only be displayed in a frame on the same origin as the page itself.)
Content-Security-Policy: frame-ancestors *uri* (The page can only be displayed in a frame on the specified origins.)

## Impact

If an attacker is successful in tricking the victim to a click jacked page. He can trick the victim to donate money to the attacker's account. An attacker may also craft a page to gather victim's information, He may use also use BEEF hook id to take control of victim's browser.

</details>

---
*Analysed by Claude on 2026-05-24*
