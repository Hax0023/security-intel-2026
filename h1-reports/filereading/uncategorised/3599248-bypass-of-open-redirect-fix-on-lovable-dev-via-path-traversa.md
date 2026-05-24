# Bypass of Open Redirect Fix on lovable.dev via /..// Path Traversal in redirect parameter

## Metadata
- **Source:** HackerOne
- **Report:** 3599248 | https://hackerone.com/reports/3599248
- **Submitted:** 2026-03-12
- **Reporter:** marioniangi
- **Program:** lovable.dev
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Open Redirect, Path Traversal, Improper Input Validation, Incomplete Security Patch
- **CVEs:** None
- **Category:** uncategorised

## Summary
A bypass exists for a previously patched open redirect vulnerability where attackers can use path traversal sequences (/..//) combined with double slashes to redirect authenticated users to arbitrary external domains. The original fix used an incomplete denylist blocking only backslash-based payloads (/\ and /%5C) while failing to prevent traversal-based bypasses. This enables phishing attacks against authenticated users who trust the lovable.dev domain.

## Attack scenario
1. Attacker crafts a malicious URL containing the payload: https://lovable.dev/auth/post-login?redirect=/..//attacker.com
2. Attacker sends this URL to victims via email, chat, or social media, appearing trustworthy due to lovable.dev domain
3. Victim clicks the link while already authenticated or authenticates during the process
4. Server processes the redirect parameter and normalizes /..// path traversal, leaving //attacker.com
5. Browser interprets //attacker.com as a protocol-relative URL and redirects to https://attacker.com
6. Victim lands on attacker's phishing page which mimics lovable.dev or a legitimate service, potentially harvesting credentials or session tokens

## Root cause
The previous security patch implemented a denylist approach blocking specific patterns (/\ and /%5C) rather than using a proper allowlist or comprehensive URL validation. The developers failed to account for path traversal sequences (/../) that normalize to double slashes (//), which are valid protocol-relative URL indicators in browsers. The fix was applied to the symptom rather than the underlying validation mechanism.

## Attacker mindset
An opportunistic researcher or malicious actor identified that the previous patch was incomplete by testing alternative path traversal techniques. They recognized that path normalization on the server converts /..// into //, which browsers then interpret as a protocol-relative URL. This approach demonstrates understanding of both server-side path processing and browser URL parsing behaviors, suggesting either fuzzing-based discovery or knowledge of common bypass techniques.

## Defensive takeaways
- Always use allowlist-based validation for redirect URLs rather than denylists; explicitly define trusted redirect domains/patterns
- Implement canonical URL parsing using built-in URL parser libraries (e.g., URL class in JavaScript) to normalize and validate URLs before redirecting
- Avoid relying on string matching or regex patterns for security controls; use proper URL parsing that handles path traversal, encoding, and protocol resolution
- Test security patches comprehensively against variant payloads including path traversal sequences, encoding bypasses, and mixed techniques
- Validate the redirect parameter against an allowlist of internal paths or trusted external domains
- Consider implementing redirect validation on both client and server side with consistent logic
- Log all redirect attempts for security monitoring and anomaly detection

## Variant hunting
Test for similar bypasses on other parameters and endpoints: redirect, return_url, next, target, callback, continue, url parameters using variants such as /..//, /..\/, ..%2F..%2F, encoding combinations (mixed %2F and /), double encoding, null bytes, unicode normalization (e.g., full-width slashes), and other path traversal sequences. Check if the fix was applied consistently across all redirect handlers in the application.

## MITRE ATT&CK
- T1566.002
- T1598.003
- T1598.004
- T1547.015

## Notes
This is a critical example of why incomplete security patches create false confidence. The original vulnerability (#3581815) was not properly resolved; the fix merely raised the bar slightly rather than implementing defense-in-depth. The fact that a bypass was found so quickly (report #3599248 references the earlier patched report #3581815) suggests the patch was inadequately tested. The post-login context makes this particularly dangerous as users are already authenticated and more likely to trust the redirect. The researcher demonstrated good security practice by reporting the bypass rather than exploiting it maliciously.

## Full report
<details><summary>Expand</summary>

## Summary:
A bypass exists for the previously patched open redirect vulnerability (report #3581815) 
on lovable.dev. The original fix blocked backslash-based payloads (/\ and /%5C), but 
fails to account for path traversal sequences combined with double slashes. By supplying 
`/..//google.com` as the redirect value, an attacker can still redirect authenticated 
users to arbitrary external domains.

After logging in, the application processes a redirect via:
https://lovable.dev/auth/post-login?redirect=/..//google.com

The server normalizes the path traversal `/../` and then treats `//google.com` as a 
protocol-relative URL, resulting in a redirect to https://google.com.

This bypass demonstrates that the previous fix used an incomplete denylist rather than 
a proper allowlist or URL parser validation.

## Steps To Reproduce:

1. Create or log in to an existing account on lovable.dev
2. Visit the following URL while authenticated:
   https://lovable.dev/auth/post-login?redirect=/..//google.com
3. Observe that you are redirected to https://google.com (external domain)

## Supporting Material/References:

- Previous related report: #3581815 (resolved)
- Payload used: /..//google.com
- Final redirect URL observed in browser: https://google.com
- The fix from report #3581815 only blocked /\ and /%5C variants
- This payload was not covered by the fix
- I have a poc

## Impact

An attacker can craft a trusted lovable.dev URL that silently redirects authenticated 
users to an arbitrary external website. This can be used in targeted phishing campaigns 
where victims trust the lovable.dev domain in the link. Since the redirect occurs 
post-login, victims are already authenticated, making social engineering attacks 
significantly more credible. The attacker could redirect to a lookalike page to steal 
credentials or session tokens.

</details>

---
*Analysed by Claude on 2026-05-24*
