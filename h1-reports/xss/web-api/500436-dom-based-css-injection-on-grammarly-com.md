# DOM-based CSS Injection via extcss Parameter on grammarly.com

## Metadata
- **Source:** HackerOne
- **Report:** 500436 | https://hackerone.com/reports/500436
- **Submitted:** 2019-02-24
- **Reporter:** gamer7112
- **Program:** Grammarly
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** DOM-based CSS Injection, Arbitrary CSS Loading, Missing Origin Validation, Potential XSS (Legacy Browsers)
- **CVEs:** None
- **Category:** web-api

## Summary
The grammarly.com embedded widget accepts an extcss URL parameter that directly loads external CSS files without origin validation or filtering. An attacker can inject malicious CSS to perform phishing attacks or achieve XSS on older browsers by loading attacker-controlled stylesheets.

## Attack scenario
1. Attacker crafts a malicious URL with extcss parameter pointing to attacker-controlled CSS file
2. Attacker tricks victim into visiting the URL (via phishing email, social engineering, etc.)
3. Victim's browser loads grammarly.com/embedded with the malicious extcss parameter
4. JavaScript code in componentWillMount extracts extcss parameter without validation
5. addExternalCss function creates a link element and appends it to document.head
6. Browser loads and applies attacker's CSS, enabling phishing UI overlay or XSS payload execution on vulnerable browsers

## Root cause
The application directly uses user-supplied extcss query parameter to construct and load external stylesheets without implementing origin whitelisting, content validation, or same-origin policy checks. The parameter is extracted from the URL and immediately passed to document.createElement/appendChild without sanitization.

## Attacker mindset
An attacker would leverage this to craft convincing phishing attacks by overlaying fake login forms or credential capture interfaces using CSS. On older browser versions (pre-CSP enforcement), they could inject javascript through CSS attribute selectors or other vector to achieve code execution.

## Defensive takeaways
- Implement strict whitelist of allowed CSS sources and validate origin of external resources
- Use Content Security Policy (CSP) to restrict stylesheet sources to trusted domains only
- Never directly load external resources from user-controlled URL parameters
- Sanitize and validate all query parameters before use in DOM manipulation
- Implement integrity checks (SRI - Subresource Integrity) for external resources
- Use CSP directives like style-src to prevent unauthorized stylesheet loading
- Consider moving CSS configuration to backend-controlled lists rather than client-side parameters

## Variant hunting
Search for other parameters in grammarly.com and similar applications that accept external resource URLs (extjs, extscript, extstylesheet, etc.). Check other embedded widgets and third-party integrations for similar CSS/JavaScript injection patterns. Test other URL parameters for CSS injection vectors.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1598 - Phishing
- T1566 - Phishing
- T1499 - Endpoint Denial of Service

## Notes
The vulnerability is particularly severe because Grammarly's embedded widget is used across many websites, potentially affecting all sites that embed it. The report specifically notes XSS potential in older browsers, suggesting CSS expression evaluation in IE or similar legacy browser quirks. The PoC uses Dropbox as a hosting vector, demonstrating ease of exploitation with free third-party services.

## Full report
<details><summary>Expand</summary>

**Summary:** An attacker can inject an external css file which can lead to phishing attacks and xss in older browsers.

**Description:** Within the main.js file the following code exists:
```javascript
t.prototype.componentWillMount = function () {
        var e = this.getCtx().nav.waypoint.query,
        t = e.extcss,
        n = e.affParams,
        a = e.minWords;
        this.affParams = n ? JSON.parse(decodeURIComponent(n))  : {
        },
        this.minWords = parseInt(a, 10),
        t && this.addExternalCss(t)
      },
      t.prototype.addExternalCss = function (e) {
        var t = document.createElement('link');
        t.setAttribute('href', e),
        t.setAttribute('rel', 'stylesheet'),
        t.setAttribute('type', 'text/css'),
        document.head.appendChild(t)
      },
```
Which allows an external css file to be loaded via the extcss parameter without any kind of origin checking or filtering.

## Browsers Verified In:

Chrome Version 72.0.3626.109
Firefox 65.0.1

## Steps To Reproduce:
1. Visit ```https://www.grammarly.com/embedded?height=300&extcss=https://www.dl.dropboxusercontent.com/s/e0g51ibqswh0v7d/xss.css?dl=0```

## Supporting Material/References:

  * CSS Injection can be used to create a phishing page like so:
{F429327}

## Impact

An attacker can use an external css file to spoof the page to their liking allowing for phishing attacks and if the victim is on an older browser an attacker can execute javascript as well.

</details>

---
*Analysed by Claude on 2026-05-12*
