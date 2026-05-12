# DOM XSS on duckduckgo.com via relsexp Parameter

## Metadata
- **Source:** HackerOne
- **Report:** 876148 | https://hackerone.com/reports/876148
- **Submitted:** 2020-05-16
- **Reporter:** cujanovic
- **Program:** DuckDuckGo
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** DOM-based Cross-Site Scripting (XSS), Improper Input Validation, Unsafe HTML Rendering
- **CVEs:** None
- **Category:** web-api

## Summary
A DOM-based XSS vulnerability exists in DuckDuckGo's search functionality through the 'relsexp' parameter, which is directly rendered into the DOM without proper sanitization. An attacker can inject arbitrary JavaScript code that executes in the victim's browser within the context of duckduckgo.com, allowing session hijacking, credential theft, or malware distribution.

## Attack scenario
1. Attacker crafts a malicious URL with JavaScript payload in the 'relsexp' parameter
2. Attacker distributes the URL via phishing email, social media, or compromised website
3. Victim clicks the link while authenticated to duckduckgo.com
4. Browser renders the page and the relsexp parameter value is inserted into DOM without escaping
5. JavaScript payload executes with access to victim's cookies, localStorage, and session data
6. Attacker exfiltrates sensitive information or performs actions on behalf of the victim

## Root cause
The 'relsexp' parameter value is directly inserted into the DOM during page rendering without proper HTML entity encoding or content sanitization, allowing HTML/JavaScript injection.

## Attacker mindset
An attacker would identify this vulnerability as an easy-to-exploit entry point requiring minimal technical skill - just crafting a URL with an img tag and onerror handler. This is attractive for phishing campaigns, especially targeting DuckDuckGo users who may have higher security awareness but still fall victim to legitimate-looking search links.

## Defensive takeaways
- Implement strict input validation and HTML entity encoding for all user-supplied parameters before DOM insertion
- Use DOM APIs safely (textContent instead of innerHTML when possible) to prevent XSS
- Apply Content Security Policy (CSP) headers to restrict inline script execution
- Conduct regular security audits of URL parameter handling across all pages
- Implement automated XSS scanning in CI/CD pipeline
- Use templating engines with automatic escaping enabled by default
- Perform security code review of any parameter that reaches the DOM

## Variant hunting
Search for other parameters that may be reflected in the page: 'ia', 'q', 'ko', 'kj', 'kk', 't' and similar URL parameters. Look for any user-controlled input in API responses, headers, or alternative search endpoints. Test POST parameters and HTTP headers (Referer, User-Agent) for similar reflection issues.

## MITRE ATT&CK
- T1190
- T1598
- T1566

## Notes
This is a straightforward reflected/DOM XSS with high impact due to DuckDuckGo's domain authority and user trust. The vulnerability requires no authentication and is easily exploitable via URL sharing. The use of image tag with onerror handler is a classic XSS payload bypass technique.

## Full report
<details><summary>Expand</summary>

Hello,
The is a DOM XSS vulnerability on https://duckduckgo.com search through the `relsexp` parameter.

PoC URL: ` https://duckduckgo.com/?q=a&relsexp="><img src=/ onerror=alert(document.domain)>&ia=web`

Screenshot:
{F830875}

Video:
{F830880}

## Impact

The attacker can execute JS code.

</details>

---
*Analysed by Claude on 2026-05-12*
