# Reflected Cross-Site Scripting (XSS) in MTN Investor Search Functionality

## Metadata
- **Source:** HackerOne
- **Report:** 1496897 | https://hackerone.com/reports/1496897
- **Submitted:** 2022-03-01
- **Reporter:** alitoni224
- **Program:** MTN Investor Relations (mtn-investor.com)
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Reflected Cross-Site Scripting (XSS), Input Validation Failure, Output Encoding Failure
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability exists in the search functionality of mtn-investor.com/mtn-cmd/index.php where user-supplied input containing the payload '-alert(1)-' is reflected back without proper sanitization or encoding. An attacker can craft malicious URLs to execute arbitrary JavaScript in victims' browsers, potentially leading to session hijacking, cookie theft, or credential harvesting.

## Attack scenario
1. Attacker crafts a malicious URL containing XSS payload in the search parameter: https://mtn-investor.com/mtn-cmd/index.php?search='-alert(1)-'
2. Attacker distributes the malicious link via phishing emails, social media, or compromised websites targeting MTN Investor Relations users
3. Victim clicks the link and visits the vulnerable page while authenticated to MTN Investor Relations
4. The JavaScript payload executes in the victim's browser within the context of the mtn-investor.com domain
5. Attacker's injected script accesses sensitive session cookies, authentication tokens, or form data
6. Attacker leverages stolen credentials or session tokens to impersonate the victim or redirect them to phishing pages

## Root cause
The search parameter in the index.php file is reflected directly in the HTTP response without proper input validation, sanitization, or HTML/JavaScript encoding. The application fails to implement security controls such as Content Security Policy (CSP), input filtering, or context-appropriate output encoding.

## Attacker mindset
An opportunistic attacker targeting a financial/investor relations website seeks to compromise user sessions and steal sensitive information. The simplicity of the vulnerability (basic alert box payload) suggests the attacker is testing for low-hanging fruit in automated or manual reconnaissance. The targeting of a financial institution indicates potential motivation for credential theft, insider trading information, or lateral movement into corporate networks.

## Defensive takeaways
- Implement strict input validation: whitelist allowed characters and reject or sanitize special characters (quotes, angle brackets, semicolons)
- Apply context-appropriate output encoding: HTML-encode all user-controlled data reflected in HTML context, use JavaScript encoding for JavaScript context
- Implement Content Security Policy (CSP) headers with strict directives to prevent inline script execution
- Use security-focused templating engines that auto-escape output by default
- Conduct regular security code reviews focusing on data flow from input to output
- Perform dynamic security testing (DAST) and static analysis (SAST) in CI/CD pipeline
- Implement httpOnly and Secure flags on session cookies to prevent JavaScript access
- Educate developers on OWASP Top 10 and secure coding practices for XSS prevention

## Variant hunting
Search for similar reflected XSS patterns in other parameters of the same endpoint (sorting, filtering, pagination), other pages within /mtn-cmd/ directory, and related subdomains. Test for DOM-based XSS in client-side JavaScript that processes URL parameters. Check for stored XSS if the search functionality stores user input in databases. Test other financial/investor relations endpoints for similar input validation gaps.

## MITRE ATT&CK
- T1190
- T1598
- T1566
- T1056
- T1539
- T1110

## Notes
The writeup lacks severity quantification and potential business impact assessment specific to a financial institution. The reporter provided minimal technical detail (payload '-alert(1)-' appears unusual; typically single or double quotes are used). No evidence of WAF/filtering bypass techniques attempted. The vulnerability is straightforward but high-impact given the sensitive nature of investor relations platforms. No timeline or remediation status provided by program. Consider whether the search functionality is accessible to unauthenticated users, which would increase attack surface.

## Full report
<details><summary>Expand</summary>

## Summary:
[cross site scripting reflected]

## Steps To Reproduce:
[at first hello
[Found that via the script site payload is reflected  '-alert(1)-' It was tested on Chrome and Firefox browsers as shown in the pictures below   ]

  1. [Simply open the link https://mtn-investor.com/mtn-cmd/index.php ]
  1. [In the search button, enter the payload  '-alert(1)-'  ]
  1. [You will notice the reflection]

## Supporting Material/References:
[list any additional material (e.g. screenshots, logs, etc.)]

  * [https://owasp.org/www-community/attacks/xss/]

## Impact

As in any vulnerability via scripted sites. The top line is that an attacker might steal cookies to abuse users' session.
- phishing scam
- Some important input data stolen

</details>

---
*Analysed by Claude on 2026-05-12*
