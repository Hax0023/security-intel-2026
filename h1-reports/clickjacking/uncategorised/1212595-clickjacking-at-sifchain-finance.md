# Clickjacking at sifchain.finance

## Metadata
- **Source:** HackerOne
- **Report:** 1212595 | https://hackerone.com/reports/1212595
- **Submitted:** 2021-05-29
- **Reporter:** manjithgowthaman
- **Program:** Sifchain
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Clickjacking, UI Redressing, Missing X-Frame-Options Header
- **CVEs:** None
- **Category:** uncategorised

## Summary
The sifchain.finance website is vulnerable to clickjacking attacks due to the absence of the X-Frame-Options HTTP response header. This allows attackers to embed the site within iframes on malicious pages and trick users into performing unintended actions. The vulnerability affects multiple URLs on the domain.

## Attack scenario
1. Attacker creates a malicious webpage and embeds sifchain.finance in a transparent iframe positioned over a fake login form or action button
2. Attacker overlays legitimate-looking UI elements (buttons, forms) using CSS to trick the user into clicking specific areas
3. User visits the malicious page believing they are interacting with legitimate content (e.g., claiming to check rewards or perform a transaction)
4. User's clicks are actually directed at the hidden sifchain.finance iframe, causing unintended actions like fund transfers, account changes, or credential submission
5. Attacker can harvest sensitive information or perform unauthorized actions on the user's sifchain account
6. If session cookies are present, the attacker can leverage the user's authenticated state to compromise the account

## Root cause
The web server is not implementing the X-Frame-Options HTTP response header, which is the primary defense mechanism against clickjacking attacks. Without this header, browsers allow the page to be framed in any context.

## Attacker mindset
An attacker would recognize that the absence of X-Frame-Options allows them to embed the financial platform in malicious contexts. For a DeFi/crypto platform like Sifchain, this could enable token theft, unauthorized transactions, or credential harvesting by overlaying deceptive UI elements on top of legitimate financial operations.

## Defensive takeaways
- Implement X-Frame-Options header with value 'DENY' or 'SAMEORIGIN' on all pages to prevent framing
- Add Content-Security-Policy header with frame-ancestors directive as an additional defense layer
- Implement frame-busting JavaScript to detect and break out of frames programmatically
- Use visual indicators (like frame-breaking scripts) to alert users if content is being displayed in an iframe
- Apply extra security measures for sensitive operations (fund transfers, account changes) such as additional confirmation prompts
- Regularly test web security headers using tools like Security Headers or Mozilla Observatory
- Consider implementing SameSite cookie attributes to limit exposure even if clickjacking succeeds
- Educate users about phishing and social engineering risks from seemingly legitimate-looking overlays

## Variant hunting
Search for other pages on sifchain.finance and related subdomains (trading interfaces, dashboard, account settings) that may also lack X-Frame-Options headers. Check for mobile versions and API endpoints that might return HTML responses. Test other crypto/DeFi platforms for similar oversights, particularly those handling token swaps or transactions where clickjacking impact would be highest.

## MITRE ATT&CK
- T1598.001
- T1566.002

## Notes
This is a straightforward clickjacking vulnerability with clear exploitation path. The PoC is basic but effective - simply embedding the site in an iframe demonstrates the vulnerability. For a financial/DeFi platform, the impact is significant as it could lead to unauthorized transactions. The fix is trivial (adding headers) but the security implications are substantial. The researcher provided good educational context but a more detailed impact scenario specific to Sifchain's functionality would have strengthened the report.

## Full report
<details><summary>Expand</summary>

Hi team,

While performing security testing of your website i have found the vulnerability called Clickjacking.

Many URLS are in scope and vulnerable to Clickjacking.

What is Clickjacking ?

Clickjacking (User Interface redress attack, UI redress attack, UI redressing) is a malicious technique of tricking a Web user into clicking on something different from what the user perceives they are clicking on, thus potentially revealing confidential information or taking control of their computer while clicking on seemingly innocuous web pages.

The server didn't return an X-Frame-Options header which means that this website could be at risk of a clickjacking attack. The X-Frame-Options HTTP response header can be used to indicate whether or not a browser should be allowed to render a page in a <frame> or <iframe>. Sites can use this to avoid clickjacking attacks, by ensuring that their content is not embedded into other sites.
This vulnerability affects Web Server.

Steps to Reproduce / POC

Vulnerable Urls:

https://sifchain.finance/

Put every above url one by one in the code of iframe, which is given below

<!DOCTYPE HTML>

<html lang="en-US">
<head>
<meta charset="UTF-8">
<title>I Frame</title>
</head>
<body>
<h3>clickjacking vulnerability</h3>
<iframe src="https://sifchain.finance/" height="550px" width="700px"></iframe>
</body>
</html>

Notice that site is visible in the Iframe

POC is in the attachments. Thanks, waiting for your response.

## Impact

Using a similar technique, keystrokes can also be hijacked. With a carefully crafted combination of stylesheets, iframes, and text boxes, a user can be led to believe they are typing in the password to their email or bank account, but are instead typing into an invisible frame controlled by the attacker.

</details>

---
*Analysed by Claude on 2026-05-24*
