# Full Path Disclosure in airship.paragonie.com '/cabins/' Endpoint

## Metadata
- **Source:** HackerOne
- **Report:** 226343 | https://hackerone.com/reports/226343
- **Submitted:** 2017-05-05
- **Reporter:** eidelweiss
- **Program:** Paragon Initiative Enterprises (Airship CMS)
- **Bounty:** Not specified
- **Severity:** low
- **Vuln:** Information Disclosure, Full Path Disclosure (FPD), Error-based Information Leakage
- **CVEs:** None
- **Category:** uncategorised

## Summary
An authenticated user accessing the '/my/cabins' endpoint triggers an unhandled error that discloses the full filesystem path of the application installation. This information disclosure vulnerability exposes the internal directory structure of the server, which can aid attackers in reconnaissance and exploitation planning.

## Attack scenario
1. Attacker creates a user account on airship.paragonie.com to gain authenticated access
2. Attacker navigates to https://airship.paragonie.com/my/cabins endpoint
3. The endpoint triggers an error condition (possibly missing data, permission issue, or database error)
4. Application fails to handle the error gracefully and returns raw error message with full filesystem path
5. Attacker captures the disclosed path information revealing server directory structure and application location
6. Attacker uses path disclosure to refine further exploitation attempts or identify other vulnerable endpoints

## Root cause
Inadequate error handling in the '/my/cabins' endpoint that returns raw exception/error messages to authenticated users instead of sanitizing output or displaying generic error pages. The application likely exposes stack traces or error logs containing absolute file paths.

## Attacker mindset
Low-effort reconnaissance gathering. Attacker tests endpoints after authentication to discover information leakage. Information disclosure is collected as part of broader reconnaissance to understand application architecture and identify attack surface.

## Defensive takeaways
- Implement centralized error handling that returns generic user-friendly messages while logging detailed errors server-side only
- Disable verbose error messages in production environments
- Configure error logging to exclude or mask absolute filesystem paths
- Implement output encoding/sanitization for all error responses
- Use custom error pages that don't expose technical details
- Regularly audit error handling across all endpoints, especially authenticated ones
- Consider implementing Web Application Firewall (WAF) rules to filter path disclosure patterns

## Variant hunting
Test other '/my/*' endpoints for similar error handling issues
Check all administrative/user-specific endpoints for FPD vulnerabilities
Test error conditions in forms (validation errors, missing fields) on authenticated pages
Attempt to trigger database errors through malformed requests on authenticated endpoints
Review other Airship CMS installations for similar patterns in error responses

## MITRE ATT&CK
- T1592
- T1592.004
- T1526

## Notes
This is a relatively low-severity issue as it requires authentication and only leaks path information. However, in combination with other vulnerabilities, path disclosure can significantly aid attackers. The researcher responsibly tested on the live site due to installation difficulties, showing good faith disclosure. The vulnerability appears to be a missing null check or error handler in the cabin retrieval logic.

## Full report
<details><summary>Expand</summary>

Hello Team,

first am so sorry if i test this in your site, since i got problem to install in my own. So when i see your blog i got end point to https://airship.paragonie.com which is "Powered By Airship" or made using Airship CMS.

**step To Reproduce**

1. register an account
2. navigate to `https://airship.paragonie.com/my/cabins`
3. and you will get an error contains with full path of installations get disclosure like shown in images bellow

{F182099}   

i am not sure this is your security concern but i need to report this and let you know.

Regards,

</details>

---
*Analysed by Claude on 2026-05-24*
