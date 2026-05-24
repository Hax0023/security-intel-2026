# Open Redirect in Serendipity exit.php

## Metadata
- **Source:** HackerOne
- **Report:** 373932 | https://hackerone.com/reports/373932
- **Submitted:** 2018-06-29
- **Reporter:** bb9866f3f743d6bf69b6836
- **Program:** Serendipity
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Open Redirect, Insufficient URL Validation
- **CVEs:** None
- **Category:** uncategorised

## Summary
Serendipity's exit.php script contains an open redirect vulnerability where the base64-encoded 'url' parameter is decoded and used in a Location header without validating the target hostname. An attacker can craft malicious links pointing to the application that redirect users to arbitrary external URLs, enabling phishing and credential harvesting attacks.

## Attack scenario
1. Attacker identifies exit.php accepts a base64-encoded URL parameter
2. Attacker base64-encodes a malicious URL (e.g., https://attacker.com/phishing) to 'aHR0cHM6Ly9hdHRhY2tlci5jb20vcGhpc2hpbmc='
3. Attacker crafts a deceptive link: https://blog.fuzzing-project.org/exit.php?url=aHR0cHM6Ly9hdHRhY2tlci5jb20vcGhpc2hpbmc= and shares it via email/social media
4. Victim clicks the link trusting the blog.fuzzing-project.org domain in the URL bar
5. The script decodes the parameter and redirects the victim to the attacker's phishing page
6. Victim enters credentials or sensitive information on the fake page controlled by the attacker

## Root cause
The application decodes the base64-encoded URL parameter and passes it directly to the Location header after only checking for response splitting via serendipity_isResponseClean(). No whitelist validation, domain allowlist, or hostname verification is performed to ensure the redirect target is legitimate.

## Attacker mindset
An attacker seeks to leverage the trusted reputation of the Serendipity blog application to conduct phishing campaigns. By using the application's own domain in the URL, the attacker bypasses user trust indicators and increases the likelihood of victims clicking the malicious link. The base64 encoding obfuscates the true destination from casual inspection.

## Defensive takeaways
- Implement a whitelist of allowed redirect domains or require relative URLs only
- Validate that the decoded URL's hostname matches a trusted allowlist before redirecting
- Use URL parsing functions to extract and validate the hostname component separately
- Consider warning users before redirecting to external domains with a confirmation page
- Log all redirect attempts for security monitoring and anomaly detection
- Disable or remove unnecessary redirect functionality if not critical to application logic
- Apply security headers like X-Frame-Options to prevent clickjacking exploitation of the redirect

## Variant hunting
Search for other endpoints accepting URL parameters with insufficient validation (e.g., redirect.php, forward.php, goto.php)
Test for similar vulnerabilities in other Serendipity versions or forks
Check for double encoding bypasses (base64 followed by URL encoding)
Look for other parameters that might be concatenated into Location headers without sanitization
Test for JavaScript-based redirects (javascript: protocol) that might bypass the response splitting check
Investigate if the vulnerability exists in other Serendipity modules or plugins

## MITRE ATT&CK
- T1598.003 - Phishing: Spearphishing Link
- T1566.002 - Phishing: Phishing - Link
- T1557.002 - Adversary-in-the-Middle: ARP Cache Poisoning

## Notes
The vulnerability demonstrates why URL validation must include hostname verification, not just response splitting checks. The base64 encoding was likely intended as obfuscation rather than security, which is a common misconception. The serendipity_isResponseClean() function only prevents header injection attacks (CRLF), not open redirects. This is a classic case where developers relied on a single security function without understanding its limitations.

## Full report
<details><summary>Expand</summary>

## Summary

Serendipity contains a script named `exit.php` that can be directly accessed. When crafting an hyperlink pointing to this page with the parameter `url` containing a base64-encoded  URL, it will redirect the user to this URL.

## Description

The file `exit.php` contains the following code:

```php
<?php
// [...]
if (isset($_GET['url_id']) && !empty($_GET['url_id']) && isset($_GET['entry_id']) && !empty($_GET['entry_id'])) {
// [...]
} elseif (isset($_GET['url']) && !empty($_GET['url'])) {
    // No entry-link ID was submitted. Possibly a spammer tried to mis-use the script to get into the top-list.
    $url = strip_tags(str_replace('&amp;', '&', base64_decode($_GET['url'])));
}

if (serendipity_isResponseClean($url)) {
    header('HTTP/1.0 301 Moved Permanently');
    header('Status: 301 Moved Permanently');
    header('Location: ' . $url);
}
```

The interesting part is the handling of `$_GET['url']`. The function `serendipity_isResponseClean()` tries to prevent response splitting issues but does not validate the hostname of the URL where the user is redirected to. 

## Steps To Reproduce

1. Access https://blog.fuzzing-project.org/exit.php?url=aHR0cHM6Ly9nb29nbGUuY29t with a browser;
1. Notice that the `Location` header of the response contains an arbitrary URL (here, https://google.com).

## Impact

An attacker can craft an hyperlink pointing to https://blog.fuzzing-project.org that, once accessed, will redirect the victim to an arbitrary URL.

</details>

---
*Analysed by Claude on 2026-05-24*
