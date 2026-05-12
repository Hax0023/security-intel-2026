# DOM XSS on duckduckgo.com via Cloud Save kp and kae Parameters

## Metadata
- **Source:** HackerOne
- **Report:** 921635 | https://hackerone.com/reports/921635
- **Submitted:** 2020-07-12
- **Reporter:** sijisu
- **Program:** DuckDuckGo
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** DOM-based Cross-Site Scripting (XSS), Improper Output Encoding, Insecure Deserialization of User-Controlled Data
- **CVEs:** None
- **Category:** web-api

## Summary
A DOM-based XSS vulnerability exists in DuckDuckGo's Cloud Save feature where the kp and kae parameters are unsafely rendered into the DOM without proper sanitization. An attacker can craft malicious Cloud Save settings and trick users into visiting a link with a specific key parameter, causing arbitrary JavaScript execution in the victim's browser context.

## Attack scenario
1. Attacker creates a malicious Cloud Save configuration by sending a POST request to /settings.js with XSS payloads in the kp or kae parameters
2. Attacker crafts a URL containing the Cloud Save key (e.g., duckduckgo.com/?q=a&key=<hash>) and shares it with victims via social engineering
3. When a victim visits the link, DuckDuckGo retrieves the Cloud Save settings from local storage or downloads them from the server
4. The malicious kp/kae values are rendered directly into the DOM without proper HTML encoding/sanitization
5. The XSS payload (e.g., img tag with onerror handler) executes in the victim's browser with full DuckDuckGo origin privileges
6. Attacker achieves arbitrary JavaScript execution, potentially stealing cookies, session tokens, or performing actions on behalf of the user

## Root cause
The application fails to properly sanitize or encode user-controlled data from Cloud Save settings (kp and kae parameters) before inserting them into the DOM. The values are treated as trusted data and rendered directly as HTML, allowing injection of arbitrary script-executing HTML tags.

## Attacker mindset
An attacker would recognize that Cloud Save settings are user-modifiable and that these values flow into the DOM rendering pipeline. By crafting payloads short enough to fit storage limits and using clever techniques like eval() with URL fragments to bypass length restrictions, they can achieve persistent XSS execution across multiple page visits and settings pages.

## Defensive takeaways
- Always HTML-encode or properly sanitize user-controlled data before rendering in DOM, regardless of its source (user input, local storage, cloud sync)
- Use established DOM APIs like textContent instead of innerHTML when displaying untrusted data
- Implement Content Security Policy (CSP) with strict script-src directives to prevent inline script execution
- Apply input validation and length limits consistently across all data storage mechanisms
- Use a well-vetted XSS prevention library or framework feature (e.g., Angular's built-in sanitization) rather than manual encoding
- Implement server-side validation for Cloud Save data before storing
- Consider using a strict allowlist approach for cloud settings format and validate against schema

## Variant hunting
Test other cloud sync or user preference features for similar unsanitized DOM rendering patterns
Check if other parameters in query strings or local storage values flow into DOM without sanitization
Examine theme customization, saved searches, and other user-configurable features that might accept special characters
Test various HTML entities, event handlers (onload, onerror, onclick), and SVG/XML based payloads
Look for similar vulnerabilities in related endpoints (settings pages, export functions, import features)
Test for stored XSS variants using other blob storage mechanisms if available

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1598 - Phishing
- T1204 - User Execution

## Notes
The vulnerability demonstrates sophisticated bypass techniques including character limit evasion using eval() with URL fragments. The persistence aspect (execution on every search visit) significantly amplifies the impact. Both POST to /settings.js for payload creation and GET parameter usage indicate a multi-step attack requiring initial access to set up malicious settings, though the key parameter reveals the settings, making it reproducible without direct account compromise.

## Full report
<details><summary>Expand</summary>

Hey there,

there is a DOM XXS vulnerability on the https://duckduckgo.com/ search result page through the `kp` and `kae` parameters of the [Cloud Save](https://help.duckduckgo.com/duckduckgo-help-pages/settings/cloud-save/) feature.

POC URL: https://duckduckgo.com/?q=s&key=bb6e45e894d7b1f3a2619df967be873b15f8eccd55d3a729f58429b59f72431e4fd4b736a0ae5cf74933bcb5136103e1c09664972b3c489d1b682f08ce070325

Video (Firefox 78.0.1): 
{F904609}

Video (Chromium 83.0.4103.116): 
{F904637}

## How to reproduce?

First, we need to create malicious "Cloud Save" setting with our XSS payloads, an attacker would do that on their computer, we can do that with the following request to duckduckgo.com:

```
POST /settings.js HTTP/1.1
Host: duckduckgo.com
Content-Length: 248

{
"command":"write",
"objectKey":"bb6e45e894d7b1f3a2619df967be873b15f8eccd55d3a729f58429b59f72431e4fd4b736a0ae5cf74933bcb5136103e1c09664972b3c489d1b682f08ce0703ff",
"obj":{
"kp":"\"><img src=/ onerror=alert(1)>",
"kae":"\"><img src=/ onerror=alert(2)>"
}
}
```

Now we just need to visit duckduckgo.com with the key parameter set, an attacker would send this link to the victim, like this: https://duckduckgo.com/?q=a&key=bb6e45e894d7b1f3a2619df967be873b15f8eccd55d3a729f58429b59f72431e4fd4b736a0ae5cf74933bcb5136103e1c09664972b3c489d1b682f08ce0703ff. The Cloud Save key is now saved in the browser's Local Storage. Because the settings are downloaded from Cloud Save on every visit of the results page, our code will be executed every time as well. Try searching https://duckduckgo.com/?q=a, it even triggers on the settings page https://duckduckgo.com/settings and others.

## What about longer payloads?

You cannot have Cloud Save settings property longer than 30 characters. However, there are many tricks on how to bypass this limitation. For example one of many great @terjanq 's payloads does the trick here. It evals the URL so you can make your payload long enough to execute malicious code.

Request to set up Cloud Save:

```
POST /settings.js HTTP/1.1
Host: duckduckgo.com
Content-Length: 211

{
"command":"write",
"objectKey":"bb6e45e894d7b1f3a2619df967be873b15f8eccd55d3a729f58429b59f72431e4fd4b736a0ae5cf74933bcb5136103e1c09664972b3c489d1b682f08ce070324",
"obj":{
"kp":"\"><svg/onload=eval(`'`+URL)>"
}
}
```

And URL that executes the code: https://duckduckgo.com/?q=s&key=bb6e45e894d7b1f3a2619df967be873b15f8eccd55d3a729f58429b59f72431e4fd4b736a0ae5cf74933bcb5136103e1c09664972b3c489d1b682f08ce070324#';alert(document.domain);

Video:
{F904653}

## Impact

Attacker can execute JavaScript.

</details>

---
*Analysed by Claude on 2026-05-12*
