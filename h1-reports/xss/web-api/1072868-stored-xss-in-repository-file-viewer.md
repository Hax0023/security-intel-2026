# Stored XSS in GitLab Repository File Viewer via Outdated swagger-ui DOMpurify

## Metadata
- **Source:** HackerOne
- **Report:** 1072868 | https://hackerone.com/reports/1072868
- **Submitted:** 2021-01-06
- **Reporter:** kannthu
- **Program:** GitLab
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Stored Cross-Site Scripting (XSS), Improper Input Sanitization, Component Vulnerability
- **CVEs:** None
- **Category:** web-api

## Summary
GitLab's OpenAPI file viewer uses an outdated version of swagger-ui with a vulnerable DOMpurify library that fails to properly sanitize user-supplied input, allowing attackers to inject arbitrary HTML elements with attributes. The vulnerability is stored in repository files and requires minimal user interaction (single click) to execute due to CSP bypass techniques using Rails data attributes.

## Attack scenario
1. Attacker identifies that GitLab uses an old swagger-ui version with vulnerable DOMpurify
2. Attacker crafts malicious OpenAPI YAML file containing HTML injection payload with data-remote, data-method, and data-type attributes targeting a remote script
3. Attacker commits this file to a repository they control or a public repository
4. Victim views the malicious OpenAPI file in GitLab's file viewer
5. Victim clicks anywhere on the page, triggering the data-remote Rails attribute to execute
6. Attacker's remote script executes in victim's browser context, enabling CSRF token theft or session hijacking

## Root cause
GitLab uses an outdated version of swagger-ui that relies on an old version of DOMpurify library insufficient for HTML sanitization. The sanitizer allows dangerous HTML elements and attributes (data-remote, data-method, data-type) to bypass filtering. Additionally, GitLab's CSP policy does not adequately restrict inline event handlers, but attackers can abuse Rails-specific data attributes that trigger JavaScript execution without inline handlers.

## Attacker mindset
An attacker would recognize that component vulnerabilities in third-party libraries present high-impact attack vectors. The use of Rails data attributes as a CSP bypass demonstrates understanding of framework-specific mechanisms. The ability to store malicious content and trigger it via simple user interaction (page click) makes this an ideal vector for account compromise campaigns targeting developers viewing repository files.

## Defensive takeaways
- Maintain up-to-date versions of all third-party dependencies, particularly security-critical libraries like DOMpurify and sanitization components
- Implement comprehensive inventory and automated scanning of component versions using dependency management tools
- Apply layered security: use CSP policies that restrict data attributes like data-remote in addition to inline scripts
- Sanitize and validate all user-supplied input used in OpenAPI specifications before rendering
- Implement framework-aware CSP rules that account for Rails data attributes and similar mechanisms
- Conduct regular security audits of UI components that parse and display user-controlled data formats (YAML, JSON, etc.)
- Consider sandbox rendering of untrusted API specifications in isolated iframes with restricted permissions

## Variant hunting
Search for similar vulnerabilities in other GitLab features using third-party UI libraries (Swagger/OpenAPI viewers), API documentation renderers, or Markdown viewers. Check for instances where DOMpurify or sanitization libraries are used but not regularly updated. Test for similar CSP bypasses using other framework-specific attributes (data-confirm, data-toggle, etc.). Examine other file viewers that render user-controlled markup formats.

## MITRE ATT&CK
- T1190 Exploit Public-Facing Application
- T1598 Phishing
- T1056 Input Capture
- T1539 Steal Web Session Cookie

## Notes
The vulnerability leverages a sophisticated understanding of both web security (DOMpurify evasion) and framework-specific mechanisms (Rails data attributes). The dual exploitation paths (direct file access and URL parameter injection) increase accessibility. The requirement for a click is not a significant barrier given legitimate user interaction with repository files. The report's identification of the CSP bypass as a separate technique demonstrates thorough vulnerability analysis.

## Full report
<details><summary>Expand</summary>

### Summary
There exists XSS in swagger-ui version used in GitLab open API viewer. The XSS exists due to the old version of DOMpurify used in swagger-ui that allows an attacker can  **inject any HTML elements with any attributes** (except script tag) on the page. 

The XSS in POC requires 1 click anywhere on the page to execute, because of CSP that does not allow to execute events from HTML tags. (f.e. <img src=1 onerror=alert(1)). I will try to find CSP bypass that will allow me to execute the script with no user interaction.

My script uses the CSP bypass presented in https://gitlab.com/gitlab-org/gitlab/-/issues/213273
```
<a   
  data-remote="true"
  data-method="get"  
  data-type="script"
  href="/wbowling/wiki/raw/master/test.js" 
  class='atwho-view select2-drop-mask pika-select'>
</a>  
```

### Steps to reproduce

1. Go to https://gitlab.com/kannthu/asdasdas123/-/blob/master/openapi.yaml (tested on Chrome and Firefox)
2. Click anywhere on the page
3. You should see the alert box

There is another way of executing this XSS. **You can add "url=https://gitlab.com/kannthu/asdasdas123/-/raw/master/openapi.yaml" parameter to the URL of any open API file in any repository, and the XSS will still work**. 

1. Open https://gitlab.com/gitlab-org/build/omnibus-mirror/alertmanager/blob/master/api/v2/openapi.yaml?url=https://gitlab.com/kannthu/asdasdas123/-/raw/master/openapi.yaml
2. Click anywhere on the page
3. You should see the alert box

### Impact

The stored XSS is triggering for any user that opens the page and clicks anywhere on the page. The PoC can easily be extended to steal the user's CSRF token and to take over the victim's account.

### Examples

- https://gitlab.com/kannthu/asdasdas123/-/blob/master/openapi.yaml
- https://gitlab.com/gitlab-org/build/omnibus-mirror/alertmanager/blob/master/api/v2/openapi.yaml?url=https://gitlab.com/kannthu/asdasdas123/-/raw/master/openapi.yaml


### What is the current *bug* behavior?
Gitlab uses an old version of swagger-ui.

### What is the expected *correct* behavior?
Gitlab should use the newest version of swagger-ui.

### Relevant logs and/or screenshots
F1146909

### Output of checks
This bug happens on GitLab.com

#### Results of GitLab environment info
-

## Impact

The stored XSS is triggering for any user that opens the page and clicks anywhere on the page. An attacker can render anything on that page - malicious form to steal the user's login and password, or simply get the user's CSRF token and to take over the victim's account.

</details>

---
*Analysed by Claude on 2026-05-12*
