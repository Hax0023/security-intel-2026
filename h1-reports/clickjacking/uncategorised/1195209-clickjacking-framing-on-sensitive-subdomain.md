# Clickjacking/Framing on Sensitive Subdomain (cryptoeconomics.sifchain.finance)

## Metadata
- **Source:** HackerOne
- **Report:** 1195209 | https://hackerone.com/reports/1195209
- **Submitted:** 2021-05-13
- **Reporter:** ilxax1
- **Program:** Sifchain
- **Bounty:** Not specified in writeup
- **Severity:** High
- **Vuln:** Clickjacking, UI Redressing, Missing X-Frame-Options Header
- **CVEs:** None
- **Category:** uncategorised

## Summary
The cryptoeconomics.sifchain.finance subdomain lacks X-Frame-Options and Content-Security-Policy headers, allowing attackers to embed the page in an iframe and perform clickjacking attacks. Users can be tricked into performing unintended actions (credential submission, fund transfers) by overlaying transparent frames on decoy content.

## Attack scenario
1. Attacker creates a decoy website with attractive content (e.g., 'Click to Claim Free Crypto Tokens')
2. Attacker embeds the vulnerable cryptoeconomics.sifchain.finance page in a transparent iframe positioned over the clickable decoy content
3. Victim visits attacker's decoy website and clicks on the apparent legitimate button
4. The click actually targets hidden UI elements on the framed Sifchain page (e.g., transaction confirmation, login form fields)
5. Victim unknowingly submits sensitive data (passwords, wallet keys, transaction approvals) to the malicious overlaid form
6. Attacker captures credentials or completes fraudulent transactions with victim's authority

## Root cause
The application fails to implement proper frame-busting security headers (X-Frame-Options: DENY or SAMEORIGIN and Content-Security-Policy frame-ancestors directive). The sensitive subdomain is frameable by any external domain, enabling UI redressing attacks.

## Attacker mindset
Targeting a cryptocurrency/DeFi platform to harvest credentials, wallet keys, or trick users into authorizing unauthorized transactions. The financial nature and user trust in the domain make this high-value target for phishing-adjacent attacks.

## Defensive takeaways
- Implement X-Frame-Options: DENY header on all pages, especially sensitive subdomains handling authentication or transactions
- Configure Content-Security-Policy with frame-ancestors 'none' or 'self' directive
- Add frame-busting JavaScript as secondary defense: if (window.self !== window.top) { window.top.location = window.self.location; }
- Apply these headers at all layers (web server, CDN, application code)
- Conduct regular security audits specifically for framing vulnerabilities on financial/authentication pages
- Consider SameSite cookie attributes to limit session hijacking via clickjacking

## Variant hunting
Scan other Sifchain subdomains (app.sifchain.finance, staking.sifchain.finance, etc.) for identical frameable endpoints
Test if parent domain (sifchain.finance) has proper headers but subdomains do not
Check for partial protections that can be bypassed (e.g., JavaScript-only frame busters that fail with noopener)
Investigate if X-Frame-Options is set differently for different URI paths on the vulnerable subdomain
Test iframe sandbox attribute combinations to determine exploitation difficulty

## MITRE ATT&CK
- T1566.002 - Phishing: Spearphishing Link (via attacker's decoy domain)
- T1187 - Forced Authentication (capturing credentials via clickjacking overlay)
- T1040 - Network Sniffing (potential credential interception if overlay captures input)
- T1598.003 - Phishing for Information via Spearphishing Link

## Notes
The writeup lacks technical depth (no actual POC code/screenshots provided despite claiming them). The severity should be High rather than Critical because successful exploitation requires user interaction and social engineering. The mention of 'lookout.net/test/clickjack.html' as testing tool is outdated/deprecated. For cryptocurrency platforms, clickjacking on transaction/approval pages poses extreme financial risk and should be prioritized for remediation. The vulnerability is trivially exploitable and affects all users indiscriminately.

## Full report
<details><summary>Expand</summary>

Vulnerability Name  :  Clickjacking /framing 
Vulnerability Description  :  Clickjacking is an interface-based attack in which user is tricked into clicking on actionable content on a hidden website by 
                                                               clicking on some other content in a decoy website .

Vulnerable Url  : https://cryptoeconomics.sifchain.finance/ 

. Steps to reproduce :
 1 -  copy the url  :  https://cryptoeconomics.sifchain.finance/#sif10jatqfd88m8s2uhtdtdl3txtayjtzsve2klyhh&type=lm
 2 - Go to test the vulnerability by using : https://www.lookout.net/test/clickjack.html
 

 $ POC :
. Screenshots .

## Impact

The user assumes that they're entering their information into a usual form but they're actually entering it in fields the hacker has overlaid on the UI. Hackers will target passwords, credit card numbers and any other valuable data they can exploit .

</details>

---
*Analysed by Claude on 2026-05-24*
