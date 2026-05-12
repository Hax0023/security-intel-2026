# XSS via Malicious Graphie Upload in Legacy API

## Metadata
- **Source:** HackerOne
- **Report:** 2846011 | https://hackerone.com/reports/2846011
- **Submitted:** 2024-11-18
- **Reporter:** sikn
- **Program:** Khan Academy
- **Bounty:** Not specified in report
- **Severity:** critical
- **Vuln:** Cross-Site Scripting (XSS), Arbitrary File Upload, Insecure Deserialization, Cache Poisoning
- **CVEs:** None
- **Category:** web-api

## Summary
An attacker can upload malicious graphies through the legacy graphie-to-png API by submitting crafted SVG and JSON payloads that hash to existing graphie identifiers, poisoning cached versions served to khanacademy.org users. The vulnerability exploits unsafe DOM injection when rendering graphie labels with typesetAsMath disabled, enabling arbitrary JavaScript execution in the context of Khan Academy domains.

## Attack scenario
1. Attacker identifies a legitimate graphie used on khanacademy.org by its hash identifier (e.g., from CDN URLs)
2. Attacker crafts malicious SVG containing onload event handlers and JSON with script payloads in label content with typesetAsMath: false
3. Attacker uploads the poisoned files to graphie-to-png.kasandbox.org using the same hash, bypassing upload validation
4. Attacker waits for CDN cache expiration or forces cache invalidation for cdn.kastatic.org
5. When users visit Khan Academy pages containing the affected graphie, the malicious SVG/JSON is served and rendered
6. XSS payload executes in user's browser with khanacademy.org context, enabling session hijacking and account takeover

## Root cause
The graphie renderer accepts and processes untrusted JSON label content without sanitization when typesetAsMath is disabled, directly injecting raw HTML/script into the DOM. The upload API does not validate or restrict the content of submitted SVG and JSON payloads, allowing attackers to override legitimate graphies. Additionally, weak cache invalidation and reliance on file hashing without integrity verification enables poisoning of cached assets.

## Attacker mindset
An attacker recognizes that graphies are widely embedded across Khan Academy's platform and that the legacy API has insufficient input validation. By targeting the caching layer and exploiting unsafe DOM rendering practices, they can achieve persistent XSS affecting all users who access pages with the compromised graphie, enabling large-scale account compromise without user interaction.

## Defensive takeaways
- Implement strict Content Security Policy (CSP) headers to restrict inline script execution and onload event handlers
- Sanitize all user-controlled JSON content before DOM injection using a robust HTML sanitization library
- Validate and restrict SVG uploads to remove event handlers (onload, onclick, etc.) or serve SVGs with Content-Type: image/svg+xml and X-Content-Type-Options: nosniff
- Implement cryptographic integrity verification (signed hashes, HMAC) for cached assets to prevent poisoning attacks
- Require authentication and rate-limiting on the graphie-to-png upload API to prevent abuse
- Use templating engines with auto-escaping instead of raw innerHTML for rendering user-controlled content
- Implement proper cache versioning and TTLs to reduce window of exposure from poisoned assets
- Audit all rendering paths for unsafe DOM manipulation (innerHTML, dangerouslySetInnerHTML equivalents)

## Variant hunting
Search for other legacy or deprecated APIs that accept user-uploaded content without validation
Audit all SVG rendering endpoints for event handler filtering and attribute sanitization
Review all JSON parsing and rendering workflows that might skip sanitization for specific content types
Identify other assets served through CDNs that rely on hash-based naming without integrity verification
Test file upload endpoints across Khan Academy infrastructure for overwrite/poisoning capabilities
Check for other rendering engines (MathJax, Plotly, etc.) with similar typesetAsMath-like flags that bypass sanitization
Investigate if S3 bucket permissions allow unauthorized updates to ka-perseus-graphie assets

## MITRE ATT&CK
- T1190
- T1059
- T1566
- T1598
- T1539
- T1021

## Notes
This vulnerability demonstrates a sophisticated attack combining multiple weaknesses: unsafe user input handling, inadequate output encoding, weak asset integrity verification, and reliance on deprecated APIs. The cache poisoning aspect significantly amplifies impact by making the attack persistent and affecting all users. The report shows good proof-of-concept methodology including both direct payload injection and cache override simulation using DevTools.

## Full report
<details><summary>Expand</summary>


An attacker can can upload malicious graphies via (http://graphie-to-png.kasandbox.org/) and (http://graphie-to-png.khanacademy.systems/) that exploit the graphie renderer.
The attack targets any page that has a graphie (`khanacademy.org`!!), as well as `cdn.kastatic.org` and `ka-perseus-graphie.s3.amazonaws.com`

# Proof of concept
## Step 1: Uploading a malicious graphie
consider the following example where https://ka-perseus-graphie.s3.amazonaws.com/2122427aa8dc4ef2a59058bc1a7a934ba6ca6747.svg is used in an article, we will override it by uploading the same JS but with malicious SVG and JSON data (because the hash is a hash of the JS).

1. **Malicious SVG:** The SVG is modified to include a malicious `onload` attribute.
```html
<svg ... onload="alert('SIKN')">...</svg>
```
2. **Malicious JSON:** A label is modified with `typesetAsMath: false`, causing the graphie renderer to inject our code to DOM. This is what will target `khanacademy.org`
```json
{
	"labels": [
		{
			"content": "<script>alert('SIKN')</script>",
			"typesetAsMath": false,
			...
		},
		...
	],
	...
}
```
```js
var form = new FormData();
form.append("js", ORIGINAL_JS);
form.append("svg", XSS_SVG);
form.append("other_data", JSON.stringify(XSS_JSON));

await fetch("http://graphie-to-png.kasandbox.org/svg", {
    "method": "POST",
    "body": form
}).then(r=>r.text())
```


## Step 2: Wait patiently
Wait until cdn.kastatic.org updates its cache, for this example I had already prepared it by not caching the original graphie (https://cdn.kastatic.org/ka-perseus-graphie/2122427aa8dc4ef2a59058bc1a7a934ba6ca6747.svg)

As for the malicious JSON, using the devtools override feature to simulate an attack shows that it works:
{F3766148}

## Impact

XSS on pages that use graphies, potentially leading to account takeovers.

</details>

---
*Analysed by Claude on 2026-05-12*
