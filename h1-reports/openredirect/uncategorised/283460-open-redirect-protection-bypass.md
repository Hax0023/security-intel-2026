# Open Redirect Protection Bypass via Protocol-Relative URL

## Metadata
- **Source:** HackerOne
- **Report:** 283460 | https://hackerone.com/reports/283460
- **Submitted:** 2017-10-27
- **Reporter:** avinash_
- **Program:** Twitter
- **Bounty:** Not specified in report
- **Severity:** medium
- **Vuln:** Open Redirect, URL Validation Bypass, Authentication Bypass
- **CVEs:** None
- **Category:** uncategorised

## Summary
Twitter's open redirect protection could be bypassed using protocol-relative URLs (starting with //) in the authorize_callback parameter. An attacker could craft a malicious authorization link that bypasses the redirect validation, causing authenticated users to be redirected to attacker-controlled domains after authorization.

## Attack scenario
1. Attacker identifies Twitter's /teams/authorize endpoint with authorize_callback parameter containing open redirect protection
2. Attacker discovers the protection only validates absolute URLs and fails to properly handle protocol-relative URLs (//domain.com syntax)
3. Attacker crafts malicious link: https://twitter.com/teams/authorize?target_screen_name=&authorize_callback=//www.attacker.com
4. Attacker distributes link to victim via social engineering or phishing
5. Victim clicks link while authenticated to Twitter and authorizes team creation
6. Victim is redirected to attacker's domain, enabling phishing, session hijacking, or credential theft

## Root cause
The authorization redirect protection regex or validation logic did not properly account for protocol-relative URLs (//). The validation likely checked for http:// and https:// schemes but failed to recognize that // inherits the current protocol and can redirect to arbitrary domains.

## Attacker mindset
An attacker would recognize this as a common bypass technique - security teams often overlook protocol-relative URLs when implementing redirect protection. The use of legitimate OAuth flow increases user trust and reduces suspicion compared to direct phishing links.

## Defensive takeaways
- Implement strict whitelist-based redirect validation instead of blacklist approaches
- Validate redirect URLs using URL parsing libraries that normalize protocol-relative URLs before checking
- Reject any redirect that doesn't explicitly start with http:// or https:// (disallow //, /, or relative paths unless in whitelist)
- Test open redirect protections against protocol-relative URLs, data URIs, and javascript: schemes
- Use Origin validation and CORS headers to prevent cross-origin redirects
- Implement Content-Security-Policy headers to further restrict redirect destinations

## Variant hunting
Test data: URIs and javascript: schemes in callback parameters
Try mixed case variations: //WWW.EXAMPLE.COM, ///example.com
Test unicode/percent-encoding bypasses: %2F%2Fexample.com
Check if backslash works instead of forward slash (\\example.com on Windows systems)
Test null byte injection: //example.com%00.twitter.com
Attempt using IPv6 notation or IP addresses: //192.168.1.1
Test redirect chains and multiple redirect parameters

## MITRE ATT&CK
- T1598.003 - Phishing: Spearphishing Link
- T1539 - Steal Web Session Cookie
- T1187 - Forced Authentication
- T1566.002 - Phishing: Spearphishing Link

## Notes
This report references a previously fixed issue (Report #281538), indicating that the initial patch was incomplete. The protocol-relative URL bypass is a well-known technique in web security and demonstrates the importance of comprehensive validation. Twitter's OAuth flow adds credibility to the attack, making social engineering more effective. The /teams/authorize endpoint suggests this vulnerability exists in business/team creation workflows.

## Full report
<details><summary>Expand</summary>

Hi

Report #281538 is fixed but Attacker can Bypass this Open Redirect Protection.

Give this link ``` https://twitter.com/teams/authorize?target_screen_name=&authorize_callback=//www.facebook.com``` to authorized victim.Twitter will say him to authorize a different account for create team.After authorization victim will be redirected to ```www.facebook.com```

Vulnerable point ```//www.facebook.com``` (You can use //www.example.com )

Open Redirection Protection Bypassed.

PoC video attached

With Best Regards

</details>

---
*Analysed by Claude on 2026-05-24*
