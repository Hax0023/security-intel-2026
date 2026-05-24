# Open Redirect via Bypass Filter in semrush.com Login

## Metadata
- **Source:** HackerOne
- **Report:** 716976 | https://hackerone.com/reports/716976
- **Submitted:** 2019-10-18
- **Reporter:** batuhanu
- **Program:** Semrush
- **Bounty:** Not specified
- **Severity:** Medium
- **Vuln:** Open Redirect, Input Validation Bypass
- **CVEs:** None
- **Category:** uncategorised

## Summary
An open redirect vulnerability exists in the login page redirect_to parameter that can be bypassed using /\ prefix notation to circumvent existing filters. Attackers can redirect authenticated users to arbitrary external domains for phishing purposes.

## Attack scenario
1. Attacker crafts malicious link: www.semrush.com/login/?redirect_to=/\attacker.com/phishing
2. Attacker sends link via email/social engineering to Semrush users
3. User clicks link and logs in normally at Semrush login page
4. After successful authentication, user is redirected to attacker.com/phishing
5. Attacker's phishing page mimics Semrush to capture additional credentials or sensitive data
6. User data or session tokens are compromised

## Root cause
Insufficient validation of the redirect_to parameter. The filter likely blocked common redirect prefixes (http://, https://, //) but failed to account for alternative bypass techniques using backslash escaping or path traversal notations.

## Attacker mindset
Finding weaknesses in security filters through fuzzing variations of payload syntax; leveraging post-authentication redirect chains where users implicitly trust the redirect destination.

## Defensive takeaways
- Implement whitelist-based redirect validation instead of blacklist filtering
- Validate redirect URLs against a whitelist of allowed domains
- Use allowlist of permitted redirect paths (relative URLs only)
- Normalize and decode user input before validation to catch bypass attempts
- Test filter logic against various bypass techniques (/\, //, //, /;, %2f, etc.)
- Implement Content Security Policy headers to restrict redirect destinations
- Log and monitor unusual redirect patterns for security alerting

## Variant hunting
Test other parameters accepting URLs (return_to, back, continue, next, url)
Test double encoding variations (%252f%252f)
Test Unicode normalization bypasses
Test mixed case protocol variations (HtTp://)
Test null byte injection (/\x00/)
Test alternative protocols (javascript:, data:, ftp://)

## MITRE ATT&CK
- T1598.003 - Phishing: Spearphishing Link
- T1566.002 - Phishing: Phishing - Link
- T1021.001 - Remote Services: Remote Service Session Hijacking

## Notes
This is a classic filter bypass vulnerability. The /\ syntax likely works because the backslash is interpreted differently across URL parsing implementations. The vulnerability is particularly effective because it leverages legitimate post-login behavior that users trust implicitly.

## Full report
<details><summary>Expand</summary>

**Summary:** 
There is an open redirect on https://www.semrush.com/login/?redirect_to=.
By using /\ at the start of the link, you can bypass the open redirect filter.

**Description:** 
An attacker can control the value of the "redirect_to" parameter and make it redirect to a malicious endpoint.

## Steps To Reproduce:
Visit: `www.semrush.com/login/?redirect_to=/\google.com`
Once you login, you will be redirected to google.com

## Impact

This vulnerability can be used for phishing attacks

</details>

---
*Analysed by Claude on 2026-05-24*
