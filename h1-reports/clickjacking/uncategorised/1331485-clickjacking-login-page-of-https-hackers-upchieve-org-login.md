# Clickjacking vulnerability on UPchieve login page

## Metadata
- **Source:** HackerOne
- **Report:** 1331485 | https://hackerone.com/reports/1331485
- **Submitted:** 2021-09-06
- **Reporter:** sara346
- **Program:** UPchieve
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Clickjacking, UI Redressing, Missing X-Frame-Options Header
- **CVEs:** None
- **Category:** uncategorised

## Summary
The login page at https://hackers.upchieve.org/login is vulnerable to clickjacking attacks due to missing X-Frame-Options headers, allowing attackers to frame the page and deceive users into performing unintended actions. An attacker can overlay the login form with transparent elements or misleading content to trick users into revealing credentials and sensitive information.

## Attack scenario
1. Attacker creates a malicious webpage with an invisible iframe containing the legitimate UPchieve login page
2. Attacker overlays transparent or visually deceptive elements on top of the framed login form
3. Victim visits the attacker's webpage, believing they are interacting with legitimate content (e.g., clicking a button to 'claim prize')
4. Victim's clicks are actually directed to the hidden login form fields within the iframe
5. Attacker captures the victim's username, password, and other credentials entered into the framed login page
6. Attacker gains unauthorized access to victim's UPchieve account and associated sensitive information

## Root cause
The application fails to implement X-Frame-Options HTTP response header or Content-Security-Policy directives to prevent the page from being framed by external domains. This allows attackers to embed the login page in their own websites.

## Attacker mindset
An attacker recognizes that the login page lacks frame protection mechanisms and exploits this to conduct social engineering attacks. They understand that users are likely to enter sensitive credentials when interacting with what appears to be a legitimate interface, making credential theft highly effective.

## Defensive takeaways
- Implement X-Frame-Options header set to 'DENY' or 'SAMEORIGIN' on all pages, especially authentication pages
- Deploy Content-Security-Policy header with frame-ancestors directive restricting framing to same-origin only
- Consider adding JavaScript frame-breaking code as a secondary defense layer
- Implement CSRF tokens on login forms to prevent unauthorized submissions
- Use SameSite cookie attributes on session cookies to limit cross-site cookie transmission
- Monitor for suspicious framing attempts using JavaScript checks

## Variant hunting
Check other authentication pages (password reset, registration) for the same vulnerability
Test registration and password reset flows for clickjacking susceptibility
Verify if HTTPS-enforced pages are still vulnerable to mixed content clickjacking
Test for variants using different frame-based attacks (SVG embedding, object tags, embed tags)
Check if sensitive pages like account settings or payment pages have the same protection gap

## MITRE ATT&CK
- T1190
- T1566
- T1598
- T1111

## Notes
Clickjacking on authentication pages represents a critical security gap as it directly leads to account compromise. The vulnerability is trivial to exploit and requires minimal technical skill. This report appears to be from the HackerOne platform's vulnerability disclosure program for UPchieve.

## Full report
<details><summary>Expand</summary>

Hello, you have discovered this unprotected login page
https://hackers.upchieve.org/login
An attacker can 
in frame page
in iframe 
and Deception of a user and obtaining a password, email and sensitive information

## Impact

An attacker can  
aDeception of a user and obtaining a password, email and sensitive information

</details>

---
*Analysed by Claude on 2026-05-24*
