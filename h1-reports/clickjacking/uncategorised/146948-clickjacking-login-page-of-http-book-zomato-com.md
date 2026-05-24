# Clickjacking vulnerability on book.zomato.com login page

## Metadata
- **Source:** HackerOne
- **Report:** 146948 | https://hackerone.com/reports/146948
- **Submitted:** 2016-06-24
- **Reporter:** benoculars
- **Program:** Zomato
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Clickjacking, UI Redressing, Missing X-Frame-Options Header
- **CVEs:** None
- **Category:** uncategorised

## Summary
The login page at book.zomato.com/account/login.aspx lacks X-Frame-Options HTTP header protection, allowing attackers to embed the page in an iframe for clickjacking attacks. An attacker could overlay transparent or disguised elements to trick users into unintended actions while appearing to interact with legitimate Zomato content.

## Attack scenario
1. Attacker creates a malicious HTML page embedding the Zomato login iframe within deceptive visual content
2. Attacker hosts the page on a controlled domain or distributes it via phishing links
3. Victim visits the attacker's page believing they are on a legitimate site
4. Victim attempts to click on what appears to be harmless content (e.g., 'Click to claim prize')
5. The click actually targets the overlaid login button or form within the Zomato iframe
6. Victim unknowingly submits credentials or performs unintended actions on the Zomato site

## Root cause
The web server does not set the X-Frame-Options HTTP response header to prevent the page from being framed, allowing any origin to embed the login page in an iframe without restriction

## Attacker mindset
An attacker would target the login page specifically because it's high-value for credential harvesting. The clickjacking vector allows bypassing same-origin policy restrictions and tricking authenticated users into performing sensitive actions without realizing it.

## Defensive takeaways
- Implement X-Frame-Options header with DENY or SAMEORIGIN value on all sensitive pages
- Add Content-Security-Policy frame-ancestors directive as a modern alternative
- Implement frame-busting JavaScript as defense-in-depth (though not primary mitigation)
- Apply clickjacking protections especially to authentication and payment pages
- Use SameSite cookie attributes to limit exposure even if clickjacking occurs
- Implement user interaction confirmation for sensitive operations

## Variant hunting
Check other subdomains (www.zomato.com, api.zomato.com) for same issue
Test payment/checkout pages for clickjacking vulnerability
Verify if restaurant booking forms have X-Frame-Options protection
Check account settings and profile modification pages
Test password reset flow for clickjacking protection
Audit all pages handling financial transactions

## MITRE ATT&CK
- T1566.002 - Phishing: Spearphishing Link
- T1189 - Drive-by Compromise
- T1598.003 - Phishing for Information: Spearphishing Link

## Notes
This is a straightforward clickjacking vulnerability with simple proof-of-concept. The fix is well-established and requires minimal development effort. The vulnerability is particularly dangerous on login pages as it could enable credential theft or session hijacking. The report demonstrates good understanding of the vulnerability but provides minimal detail on actual impact (no evidence of credential theft or unauthorized actions).

## Full report
<details><summary>Expand</summary>

The login page on book.zomato.com (http://book.zomato.com/account/login.aspx) is vulnerable to a clickjacking attack.

### Reproduction steps:

1. Paste the following HTML into a text editor and save the file as .html

```
<html>
<body>
<iframe src="http://book.zomato.com/account/login.aspx" width="500" height="500">
</body>
</html>
```

2. Open the file in a web browser
3. Note that the iframe appears with the login page inside

### Remediation:
Using the X-Frame-Options header.

OWASP: https://www.owasp.org/index.php/Clickjacking_Defense_Cheat_Sheet




</details>

---
*Analysed by Claude on 2026-05-24*
