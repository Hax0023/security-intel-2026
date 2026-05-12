# XSS via SVG Foreign Object in Issue Reference Tooltips

## Metadata
- **Source:** HackerOne
- **Report:** 831962 | https://hackerone.com/reports/831962
- **Submitted:** 2020-03-26
- **Reporter:** yvvdwf
- **Program:** GitLab
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Cross-Site Scripting (XSS), Improper Input Sanitization, SVG-based XSS
- **CVEs:** None
- **Category:** web-api

## Summary
GitLab's Bootstrap tooltip sanitization allows SVG and USE elements with xlink:href attributes, enabling attackers to load external SVG resources containing malicious iframes and scripts. When users hover over issue references, the XSS payload executes via svg foreignObject elements containing iframes with arbitrary JavaScript. The vulnerability is Firefox-specific due to Firefox's support for foreignObject elements.

## Attack scenario
1. Attacker creates a malicious JavaScript file in a GitLab project and exposes it via CI/CD artifacts with application/javascript MIME type to bypass content-type restrictions
2. Attacker creates an SVG file containing a foreignObject with an iframe that loads the malicious JavaScript from the artifacts endpoint
3. Attacker creates a GitLab issue with a title containing an SVG USE element referencing the malicious SVG file via xlink:href
4. Attacker posts an issue reference (e.g., #1) in a discussion or wiki page where other users can see it
5. When victims hover over the issue reference link, the Bootstrap tooltip is triggered and renders the SVG content
6. The SVG foreignObject iframe loads and executes the arbitrary JavaScript in the victim's browser context

## Root cause
GitLab's Bootstrap tooltip HTML sanitizer whitelists SVG elements (<svg>, <use>) and the xlink:href attribute to preserve legitimate SVG content. However, this whitelist does not account for the combination of SVG foreign objects with iframes that can bypass MIME-type restrictions through CI/CD artifacts, allowing external script execution within the sanitized SVG context.

## Attacker mindset
The attacker discovered a multi-stage bypass of GitLab's security controls by chaining together several legitimate features (CI/CD artifacts with MIME-type override, SVG rendering in tooltips, foreignObject support) into an unintended attack vector. This demonstrates sophisticated understanding of browser security boundaries and GitLab's architecture.

## Defensive takeaways
- Do not whitelist SVG elements without also restricting or disabling nested interactive elements like foreignObject and iframe
- Implement stricter Content Security Policy (CSP) headers to prevent external resource loading from user-controlled content
- Consider disabling SVG rendering in automatically-generated tooltips or use a more restrictive sanitizer that removes foreignObject elements entirely
- Review CI/CD artifact serving to ensure MIME-type overrides do not circumvent security headers like X-Content-Type-Options
- Test XSS filters across multiple browsers (Firefox, Safari, Chrome, Edge) as rendering engines handle SVG and foreignObject differently
- Sanitize issue titles separately from tooltip rendering and avoid embedding arbitrary SVG in user-controlled content

## Variant hunting
Check other areas where SVG content is rendered in tooltips or hover states across GitLab
Test if other SVG elements (image, embed, object) can be used instead of foreignObject for similar attacks
Verify if other HTML attributes besides xlink:href can reference external resources in whitelisted SVG elements
Test other browsers (Edge, Opera) to identify additional affected platforms
Check if the vulnerability exists in other GitLab features that use Bootstrap tooltips with user-controlled content
Investigate if the svg4everybody polyfill can be exploited separately for older browsers

## MITRE ATT&CK
- T1190
- T1203

## Notes
This is a browser-specific vulnerability that demonstrates the dangers of piecemeal HTML sanitization. Firefox's support for SVG foreignObject elements is critical to the attack chain, making this a Firefox-specific issue at the time of reporting. The attacker creatively bypassed MIME-type restrictions through GitLab's own CI/CD system, showing how legitimate features can be chained into security bypasses. The report shows excellent vulnerability research methodology with clear reproduction steps.

## Full report
<details><summary>Expand</summary>

Dear team,

I found an XSS that occurs when users move mouse over reference numbers of issues. 
This XSS occurs on Firefox. It does not occurs on Webkit-based ones such as Safari, Chrome. I haven't tested on Edge.
It can be also occured in older browsers due to [`svg4everybody()`](https://gitlab.com/gitlab-org/gitlab/-/blob/master/app/assets/javascripts/commons/polyfills/svg.js#L11) and [`cachedDocument.body.innerHTML = xhr.responseText`](https://github.com/jonathantneal/svg4everybody/blob/v2.1.9/dist/svg4everybody.js#L36)

### Summary

XSS caused by enabling HTML of tooltip of issues' reference numbers.
Bootstrap sanitizes macilious tags/attributes of HTML tooltips.
The issue is that gitlab [allows](https://gitlab.com/gitlab-org/gitlab/-/blob/master/app/assets/javascripts/commons/bootstrap.js#L77) `<svg>`, `<use>` and its `xlink:href` attribute.
This allows attacker to link external resource to svg images, then, to cause the XSS.


### Steps to reproduce

Four big steps to reproduce:

1. create a javascript file
2. create a file containing external svg resource
3. create an issue's title having svg content that use the resource above
4. create a reference to the issue, XSS occurs when users move mouse over the reference link

Steps 1,2,3 are supposed to realized in a same project.

#### 1. Create a javascript file

This step creates a javascript file that may contain arbitrary attack script.
For example, add a new file `alert.js` in a selected project with the following content:

```javascript
alert('Hello: ' + window.parent.location.href);
```

This script will be used by an `iframe`.

Since gitlab changes its mime type to ['text/plain'](https://gitlab.com/gitlab-org/gitlab/-/blob/master/app/controllers/concerns/send_file_upload.rb#L16) and set header `X-Content-Type-Options: nosniff`, browser will refuse to execute the javascript file if it will be loaded by script tag, such as `<script src=alert.js></script`.

This can be bypassed by using `job artifacts`.

Create another file `.gitlab-ci.yml` with the following content:

```yml
js:
  script: echo "to generate mime type application/javascript"
  artifacts:
    paths:
    - alert.js
    expire_in: 4 week
```

After saving the file, gitlab CI/CD will start runing. Wait for the job finished.
Browse `Job artifacts`, then get the raw link of the generated `alert.js` file, for example:
`https://gitlab.com/yvvdwf/svg-use-xss-firefox/-/jobs/486384886/artifacts/raw/alert.js`

Note that the mime type of this js file is now `application/javascript`.

#### 2. Create a svg file

Add the third file in to the project with the name `xss.svg` and the following content:

```xml
<svg id="xss" xmlns="http://www.w3.org/2000/svg">
	<foreignObject>
		<iframe xmlns="http://www.w3.org/1999/xhtml" srcdoc='&lt;script src=https://gitlab.com/yvvdwf/svg-use-xss-firefox/-/jobs/486384886/artifacts/raw/alert.js&gt; &lt;/script&gt;'></iframe>
	</foreignObject>
</svg>
```

Please note that, you must replace the link to `alert.js` file with your.


#### 3. Create an issue

Create a new issue having the following title:
 
`<svg><use xlink:href="https://gitlab.com/yvvdwf/svg-use-xss-firefox/-/raw/master/xss.svg#xss"/></svg>`

#### 4. Create a reference to the issue

In an issue discussion, or in a wiki page, enter the reference number of the issue, for example (suppose the issue id = 1):
`Move mouse over #1 to see alert`

When you move mouse over the number 1, you will see a (normal) tooltip and a popup executed by the `alert.js` file above.

This has been tested on the latest Firefox (74.0 (64-bit)) on macOS. Firefox allows `foreignObject` (but not [webkit](https://bugs.webkit.org/show_bug.cgi?id=91515))

### Impact

Attacker may perform arbitrary actions on behalf of users at the client side.

### Examples

An example is on https://gitlab.com/yvvdwf/svg-use-xss-firefox
This project is private. Please let me know if you cannot access it.


### What is the expected *correct* behavior?

Malicious scripts must not be executed due to svg content.

### Output of checks

This bug happens on GitLab.com

## Impact

Attacker may perform arbitrary actions on behalf of users at the client side.

</details>

---
*Analysed by Claude on 2026-05-12*
