# Clickjacking Vulnerability in topechelon.com Main Domain

## Metadata
- **Source:** HackerOne
- **Report:** 2964441 | https://hackerone.com/reports/2964441
- **Submitted:** 2025-01-29
- **Reporter:** genz-1
- **Program:** HackerOne
- **Bounty:** Not specified in report
- **Severity:** medium
- **Vuln:** Clickjacking, UI Redressing, Missing X-Frame-Options Header, Missing CSP frame-ancestors Directive
- **CVEs:** None
- **Category:** uncategorised

## Summary
The topechelon.com domain is vulnerable to clickjacking attacks due to missing X-Frame-Options and Content-Security-Policy headers, allowing attackers to embed the site in transparent iframes and trick users into unintended actions. An attacker can overlay deceptive UI elements on top of an invisible iframe to manipulate user interactions, potentially leading to account takeover, credential theft, or unauthorized operations.

## Attack scenario
1. Attacker creates a malicious HTML page containing an invisible or semi-transparent iframe pointing to topechelon.com
2. Attacker overlays deceptive UI elements (buttons, forms) on top of the iframe positioned to align with sensitive target elements
3. Attacker tricks a logged-in user into visiting the malicious page through social engineering or phishing
4. When the user interacts with the visible deceptive elements, clicks are actually captured by the hidden iframe targeting sensitive functions
5. The victim unknowingly performs actions on their topechelon.com account such as changing settings, approving transactions, or submitting sensitive forms
6. Attacker achieves account compromise, credential theft, or other unauthorized modifications

## Root cause
The web application fails to implement HTTP security headers (X-Frame-Options and Content-Security-Policy frame-ancestors) that prevent the site from being embedded in iframes, allowing arbitrary third-party domains to frame the application's content.

## Attacker mindset
An attacker exploiting this vulnerability seeks to manipulate legitimate user sessions without their knowledge. The attacker leverages the trust users have in the legitimate domain by creating convincing deceptive interfaces that trick users into performing unintended actions on their accounts. This is a classic social engineering combined with technical exploitation approach.

## Defensive takeaways
- Implement X-Frame-Options header set to DENY or SAMEORIGIN on all sensitive pages
- Add Content-Security-Policy header with frame-ancestors directive set to 'self' or specific trusted domains only
- Deploy frame-busting JavaScript as an additional defense-in-depth layer (though not primary mitigation)
- Regularly audit HTTP security headers across entire application using automated scanning tools
- Test all user-facing pages for clickjacking vulnerability using browser developer tools and PoC pages
- Implement additional protections for sensitive operations (re-authentication, CAPTCHAs, confirmation dialogs)
- Monitor for suspicious referrer patterns indicating potential clickjacking attacks
- Educate users about risks of clicking on untrusted links and unexpected dialogs

## Variant hunting
Search for other topechelon.com subdomains and endpoints without proper framing protections. Check if any sensitive functionality pages (login, payment, account settings, admin panels) lack X-Frame-Options headers. Test for partial CSP implementations that may have bypasses. Look for legacy pages that may have been overlooked during security implementations.

## MITRE ATT&CK
- T1189
- T1566
- T1598
- T1187
- T1040

## Notes
The PoC demonstrates a straightforward but effective attack. Clickjacking is categorized as medium severity rather than high because it requires user interaction and is contingent on the user being logged in or authenticated. However, in contexts involving sensitive operations (payment approvals, account deletion), this could escalate to high severity. The report provides clear remediation steps aligned with OWASP and industry best practices. HackerOne report reference: 2964441

## Full report
<details><summary>Expand</summary>

## **Summary:**  
The target website is vulnerable to Clickjacking, a web-based attack that tricks users into interacting with a hidden or disguised iframe. Attackers can exploit this vulnerability to manipulate user actions, potentially leading to unauthorized activities such as unintended clicks, form submissions, or credential theft.  

## **Steps to Reproduce:**  
1. **Create an HTML page** embedding the target website using an `<iframe>`.  
2. **Modify CSS** to make the iframe transparent or overlay it with deceptive UI elements.  
3. **Host the HTML page** and trick users into interacting with it.  

## **Proof of Concept (PoC):**  
```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Clickjacking PoC</title>
<style>
    iframe {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        opacity: 0.6; /* Makes the iframe invisible */
        z-index: 99;
    }

    button {
        z-index: 100;
        top:400px;
        position: relative;
    }
    h1 {
        top: 300px;
        position: relative;

    }
</style>
</head>
<body>
<h1>Click the button for a surprise!</h1>
<button onclick="alert('Surprise!')">Click Me!</button>

<!-- Invisible iframe targeting the account deletion URL -->
<iframe id="target-frame" src="https://topechelon.com/" frameborder="0"></iframe>

<script>
    
    document.getElementById('target-frame').onload = function() {
        
        console.log('Iframe has loaded, ready for clickjacking.');
    };
</script>
</body>
</html>
```
{F4001108}

## Impact

- **User Account Takeover:** If a logged-in user interacts with the iframe, attackers could force unintended actions.  
- **Phishing Attacks:** Users may unknowingly enter sensitive credentials.  
- **Malicious Actions:** Attackers can exploit user interactions to modify settings, submit forms, or perform other unintended operations.  

## **Recommended Mitigation:**  
To prevent Clickjacking attacks, implement the following security measures:  

1. **Use the X-Frame-Options HTTP Header:**  
   - `X-Frame-Options: DENY` (Prevents embedding in iframes).  
   - `X-Frame-Options: SAMEORIGIN` (Allows iframes only from the same domain).  

2. **Use Content Security Policy (CSP) Frame-Ancestors Directive:**  
   - `Content-Security-Policy: frame-ancestors 'self'`  

3. **JavaScript-Based Frame Busting (as an additional security measure):**  
   ```javascript
   if (window.top !== window.self) {
       window.top.location = window.self.location;
   }

</details>

---
*Analysed by Claude on 2026-05-24*
