# Open Redirect Filter Bypass via Backslash Character in URL Parameter

## Metadata
- **Source:** HackerOne
- **Report:** 840736 | https://hackerone.com/reports/840736
- **Submitted:** 2020-04-05
- **Reporter:** cristiancornea
- **Program:** myndr.net
- **Bounty:** Not specified in writeup
- **Severity:** medium
- **Vuln:** Open Redirect, Authentication Bypass, URL Validation Bypass
- **CVEs:** None
- **Category:** uncategorised

## Summary
An open redirect vulnerability exists in the ref_url parameter on meta.myndr.net due to improper domain validation. The filter checking for trusted domain 'dashboard.myndr.net' can be bypassed by injecting a backslash character before the trusted domain name, causing redirects to attacker-controlled domains. This enables phishing attacks while appearing to redirect through a trusted domain.

## Attack scenario
1. Attacker identifies the ref_url parameter on meta.myndr.net/latest/meta-data/filter-id/add used for redirects
2. Attacker discovers the application validates against trusted domain 'dashboard.myndr.net'
3. Attacker crafts malicious URL: http://meta.myndr.net/latest/meta-data/filter-id/add/?ref_url=http://phishing.com\dashboard.myndr.net/../../../
4. Attacker sends crafted URL to victims via email or social engineering
5. Victim clicks link, browser processes backslash as path separator in certain contexts
6. User is redirected to attacker's phishing domain while security filters see 'dashboard.myndr.net' in URL

## Root cause
The application's domain validation logic fails to properly handle backslash characters in URLs. The validation likely uses a string search or regex pattern that only checks if 'dashboard.myndr.net' appears in the URL without normalizing or properly parsing the URL structure. The backslash character is not treated as a special character during validation, allowing it to be inserted between the attacker's domain and the trusted domain.

## Attacker mindset
Attacker systematically tested URL parsing edge cases, discovering that different components (browsers, servers, security filters) handle backslashes inconsistently. The attacker recognized that inserting a backslash before the trusted domain creates a discrepancy between what security tools see (trusted domain present) and where the actual redirect goes (attacker domain). This is a classic case of exploiting inconsistencies between validation logic and actual URL behavior.

## Defensive takeaways
- Never rely on string matching or substring searches for URL validation - use proper URL parsing libraries
- Normalize URLs before validation by decoding percent-encoded characters and resolving path traversal sequences
- Use whitelist-based validation with explicit protocol and domain checks, not blacklist/filter approaches
- Parse URLs using language-native URL parsing functions that handle edge cases consistently
- Validate the final redirect destination after all URL processing is complete
- Be aware that different URL parsers (browsers, servers, security tools) may interpret special characters differently
- Include backslash and other special characters in test cases for URL validation logic
- Implement server-side redirect validation that resolves the final destination before redirecting

## Variant hunting
Test other special characters that may be mishandled: forward slash variations, encoded characters (%2f, %5c), mixed case domain comparisons
Try alternative path traversal: http://phishing.com/./dashboard.myndr.net, http://phishing.com%5cdashboard.myndr.net
Test on different URL parameters beyond ref_url that accept redirect destinations
Check if other trusted domains in the application have similar bypass possibilities
Test URL fragments and query parameters: http://phishing.com#dashboard.myndr.net, http://phishing.com?domain=dashboard.myndr.net
Investigate if other special characters like null bytes or unicode characters bypass validation

## MITRE ATT&CK
- T1598.003
- T1566.002
- T1021.005

## Notes
This vulnerability demonstrates the importance of secure redirect implementation. The bypass method exploits a fundamental mismatch between how the validation logic interprets the URL string and how browsers/servers actually process it. The backslash character behavior varies significantly across platforms - in some contexts it's treated as a path separator, in others as a literal character, which the attacker leveraged. The vulnerability is particularly dangerous because it maintains the appearance of a trusted domain in the URL string while actually redirecting elsewhere, making it effective against both automated security filters and human inspection.

## Full report
<details><summary>Expand</summary>

Hi, I hope I find you all safe and good regarding those hard times nowadays.

## Summary:
Found an Open Redirect vulnerability on http://meta.myndr.net by bypassing the trusted domain filter using a '\' character.

I was able to get the original redirection URL from the register button located at http://dashboard.myndr.net/auth/login

Original Redirection URL
```http://meta.myndr.net/latest/meta-data/filter-id/add?ref_url=http://dashboard.myndr.net/auth/register?id= ```

Malicious URL 
```http://meta.myndr.net/latest/meta-data/filter-id/add/?ref_url=http://phishing.com\dashboard.myndr.net/../../../ ```

The vulnerable URL parameter is ```ref_url```

The trusted domain (or string) is ```dashboard.myndr.net```

It can be bypassed only from its beginning!  (between ```http://``` and the string) and not after ```.net```

## Steps To Reproduce:
Navigate to : ```http://meta.myndr.net/latest/meta-data/filter-id/add/?ref_url=http://phishing.com\dashboard.myndr.net/../../../```

You will be redirected to ```phising.com``` domain

## PoC: attached to the report

## Impact

1. Phishing campaigns can be initiated using such a vulnerability
2. It is an efficient way to bypass monitoring and email filters within an organization (the organization can check the "trust" level of each domains that they receive emails from)

</details>

---
*Analysed by Claude on 2026-05-24*
