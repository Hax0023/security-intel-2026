# Clickjacking Vulnerability - Missing X-Frame-Options Header

## Metadata
- **Source:** HackerOne
- **Report:** 688546 | https://hackerone.com/reports/688546
- **Submitted:** 2019-09-05
- **Reporter:** paramdham
- **Program:** Outpost
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Clickjacking, UI Redress Attack, Missing Security Headers
- **CVEs:** None
- **Category:** uncategorised

## Summary
The target website is vulnerable to clickjacking attacks due to missing X-Frame-Options HTTP headers, allowing attackers to embed the site within iframes on malicious pages. An attacker can overlay invisible frames to trick users into performing unintended actions such as adding arbitrary tasks or performing other sensitive operations.

## Attack scenario
1. Attacker creates a malicious HTML page that embeds the vulnerable Outpost application within an invisible iframe
2. Attacker overlays clickable UI elements (buttons, links) on top of the framed content, positioned to align with sensitive actions in the embedded application
3. Attacker hosts the malicious page and tricks users into visiting it through social engineering, phishing, or watering hole attacks
4. Unsuspecting user clicks on what they believe is a legitimate button or link on the attacker's page
5. The click actually targets the hidden frame, performing unintended actions on the Outpost application (e.g., changing preferences, adding tasks)
6. User's account performs malicious actions without their knowledge or consent

## Root cause
The web application fails to implement the X-Frame-Options HTTP response header, which is the primary defense mechanism against clickjacking. Without this header, the browser allows the page to be embedded in iframes on any origin, enabling the attack vector.

## Attacker mindset
An attacker exploits the lack of framing restrictions to perform unauthorized actions on behalf of authenticated users. The attack is attractive because it requires no complex exploitation, works cross-domain, and can be scaled across many victims through widespread distribution of the malicious page.

## Defensive takeaways
- Implement X-Frame-Options header with appropriate value (DENY, SAMEORIGIN, or ALLOW-FROM for specific trusted origins) on all HTTP responses
- Use Content-Security-Policy (CSP) frame-ancestors directive as a modern alternative/supplement to X-Frame-Options
- Apply frame-busting JavaScript code as a secondary defense layer
- Implement SameSite cookie attribute to prevent CSRF-like attacks via clickjacking
- Audit all pages and endpoints to ensure consistent security header implementation across the entire application
- Test for clickjacking vulnerabilities during security testing and integrate into CI/CD pipeline

## Variant hunting
Check for missing X-Frame-Options on administrative panels and sensitive function pages
Test if CSP frame-ancestors directive is properly configured when X-Frame-Options is present
Look for pages that explicitly allow framing (ALLOW-FROM with overly permissive origins)
Verify if the header is missing only on certain endpoints or globally
Test for bypass techniques using different framing methods (object, embed, picture tags)
Check if the application implements frame-busting JavaScript that can be bypassed

## MITRE ATT&CK
- T1566.002 - Phishing: Spearphishing Link (distribution vector)
- T1548 - Abuse Elevation Control Mechanism (performing privileged actions via clickjacking)
- T1204.1 - User Execution: Malicious Link (user clicks on crafted page)

## Notes
This is a classic and well-documented vulnerability. The PoC is straightforward and demonstrates the vulnerability clearly. The impact varies depending on what actions are available to users on the target application - with authenticated users, the impact could be significant (changing settings, adding tasks, modifying data). The fix is simple (adding one HTTP header) but requires comprehensive implementation across the entire application.

## Full report
<details><summary>Expand</summary>

##Summary

Clickjacking (User Interface redress attack, UI redress attack, UI redressing) is a malicious technique of tricking a Web user into clicking on something different from what the user perceives they are clicking on, thus potentially revealing confidential information or taking control of their computer while clicking on seemingly innocuous web pages.

Websites are at risk of a clickjacking attack when they allow content to be embedded within a frame.

An attacker may use this risk to invisibly load the target website into their own site and trick users into clicking on links which they never intended to. An "X-Frame-Options" header should be sent by the server to either deny framing of content, only allow it from the same origin or allow it from a trusted URIs.


##Proof of concept code :- 

Copy the above code and paste it in notepad and save it with .html extention
and open it in browser

```
<html> 
<head> 
<title>Clickjack test page</title> 
</head> 
<body> 
<p>Website is vulnerable to clickjacking!</p>

<iframe src="https://app.outpost.co/settings/preferences"  sandbox="allow-top-navigation allow-same-origin allow-scripts" width="500" height="500"></iframe> 

</body> 
</html>
```

Copy and paste above given code and  save it with hack.html and  open it in browser




##Recommendation :- 

Add X-FRAME-OPTIONS header to mitigate the issue

## Impact

It allows remote attackers to do some clickjacking which can be used for adding arbitrary tasks . Why? Almost all of your page has missing X-FRAME-OPTIONS header.


##Thanks

</details>

---
*Analysed by Claude on 2026-05-24*
