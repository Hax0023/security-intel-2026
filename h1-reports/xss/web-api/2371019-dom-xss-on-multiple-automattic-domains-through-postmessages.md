# DOM XSS on Multiple Automattic Domains Through PostMessages via Jetpack Likes Feature

## Metadata
- **Source:** HackerOne
- **Report:** 2371019 | https://hackerone.com/reports/2371019
- **Submitted:** 2024-02-12
- **Reporter:** renniepak
- **Program:** Automattic
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** DOM-based Cross-Site Scripting (XSS), Insecure PostMessage Handler, Insufficient Input Validation, Improper Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A chained vulnerability combining DOM XSS on widgets.wp.com with an insecure postMessage listener in Jetpack's Likes feature enables arbitrary JavaScript execution on over 100,000 websites using Jetpack. The vulnerability exploits unvalidated URL parameters on the sharing-buttons-preview endpoint and fails to encode the avatar_URL parameter before inserting it into the DOM via innerHTML.

## Attack scenario
1. Attacker crafts a malicious URL with XSS payload in the custom[0][name] parameter targeting widgets.wp.com/sharing-buttons-preview
2. Attacker hosts a social engineering page linking to the malicious URL or embeds it in content
3. When a user clicks the link, the XSS executes on widgets.wp.com, giving attacker script execution in that origin context
4. Attacker's script sends a crafted postMessage to the parent window with malicious avatar_URL containing JavaScript payload
5. The Jetpack Likes postMessage listener accepts the message (origin check passes due to attacker's script running on widgets.wp.com)
6. The avatar_URL payload is inserted directly into DOM via innerHTML without encoding, executing XSS on the victim's website

## Root cause
Two compounding security issues: (1) DOM XSS on widgets.wp.com caused by lack of input validation and output encoding of URL parameters in the sharing-buttons-preview script, (2) Jetpack Likes feature's postMessage listener failing to encode the avatar_URL parameter before using it in innerHTML despite having origin validation, removing defense-in-depth encoding that existed in older versions

## Attacker mindset
An attacker would recognize that compromising a shared widget domain (widgets.wp.com) is highly valuable because it's trusted by thousands of downstream websites. By chaining the XSS on the widget domain with insecure postMessage handling, they achieve broad impact across all Jetpack installations. The removal of encoding from older versions suggests attackers might monitor for security regressions in popular plugins.

## Defensive takeaways
- Always validate and encode URL parameters, especially those used in template rendering or DOM manipulation
- Implement defense-in-depth: validate and encode data at multiple layers (input validation AND output encoding)
- Never insert untrusted data into innerHTML; use textContent or safely constructed DOM methods instead
- When handling postMessages, validate not only origin but also message structure, types, and content
- Encoding removed from older versions suggests security regression monitoring and continuous validation practices are essential
- Limit scope of shared widget domains; consider sandboxing iframe-based widgets with restrictive permissions
- For postMessage handlers receiving data that will be rendered, apply output encoding even if origin is validated
- Conduct security audits when making changes to security-sensitive code, especially when simplifying or removing encoders

## Variant hunting
Search for other postMessage listeners in Automattic properties that accept messages from widget domains without encoding rendered data
Audit other Jetpack features for similar patterns of unvalidated postMessage handling (comments, social, etc.)
Review widgets.wp.com for additional URL parameters susceptible to DOM XSS beyond the sharing-buttons-preview endpoint
Check other Automattic widget endpoints (gravatar, vip, etc.) for similar URL parameter injection vulnerabilities
Investigate if other WordPress.com plugins or themes have similar postMessage listeners with origin validation but missing output encoding
Search for instances where innerHTML is used with postMessage data across Automattic properties
Review git history for commits that removed or modified encoding functions in postMessage handlers

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1059.007 - Command and Scripting Interpreter: JavaScript
- T1566.002 - Phishing: Spearphishing Link
- T1200 - Traffic Redirection
- T1539 - Steal Web Session Cookie
- T1005 - Data from Local System
- T1602.001 - Data from Information Repositories: Confluence

## Notes
This report demonstrates the critical importance of supply chain security in web platforms. A vulnerability in a trusted widget domain (widgets.wp.com) becomes a blast radius affecting 100k+ downstream sites. The fact that encoding was present in older Jetpack versions but removed suggests either a refactoring mistake or misunderstanding of security implications. The reporter properly staged the vulnerability discovery by first identifying the widget XSS, then recognizing how it chains with the postMessage listener. The PoC effectively demonstrates cross-domain impact by showing XSS execution on wordpress.com and jetpack.com domains.

## Full report
<details><summary>Expand</summary>

Hi Automattic team,

I have found a 2 flaws that when combined lead to DOM XSS on every website that is using Jetpack with the [Likes](https://jetpack.com/support/likes/) feature enabled. 

The 2 flaws are respectively:

- A DOM XSS vulnerability on https://widgets.wp.com/sharing-buttons-preview/
- The Jetpack plugin creates a postMessage listener allowing messages from the "widgets.wp.com" origin, but will not validate nor encode the `avatar_url` parameter before applying it to the DOM causing XSS.

## Reproduction:

- Navigate to https://0-a.nl/jetpackxssclick.html?url=https://wordpress.com/blog/2024/01/31/http3/ and click the `PoC link`.

## Result

In the newly opened window a `alert(document.domain)` will pop on https://wordpress.com

{F3044196}

## Root causes

### XSS on widgets.wp.com

The DOM XSS here is caused by the following included script:

*https://widgets.wp.com/sharing-buttons-preview/js/preview.js*
```javascript
        if (_.isArray(r.custom)) {
            i = _.template(e("#tmpl-custom-button").html());
            s = _.map(r.custom, function(e) {
                var t = g.parseUrl(e.icon);
                return new d({
                    ID: e.name,
                    markup: i({
                        icon: o + "/" + t.host + t.pathname,
                        name: e.name
                    })
                })
            });
            n = n.concat(s)
        }
```
It's not that obvious because of the minified javascript but what happens is that 2 url parameters are parsed and used to add a UI element to the DOM:

?custom[0][icon]=iconurl&custom[0][name]=name

We can abuse the `name` parameter to create an XSS.

https://widgets.wp.com/sharing-buttons-preview/?custom[0][icon]=iconurl&custom[0][name]=%22%3E%3Cimg%20src%20onerror=alert()%3E

{F3044216}

### Insecure postMessage listener / codeblock

When we navigate to a website that has the Jetpack Likes feature enabled, a postMessage listener will be launched that will execute the `JetpackLikesMessageListener` function when a message arrives.

We can see it contains an origin check to only allow messages from widgets.wp.com. We can bypass this now since we have XSS on that domain:

```javascript
const allowedOrigin = 'https://widgets.wp.com';
	if ( allowedOrigin !== event.origin ) {
		return;
	}
```

When we follow the code to the `showOtherGravatars` case, you'll see it use a `liker.avatar_URL` parameter (that is received via a postMessage) directly with innerHTML. This will allow us to send a tampered postMessage causing the XSS to be triggered.

```javascript
element.innerHTML = `
				<a href="${ encodeURI( liker.profile_URL ) }" rel="nofollow" target="_parent" class="wpl-liker">
					<img src="${ liker.avatar_URL }"
						alt=""
						style="width: 28px; height: 28px;" />
					<span></span>
				</a>
				`;
```

## Mitigation

- Applying input validation and output encoding on the sharing-button page to mitigate the XSS https://widgets.wp.com/sharing-buttons-preview/
- Defence in depth: now any XSS on widgets.wp.com will lead to multiple XSSes all over the internet (anyone using the Jetpack Likes features). To mitigate this, I would also apply `encodeURI` to the avatar_url before using it in `innerHTML`. Upon further research it seemed older version of the plugin did exactly this, but in later versions this was removed.

## Impact

XSS on a number of Automattic domains:

https://0-a.nl/jetpackxssclick.html?url=https://wordpress.com/blog/2024/01/31/http3
https://0-a.nl/jetpackxssclick.html?url=https://jetpack.com/blog/wordpress-navigation-menu/

You probably have better insights in this (also I'd love to hear the actual number :) ) but searching publicwww.com revealed over 100k websites using this feature, meaning 100k domains vulnerable to this XSS.

This is also the reason I picked `High` for severity. If it was just wordpress.com I would probably have gone for `Medium` which is more typical for these kind of XSSes without providing more impact specific to the vulnerable domain. But in this case the vulnerability reaches far beyond the 1 domain.

In general, if an attacker can control a script that is executed in the victim's browser, then they can typically fully compromise that user. Amongst other things, the attacker can:

* Perform any action within the application that the user can perform.
* View any information that the user is able to view.
* Modify any information that the user is able to modify.

</details>

---
*Analysed by Claude on 2026-05-12*
