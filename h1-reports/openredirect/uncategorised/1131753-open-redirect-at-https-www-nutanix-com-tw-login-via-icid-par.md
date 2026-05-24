# Open Redirect at https://www.nutanix.com/tw/login via icid parameter

## Metadata
- **Source:** HackerOne
- **Report:** 1131753 | https://hackerone.com/reports/1131753
- **Submitted:** 2021-03-21
- **Reporter:** zevfw5pp
- **Program:** Nutanix
- **Bounty:** Not specified in report
- **Severity:** medium
- **Vuln:** Open Redirect, URL Parameter Injection
- **CVEs:** None
- **Category:** uncategorised

## Summary
An open redirect vulnerability exists in the Nutanix login page at /tw/login endpoint where the 'redirectUrl' parameter is not properly validated before redirecting users. An attacker can craft a malicious URL with a redirectUrl parameter pointing to an external domain to redirect authenticated users to phishing or malicious sites.

## Attack scenario
1. Attacker crafts a malicious URL with redirectUrl parameter pointing to attacker-controlled phishing domain
2. Attacker sends the URL to Nutanix users via email, social engineering, or other channels
3. User clicks the link believing it's legitimate Nutanix login
4. User enters credentials on legitimate Nutanix login page
5. Upon successful authentication, user is automatically redirected to attacker's domain
6. Attacker harvests additional credentials or performs further phishing attacks

## Root cause
The 'redirectUrl' parameter is accepted and used in redirect functionality without proper validation or allowlisting of safe redirect destinations. The application likely uses client-side redirect logic that trusts user-supplied parameters.

## Attacker mindset
Use legitimate Nutanix login flow to gain user trust, then redirect to phishing site to harvest credentials or session tokens. The combination of legitimate origin with unexpected redirect creates cognitive dissonance that bypasses user security awareness.

## Defensive takeaways
- Implement whitelist of allowed redirect destinations (e.g., only Nutanix domains)
- Validate and sanitize all redirect URL parameters server-side before performing redirects
- Use relative URLs instead of absolute URLs where possible
- Implement URL parsing validation to detect domain changes
- Add user warnings when redirecting to external domains
- Consider removing unnecessary redirect parameters entirely
- Implement Content Security Policy (CSP) headers to limit redirect targets

## Variant hunting
Check other authentication endpoints (/login, /auth, /signin) for similar redirect parameters
Test alternative parameter names (redirect, return_url, next, continue, target, callback_url)
Examine all URL manipulation parameters on login pages
Check for double-encoding bypasses (%253D, etc.) in validation logic
Test parameter pollution with multiple redirect parameters
Verify if other Nutanix subdomains or applications have similar issues
Check for open redirects in logout/post-logout redirect functionality

## MITRE ATT&CK
- T1598.003 - Phishing: Spearphishing Link
- T1598.002 - Phishing: Spearphishing Link via Credential Harvesting
- T1566.002 - Phishing: Phishing - Spearphishing Link

## Notes
The report shows minimal detail but demonstrates a clear open redirect vulnerability. The use of URL encoding (%3D for =, %3A for :, %2F for /, %2E for .) suggests the researcher may have been testing encoding bypasses. The 'icid' parameter (likely internal campaign ID) and 'isSigningAction' parameters appear to be legitimate tracking parameters, while 'redirectUrl' is the vulnerable parameter. This is a common pattern in marketing/campaign tracking systems where URLs are constructed dynamically.

## Full report
<details><summary>Expand</summary>

hi ,  i find open redirct  in  https://www.nutanix.com

visit this url https://www.nutanix.com/tw/login?icid%3D24N58XTYY6AA=&isSigningAction=Yes&redirectUrl=https%3A%2F%2Fwww.baidu.com%23%40www.nutanix.com

## Impact

open redirct

</details>

---
*Analysed by Claude on 2026-05-24*
