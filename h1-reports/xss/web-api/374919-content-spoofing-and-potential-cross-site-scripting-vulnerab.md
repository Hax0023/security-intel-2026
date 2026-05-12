# Content Spoofing and Cross-Site Scripting via Unvalidated postMessage Handler on HackerOne

## Metadata
- **Source:** HackerOne
- **Report:** 374919 | https://hackerone.com/reports/374919
- **Submitted:** 2018-07-01
- **Reporter:** suresh1c
- **Program:** HackerOne
- **Bounty:** Unknown (not specified in report)
- **Severity:** high
- **Vuln:** Cross-Site Scripting (XSS), Content Spoofing, Improper Input Validation, Insecure postMessage Implementation
- **CVEs:** None
- **Category:** web-api

## Summary
HackerOne's integration with a third-party Drift chat script (hp9revvwkk62.js) contains a vulnerable postMessage handler that lacks origin validation and contains a logic flaw in the window opener check. An attacker can exploit this to send arbitrary messages and potentially inject malicious content or execute XSS payloads, allowing manipulation of page events and spoofing of legitimate HackerOne content.

## Attack scenario
1. Attacker creates a malicious webpage (e.g., othertest45.azurewebsites.net/ddd.html) that opens a popup window to www.hackerone.com
2. Attacker's webpage uses postMessage API to send crafted messages to the HackerOne window without origin verification
3. The vulnerable handleMessage function in the Drift script accepts the message because e.source===window.opener evaluates to true due to the logic flaw
4. Attacker sends messages that trigger page events or inject content (including XSS payloads like url("javascript:alert(1);")
5. The injected content is rendered on HackerOne, potentially defacing the page or stealing user data
6. Users visiting HackerOne see spoofed content or malicious messages appearing to come from HackerOne, damaging reputation and trust

## Root cause
The postMessage handler in the third-party Drift script fails to validate the message origin and contains a flawed conditional check (e.source===window.opener) that allows cross-domain messages from any window opener. Additionally, the subsequent handling of the message data lacks proper sanitization, enabling XSS injection.

## Attacker mindset
An attacker would seek to exploit the trust users place in HackerOne's domain to deliver phishing content, defacement, or credential harvesting. The attacker recognizes that postMessage is a common vector when origin validation is missing and leverages the window.opener relationship to bypass basic checks. They may also test various XSS payloads to circumvent CSP restrictions.

## Defensive takeaways
- Always validate the origin of postMessage events using e.origin check, not just e.source comparisons
- Implement strict whitelist of allowed origins (e.g., only your own domain)
- Avoid trusting e.source===window.opener as a security control; explicitly verify e.origin against expected domains
- Sanitize and validate all data received via postMessage before using it in DOM operations
- Audit third-party scripts (especially chat/analytics libraries) for postMessage handlers and security misconfigurations
- Implement Content Security Policy (CSP) headers with nonce/hash to prevent inline script execution
- Use iframe sandbox attributes to restrict capabilities of embedded third-party content
- Regular security audits of external script dependencies and their update status

## Variant hunting
Similar vulnerabilities likely exist in other HackerOne integrations with third-party services. Hunt for: (1) other postMessage handlers lacking origin validation in Drift or competitor chat libraries, (2) unvalidated window.opener checks in other widgets/iframes, (3) similar logic flaws in other third-party analytics or support tools, (4) postMessage handlers that rely solely on source comparison without origin validation across the web.

## MITRE ATT&CK
- T1190
- T1189
- T1566
- T1566.002
- T1598
- T1598.003

## Notes
The vulnerability is compounded by HackerOne's reliance on a third-party Drift script over which they may have limited control. However, HackerOne should still audit third-party scripts or request patches from Drift. The PoC demonstrates practical exploitability. The attacker notes that XSS may be partially mitigated by CSP but bypasses exist (e.g., url() payloads). This is a supply chain security issue affecting a high-profile security platform.

## Full report
<details><summary>Expand</summary>

**Summary:**
           Hackerone.com using following script file 
https://js.driftt.com/include/1530431100000/hp9revvwkk62.js
you can see the below script on page
this.handleMessage=function(e){if(e&&e.data){var t=document.getElementById(Si);if(t&&(e.source===t.contentWindow||e.source===window.opener)){
handleMessage method used for handle the cross domain windows messaging

here missing validation of origin and the condition e.source===window.opener always true 
So attacker can handle all  the events in that page

### Steps To Reproduce
Pocurl: https://othertest45.azurewebsites.net/ddd.html
Load the PoC url and enable popup always
click the button on page it will trigger events and you can see  modification on page

XSS may be blocked due to recent content security policy but url("javascript:alert(1);") is valid payload

To fix the issue remove the condition e.source===window.opener or validate the origin

## Impact

Attacker can perform all the events and action given on that javascript page.
and display vulnerable content or message it will damage the reputation of hackerone

</details>

---
*Analysed by Claude on 2026-05-12*
