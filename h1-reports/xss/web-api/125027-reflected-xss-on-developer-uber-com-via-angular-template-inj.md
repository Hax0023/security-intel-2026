# Reflected XSS on developer.uber.com via Angular Template Injection

## Metadata
- **Source:** HackerOne
- **Report:** 125027 | https://hackerone.com/reports/125027
- **Submitted:** 2016-03-22
- **Reporter:** albinowax
- **Program:** Uber
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Reflected XSS, Client-Side Template Injection, Angular Sandbox Escape
- **CVEs:** None
- **Category:** web-api

## Summary
The developer.uber.com application reflected user input from the 'q' query parameter directly into an Angular template without proper sanitization, allowing attackers to inject malicious template expressions. By exploiting Angular's template syntax and sandbox escape techniques, an attacker could execute arbitrary JavaScript in the context of a developer's browser session.

## Attack scenario
1. Attacker crafts a malicious URL containing Angular template injection payload in the 'q' parameter pointing to developer.uber.com/docs/deep-linking
2. Attacker sends the URL to a developer via email or other social engineering method
3. When the developer clicks the link, the payload is reflected into the page and processed by the Angular framework
4. Angular evaluates the template expression, which uses a sandbox escape technique to break out of Angular's expression sandbox
5. The escaped expression executes arbitrary JavaScript code (e.g., alert(1)) with the developer's privileges
6. Attacker can steal session tokens, API credentials, or hijack the developer account to compromise associated applications

## Root cause
User input from the 'q' query parameter was dynamically embedded into a client-side Angular template without proper sanitization or encoding. The application failed to either escape curly braces or use Angular's ng-non-bindable directive, allowing template expressions to be interpreted and executed by the Angular framework.

## Attacker mindset
An attacker targeting developer platforms recognizes that compromising developer accounts provides access to production credentials, API keys, and application deployment systems. By using a simple reflected XSS, the attacker can deliver a targeted phishing attack that appears to come from legitimate documentation pages, increasing success rates. The use of Angular sandbox escapes demonstrates knowledge of framework-specific attack vectors.

## Defensive takeaways
- Never dynamically embed unsanitized user input into client-side templates or HTML
- Implement whitelist-based input validation; reject any input containing template syntax characters like {{ and }}
- Use Angular's built-in sanitization and the ng-non-bindable directive for any user-controlled content
- Apply Content Security Policy (CSP) headers to restrict inline script execution and sandboxing
- Perform server-side sanitization in addition to client-side protections
- Regularly update Angular framework to patch known sandbox escapes, though recognize this is not a complete mitigation
- Implement output encoding appropriate to the context (HTML, JavaScript, URL encoding)
- Use automated security scanning tools to detect template injection vulnerabilities during development

## Variant hunting
Search for similar patterns in other Uber properties and subdomains that accept query parameters processed by Angular frameworks. Look for other template engines (Vue, React if using dangerouslySetInnerHTML, Handlebars, Mustache) with similar injection vulnerabilities. Test other parameters beyond 'q' that might be reflected in templates. Check for server-side template injection if parameters are processed server-side before rendering.

## MITRE ATT&CK
- T1190
- T1566
- T1059

## Notes
The report demonstrates a sophisticated understanding of Angular internals by using a sandbox escape that specifically targets IE11. The vulnerability chain from template injection to JavaScript execution is classic but remains impactful on developer-focused platforms where credentials are high-value targets. The attacker provided both a simple proof-of-concept and a more advanced browser-specific payload, showing escalation capability.

## Full report
<details><summary>Expand</summary>

developer.uber.com is vulnerable to reflected XSS via Angular template injection.

The following url demonstrates the root issue using a trivial payload: https://developer.uber.com/docs/deep-linking?q=wrtz{{7*7}}

If you view the rendered source of the resulting page, you'll find the string 'wrtz49', showing the input has been evaluated.

This URL uses an Angular sandbox escape to obtain arbitrary JavaScript execution and execute alert(1). It's designed to work in Internet Explorer 11, but the technique could probably be used to target other browsers given sufficient effort. I've attached a screenshot of the result.
`https://developer.uber.com/docs/deep-linking?q=wrtz{{(_="".sub).call.call({}[$="constructor"].getOwnPropertyDescriptor(_.__proto__,$).value,0,"alert(1)")()}}zzzz`


Client-side template injection vulnerabilities arise when applications using a client-side template framework dynamically embed user input in web pages. When a web page is rendered, the framework will scan the page for template expressions, and execute any that it encounters. An attacker can exploit this by supplying a malicious template expression that launches a cross-site scripting (XSS) attack. For further information on this technique, please refer to http://blog.portswigger.net/2016/01/xss-without-html-client-side-template.html

If possible, avoid using server-side code to dynamically embed user input into client-side templates. If this is not practical, consider using the ng-non-bindable directive or filtering out { and } from user input. Upgrading Angular may prevent this particular sandbox escape from working, but is not a robust fix as Angular maintain that the sandbox isn't a security feature and can't be trusted.

This vulnerability could be used to hijack developer accounts and associated apps.




</details>

---
*Analysed by Claude on 2026-05-12*
