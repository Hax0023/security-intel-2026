# Self DOM-Based XSS in www.hackerone.com Contact Form

## Metadata
- **Source:** HackerOne
- **Report:** 406587 | https://hackerone.com/reports/406587
- **Submitted:** 2018-09-06
- **Reporter:** adac95
- **Program:** HackerOne
- **Bounty:** Not specified
- **Severity:** Medium
- **Vuln:** DOM-based Cross-Site Scripting (XSS), Unsafe innerHTML Usage, Client-side Input Validation Bypass
- **CVEs:** None
- **Category:** web-api

## Summary
A DOM-based XSS vulnerability exists in the HackerOne contact form triggered via URI fragment (#contact/). The vulnerable 'strip()' function uses innerHTML to parse user input, allowing event handler execution. Exploitation is mitigated by CSP but remains viable in browsers with CSP disabled or bypassed.

## Attack scenario
1. Attacker crafts malicious payload containing HTML with event handlers (e.g., <img src=x onerror=alert(1) />)
2. Attacker tricks user into navigating to www.hackerone.com/#contact/ via phishing or social engineering
3. User pastes attacker's payload into the 'Message' textarea field
4. User clicks 'send message' button, triggering form submission
5. JavaScript strip() function executes, parsing payload via innerHTML property
6. Browser attempts to execute inline JavaScript event handler; CSP blocks execution in modern browsers, but succeeds if CSP is disabled

## Root cause
The strip() function uses innerHTML to parse user input before extracting text content. While the intent is HTML removal, innerHTML inherently executes JavaScript within the parsed HTML (event handlers, script tags). This creates a DOM-based XSS vulnerability exploitable client-side before any server-side validation occurs.

## Attacker mindset
Attacker recognizes that the strip() function is ineffective security control and exploitable through social engineering. Attacker understands that CSP is the only mitigation and targets users with older browsers or disabled CSP. Attacker also notes that even if strip() worked, server-side validation is absent, allowing request interception via Burp Suite to inject payloads.

## Defensive takeaways
- Never use innerHTML with user input; use textContent, innerText, or DOM APIs instead
- Implement server-side input validation and sanitization; client-side controls are bypassable
- Use established sanitization libraries (DOMPurify, etc.) rather than custom implementations
- Do not rely solely on CSP as a defense; it should complement, not replace, proper input handling
- Validate form data on the server before processing or storing; never trust client-side validation
- Consider whether HTML stripping is necessary; if not, reject rather than sanitize user input
- Use Content Security Policy as defense-in-depth, but assume it may be bypassed or disabled

## Variant hunting
Search for other use of innerHTML with user-controlled variables across codebase
Identify all URI fragment handlers (#contact/, #login/, etc.) and review input handling
Test other form fields beyond textarea for similar DOM-XSS patterns
Review Marketo integration endpoints for similar unsafe JavaScript patterns
Check for event handler injection via data attributes (data-*, on* attributes)
Test with SVG payloads and other vectors bypassing img onerror filters
Examine if CSP can be bypassed via nonce injection or trusted inline sources

## MITRE ATT&CK
- T1190
- T1566
- T1204.001

## Notes
Vulnerability is classified as 'self' XSS because execution occurs in the attacker's own session after social engineering, not affecting other users directly. CSP presence demonstrates security awareness but insufficient as sole mitigation. The strip() function reinforces the misconception that client-side validation provides security. Report demonstrates good practice in explaining bypass methods (Burp Suite interception) and CSP disablement testing.

## Full report
<details><summary>Expand</summary>

**Summary:**
There is a 'self' DOM-based cross-site scripting vulnerability in the contact form available on the www.hackerone.com website. This could allow an attacker to perform cross-site scripting, or other client-side attacks, against users of the application. However, the risk presented by this issue is significantly reduced because exploitation would require an element of social engineering to succeed, and the website's Content Security Policy (CSP) blocked the execution of inline scripts.

**Description:**
The HackerOne contact form is automatically displayed when the string  'contact/' is detected in the URI fragment on any page under the www.hackerone.com domain (for example, https://www.hackerone.com/#contact/). When the 'submit' button is clicked, the following JavaScript functions are executed:

```javascript
//Marketo Form Code
function strip(html) {
    var tmp = document.createElement("DIV");
    tmp.innerHTML = html;
    return tmp.textContent || tmp.innerText || "";
}

$('form').submit(function() {
    $('textarea').val(function() {
        return strip($(this).val());
    });
});
```
The 'submit' event handler passes the current value of any 'textarea' elements to the 'strip' function. This function creates a new 'div' element, sets the 'innerHTML'  property to the provided value, and then returns the 'textContent' property of the resulting div. This type of code is typically used to remove HTML tags from a string, as the textContent property contains the String which was rendered by the browser when the HTML was parsed. (A reference to this exact function was also found on Stack Overflow: https://stackoverflow.com/questions/12941663/removing-html-tags-from-a-string-and-keeping-colon) 

However , this particular method is inherently insecure because it uses 'innerHTML'. When user input is provided to the 'innerHTML' property, it is parsed by the web browser and can therefore lead to the execution of malicious JavaScript. A screenshot has been attached to this report showing the result in the web browser when the following payload was typed into the 'Message' textarea of the HackerOne contact form, and the 'send message' button was clicked:

```html
<img src=x onerror=alert(1) />
```
The developer console (in Google Chrome) displayed two errors - one which stated that https://www.hackerone.com/x was requested and returned a 404 (due to the src attribute of the img tag), and another which reported a violation of the website's CSP. This second error occurred because the browser attempted to execute the JavaScript code in the 'onerror' attribute, but the website's CSP did not allow it. Performing the same actions in a browser with CSP disabled allowed the JavaScript in the 'onerror' attribute to execute.

An attacker could exploit this vulnerability by convincing a user (ideally with a browser which does not support CSP) to paste a malicious payload into the 'message' field of the contact form and then click the 'send message' button.

It should also be noted that, if the 'strip' function was implemented to prevent an attacker from sending malicious HTML to Marketo or the server, it can be trivially bypassed using an intercepting proxy tool such as Burp Suite. By intercepting the HTTP request sent once the form submission is complete, any HTML 'stripped' by the JavaScript can simply be replaced. In light of this, developers should consider whether the 'strip' function is required - any validation or sanitization should  be performed by the server, where it cannot be influenced by an attacker.

If the 'strip' function is required, it is recommended that it is replaced with a solution which does not require the use of 'innerHTML'. A suitable alternative may be the use of a regex to remove common HTML characters.

### Steps To Reproduce

1. Open the https://www.hackerone.com/#contact/ page and open the browser's developer tools
2.  Type "<img src=x onerror=alert(1) />" into the 'message' textarea
3.  Click the 'send message' button
4. Check the developer console to view the two errors

(alternatively, disable CSP in your web browser and repeat the steps above. The JavaScript code 'alert(1)' should execute)

## Impact

The attacker could achieve XSS in the www.hackerone.com website.

</details>

---
*Analysed by Claude on 2026-05-12*
