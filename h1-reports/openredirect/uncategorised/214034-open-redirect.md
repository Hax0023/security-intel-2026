# Open Redirect via Unvalidated URL Parameter in Dashboard Todos Controller

## Metadata
- **Source:** HackerOne
- **Report:** 214034 | https://hackerone.com/reports/214034
- **Submitted:** 2017-03-16
- **Reporter:** eadz
- **Program:** GitLab
- **Bounty:** Not specified in writeup
- **Severity:** medium
- **Vuln:** Open Redirect, URL Redirection to Untrusted Site
- **CVEs:** None
- **Category:** uncategorised

## Summary
GitLab's Dashboard::TodosController and other controllers contain an open redirect vulnerability by directly merging user-supplied parameters into redirect_to calls without validation. An attacker can craft a malicious URL with a `host` parameter to redirect authenticated users to arbitrary external domains.

## Attack scenario
1. Attacker identifies the vulnerability in the todos dashboard redirect logic
2. Attacker crafts a phishing URL: https://gitlab.com/dashboard/todos?page=99999999&host=www.google.com
3. Attacker sends the malicious link to GitLab users via email/social engineering
4. Victim clicks the link while authenticated to GitLab
5. The application redirects victim to attacker-controlled domain (www.google.com or lookalike)
6. Attacker captures credentials or performs further exploitation on the phishing page

## Root cause
The controller uses `redirect_to params.merge(..)` pattern which allows arbitrary parameters to override redirect destinations. The `host` parameter is passed unsanitized into the redirect logic, enabling open redirect attacks. No URL validation or whitelist is applied before performing redirects.

## Attacker mindset
Low effort, high reward attack vector. The vulnerability is widespread across multiple controllers using the same unsafe pattern. Useful for credential harvesting and session hijacking through phishing with legitimate-looking GitLab URLs.

## Defensive takeaways
- Never pass unsanitized user input directly to redirect_to() or similar redirect functions
- Implement URL validation that only allows relative URLs or whitelisted domains
- Use URL.parse and check domain/host against a whitelist before redirecting
- Audit codebase for all instances of redirect_to params.merge(..) pattern
- Sanitize or remove sensitive parameters from URL before using in redirects
- Use Rails helper methods like redirect_back with fallback_location instead of params-based redirects
- Implement Content Security Policy headers to mitigate redirect impact

## Variant hunting
Search codebase for: redirect_to with params.merge, redirect_to with string interpolation of params, any redirect functions accepting user-controlled host/domain parameters. Check all controller actions that perform redirects after processing pagination, filtering, or sorting parameters.

## MITRE ATT&CK
- T1598.003
- T1189

## Notes
This is a classic and widespread vulnerability pattern. The researcher identified not just the initial bug but also noted the same issue likely exists in Projects::IssuesController and throughout the codebase, indicating systemic poor practice rather than isolated issue. Open redirects are often chained with phishing for credential theft.

## Full report
<details><summary>Expand</summary>

POC:

$GITLAB_INSTANCE = gitlab.com

Visit: 

https://$GITLAB_INSTANCE/dashboard/todos?page=99999999&host=www.google.com

Bug is in Dashboard::TodosController line 10

Likey
Same bug in Projects::IssuesController line 32
and other places in the codebase where you `redirect_to params.merge(..)` 


</details>

---
*Analysed by Claude on 2026-05-24*
