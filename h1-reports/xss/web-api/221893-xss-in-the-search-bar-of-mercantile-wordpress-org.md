# XSS in mercantile.wordpress.org Search Bar via AngularJS Template Injection

## Metadata
- **Source:** HackerOne
- **Report:** 221893 | https://hackerone.com/reports/221893
- **Submitted:** 2017-04-18
- **Reporter:** codertom
- **Program:** WordPress.org Bug Bounty Program
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Cross-Site Scripting (XSS), Template Injection, AngularJS Expression Language Injection
- **CVEs:** None
- **Category:** web-api

## Summary
A Cross-Site Scripting vulnerability exists in the search functionality of mercantile.wordpress.org, where user input is not properly sanitized before being rendered in an AngularJS context. An attacker can inject malicious AngularJS expressions through the search parameter to execute arbitrary JavaScript code in the context of the victim's browser.

## Attack scenario
1. Attacker crafts a malicious search query containing AngularJS template injection payload targeting the ng-bindable directive
2. Attacker sends victim a link to mercantile.wordpress.org with the malicious payload in the search parameter (s=)
3. Victim clicks the link and the page loads with the payload in the search parameter
4. AngularJS processes the search parameter content and executes the injected expressions without proper sanitization
5. Attacker's JavaScript code executes with victim's privileges, allowing session hijacking, credential theft, or malware distribution
6. Proof of concept demonstrates successful JavaScript execution via browser prompt dialog showing document.domain

## Root cause
The application fails to properly sanitize or escape user input from the search parameter before passing it to AngularJS templating engine. The presence of ng-bindable directive in the HTML source indicates user input is being directly bound to Angular expressions without using secure bindings like ng-bind-html with $sanitize service.

## Attacker mindset
Opportunistic researcher discovering low-hanging fruit through source code inspection. The attacker identified AngularJS usage via ng-bindable, recognized the template injection opportunity, and crafted a sophisticated payload exploiting AngularJS's $scope manipulation to bypass potential basic filters and achieve arbitrary code execution.

## Defensive takeaways
- Never trust user input in search parameters; implement strict input validation and output encoding
- Use AngularJS's built-in sanitization services ($sanitize) when binding user-supplied HTML content
- Prefer ng-bind and property binding over ng-bindable for dynamic content, especially user input
- Implement Content Security Policy (CSP) headers to mitigate XSS impact and restrict inline script execution
- Use security-focused Angular versions and keep frameworks updated with security patches
- Perform security code review of frontend template rendering logic, particularly for search and dynamic content features
- Apply output encoding/escaping appropriate to context (HTML context, attribute context, JavaScript context)

## Variant hunting
Look for similar template injection vulnerabilities in other WordPress.org subdomains or properties that use AngularJS. Search for other user input points (filters, sorting, pagination) that may be reflected in ng-bindable contexts. Test for SSTI in other JavaScript frameworks (Vue.js, React with custom templates). Examine other search functionalities across WordPress ecosystem for improper input handling with client-side templating engines.

## MITRE ATT&CK
- T1190
- T1598
- T1566

## Notes
The payload is sophisticated, exploiting AngularJS's internal mechanisms ($_apply, $scope manipulation, $eval) to execute code even if basic expression filters exist. The use of ng-bindable rather than ng-bind-html suggests the developers may have underestimated the security implications of this directive. Report appears to be from early WordPress.org H1 program participation (report 221893 indicates 2016-2017 timeframe). The vulnerability demonstrates why client-side frameworks require security-conscious implementation of user input handling.

## Full report
<details><summary>Expand</summary>

Hi wordpress! Glad to see you here at H1.

       I found a XSS issue in the https://mercantile.wordpress.org/s=<payload here>
This works with the angular js payloads. I did inject a angular js code its because I found the `ng-bindable` in the source.

###STEPS TO REPRODUCE
1. Go to https://mercantile.wordpress.org
2. Click on search and put this payload:
>
`{{
    c=''.sub.call;b=''.sub.bind;a=''.sub.apply;
    c.$apply=$apply;c.$eval=b;op=$root.$$phase;
    $root.$$phase=null;od=$root.$digest;$root.$digest=({}).toString;
    C=c.$apply(c);$root.$$phase=op;$root.$digest=od;
    B=C(b,c,b);$evalAsync("
    astNode=pop();astNode.type='UnaryExpression';
    astNode.operator='(window.X?void0:(window.X=true,prompt(document.domain)))+';
    astNode.argument={type:'Identifier',name:'foo'};
    ");
    m1=B($$asyncQueue.pop().expression,null,$root);
    m2=B(C,null,m1);[].push.apply=m2;a=''.sub;
    $eval('a(b.c)');[].push.apply=a;
}}`
As you could now see the domain has been popped up.

If you have any questions just tell me and I will try my best to have an answer.

Kind Regards,
Tom
    


</details>

---
*Analysed by Claude on 2026-05-12*
