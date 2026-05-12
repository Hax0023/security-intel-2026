# Mutation Based Stored XSS on Trix Editor version 2.1.8

## Metadata
- **Source:** HackerOne
- **Report:** 2819573 | https://hackerone.com/reports/2819573
- **Submitted:** 2024-11-04
- **Reporter:** sudi
- **Program:** Basecamp Trix Editor
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Stored Cross-Site Scripting (XSS), Mutation XSS (mXSS), Sanitizer Bypass
- **CVEs:** None
- **Category:** web-api

## Summary
A mutation-based XSS vulnerability exists in Trix Editor's sanitizer that can be exploited via copy-paste operations. By leveraging MathML mutation vectors with nested HTML elements, attackers can bypass the sanitizer and inject malicious JavaScript code that executes in the user's context.

## Attack scenario
1. Attacker crafts a malicious HTML payload containing a div with data-trix-attachment attribute
2. The attachment content includes a mutation XSS vector using MathML elements (<math><mtext><table><mglyph><style>)
3. Within the style tag, attacker embeds an img element with onerror event handler containing JavaScript
4. Attacker tricks user into copying the rendered text from a webpage containing this payload
5. User pastes the content into a Trix Editor instance
6. During paste processing, the sanitizer fails to properly neutralize the mutation-based XSS vector, allowing the JavaScript to execute

## Root cause
The Trix Editor's HTML sanitizer does not adequately handle mutation XSS attacks that exploit the difference between how HTML is parsed during sanitization versus how the DOM renders the final content. MathML elements combined with nested HTML create a mutation context where malicious payloads bypass filtering rules.

## Attacker mindset
An attacker would identify that Trix Editor is widely used in web applications for rich text editing. By researching known mutation XSS techniques (particularly MathML-based bypasses documented in DOMPurify research), the attacker can craft payloads that exploit the gap between sanitization and rendering. The copy-paste vector is preferred because it's a common user action and may trigger different sanitization code paths than direct input.

## Defensive takeaways
- Implement mutation XSS resistant sanitization by sanitizing after DOM parsing, not just input strings
- Use well-maintained sanitization libraries (DOMPurify, etc.) and keep them updated to patch known mXSS vectors
- Disable or strictly control MathML and SVG handling if not required by application functionality
- Apply Content Security Policy (CSP) with script-src restrictions to limit XSS impact
- Sanitize data both on paste/input events and before rendering to catch mutation vectors
- Test sanitizer with mutation XSS payloads from security research (Securitum, DOMPurify bypasses)
- Use iframe sandboxing for editor content to isolate execution context
- Implement output encoding in addition to input sanitization as defense-in-depth

## Variant hunting
Search for similar mutation XSS vectors in Trix using: SVG-based mutations with <foreignObject>, nested table mutations, style tag context escaping, other MathML element combinations (<mi>, <mo>, <mn>), iframe attribute injection within attachments, and canvas/script element nesting patterns. Test paste handlers specifically as they may use different code paths than direct input.

## MITRE ATT&CK
- T1190
- T1059
- T1566.002
- T1204.001

## Notes
This vulnerability is a stored XSS (not just reflected) because the malicious payload is persisted in the attachment metadata. The mutation aspect makes it particularly dangerous as traditional sanitizers may not catch it. The researcher references prior work on DOMPurify bypasses and Securitum's mutation XSS research, indicating this is a known attack pattern that Trix failed to address. The issue affects the latest version at time of report (2.1.8), suggesting the library may not prioritize mXSS protections.

## Full report
<details><summary>Expand</summary>

Heyy there,
I have found a bypass for the sanitizer used in Trix Editor https://github.com/basecamp/trix , the bypass is kind a  of mutation based , using copy paste vector it's possible to perform the xss.

An example payload would be:

```html
copy<div data-trix-attachment="{&quot;contentType&quot;:&quot;text/html5&quot;,&quot;content&quot;:&quot;&lt;math&gt;&lt;mtext&gt;&lt;table&gt;&lt;mglyph&gt;&lt;style&gt;&lt;img src=x onerror=alert()&gt;&lt;/style&gt;XSS POC&quot;}"></div>me
```

Decoding the html entity you get the below payload ,which contains the mutation xss vector
```html
<math><mtext><table><mglyph><style><img src=x onerror=alert()></style>
```

For more details on this bypass you can read here: https://research.securitum.com/mutation-xss-via-mathml-mutation-dompurify-2-0-17-bypass/
There will exist will more simple vectors this is just an example which worked out of the blue.

-------------------------------------------------

**Steps to reproduce:**

Using the similar poc from the report #2521419 we can replicate the bug, just save the below code in .html file and then copy the text saying `copy me` and paste it in the editor this will popup an alert.

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Trix Editor XSS Demo</title>
  <script src="https://cdn.jsdelivr.net/npm/trix@2.1.8/dist/trix.umd.js"></script>
  <link href="https://cdn.jsdelivr.net/npm/trix@2.1.1/dist/trix.min.css" rel="stylesheet">
</head>
<body>
  <h1>Trix Editor XSS Demo</h1>
  <trix-editor></trix-editor>
  <script>
  document.write(`copy<div data-trix-attachment="{&quot;contentType&quot;:&quot;text/html5&quot;,&quot;content&quot;:&quot;&lt;math&gt;&lt;mtext&gt;&lt;table&gt;&lt;mglyph&gt;&lt;style&gt;&lt;img src=x onerror=alert()&gt;&lt;/style&gt;XSS POC&quot;}"></div>me`);
  </script>
</body>
</html>

```

{F3733124}

## Impact

An attacker could exploit these vulnerabilities to execute arbitrary JavaScript code within the context of the user's session, potentially leading to unauthorized actions being performed or sensitive information being disclosed.

</details>

---
*Analysed by Claude on 2026-05-12*
