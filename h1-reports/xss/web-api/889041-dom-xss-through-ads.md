# DOM XSS through Unsafe Ad Injection via URL Parameter

## Metadata
- **Source:** HackerOne
- **Report:** 889041 | https://hackerone.com/reports/889041
- **Submitted:** 2020-06-02
- **Reporter:** bemodtwz
- **Program:** Urban Dictionary
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** DOM-based Cross-Site Scripting (XSS), Unsafe use of document.write(), Improper Input Validation, Unsafe JavaScript String Concatenation
- **CVEs:** None
- **Category:** web-api

## Summary
Multiple ad networks hosting ads on urbandictionary.com are vulnerable to DOM XSS through improper handling of the page URL. The pwt.js script's displayCreative function injects the containing page's URL into JavaScript strings without proper escaping, allowing attackers to break out of string context via single quote characters in the URL fragment. An attacker can inject arbitrary JavaScript by crafting a malicious URL that executes with the victim's origin context.

## Attack scenario
1. Attacker crafts a malicious URL containing JavaScript payload in the fragment: https://www.urbandictionary.com/define.php?term=#asdf'-alert(document.domain)-'asdf
2. Attacker distributes the URL via phishing, social media, or other vectors to target users
3. Victim clicks the link and visits the page, which loads ad network scripts including pwt.js
4. The displayCreative function retrieves the page URL and embeds it unsafely into a JavaScript string: url='https://...#asdf'-alert(document.domain)-'asdf'
5. The single quote in the payload breaks out of the string context, allowing arbitrary JavaScript execution
6. Malicious script executes under www.urbandictionary.com origin, potentially accessing authenticated sessions, modifying page content, or performing actions on behalf of the victim

## Root cause
The pwt.js script's displayCreative function uses document.write() to inject ads into the page and includes the referring page's full URL (including fragment/hash) as a parameter within a JavaScript string without proper escaping or sanitization. The use of single quotes as string delimiters combined with unescaped user-controlled input (URL fragment) creates an exploitable context for breaking out of the string literal.

## Attacker mindset
An attacker would recognize that ad networks frequently pass page URLs as parameters for tracking and context purposes. By identifying that the URL is embedded directly into executable JavaScript without escaping, the attacker can craft payloads using quote characters to escape the string context and inject arbitrary code. The attacker leverages the ad network's trust relationship with the host site to execute code under the legitimate origin.

## Defensive takeaways
- Never use document.write() with unsanitized or user-controlled content; consider using safer DOM manipulation methods like innerHTML with proper escaping or textContent
- Always URL-encode or properly escape user-controlled data when embedding it into JavaScript string literals; use JSON.stringify() or similar safe serialization methods
- Implement Content Security Policy (CSP) headers with strict script-src directives to mitigate XSS impact by restricting inline script execution
- Sanitize and validate the referring page URL before embedding it into ad scripts; strip fragment identifiers or validate against expected patterns
- Use modern ad loading mechanisms that don't rely on document.write() which is deprecated and inherently unsafe
- Implement regular security audits of third-party ad network scripts and their parameter handling
- Consider subresource integrity (SRI) or content security policy to control what ad networks can execute
- Educate ad network partners on secure coding practices regarding parameter injection and string escaping

## Variant hunting
Look for similar vulnerabilities in other ad networks that accept page URL parameters, particularly those using document.write() or similar unsafe DOM manipulation. Check for other URL parameters passed to ad scripts (referrer, callback functions, redirect URLs, user identifiers). Examine other ad libraries on the same site that may have similar parameter injection patterns. Test ad parameters with various encoding and quote characters (double quotes, backticks, template literals) to find alternative escape vectors.

## MITRE ATT&CK
- T1190
- T1203
- T1539
- T1566

## Notes
The vulnerability's reliability depends on which ad loads, suggesting multiple ad networks are affected. The use of URL fragments (#) to inject payloads is clever as it's not typically logged or filtered server-side. The reporter notes that CORS restrictions on the sister domain (urbandictionary.store) limit the immediate impact of credential theft, but the XSS still allows session hijacking, account takeover, and malicious content injection. The Eval Villain Firefox extension mentioned could be useful for detecting similar unsafe eval/write patterns in other sites.

## Full report
<details><summary>Expand</summary>

Multiple ads hosted on www.urbandictionary.com make the www.urbandictionary.com origin vulnerable to DOM XSS.  Attached is an image of `alert(document.domain)` executing. The injection works in Firefox and Chrome.

Visiting the following URL will **probably** cause an alert box displaying the  document.domain as www.urbandictionary.com.
`https://www.urbandictionary.com/define.php?term=#asdf'-alert(document.domain)-'asdf`

I say "probably" because the exploit depends on the loading of certain ads. Doing this from a fresh browser session usually causes the alert box. If not refreshing the page a few times, allowing the page to fully load, usually causes the pop-up. It all depends on which ad loads.

It appears the `pwt.js` JavaScript file uses the `displayCreative` function to display a unique ad. This apparently is done by executing `document.write` in an anonymous function to write the ad into the  the www.urbandictionary.com page. Visiting the above link will cause one of the ads to execute `document.domain` with a string that contains the following:

```
<script type='text/javascript'>
url='https://vap3ord1.lijit.com/res/sovrn.containertag.new.min.js…252de1&loc=https://www.urbandictionary.com/define.php?term=#asdf'-alert(document.domain)-'',
```
Many ads want a reference to the website that is loading them, so they inject the URL of the hosting page into the ad source. Since the vulnerable inject the containing page into a JavaScript single quote string, a single quote can be used to escape out of the string. This results in the JavaScript alert function being called.

The stack trace for the above injection follows:
```
    <anonymous> (index):2
    displayCreative pwt.js:11048
    displayCreative pwt.js:13098
    displayCreative pwt.js:10759
    <anonymous> define.php:1
    apply define.php:347
    <anonymous> (index):2
    <anonymous> (index):2
    Caspr (index):2
    Caspr (index):2
    casprInvocation (index):3
    <anonymous> (index):8
    <anonymous> (index):8
```

Multiple ads contain the nearly the same vulnerability. The stack trace is always the same.  The string passed to `document.domain` is different depending on the ad. I will try to include a few examples by attaching files showing the entire content being passed to `document.write`.  

 I obtained the strings passed to `document.domain` using the Eval Villain extension for Firefox, which I developed. This extension may assist you in finding the cause of the vulnerability, or verifying it's existence.

## Impact

DOM XSS allows an attacker to run arbitrary JavaScript under you origin. Since users can authenticate to this origin, an attacker could use this to perform actions in behalf of a victim using the victim session. I  have not yet authenticated to the site, so I don't know exactly what all that would entail.

An attacker could use this vulnerability to add malicious or inappropriate content to your website or takeover the ads seen there. 

So far, it appears the urbandictionary.store does **not** grant the vulnerable origin any CORS privileges. This means an attacker most likely can NOT steal credit card information or modify purchases.

</details>

---
*Analysed by Claude on 2026-05-12*
