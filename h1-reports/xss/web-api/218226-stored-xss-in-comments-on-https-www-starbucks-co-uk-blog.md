# Stored XSS in Blog Comments via WAF Bypass on Starbucks UK

## Metadata
- **Source:** HackerOne
- **Report:** 218226 | https://hackerone.com/reports/218226
- **Submitted:** 2017-04-02
- **Reporter:** bayotop
- **Program:** Starbucks
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Stored Cross-Site Scripting (XSS), Insufficient Input Validation, WAF Bypass
- **CVEs:** None
- **Category:** web-api

## Summary
A stored XSS vulnerability exists in the blog comment functionality on Starbucks UK website where the 'author' parameter is not properly HTML-encoded before being rendered in comments. An attacker can bypass the WAF protection by using alternative event handler attributes like 'onbeforescriptexecute' instead of the blocked 'onload' or 'onerror' variants, allowing arbitrary JavaScript execution in victim browsers.

## Attack scenario
1. Attacker identifies that blog comments accept user input via the /blog/addcomment endpoint
2. Attacker discovers that the 'author' parameter is rendered without proper HTML encoding in published comments
3. Attacker identifies WAF blocks direct <script> tags and common on* event handlers (onload, onerror, etc.)
4. Attacker crafts malicious payload using alternative event handler (onbeforescriptexecute) combined with custom HTML tag to bypass WAF filters
5. Attacker submits comment with payload: '</li></ul></li></ul></div></div></div></div><test/onbeforescriptexecute=confirm`h1poc`>'
6. Payload persists in database and executes in all users' browsers when viewing the compromised blog post

## Root cause
The application implements incomplete output encoding and relies on a blacklist-based WAF that does not account for all possible HTML event handlers. The 'author' field is inserted into HTML context without proper escaping, and the WAF only blocks well-known event attributes rather than enforcing a whitelist approach or implementing context-aware encoding.

## Attacker mindset
The attacker researched and documented multiple WAF bypass techniques by testing alternative event handlers that achieve the same XSS outcome. They demonstrated thorough knowledge of HTML event handlers and modern browser capabilities, methodically bypassing security controls through enumeration rather than brute force. The attacker responsibly disclosed the issue while providing comprehensive remediation guidance and even attempted to minimize damage by noting multiple test payloads.

## Defensive takeaways
- Always output-encode user input based on context (HTML encoding for HTML context, JavaScript encoding for JS context, URL encoding for URLs)
- Never rely solely on WAF blacklists - use whitelist approaches or parameterized output methods instead
- Consider using Content Security Policy (CSP) with strict directives to mitigate XSS impact
- Implement server-side validation and sanitization using established libraries (e.g., OWASP Java Encoder, DOMPurify)
- Derive author information from authenticated session rather than accepting it as user input
- Use security-focused templating engines that enforce automatic context-aware encoding
- Conduct comprehensive testing of all HTML event handlers, not just common ones
- Implement regular security audits and WAF rule review with threat modeling for bypass techniques

## Variant hunting
Test other event handlers on various HTML elements: onload, onmouseover, ontouchstart, onwheel, onscroll, onwheel
Attempt payloads on different HTML elements (div, span, img, svg, iframe) which may have different event handler support
Check if other user input fields (comment body, email) have similar encoding issues
Test for DOM-based XSS if comment data is processed client-side
Verify if similar comment functionality exists on other Starbucks regional sites or subdomains
Attempt to chain with CSRF to automate malicious comment submission
Test mutation XSS (mXSS) techniques that bypass HTML parsers

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1598 - Phishing - Search Open Websites/Domains
- T1566 - Phishing - Spearphishing via Web
- T1059 - Command and Scripting Interpreter

## Notes
The reporter demonstrated exceptional security research methodology by documenting the WAF bypass technique comprehensively and providing a list of alternative event handlers. The use of closing tags to escape from the existing HTML structure shows advanced payload crafting. The report notes contamination from multiple test payloads on the live site, suggesting real-time verification. Report ID 218226 from HackerOne indicates this was a legitimate disclosure program.

## Full report
<details><summary>Expand</summary>

Hi,

there are a lot of published blog post under https://www.starbucks.co.uk/blog/*. You can find plenty of them using this google dork `site:www.starbucks.co.uk inurl:blog/`. Notice the comments functionality at the bottom at the page.

When a comment is sent the following request is made:
```http
POST /blog/addcomment HTTP/1.1
Host: www.starbucks.co.uk
User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0
Accept: text/html, */*; q=0.01
Accept-Language: en-US,en;q=0.5
X-NewRelic-ID: VQUHVlNSARACV1JSBAIGVA==
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
X-Requested-With: XMLHttpRequest
Referer: https://www.starbucks.co.uk/blog/setting-the-record-straight-on-starbucks-uk-taxes-and-profitability
Content-Length: 321
Cookie: [redacted]
Connection: close

Body=Nice&ParentId=0&PostID=1241&author=ope67164%40disaq.com
```
The values of the `Body` and `author` parameters will be rendered into the page as a new comment. The value from the `author` parameter is not correctly encoded. This allows to inject arbitrary valid HTML.

You seem to be using a WAF which will block request (500) containing `<script></script>` and various input matching `on*=`.  However, I managed to find a bypass:

```html
</li></ul></li></ul></div></div></div></div><test/onbeforescriptexecute=confirm`h1poc`>
```

This will work on latest FF as can be seen here: https://www.starbucks.co.uk/blog/setting-the-record-straight-on-starbucks-uk-taxes-and-profitability

Note that the closing tags are just to make the script execute (I'm sorry for the multiple payloads on that site, once the above comment was sent, all previous attempts started to work. Would be great if you could clean up the comments at the end).

Here is a list of all potential `on*=` events I could find, that will bypass your WAF an can be used to create cross-browser payloads:

```
onsearch
onwebkitanimationiteration
onwebkitanimationstart
onanimationiteration
onwebkitanimationend
onanimationstart
ondataavailable
ontransitionend
onanimationend
onreceived
onpopstate
```

To fix this issue make sure the `author` value is correctly encoded. It could be also taken from the current user's session instead of the POST data. Also I recommend adding the aforementioned events to your WAF blacklist.

Please let me know in case you need any more information from my side. 

</details>

---
*Analysed by Claude on 2026-05-12*
