# wp-embed XSS on Safari via postMessage javascript: URI Bypass

## Metadata
- **Source:** HackerOne
- **Report:** 1238528 | https://hackerone.com/reports/1238528
- **Submitted:** 2021-06-20
- **Reporter:** zoczus
- **Program:** WordPress
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Cross-Site Scripting (XSS), Improper Input Validation, Browser-Specific Vulnerability
- **CVEs:** None
- **Category:** web-api

## Summary
A Safari-specific XSS vulnerability exists in WordPress embed functionality where the postMessage handler fails to properly validate URI schemes before setting top-level location. Attackers can craft malicious embedded posts that execute arbitrary JavaScript on victim WordPress sites by exploiting Safari's non-standard handling of javascript: URIs in anchor element host parsing.

## Attack scenario
1. Attacker sets up a malicious WordPress instance and modifies the embed.php template to extract the embed secret from the iframe's location hash
2. Attacker creates a blog post on their WordPress site and publishes it to obtain a valid embed URL
3. Victim WordPress site administrator embeds the attacker's blog post into their own site using WordPress's embed feature
4. The embedded iframe loads on victim's site; attacker's malicious JavaScript sends a postMessage with message type 'link' and a crafted javascript: URI that passes Safari's hostname validation
5. WordPress's receiveEmbedMessage handler validates the hostname using Safari's non-standard URL parsing, which incorrectly extracts the attacker's domain from the javascript: URI
6. The handler sets window.top.location.href to the javascript: URI, executing arbitrary code in the victim site's top window context

## Root cause
The embed postMessage handler implements hostname validation by creating anchor elements and comparing the 'host' property. Safari has non-standard behavior where javascript: URIs with embedded domain names (e.g., javascript://attacker.com/code) return the embedded domain as the host value, bypassing the security check. Other browsers correctly return empty string for javascript: scheme, preventing exploitation.

## Attacker mindset
The attacker recognized a browser-specific implementation detail in URL parsing logic. Rather than attacking the authorization model (which requires knowing the secret), the attacker found that Safari's URL parser handles URI schemes differently, allowing the attacker to satisfy the hostname validation check while injecting a javascript: protocol execution vector.

## Defensive takeaways
- Implement URI scheme whitelisting (only allow http:// and https://) in postMessage handlers before any location.href assignment
- Avoid relying on anchor element properties for security-critical validation, as browser behavior varies; use explicit URL parsing and validation
- Consider using URL constructor API with try-catch for robust protocol validation across all browsers
- Apply Content-Security-Policy to restrict script-src and prevent javascript: URI execution
- Test security controls against all major browsers and Safari specifically, as implementation details can vary significantly
- Use URL.parse() or similar standardized methods rather than DOM manipulation for parsing untrusted URLs

## Variant hunting
Test other data: URIs and blob: URIs for similar Safari parsing quirks in postMessage handlers
Search for other instances where embed.php or similar files use postMessage to modify top.location
Test vimeo, youtube, and other third-party embed implementations for similar hostname validation bypasses
Check for Safari-specific handling in other postMessage handlers that validate origins using anchor element properties
Test whether other URI schemes with embedded domains (e.g., data: with embedded URLs) bypass validation in Safari
Examine other WordPress plugins that handle cross-origin communication via postMessage

## MITRE ATT&CK
- T1190
- T1657
- T1185

## Notes
This vulnerability demonstrates how browser-specific implementation details in URI parsing can introduce security bypass opportunities. The attack requires user interaction (embedding a post) and knowledge of the embed secret, but the secret is derived from the iframe's location hash and is transmitted in the iframe's src attribute. The reporter provided a working proof-of-concept and clear remediation advice. CVE assignment was requested but not confirmed in the report content.

## Full report
<details><summary>Expand</summary>

Hello! I'd like to report an XSS vulberability which works only on Safari browser (and maybe on others which I didn't checked. It defo doesn't work on both Chrome and Firefox). The other requirement which need to be met is attacker's blog post being embed on destination (victim) blog. 

## Analysis

Let's take a look to the core of problem - JavaScript postMessage handler: 

```javascript
     if (c.wp.receiveEmbedMessage = function(e) {
            var t = e.data;
            if (t)
                if (t.secret || t.message || t.value)
                    if (!/[^a-zA-Z0-9]/.test(t.secret)) {
                        for (var r, a, i, s = d.querySelectorAll('iframe[data-secret="' + t.secret + '"]'), n = d.querySelectorAll('blockquote[data-secret="' + t.secret + '"]'), o = 0; o < n.length; o++)
                            n[o].style.display = "none";
                        for (o = 0; o < s.length; o++)
                            if (r = s[o],
                            e.source === r.contentWindow) {
                                if (r.removeAttribute("style"),
                                "height" === t.message) {
                                    if (1e3 < (i = parseInt(t.value, 10)))
                                        i = 1e3;
                                    else if (~~i < 200)
                                        i = 200;
                                    r.height = i
                                }
                                if ("link" === t.message)
                                    if (a = d.createElement("a"),
                                    i = d.createElement("a"),
                                    a.href = r.getAttribute("src"),
                                    i.href = t.value,
                                    i.host === a.host)
                                        if (d.activeElement === r)
                                            c.top.location.href = t.value
                            }
                    }
        }
```

Things need to be noticed: 

- Secret need to be known (but it's provided as location.hash of embed webpage, so it's not a problem)
- Only content window can send postMessages (which is cool, as it's attacker website)
- If **message** attribute of postMessage data has `link` value - crazy things are happening
- most important ```c.top.location.href = t.value``` where `t` is postMessage data controlled by attacker. 

The last point obviously can lead to XSS if attacker will use ```javascript:alert(document.domain)``` as `t.value`, however - before it happen important check is made:

```javascript
     if (a = d.createElement("a"),
                                    i = d.createElement("a"),
                                    a.href = r.getAttribute("src"),
                                    i.href = t.value,
                                    i.host === a.host)
```

This code checks if **hostname** provided in ```t.value``` is the same as **hostname** of embed page. It create `<a>` element, but `t.value` as `href` attribute and then - takes `host` attribute of created URL. This approach is of course way better than some regexp magic ;-) but there's a behavior specific in Safari browser:

```
> var a = document.createElement("a")
> a.href="javascript://google.com/%0aalert(document.domain);//"
> console.log(a.host)
< google.com
```

All other browsers return empty string in case of using `javascript:` scheme, but not Safari. :) This could lead attacker to use `javascript` schema and execute javascript code in top window (victim's blog)


## Steps To Reproduce:

1. Get evil wordpress instance ;-) 
2. Edit `wordpress/wp-includes/theme-compat/embed.php` file and add your custom HTML code:

```html
<script>
if(document.location.hash.indexOf("secret") != -1) {
  secret = document.location.hash.split("=")[1];
  window.top.postMessage({"secret":secret,"message":"link","value":"javascript://"+document.location.host+"/%0aalert(document.domain);//"},"*");
}
</script>
```
3. Create any post on attacker blog, publish it and get it's URL.
4. On victim wordpress site (Safari) add new post with embed post from victim wordpress
5. Alert executed. :) 

Sample blogpost that can be embedded: `https://ropchain.org/lab/wordpress/2021/06/20/embed-me/`

## Recommendations

It's recommended to also validate schema of links and allow only HTTP / HTTPS links in postMessages.

## Impact

Ability to execute JavaScript code on wordpress page which embeded attacker's blogpost. 

Please assign CVE identifier to this vulnerability. While crediting it, please use:

*Jakub Żoczek, Senior Security Researcher @ Securitum [https://securitum.pl/](https://securitum.pl/)*

All the best!

</details>

---
*Analysed by Claude on 2026-05-12*
