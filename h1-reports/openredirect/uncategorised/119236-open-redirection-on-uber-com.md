# Open Redirection via Double Slash Path Traversal on Uber.com

## Metadata
- **Source:** HackerOne
- **Report:** 119236 | https://hackerone.com/reports/119236
- **Submitted:** 2016-02-28
- **Reporter:** rohk
- **Program:** Uber
- **Bounty:** Not specified in report
- **Severity:** medium
- **Vuln:** Open Redirection, URL Manipulation, Path Traversal
- **CVEs:** None
- **Category:** uncategorised

## Summary
An open redirection vulnerability exists on Uber.com where double slashes in the URL path can be exploited to redirect users to arbitrary external websites. By crafting URLs like `http://uber.com//[external-domain]/[path]`, attackers can bypass SSL validation and redirect authenticated users to malicious sites while maintaining Uber's trusted domain in the URL bar.

## Attack scenario
1. Attacker identifies that Uber.com improperly parses URLs with double slashes (//)
2. Attacker crafts a malicious URL such as `http://uber.com//attacker.com/phishing-page` that redirects to their control
3. Attacker distributes the link via email, chat, or social media, claiming it leads to legitimate Uber content
4. User clicks the link believing it originates from Uber due to the domain in the URL
5. Browser redirects user to attacker's domain while displaying Uber.com in address bar initially
6. Attacker captures credentials or delivers malicious content (malware, phishing forms)

## Root cause
Improper URL parsing and validation logic that fails to normalize path separators. The application likely does not canonicalize URLs before processing redirects, allowing double slashes to be interpreted as a protocol-relative URL or path escape mechanism. When combined with HTTP (non-HTTPS), the redirect occurs without SSL/certificate validation warnings.

## Attacker mindset
Phishing and social engineering through URL spoofing. The attacker recognized that users trust the visible domain in URLs and exploited weak path parsing to create URLs that appear to come from Uber while actually redirecting elsewhere. The progression from HTTPS failures to HTTP success indicates methodical testing of the validation logic.

## Defensive takeaways
- Implement strict URL canonicalization before any redirect logic (normalize //, ///, etc.)
- Use URL parsing libraries that enforce strict RFC compliance rather than custom parsing
- Whitelist allowed redirect destinations and reject any external URLs
- Enforce HTTPS-only redirects with HSTS headers to prevent protocol downgrade attacks
- Implement redirect validation that detects and blocks protocol-relative URLs (//example.com)
- Log and monitor suspicious redirect attempts for security analytics
- Use Content-Security-Policy headers to restrict redirection behavior
- Security review all user-controlled URL parameters used in redirect logic

## Variant hunting
Test triple slashes and other path separator combinations (///, ////, etc.)
Attempt backslash variations on Windows-based backends (\\domain.com)
Test with encoded slashes (%2f, %252f) that may bypass initial validation
Check subdomain handling: `uber.com.attacker.com` style domain confusion
Test fragments and query parameters for similar redirect logic
Examine other URL schemes (ftp://, file://, javascript:) for additional bypass vectors
Test with different TLDs and domain structures
Check if the vulnerability exists on subdomains or regional variants

## MITRE ATT&CK
- T1598.003 - Phishing: Spearphishing Link
- T1566.002 - Phishing: Phishing - Email
- T1566.004 - Phishing: Phishing - Social Media

## Notes
This is a classic open redirection vulnerability with moderate impact. The progression of the researcher's testing methodology is notable—they systematically tested HTTPS (failed), then HTTP (succeeded), identifying that SSL validation was the limiting factor. The practical impact is primarily phishing/social engineering rather than direct authentication bypass. The bounty amount appears redacted or not publicly disclosed in the report content provided.

## Full report
<details><summary>Expand</summary>

There seems to be an open redirection on Uber.com

When a user uses `https://www.uber.com//google.com/cities` it will lead to a `Page Not Found` on the Uber website but if the google.com is changed to an IP address such as `https://www.uber.com//216.58.217.206/[param]` it will lead to either a 404 or an SSL error depending on what kind of website you are trying to reach.
But remove the `https://` and now you will be able to reach any website with the IP address. `uber.com//216.58.217.206/calendar` will redirect to Google's Calendar without any of the SSL error or 404 error.

Also for an hyperlink to be activated the attacker can send the URL `http://uber.com//216.58.217.206/calendar` (changing the https -> http)

Proof of Concept:
A user can be sent a URL link that can lead to malicious content. The user will believe the link is trust-worthy because it still has the name of Uber.

</details>

---
*Analysed by Claude on 2026-05-24*
