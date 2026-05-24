# Open Redirection via Case-Sensitive Bypass and Decimal IP Encoding at Chaturbate Login

## Metadata
- **Source:** HackerOne
- **Report:** 411723 | https://hackerone.com/reports/411723
- **Submitted:** 2018-09-20
- **Reporter:** shailesh4594
- **Program:** Chaturbate
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Open Redirection, Insufficient Input Validation, Weak Access Control
- **CVEs:** None
- **Category:** uncategorised

## Summary
The login endpoint at chaturbate.com/auth/login/ contains an open redirection vulnerability in the 'next' parameter. While a protection mechanism exists to block 'http' keyword detection, it can be bypassed through case manipulation ('Http:') combined with decimal-encoded IP addresses, allowing attackers to redirect authenticated users to arbitrary external sites.

## Attack scenario
1. Attacker crafts a malicious URL: https://chaturbate.com/auth/login/?next=Http://3627732462 (or similar decimal IP encoding)
2. Attacker distributes the URL via phishing email, social media, or other channels targeting Chaturbate users
3. Victim clicks the link and is presented with the legitimate Chaturbate login page
4. Victim authenticates with their credentials on the genuine login form
5. After successful authentication, the application processes the 'next' parameter and bypasses the weak validation
6. User is silently redirected to attacker's controlled domain (e.g., phishing page mimicking Chaturbate) where credentials or sensitive information can be harvested

## Root cause
The validation logic implements a case-sensitive blacklist check for the 'http' keyword without proper canonicalization. The protection fails because: (1) string matching is case-sensitive, allowing 'Http:' bypass, (2) decimal IP notation (e.g., 3627732462 instead of dotted notation) evades pattern-based detection, (3) no whitelist of allowed domains or URL scheme validation is implemented.

## Attacker mindset
An attacker recognizes that simple keyword filtering is ineffective and exploits common encoding/obfuscation techniques. The attacker understands HTTP URL structure variations and IP address representation formats. They target the post-authentication redirect because users trust it comes from the legitimate application, making phishing more effective.

## Defensive takeaways
- Implement allowlist-based validation for redirect destinations (whitelist known internal domains/paths)
- Use case-insensitive regex patterns or normalize input to lowercase before validation
- Validate URL scheme, hostname, and port using URL parsing libraries rather than string matching
- Consider implementing URL encoding/decoding before validation to catch obfuscated payloads
- Avoid relying solely on blacklist approaches; combine with URL parsing and domain whitelisting
- Add security headers like X-Frame-Options to prevent clickjacking on redirect targets
- Log and monitor unusual redirect attempts for anomaly detection
- Educate users about open redirection risks and how to verify URLs before clicking

## Variant hunting
Test uppercase variations: HTTPS://, hTTp://, HtTp://, etc.
Try alternative IP representations: octal notation, hexadecimal, mixed notation
Test protocol variations: ftp://, file://, javascript://, data:// schemes
Check if double-encoding bypasses validation: %48%74%74%70://
Test with null bytes: http%00.com to see if validation is truncated
Try newline injection: http%0d%0agoogle.com
Test with tab/space characters: ht tp://
Check if backslash escaping works: htt\p://
Test redirect parameter variations: redirect=, return=, goto=, url=
Test with port numbers and credentials in URL: http://attacker:pass@google.com/

## MITRE ATT&CK
- T1598.003
- T1566.002
- T1192

## Notes
This is a classic case of weak input validation being circumvented through simple obfuscation. The vulnerability is particularly dangerous in authentication flows because users have just logged in and are in a trusting state. The decimal IP encoding (3627732462 = 216.58.192.142, Google's IP) demonstrates how attackers combine multiple evasion techniques. Chaturbate's platform and user base make this especially impactful for phishing campaigns targeting adult content consumers.

## Full report
<details><summary>Expand</summary>

Hi,

##Summary##
An attacker can redirect vicitm on an external website using https://chaturbate.com/auth/login/ endpoint because `next` parameter is not being validated properly. There is a protection existed but it's weak and can be bypassed.

`http` keyword is detected and protection works if payload contains `http` at beginning but that check can be bypassed using `Http` keyword. Though, only numeric is allowed after `Http:` so we can use decimal form of external domain/IP-address. In PoC, `3627732462` is decimal form of IP address of google.com.

## Steps To Reproduce:

  1. Open https://chaturbate.com/auth/login/?next=Http:3627732462
  1. Get logged in
  1. You will be redirected on https://google.com instead of a chaturbate website
  1. Done

###Suggested Fix:
Use more strong regular expression at this endpoint.

## Impact

- Simplifies phishing attacks
- Reflected File Download

</details>

---
*Analysed by Claude on 2026-05-24*
