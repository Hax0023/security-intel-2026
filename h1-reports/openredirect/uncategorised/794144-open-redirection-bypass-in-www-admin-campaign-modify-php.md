# Open Redirection Bypass in /www/admin/campaign-modify.php via Protocol-Relative URL Encoding

## Metadata
- **Source:** HackerOne
- **Report:** 794144 | https://hackerone.com/reports/794144
- **Submitted:** 2020-02-12
- **Reporter:** hoangn14
- **Program:** Unknown
- **Bounty:** Not specified in writeup
- **Severity:** medium
- **Vuln:** Open Redirection, Insufficient Input Validation, URL Filtering Bypass
- **CVEs:** CVE-2020-8143
- **Category:** uncategorised

## Summary
An open redirection vulnerability exists in the campaign-modify.php admin endpoint that fails to properly validate the returnurl parameter. By encoding multiple forward slashes as %2F%2F%2F%2F, attackers can bypass the redirect filter to redirect users to arbitrary external domains, enabling phishing attacks.

## Attack scenario
1. Attacker crafts a malicious URL: /www/admin/campaign-modify.php?clientid=&campaignid=&returnurl=%2F%2F%2F%2Fmalicious.com
2. Attacker sends the link to an admin user via phishing email or social engineering
3. Admin user clicks the link, views legitimate campaign modification page (appears trustworthy due to domain)
4. After completing actions, user is redirected via the returnurl parameter
5. Browser interprets %2F%2F%2F%2Fmalicious.com as a protocol-relative URL (////malicious.com)
6. User is redirected to attacker-controlled phishing page and credentials/sensitive data are harvested

## Root cause
The application implements a blacklist-based redirect filter that only checks for obvious redirect patterns (likely http://, https://, //) but fails to account for URL encoding bypasses using percent-encoded slashes (%2F). The filter doesn't properly decode and validate the parameter before processing redirects.

## Attacker mindset
Target admin users with legitimate-looking redirects from trusted domains to harvest credentials or steal session tokens. The encoding bypass allows evasion of basic security filters through simple encoding obfuscation.

## Defensive takeaways
- Use whitelist-based validation for redirect destinations instead of blacklist filtering
- Decode URL parameters before applying validation logic to catch encoded bypass attempts
- Implement strict redirect validation using URL parsing libraries rather than regex patterns
- Validate that redirect URLs are relative (start with /) or belong to whitelisted domains only
- Avoid trusting user-supplied redirect parameters; use server-side redirect mappings instead
- Log and alert on suspicious redirect attempts for security monitoring

## Variant hunting
Check other parameters accepting URLs (callback, redirect, next, return, goto, forward, etc.)
Test double URL encoding (%252F%252F%252F%252F) and mixed encoding bypasses
Test Unicode encoding (\u002F) and HTML entity encoding variants
Check for similar vulnerabilities in other admin endpoints
Test backslash encoding (%5C) for Windows path bypass
Examine if path traversal (../) can be used in conjunction with redirect bypass
Test with data: URIs, javascript: URIs, and blob: URIs

## MITRE ATT&CK
- T1598.003
- T1566.002
- T1598.002

## Notes
The vulnerability specifically leverages protocol-relative URL syntax (////) combined with URL encoding to bypass simplistic string matching filters. This is a common pattern in redirect vulnerabilities where developers forget to account for multiple encoding layers. Admin endpoints are particularly high-value targets as they have elevated privileges.

## Full report
<details><summary>Expand</summary>

### Description
- There is an open redirect on /www/admin/campaign-modify.php?return_url= {F713773}
- By using //// at the start of the link, you can bypass the open redirect filter.

- example: `/www/admin/campaign-modify.php?clientid=&campaignid=&returnurl=%2F%2F%2F%2Fhackerone.com`

## Impact

This vulnerability can be used for phishing attacks

</details>

---
*Analysed by Claude on 2026-05-24*
