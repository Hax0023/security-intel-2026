# XSS in new.loading.page.html via Unvalidated Redirect Parameter

## Metadata
- **Source:** HackerOne
- **Report:** 2419227 | https://hackerone.com/reports/2419227
- **Submitted:** 2024-03-16
- **Reporter:** aviv_keller
- **Program:** GoCD
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Cross-Site Scripting (XSS), Open Redirect, Improper Input Validation
- **CVEs:** CVE-2024-28866
- **Category:** web-api

## Summary
The new.loading.page.html file contains a reflected XSS vulnerability in the redirect_to query parameter that fails to validate or sanitize the target URL before assignment to window.location. An attacker can craft a malicious URL containing javascript: protocol handlers that execute arbitrary JavaScript in the victim's browser context.

## Attack scenario
1. Attacker crafts a malicious URL containing ?redirect_to=javascript:alert('XSS') or similar payload
2. Attacker distributes the URL via phishing email, social engineering, or advertisement
3. Victim clicks the link and is directed to the GoCD loading page with the malicious parameter
4. The redirectToLanding() function executes and extracts the redirect_to parameter value
5. The parameter value is decoded but not validated, then directly assigned to window.location
6. The javascript: URI executes in the victim's browser, allowing cookie theft, session hijacking, or further exploitation

## Root cause
Insufficient input validation and use of decodeURIComponent() without URL scheme validation before assignment to window.location. The code trusts user-supplied query parameters without checking if they reference safe protocols (http/https).

## Attacker mindset
An attacker recognizes that loading pages are often bypassed or not heavily scrutinized by users, making them ideal vectors for credential harvesting or malware delivery. The redirect_to parameter is a common anti-pattern that developers implement without proper security controls.

## Defensive takeaways
- Validate redirect URLs against a whitelist of allowed domains or use relative URLs only
- Implement URL scheme validation to restrict to http/https protocols only
- Use URL parsing APIs (URL constructor) to properly validate and sanitize URLs before navigation
- Avoid decodeURIComponent() when not necessary; parse query parameters safely
- Implement Content Security Policy (CSP) with script-src restrictions to prevent inline script execution
- Use frameworks with automatic XSS protection rather than manual string manipulation
- Perform security code reviews specifically targeting navigation and redirect logic

## Variant hunting
Search for similar patterns in other loading pages, error pages, or callback handlers that accept redirect_to, return_to, next, or goto parameters without validation. Check for window.location assignments anywhere user input is processed.

## MITRE ATT&CK
- T1190
- T1598
- T1566

## Notes
This is a classic reflected XSS vulnerability with high exploitability due to ease of URL crafting and distribution. The loading page context suggests this could be used to target users during authentication flows, increasing impact potential for credential theft.

## Full report
<details><summary>Expand</summary>

# Overview
The vulnerability arises from inadequate handling of query parameters, enabling attackers to insert `javascript:` URIs as redirectors within the `new.loading.page.html` file.

```js
var redirectToLanding = function() {
  var locationData = window.location.search.match(/(\?|&)redirect_to=([^&]+)(&|$)/);
  if (locationData === null) {
    window.location.reload(true);
  } else {
    window.location = decodeURIComponent(locationData[2]);
  }
}
```

[View Permalink](https://github.com/gocd/gocd/blob/0199f22311c83c88ee249a3a71907ce6f58ebd9f/jetty/src/main/resources/loading_pages/new.loading.page.html#L397-L404)

When the URL's query is `?redirect_to=javascript:alert("XSS")`, `locationData[2]` equals `'javascript:alert("XSS")'`. Subsequently, triggering `redirectToLanding` leads to XSS exploitation.

## Impact

Attackers can inject javascript: URIs to execute unauthorized scripts, potentially stealing sensitive information such as session cookies or performing actions on behalf of the user.

</details>

---
*Analysed by Claude on 2026-05-12*
