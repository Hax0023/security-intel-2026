# Open Redirect on Unsupported Browser Warning Page

## Metadata
- **Source:** HackerOne
- **Report:** 1977222 | https://hackerone.com/reports/1977222
- **Submitted:** 2023-05-08
- **Reporter:** akshayravic09yc47
- **Program:** Nextcloud
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Open Redirect, Insufficient Input Validation, Unvalidated Redirect
- **CVEs:** CVE-2023-35171
- **Category:** uncategorised

## Summary
The UnsupportedBrowser.vue component in Nextcloud Server contains an open redirect vulnerability in the redirect_url parameter. An attacker can base64-encode a malicious URL and trick users into visiting a crafted link that redirects them to arbitrary external sites. The vulnerability exists because the decoded URL is never validated before performing the redirect.

## Attack scenario
1. Attacker identifies the UnsupportedBrowser.vue component that accepts a redirect_url query parameter
2. Attacker base64-encodes a malicious URL (e.g., attacker.com/phishing) to bypass simple checks
3. Attacker crafts a URL on the legitimate Nextcloud domain with the malicious payload: ?redirect_url=base64_encoded_malicious_url
4. Attacker sends this link to victims via email, social engineering, or by compromising legitimate resources
5. Victim visits the link from the trusted Nextcloud domain, triggering the unsupported browser warning
6. The JavaScript code decodes the redirect_url parameter and redirects the victim to attacker.com without validation

## Root cause
The application decodes and trusts user-supplied input without performing URL validation. The code extracts the redirect_url query parameter, decodes it from base64, and immediately assigns it to window.location without checking if the URL is a trusted internal URL or whitelisted domain.

## Attacker mindset
An attacker leverages base64 encoding as obfuscation to appear legitimate while redirecting users to phishing pages or malware distribution sites. By exploiting trust in the Nextcloud domain, the attacker increases click-through rates for credential theft or malware delivery campaigns.

## Defensive takeaways
- Implement URL validation before redirects by checking if URLs are relative paths or belong to a whitelist of trusted domains
- Use URL parsing to verify the protocol (http/https only) and hostname against allowed hosts
- Consider avoiding client-side redirects with user input entirely; use server-side validation instead
- Implement user warnings before redirecting to external domains, similar to HackerOne's approach
- Add a safelist of allowed redirect destinations rather than blocking malicious patterns
- Sanitize and validate all URL parameters regardless of encoding (base64, URL-encoded, etc.)
- Use Content-Security-Policy headers to restrict redirect destinations

## Variant hunting
Search for similar patterns in other .vue components or JavaScript files that: (1) accept URL parameters (redirect, return_url, next, callback, etc.), (2) decode or parse user input, (3) perform window.location assignments, (4) exist in authentication or error handling flows. Check for bypass attempts using protocol-relative URLs (//attacker.com), data URIs, javascript: schemes, or nested encoding.

## MITRE ATT&CK
- T1598.003
- T1566.002
- T1195.002

## Notes
Base64 encoding is not a security measure and should not be relied upon for validation. The vulnerability is exacerbated by its placement on the unsupported browser warning page, which may appear less scrutinized by users. Server-side validation with allowlist checking is the recommended mitigation approach.

## Full report
<details><summary>Expand</summary>

Hello team,
The below mentioned source code is using a unsanitized URL redirection mechanism which will cause open redirection vulnerability

```
			const urlParams = new URLSearchParams(window.location.search)
			if (urlParams.has('redirect_url')) {
				const redirectPath = Buffer.from(urlParams.get('redirect_url'), 'base64').toString() || '/'
				window.location = redirectPath
				return
			}
```
The `UnsupportedBrowser.vue` component used to display a message to users of unsupported browsers. If the user's browser is unsupported, it will display a message with an icon and a button to continue browsing with the unsupported browser.The script checks if there is a query parameter called `redirect_url` in the query string. If the parameter is present, it decodes the value of the parameter from base64 and then redirects the user to the decoded URL and it does not validate the decoded URL or check whether it is a trusted URL before redirecting the user. This makes it possible for an attacker to construct a malicious URL that includes the `redirect_url` parameter and a URL of their choice. When a user clicks on the link, the script will decode the value of the `redirect_url` parameter and redirect the user to the attacker's URL

#Vulnerable Source Permalink:
https://github.com/nextcloud/server/blob/master/core/src/views/UnsupportedBrowser.vue#L140-#L146

#Mitigation:
- Use any functions that check if the input of the `redirect_url` parameter and ensure that it is a trusted URL before redirecting the user.
- Add a Link warning popup like hackerone do, proceed redirection only when user accept the conditions, example like this:

{F2340720}

## Impact

If the app does not validate untrusted user input, an attacker could supply a URL that redirects an unsuspecting victim from a legitimate domain to an attacker's site.

</details>

---
*Analysed by Claude on 2026-05-24*
