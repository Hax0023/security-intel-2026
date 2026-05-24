# Open Redirect in Switch Account Functionality

## Metadata
- **Source:** HackerOne
- **Report:** 390663 | https://hackerone.com/reports/390663
- **Submitted:** 2018-08-05
- **Reporter:** sumni
- **Program:** Unknown (HackerOne Report #390663)
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Open Redirect, Unvalidated Redirects and Forwards
- **CVEs:** CVE-2019-5433
- **Category:** uncategorised

## Summary
The account-switch.php endpoint accepts an unvalidated return_url parameter that redirects users to arbitrary external domains. This vulnerability can be exploited in phishing campaigns by crafting malicious URLs that appear legitimate but redirect authenticated users to attacker-controlled sites.

## Attack scenario
1. Attacker discovers the open redirect vulnerability in the return_url parameter of account-switch.php
2. Attacker crafts a malicious URL like http://legitimate-site.com/www/admin/account-switch.php?return_url=http://attacker.com/phish
3. Attacker sends this URL to target users via email, support channels, or social engineering claiming it's a legitimate account action
4. Victim clicks the link while authenticated and is redirected to attacker's phishing page
5. Victim's browser context maintains authentication cookies, making credential theft or session hijacking more convincing
6. Attacker captures credentials or performs further attacks against the victim

## Root cause
The return_url parameter is directly used in a redirect without validation, whitelisting, or domain verification. The application trusts user-supplied input for determining redirect destinations.

## Attacker mindset
Leverage trusted domain context and user authentication state to execute phishing attacks with higher success rates. Use URL obfuscation with unused parameters to increase legitimacy perception and create attribution confusion.

## Defensive takeaways
- Implement domain whitelist validation before redirecting - only allow redirects to same domain or pre-approved domains
- Use URL parsing libraries to validate that redirect targets match current domain
- Implement allowlist patterns for relative URLs only (e.g., /path/to/page)
- Sanitize and validate all redirect parameters on both client and server side
- Log all redirect attempts for security monitoring
- Consider using POST-Redirect-GET pattern with server-stored redirect URLs instead of URL parameters
- Implement Content Security Policy headers to limit external redirects
- Add security warnings when redirecting to external domains

## Variant hunting
Search for other endpoints using redirect/return_url parameters (logout, signin callbacks, etc.)
Test URL encoding bypasses (double encoding, unicode encoding) in return_url
Check for protocol validation bypasses (javascript:, data:, vbscript: schemes)
Test relative vs absolute URL handling
Look for similar patterns in other account management functionalities
Check if authentication state affects validation logic

## MITRE ATT&CK
- T1598.003
- T1192

## Notes
This is a classic open redirect vulnerability with elevated risk due to being in an authenticated context. The attacker's suggested obfuscation techniques demonstrate sophisticated phishing campaign methodology. The fix is straightforward but requires careful implementation to avoid introducing new security issues or breaking legitimate functionality.

## Full report
<details><summary>Expand</summary>

To reproduce this vulnerability:
1. You have to be logged in user
2. Enter address: http://<your_local_installation>/www/admin/account-switch.php?return_url=http://127.0.0.1:12345/test 

This is due to unrestricted redirection url passed in in the `return_url` parameter. I would recommend to use some kind of whitelisting or a check if you are redirecting to the same domain you were before.

## Impact

This kind of open redirect vulnerabilities are used in fishing campaigns. I assume that in this case a support request containing a crafted url would have a higher chances of success. For additional malicious url obfuscation you can:
- add some unused parameters that would suggest identifiers of campaigns, other accounts and other revive specific information
- register a domain name similar to the attacked one

</details>

---
*Analysed by Claude on 2026-05-24*
