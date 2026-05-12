# DOM XSS via Unencoded window.location.hash in jQuery Selector - Forescout Homepage

## Metadata
- **Source:** HackerOne
- **Report:** 704266 | https://hackerone.com/reports/704266
- **Submitted:** 2019-09-30
- **Reporter:** enesdexh1
- **Program:** Forescout
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** DOM-based XSS, Improper Input Validation, Unsafe jQuery Selector
- **CVEs:** None
- **Category:** web-api

## Summary
A DOM-based XSS vulnerability exists on forescout.com's homepage where user-controlled window.location.hash is directly injected into a jQuery selector without sanitization. The vulnerability is exploitable in Microsoft Edge and IE browsers due to their less strict URL encoding of hash fragments compared to Chrome and Firefox.

## Attack scenario
1. Attacker crafts a malicious URL: https://www.forescout.com/#<img src=x onerror=alert('XSS')>
2. Attacker sends the link to target victims via email, social engineering, or other phishing vectors
3. Target clicks the link in Internet Explorer or Microsoft Edge browser
4. JavaScript code executes: jQuery('a.fancybox-inline[href="' + window.location.hash + '"]:first')
5. The hash fragment is inserted directly into the jQuery selector string without encoding
6. Browser parses the selector as HTML, executing the onerror event handler with arbitrary JavaScript

## Root cause
The jQuery code directly concatenates window.location.hash into a CSS selector without HTML encoding or input validation. The hash value is user-controlled and not sanitized before being used in DOM manipulation. While Chrome and Firefox apply stricter URL encoding to hash fragments, IE and Edge allow raw HTML characters in the hash, making the payload viable.

## Attacker mindset
An attacker would recognize this as a low-hanging fruit DOM XSS vulnerability that requires only social engineering to deliver the payload. The attacker exploits browser-specific quirks (IE/Edge behavior) to bypass protections that would work in modern browsers. The attack is particularly effective because it appears to come from a legitimate forescout.com domain.

## Defensive takeaways
- Never directly concatenate user-controlled input (including window.location.hash, search params, etc.) into jQuery selectors or DOM manipulation methods
- Use textContent or innerText instead of innerHTML when setting dynamic content
- Implement HTML/JavaScript encoding for any user input before DOM insertion
- Use CSS selectors with proper escaping when user input is needed (jQuery.escapeSelector or similar utilities)
- Validate and sanitize all input from location object properties (hash, search, pathname)
- Implement Content Security Policy (CSP) to mitigate XSS impact
- Use a security-focused templating engine or framework that auto-escapes by default
- Test security implications across all supported browsers, not just modern ones

## Variant hunting
Search for other jQuery selectors using window.location properties without encoding: window.location.search, window.location.pathname
Look for innerHTML/insertAdjacentHTML usage with window.location hash/search
Identify other pages using similar jQuery 'fancybox' or modal popup patterns with URL-based selectors
Check for similar patterns in other Forescout properties or subdomains
Search codebase for regex patterns like jQuery\('.*?' \+ window\.location to find similar vulnerabilities
Test hash-based routing in single-page applications (SPAs) on the same domain

## MITRE ATT&CK
- T1190
- T1566
- T1598
- T1204

## Notes
This is a classic DOM XSS vulnerability with browser-specific exploitation requirements. The use of jQuery selectors as an attack vector is notable - many developers assume jQuery methods are safe, but improper concatenation can create security issues. The vulnerability is browser-dependent, making it interesting from a security research perspective but somewhat limited in real-world impact since modern browsers would be unaffected. However, many corporate environments still use IE/Edge, increasing the actual risk. The writeup is from 2019-2020 era when these issues were more common.

## Full report
<details><summary>Expand</summary>

## Summary:
I've found an DOM Based XSS on homepage 

## Steps To Reproduce:
1.Go to this url and you'll see alert pop
`https://www.forescout.com/#<img src=x onerror=alert('XSS')>`

But this will work just on ME/IE browsers because chrome and firefox have default encode system hash url

And vulnerable code is on your directly source code within jquery code. As you can see there is no encode in ==window.location.hash== code so when we open the page with #<img src=x onerror=alert(1)> it executes code.

`jQuery(window).load(function() {
    jQuery('a.fancybox-inline[href="' + window.location.hash + '"]:first').each(function() {
        jQuery(this).delay(700).trigger('click');
    });
});`

## Supporting Material/References:
I have uploaded a picture to show you POC


Regards 
Enesdex

## Impact

--Hacker can execute malicious codes in victim's browser
--Hacker can redirect user to malicious website
--Hacker can steal victim's cookies etc.

</details>

---
*Analysed by Claude on 2026-05-12*
