# Open Redirect on hackerone.com via URL Path Traversal

## Metadata
- **Source:** HackerOne
- **Report:** 57163 | https://hackerone.com/reports/57163
- **Submitted:** 2015-04-18
- **Reporter:** abze
- **Program:** HackerOne
- **Bounty:** Not specified in report
- **Severity:** Medium
- **Vuln:** Open Redirect, URL Path Traversal, Insufficient Input Validation
- **CVEs:** None
- **Category:** uncategorised

## Summary
An open redirect vulnerability exists on hackerone.com where specially crafted URLs with encoded forward slashes and path traversal sequences can redirect users to arbitrary domains. The vulnerability allows attackers to bypass URL validation by using URL encoding and double slashes in the path component.

## Attack scenario
1. Attacker crafts a malicious URL using encoded forward slash (%2F) followed by a target domain: https://hackerone.com/%2F1572395042
2. Attacker embeds this URL in a phishing email or social engineering message, appearing to come from a trusted HackerOne domain
3. Victim clicks the link believing it originates from HackerOne due to domain trust
4. The application processes the encoded URL and redirects to the attacker's specified domain (example.com)
5. Victim is now on attacker-controlled domain where credentials or sensitive information can be harvested
6. Attacker uses stolen session tokens or credentials to impersonate the victim on HackerOne

## Root cause
The application's redirect handling mechanism fails to properly validate and normalize URLs before performing redirects. The validation logic either: (1) does not decode URL-encoded characters before comparison, (2) does not properly validate the destination domain, or (3) treats double slashes (//) as equivalent to single slashes without proper canonicalization.

## Attacker mindset
An attacker would seek to abuse trust in the HackerOne domain for credential harvesting, session hijacking, or malware distribution. The attacker specifically investigated URL encoding patterns and discovered that certain domain patterns bypass validation (//hackerone.com works but //hackerone1.com doesn't), indicating they performed fuzzing to understand the validation logic.

## Defensive takeaways
- Implement strict URL validation using allowlists rather than blocklists
- Canonicalize and fully decode all URLs before validation and comparison
- Validate that redirect destinations are same-origin or on an approved domain whitelist
- Implement proper URL parsing using language-native libraries rather than regex or manual string manipulation
- Use relative URL redirects where possible instead of absolute URLs
- Implement Content Security Policy (CSP) with frame-ancestors and base-uri directives
- Add security headers to prevent unintended redirects
- Log and monitor redirect attempts to unusual domains for security analysis

## Variant hunting
Test other URL encoding schemes: %252F (double encoding), Unicode escapes, backslash encoding
Test protocol-relative URLs: //example.com, ///example.com
Test with various protocol schemes: javascript:, data:, vbscript:
Test subdomain variations: https://hackerone.com/@example.com, https://hackerone.com/;example.com
Test parameter-based redirects if present: ?redirect=, ?url=, ?next=
Test using null bytes: %00, to truncate validation logic
Test with internationalized domain names (IDN) bypasses

## MITRE ATT&CK
- T1598.003
- T1598.002
- T1566.002
- T1187

## Notes
The reporter demonstrated security awareness by not only reporting the vulnerability but also investigating its scope and peculiar behavior (why //hackerone.com works but //hackerone1.com doesn't). This suggests the validation logic may check for domain presence or use pattern matching rather than proper URL parsing. The encoded forward slash (%2F) bypass indicates insufficient URL normalization. The reporter's incomplete investigation actually provides good direction for HackerOne's security team to focus on URL parsing and validation logic in their redirect handling.

## Full report
<details><summary>Expand</summary>

Hello!

I would like to report about open-redirect on hackerone.com

Here is the PoC that redirects to example.com IP address: https://hackerone.com/%2F1572395042

There is one more strange behavior in URL. For example:
https://hackerone.com//hackerone.com - works
https://hackerone.com//hackerone1.com - doesn't work

I will investigate it further and get back with details if I find something more.

Thanks!

</details>

---
*Analysed by Claude on 2026-05-24*
