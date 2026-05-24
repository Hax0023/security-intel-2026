# Bypass of Open Redirect Fix on lovable.dev via /..// Path Traversal in redirect parameter

## Metadata
- **Source:** HackerOne
- **Report:** 3599248 | https://hackerone.com/reports/3599248
- **Submitted:** 2026-03-12
- **Reporter:** marioniangi
- **Program:** lovable.dev
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Open Redirect, Path Traversal Bypass, Incomplete Input Validation
- **CVEs:** None
- **Category:** uncategorised

## Summary
A bypass exists for a previously patched open redirect vulnerability where path traversal sequences (/..//) combined with double slashes circumvent the denylist-based fix. Attackers can redirect authenticated users to arbitrary external domains via crafted redirect parameters, enabling phishing attacks against trusted users.

## Attack scenario
1. Attacker identifies the patched open redirect vulnerability uses a denylist approach blocking /\ and /%5C
2. Attacker discovers that path traversal normalization combined with protocol-relative URLs bypasses the denylist
3. Attacker crafts malicious URL: https://lovable.dev/auth/post-login?redirect=/..//google.com
4. Attacker sends URL to target user in phishing email, appearing to come from trusted lovable.dev domain
5. Authenticated user clicks link and is silently redirected to attacker-controlled lookalike domain
6. Attacker harvests credentials or session tokens from redirected victim

## Root cause
The previous patch implemented a denylist-based approach targeting specific encoding patterns (/\ and /%5C) rather than adopting proper allowlist validation or secure URL parsing. Path traversal sequences (/..//) are normalized by the server before processing, converting the payload to //google.com which is then interpreted as a protocol-relative URL, bypassing the incomplete denylist.

## Attacker mindset
Attacker demonstrated methodical vulnerability analysis by understanding the previous patch mechanism and finding orthogonal bypass techniques. This shows understanding of URL parsing mechanics, path normalization behaviors, and the weakness of denylist approaches. Attacker likely follows security research principles of testing complementary payloads when initial vectors are blocked.

## Defensive takeaways
- Use allowlist-based validation instead of denylists for redirect parameters; only permit URLs matching approved domains or relative paths
- Implement proper URL parsing libraries (not regex) to validate redirect targets before normalization
- Normalize user input before validation, not after, to prevent bypass through encoding/traversal tricks
- Perform security regression testing when patching vulnerabilities to ensure new payloads and variants are blocked
- Consider redirects to external domains as high-risk and require explicit allowlisting per domain
- Log and monitor suspicious redirect attempts for security anomalies

## Variant hunting
Test other path traversal patterns: /..\/, /../\/, /...//
Test double-encoding: /%2e%2e%2fgoogle.com
Test mixed case: /..//Google.com
Test backslash variants on different URL schemes: \\google.com, /%5cgoogle.com
Test directory traversal with dots: /./google.com, ////google.com
Test null byte injection if applicable: /..//google.com%00
Test other denylist bypasses: @google.com, google.com#, javascript:, data:

## MITRE ATT&CK
- T1190
- T1598
- T1566

## Notes
This report exemplifies the fundamental weakness of security-through-obscurity approaches (denylists). The vulnerability was previously reported (#3581815) and patched incompletely, indicating insufficient security review depth. The /..// bypass is elegantly simple, combining path traversal normalization with protocol-relative URL parsing—two standard web technologies that interact unexpectedly. This demonstrates the importance of understanding the full request processing pipeline when implementing security fixes.

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
