# Denial of Service via Array Input in Email Settings

## Metadata
- **Source:** HackerOne
- **Report:** 961997 | https://hackerone.com/reports/961997
- **Submitted:** 2020-08-19
- **Reporter:** stilobit
- **Program:** Nextcloud
- **Bounty:** Not specified in report
- **Severity:** medium
- **Vuln:** Improper Input Validation, Type Confusion, Denial of Service
- **CVEs:** None
- **Category:** uncategorised

## Summary
A Denial of Service vulnerability exists in Nextcloud settings where submitting an array as the email parameter causes a 500 Internal Server Error. The server fails to properly validate and sanitize the email input type, resulting in unhandled exceptions that crash the request handler and potentially impact server availability.

## Attack scenario
1. Attacker navigates to the user settings page at /index.php/settings/users/[userid]/settings
2. Attacker intercepts the email update request using a proxy tool
3. Attacker modifies the email parameter from a string to an array (e.g., email[]=value)
4. Attacker submits the malformed request to the server
5. Server fails to validate the input type and attempts to process array as string
6. Unhandled exception occurs, returning 500 error and potentially exhausting resources if repeated

## Root cause
The email input field in the settings endpoint lacks proper type validation before processing. The application assumes the email parameter will always be a string but does not enforce or validate this assumption, allowing an attacker to submit alternative data types like arrays that trigger unhandled exceptions.

## Attacker mindset
An attacker seeks to disrupt service availability without authentication complexity. By discovering that a simple parameter type change causes server errors, the attacker can weaponize this into a DoS attack that requires minimal sophistication—just modifying a request parameter format rather than finding complex logic flaws.

## Defensive takeaways
- Implement strict input type validation for all user-supplied parameters before processing
- Use schema validation frameworks to enforce expected data types (string, integer, email format)
- Wrap email processing logic in try-catch blocks with appropriate error handling rather than allowing exceptions to propagate
- Add rate limiting on settings modification endpoints to mitigate DoS impact
- Implement automated input fuzzing in security testing pipelines to catch type confusion vulnerabilities
- Log and alert on repeated 500 errors from settings endpoints as potential DoS indicators
- Use static analysis tools to identify unsafe type assumptions throughout the codebase

## Variant hunting
Test other string fields in settings (username, display name, phone) with array inputs
Attempt nested arrays and objects in email parameter to trigger deeper type confusion
Check other Nextcloud endpoints that accept email parameters for similar validation gaps
Test email field with null, undefined, and object inputs
Investigate if other user profile endpoints share similar type validation weaknesses
Probe admin-only settings endpoints for the same vulnerability pattern

## MITRE ATT&CK
- T1499.4
- T1190

## Notes
This is a relatively low-effort vulnerability requiring minimal authentication (user can modify own settings). The impact is availability rather than confidentiality/integrity. The fix is straightforward: add input type validation. The report lacks technical depth (references video evidence not visible) but clearly demonstrates reproducible DoS condition. Likely affects multiple parameter types throughout the application if root cause is endemic type validation weakness.

## Full report
<details><summary>Expand</summary>

in settings `https://demo2.nextcloud.com/index.php/settings/users/TweLbFT93aqRnEfF/settings`
when you submit the request with email value Array the server return `500 Internal Server Error`
Poc video:
F954435

## Impact

denial a service attack on the server. This may lead to the website becoming slow or unresponsive.

</details>

---
*Analysed by Claude on 2026-05-24*
