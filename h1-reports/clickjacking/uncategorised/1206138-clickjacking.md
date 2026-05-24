# Clickjacking via Missing X-Frame-Options Header on Sifchain Finance

## Metadata
- **Source:** HackerOne
- **Report:** 1206138 | https://hackerone.com/reports/1206138
- **Submitted:** 2021-05-23
- **Reporter:** whiteraven0101
- **Program:** Sifchain Finance
- **Bounty:** Not specified
- **Severity:** Medium
- **Vuln:** Clickjacking, UI Redressing, Missing Security Headers
- **CVEs:** None
- **Category:** uncategorised

## Summary
Multiple Sifchain Finance domains lack X-Frame-Options headers, allowing attackers to embed the site in iframes and perform clickjacking attacks. An attacker can trick users into performing unintended actions such as approving transactions, transferring funds, or delegating stake through transparent or hidden overlays.

## Attack scenario
1. Attacker creates a malicious website embedding Sifchain Finance DEX interface in an iframe
2. Attacker overlays transparent clickable elements or hides the iframe with opacity controls
3. Victim visits attacker's malicious site believing they are on a legitimate service
4. Victim clicks on what appears to be harmless content but actually clicks hidden buttons on the Sifchain DEX
5. Unintended actions execute such as swap transactions, liquidity provision, or stake delegation
6. Victim's funds or delegated tokens are transferred without their knowledge or consent

## Root cause
The application fails to implement proper frame-busting mechanisms by not setting the X-Frame-Options HTTP response header to DENY or SAMEORIGIN, allowing the site to be embedded in third-party iframes without restriction.

## Attacker mindset
An attacker recognizes that financial DeFi platforms are high-value targets. By embedding the DEX interface invisibly, they can trick users into executing transactions (swaps, liquidity pools, staking) that directly transfer funds or grant token approvals to attacker-controlled addresses.

## Defensive takeaways
- Implement X-Frame-Options: DENY or SAMEORIGIN headers on all pages to prevent framing
- Alternatively, use Content-Security-Policy frame-ancestors directive as modern replacement
- Implement frame-busting JavaScript as secondary defense: if (window.self !== window.top) { window.top.location = window.self.location; }
- Use SameSite cookie attributes to prevent CSRF exploitation in clickjacking scenarios
- Implement visual indicators or warnings when users are performing sensitive actions
- Apply input validation and require explicit user confirmation for critical transactions
- Monitor and log transaction patterns to detect suspicious activity

## Variant hunting
Search for other endpoints on *.sifchain.finance domains lacking frame-options; test admin panels, governance voting interfaces, and token management pages; check sister projects or related smart contract frontends for same vulnerability pattern.

## MITRE ATT&CK
- T1189
- T1566

## Notes
This is a straightforward clickjacking vulnerability in a financial DeFi application. While the reporter's proof-of-concept is basic (simple iframe embedding), the real impact is significant given Sifchain's DEX nature where unintended swaps, liquidity additions, or stake delegations result in direct financial loss. The vulnerability affects multiple critical user-facing endpoints. Severity should be Medium to High depending on program's impact assessment for financial fraud. The report demonstrates lack of security headers implementation across the domain.

## Full report
<details><summary>Expand</summary>

Bug Bounty Report(Vulnerability Report)

Vulnerability Name:  UI Redressing (Clickjacking)

Vulnerability Description:  Clickjacking (classified as a User Interface redress attack, UI redress attack, UI redressing) is a malicious technique of tricking a user into clicking on something different from what the user perceives, thus potentially revealing confidential information or allowing others to take control of their computer while clicking on seemingly innocuous objects, including web pages.Clickjacking is an instance of the confused deputy problem, wherein a computer is tricked into misusing its authority.

Summery: The below listed links, dont have X-FRAME-OPTIONS set to DENY or SAMEORIGIN so they are vulnerable to clickjacking

Vulnerable Website: https://sifchain.finance/

Beowser Verified in:Firefox[Version: 78.3.0esr (64-bit)]

Steps To Reproduce: 
       i. Here are the steps to reproduce the attack:
     1.Run the bellow code from browser and you can see that the website is vulnerable to clickjacking attack
<!doctype html>
<html>
 <head> 
  <style>
      iframe{
        width:500px;
        height:900px;
      }
      #http{
        height:900px;
        width:500px;
      }
  </style> 
 </head> 

 <body> 
  <h1>--------------------This is a malicious website-------------------</h1>
  <h1>The vulnerable website:-</nn></h1>
  <iframe src="https://sifchain.finance/"></iframe>
  <iframe id="http" src="https://dex.sifchain.finance/#/peg"></iframe>
 </body>
</html>

this html code can embed these urls  on another malicious website whice can be harmful for 
users.


Following links are vulnerable to Clickjacking:
1.https://sifchain.finance/
2.https://dex.sifchain.finance/#/peg
3.https://blockexplorer.sifchain.finance/voting-power-distribution
4.https://blockexplorer.sifchain.finance/transactions
5.https://dex.sifchain.finance/#/stake-delegate
6.https://dex.sifchain.finance/#/swap
7.https://dex.sifchain.finance/#/pool/add-liquidity
8.etc.

## Impact

Here are the impacts of the vulnerability:
 1.with this vulnerability attackers can control or hijack users clicks
2.Affect the users interaction on your platform. Such unintended behavior is definitely not wanted by any user.
3.Such effect upon your users could significantly harm your overall reputation and customer loss.
4.Using a similar technique, keystrokes can also be hijacked. With a carefully crafted combination of stylesheets, iframes, and text boxes, a user can be led to believe they are typing in the password to their email or bank account, but are instead typing into an invisible frame controlled by the attackerp

</details>

---
*Analysed by Claude on 2026-05-24*
