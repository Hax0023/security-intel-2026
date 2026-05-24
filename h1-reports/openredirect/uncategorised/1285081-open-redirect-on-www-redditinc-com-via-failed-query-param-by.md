# Open Redirect Bypass on www.redditinc.com via `failed` Parameter

## Metadata
- **Source:** HackerOne
- **Report:** 1285081 | https://hackerone.com/reports/1285081
- **Submitted:** 2021-07-30
- **Reporter:** lu3ky-13
- **Program:** Reddit/Reddit Inc
- **Bounty:** Not specified in report
- **Severity:** medium
- **Vuln:** Open Redirect, URL Parameter Validation Bypass
- **CVEs:** None
- **Category:** uncategorised

## Summary
A researcher discovered a bypass to a previously patched open redirect vulnerability (report #1257753) on Reddit's AMA form submission endpoint. By using the protocol-relative URL format (//evil.com) in the `failed` parameter instead of fully qualified URLs, the security fix was circumvented, allowing attackers to redirect users to arbitrary external domains.

## Attack scenario
1. Attacker crafts a malicious URL targeting www.redditinc.com/ama endpoint with a legitimate-looking form submission
2. Attacker sets the `failed` parameter to //evil.com (protocol-relative URL) instead of http://evil.com to bypass the original validation
3. Attacker shares the crafted URL in Reddit communities or via phishing emails, appearing to be from Reddit's official AMA page
4. User fills out the AMA request form and on validation failure, gets redirected to evil.com instead of staying on Reddit's domain
5. Attacker can host credential harvesting pages, malware, or perform further social engineering attacks on the redirected users

## Root cause
Incomplete URL validation in the `failed` parameter handler. The original fix likely blocked absolute URLs (http://, https://) but failed to account for protocol-relative URLs (//), which browsers interpret as valid redirects to any domain using the current protocol.

## Attacker mindset
The researcher demonstrated security-conscious behavior by reporting the bypass responsibly. However, from an attacker's perspective, this represents discovering a bypass technique to weaponized parameters—testing protocol-relative URL encoding, different URL schemes, and encoding variations to evade input validation filters.

## Defensive takeaways
- Implement whitelist-based URL validation using URL parsing libraries rather than blacklist regex patterns
- Validate both absolute URLs (http://, https://) and protocol-relative URLs (//)
- Use strict redirect validation: only allow redirects to whitelisted domains or relative paths (starts with /)
- Parse URLs using built-in language libraries to normalize and validate before comparison
- Implement server-side redirect validation separate from client-side checks
- Regular security testing of previously patched vulnerabilities with variant payloads

## Variant hunting
Test similar parameters for open redirect: `success`, `redirect`, `return_to`, `next`, `continue`, `goto`. Try URL encoding variations: %2f%2f, backslash variants, data: URLs, javascript: protocols. Test on other Reddit subdomains and form endpoints. Check for improper encoding of already-encoded slashes.

## MITRE ATT&CK
- T1598.003 - Phishing: Spearphishing Link
- T1566.002 - Phishing: Phishing - Link
- T1589.001 - Gather Victim Identity Information: Credentials

## Notes
This is a classic bypass scenario where a security patch was incomplete. The researcher appropriately reported the original vulnerability first, then discovered the bypass when testing the fixed version. The use of //evil.com (protocol-relative URLs) is a well-known bypass technique that should be included in security testing playbooks. The report includes multiple screenshots and the complete POC URLs, making reproduction straightforward.

## Full report
<details><summary>Expand</summary>

hello dear support

i have found bypass to open redirect this submission #1257753 after the fixed by sec team 
{F1394378}
old open redirect it;s fixed and not working  this url 
https://www.redditinc.com/ama?action=zendesk%2fdefault%2fsubmit&redirect=74bcbfb4f9c047fb4e467dd203ca3b30f2b31216551ab9db2bf44911c029d506thank-you%2fama-form-step-1&success=thank-you%2fama-form-step-1&failed=http://evil.com&ticket_form_id=360000307211&subject=AMA+Request&name=%27%22%3e%3c%2fscript%3e%3cimg+src%3dx+onerror%3dalert%28%29%3e%7b%7b7*7%7d%7d&email=wehifyyis@solarunited.net&email_confirm=wehifyyis@solarunited.net&participants=%27%22%3e%3c%2fscript%3e%3cimg+src%3dx+onerror%3dalert%28%29%3e%7b%7b7*7%7d%7d&description=%27%22%3e%3c%2fscript%3e%3cimg+src%3dx+onerror%3dalert%28%29%3e%7b%7b7*7%7d%7d&organization=%27%22%3e%3c%2fscript%3e%3cimg+src%3dx+onerror%3dalert%28%29%3e%7b%7b7*7%7d%7d&timeframe=next-week&timezone=%28GMT-05%3a00%29+Eastern+Time+%28US+%26+Canada%29&g-recaptcha-response=03AGdBq26GE8j1nvvxRFyoLySXC_sqwwVN0y8SUOy5Dt_EpgjZ_NcTluixasj63r4R-p88FygQDqWM_xAD2usiKGStmYqRt6o7DKUbfFAoJYH_e2RQnymyCPuln8k3AKMBLEVZ_aGU0hoCqzivt7ZaZWKARPDhrSOacKG4M5O7KD7LIbDAq28NtmuK7ByV0oHsM2uUQOwSv8kfsGRh5pXjLo4No1X2tlQUmj1cy7vEPQ0TJvpWzCLnc8vmhl3tjraPCqIXYkrMuf1nqAPx_0mnggUk_jUAy21JSJVGHJroH3asn70y3wOfCr_nYNAyfWo2mm3Ar5iXNwBOkq7ERaltBj9ZSaZdcOBMTq8tfKrR1mZ0h82owoCQTno3ZXHplZ7XHhegeJDOw5F4dcLHSKmiZfUNDkRqSuCO0HfDxov2ty0FWn_y9RR45fdABD--c0dqITZEUcWqJrkx&agreement=yes
this old  submission

and bypass here  

https://www.redditinc.com/ama?action=zendesk%2fdefault%2fsubmit&redirect=74bcbfb4f9c047fb4e467dd203ca3b30f2b31216551ab9db2bf44911c029d506thank-you%2fama-form-step-1&success=thank-you%2fama-form-step-1&failed=//evil.com&ticket_form_id=360000307211&subject=AMA+Request&name=ergergerg&email=tzzyspu@northsixty.com&email_confirm=tzzyspu@northsixty.com&participants=ergerg&description=ergerg&organization=ergerg&timeframe=month-plus&timezone=%28GMT-07%3a00%29+Arizona&g-recaptcha-response=03AGdBq27Lwm_f_tiYnQMq03oi7u4iTRuxyKgIuJd80Atn2dslKRSRtojLo4zmE7bxWVskHfPWbwB1jhB_nFFnONPa8m3h1ad16G4olvmuj8uTGQEW_LpXhKG3bJqVepH4OVWkZTSo7-sCuhI6ZmyZDa03Ai3zrUvGUeJDUoQGDWW4WgdglWO3TqBzQt_lDcizkX2yGHxasyCkNiifMuarK2Bp6oH52kTUtdnSHoVELj6qDIw0-B1ytpJzKBodibN7txKqSA7-airAZUH7oGU6HZHlH5BW54kJluRlAbGWsL_pMoj6hwYwVFZ7xZzmktYtyHgn5e3TYvd4lUTwmMTReE1v4X0WIID41KgSj9Fcn8KYGo85w5pXY72o-BKWxirNxs_2lh9-WIITsqEL3eTIttbPueaZ5aIb7PS5R51r8nhnTygrWv6_NI8Y5LroEgATxHEch6bWq6-5&agreement=yes


i bypass and i add this //evil.com to  failed=

{F1394382}

{F1394384}

## Impact

Open Redirect and bypass

</details>

---
*Analysed by Claude on 2026-05-24*
