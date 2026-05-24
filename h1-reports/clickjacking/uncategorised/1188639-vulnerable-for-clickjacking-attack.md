# Clickjacking Vulnerability - Missing X-Frame-Options Header

## Metadata
- **Source:** HackerOne
- **Report:** 1188639 | https://hackerone.com/reports/1188639
- **Submitted:** 2021-05-07
- **Reporter:** akay0783
- **Program:** Sifchain (sifchain.finance)
- **Bounty:** Not specified
- **Severity:** Medium
- **Vuln:** Clickjacking, UI Redress Attack, Missing Security Header
- **CVEs:** None
- **Category:** uncategorised

## Summary
The target website lacks the X-Frame-Options HTTP response header, allowing the page to be embedded in iframes on attacker-controlled sites. This enables clickjacking attacks where users can be tricked into performing unintended actions on the embedded page through UI redressing techniques.

## Attack scenario
1. Attacker creates a malicious webpage containing an iframe that loads the vulnerable sifchain.finance site
2. Attacker uses CSS styling to overlay transparent or opaque UI elements over the framed content to obscure the true target
3. Victim visits the attacker's webpage believing they are interacting with legitimate content
4. Victim clicks on what appears to be a benign button or link, but actually clicks on a hidden element within the framed sifchain.finance page
5. Hidden click triggers unintended action such as fund transfer, account modification, or sensitive data disclosure
6. Attack succeeds without victim awareness of the true target of their action

## Root cause
The web server fails to include the X-Frame-Options HTTP response header in server responses, which would prevent the page from being embedded in frames on other origins. This is a missing security control implementation.

## Attacker mindset
Attacker seeks to manipulate user interactions to perform actions on behalf of authenticated victims, targeting financial or sensitive operations. By hosting the attack on a trusted-looking domain and obscuring the true target, the attacker maximizes success rate while maintaining plausible deniability.

## Defensive takeaways
- Implement X-Frame-Options header set to 'DENY' or 'SAMEORIGIN' in all HTTP responses
- Alternatively, use Content-Security-Policy frame-ancestors directive for modern browsers
- Apply defense-in-depth by combining both X-Frame-Options and CSP headers
- Validate all sensitive operations require explicit user confirmation beyond simple clicks
- Implement SameSite cookie attributes to prevent session hijacking via cross-site requests
- Use JavaScript frame-busting code as secondary mitigation (breakout.js pattern)
- Monitor and alert on unusual cross-origin iframe embedding attempts

## Variant hunting
Check for missing X-Frame-Options on all subdomains and API endpoints
Test for bypasses using X-Frame-Options: ALLOW-FROM (deprecated) with origin variations
Verify CSP frame-ancestors directive is properly configured and not overly permissive
Identify other sensitive endpoints vulnerable to framing (login, payment, admin panels)
Test for clickjacking on form submission endpoints and state-changing operations
Check Content-Security-Policy directives for frame-ancestors: *; or similar bypasses

## MITRE ATT&CK
- T1190
- T1566.002

## Notes
This report is relatively straightforward - missing security header vulnerability. The impact depends on what sensitive actions users can perform on the vulnerable site. Financial/DeFi platforms like Sifchain represent high-value targets. The proof-of-concept is clear and reproducible. Report quality is moderate - lacks specific impact demonstration but clearly articulates the vulnerability. No evidence of actual exploitation provided, only theoretical risk demonstration.

## Full report
<details><summary>Expand</summary>

## Summary:
Hii Team,
I know that I have reported to you outside of Scope. The report is related to the mentioned company and the vulnerability can endanger your business so I  report this vulnerability to you.
Clickjacking (User Interface redress attack, UI redress attack, UI redressing) is a malicious technique of tricking a Web user into clicking on something different from what the user perceives they are clicking on, thus potentially revealing confidential information or taking control of their computer while clicking on seemingly innocuous web pages.
The server didn't return an X-Frame-Options header which means that this website could be at risk of a clickjacking attack. The X-Frame-Options HTTP response header can be used to indicate whether or not a browser should be allowed to render a page in a <frame> or <iframe>. Sites can use this to avoid clickjacking attacks, by ensuring that their content is not embedded into other sites.
This vulnerability affects the Web Server.

## Steps To Reproduce:
  1.Copy URL: https://sifchain.finance
  2. put the URL in the below code of the iframe

<html>
<head>
<title>Clickjack test page</title>
</head>
<body>
<p>Website is vulnerable to clickjacking!</p>
 <iframe src="https://sifchain.finance/" width="1000" height="600"></iframe>
</body>
</html>

  3. Observe that site is getting displayed in Iframe

## Impact

With a carefully crafted combination of stylesheets, iframes, and text boxes, a user can be led to believe they are typing in the password to their email or bank account, but are instead typing into an invisible frame controlled by the attacker.

</details>

---
*Analysed by Claude on 2026-05-24*
