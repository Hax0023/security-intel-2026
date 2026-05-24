# Object Level Access Control Bypass on Yelp Internal Admin Tool - Unauthenticated Access to ELMAH Error Logs

## Metadata
- **Source:** HackerOne
- **Report:** 2891449 | https://hackerone.com/reports/2891449
- **Submitted:** 2024-12-10
- **Reporter:** mester_x
- **Program:** Yelp
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Broken Object Level Authorization (BOLA), Missing Authentication, Information Disclosure, Inadequate Access Control
- **CVEs:** None
- **Category:** uncategorised

## Summary
An unauthenticated attacker can access the ELMAH error logging endpoint on the internal Yelp admin tool (proze.yelp.com) without authentication, retrieving detailed API logs containing full HTTP requests, session cookies, and sensitive debugging information. The lack of object-level access control allows reading logs from any date and browsing all error details, enabling account hijacking and full administrative takeover.

## Attack scenario
1. Attacker discovers proze.yelp.com redirects to main domain but app/login exists
2. Attacker directly accesses /tmwebapi/elmah.axd endpoint without authentication
3. Attacker retrieves paginated error logs containing 100+ requests with sensitive data
4. Attacker clicks 'Details' on any log entry to view complete HTTP request including cookies and secrets
5. Attacker accesses specific log entries via direct UUID in detail endpoint (elmah.axd/detail?id=UUID)
6. Attacker extracts session tokens, credentials, and sensitive parameters to hijack admin accounts

## Root cause
The ELMAH (Error Logging, Handling, and Management Library) debugging endpoint was exposed without authentication or authorization checks. The application relied on obscurity (subdomain isolation) rather than implementing proper authentication on the API endpoint and object-level access controls on individual error log records.

## Attacker mindset
An attacker recognizes that internal admin tools often contain valuable debugging information and leverages common patterns (like ELMAH endpoints) to discover unprotected diagnostic interfaces. The attacker understands that error logs frequently contain authentication tokens and sensitive request data, making them high-value reconnaissance targets for account takeover.

## Defensive takeaways
- Never rely solely on subdomain isolation or obscurity for security of sensitive endpoints
- Implement mandatory authentication on ALL internal admin tool endpoints, including error logging and debugging interfaces
- Enforce object-level authorization checks before returning individual error log records
- Disable or properly secure diagnostic/debugging endpoints (ELMAH, stack traces) in production environments
- Implement rate limiting and monitoring on administrative endpoints
- Sanitize error logs to remove sensitive data like session tokens, passwords, and API keys before storage
- Use defense-in-depth: combine authentication, authorization, and data filtering
- Regularly audit and scan for exposed diagnostic endpoints using tools that check for common patterns
- Implement proper RBAC with principle of least privilege for admin tool access
- Log and alert on access to sensitive debugging endpoints

## Variant hunting
Search for other ELMAH endpoints on different Yelp subdomains (e.g., admin.yelp.com, internal.yelp.com)
Check for other diagnostic endpoints: /elmah.axd, /health, /debug, /status, /logs, /trace, /nlog.axd, /log4net.axd
Test for similar broken access control on other internal APIs (/tmwebapi/* paths)
Look for unauthenticated access to admin dashboards, metrics, or monitoring endpoints
Enumerate other error logging frameworks (NLog, Log4Net, Serilog) that may have exposed endpoints
Test if pagination/enumeration is possible on other log endpoints to retrieve historical data
Check for path traversal attempts to access logs outside the current date range
Test if session tokens extracted from logs can be used for account hijacking

## MITRE ATT&CK
- T1190 Exploit Public-Facing Application
- T1526 Passive Scanning
- T1539 Steal Web Session Cookie
- T1087 Account Discovery
- T1078 Valid Accounts
- T1557 Man-in-the-Browser
- T1040 Traffic Capture or Replay
- T1580 Cloud Infrastructure Discovery

## Notes
This is a critical vulnerability combining multiple weaknesses: missing authentication, broken object-level authorization (BOLA/IDOR), and sensitive information disclosure. The ELMAH endpoint is a well-known attack surface that should be immediately disabled or secured in production. The fact that pagination allows accessing historical logs from specific dates increases the window of exposed sensitive data. This represents a complete compromise of the internal admin tool and potential full account takeover (ATO) of administrative accounts.

## Full report
<details><summary>Expand</summary>

# Summary:
When you visit the subdomain https://proze.yelp.com/ it'll redirect you to the main domain https://www.yelp.com/, The tests show that the application hosts an internal administration tool called  **Tailored Mail**, you can verify this by visiting the endpoint https://proze.yelp.com/app/login.
Since the application is for the internal Yelp admins, you can't access the API or hit any internal data (should be).

**The bug found is a lack of Object level on the internal API Error and debugging endpoint allows unauthenticated attackers to read the internal admin's full sessions, HTTP requests data, and other internal information.**

* The endpoint retrieves the API logs and you can visit each log details and you can read the entire user HTT request and internal data.
* **An attacker can use the retrieved HTTP request data to hijack the admin's accounts, which leads to full ATO.**


# Platform(s) Affected:
https://proze.yelp.com/


# POC:
* The video below is proof:
███████

# Steps To Reproduce:

  1. Visit the subdomain https://proze.yelp.com to verify that you have no access and will redirected to the main domain.
  1. Now visit the admin tool application login https://proze.yelp.com/app/login to verify the existence of the administration tool application there
  1. Visit the endpoint [/tmwebapi/elmah.axd](https://proze.yelp.com/tmwebapi/elmah.axd?page=1&size=100) to read the first last 100 requests logs.
  1. Press `Details` to read any log full internal data
  1. Now visit the endpoint [5A4E7ED8-28E8-4E39-9017-F55E2C9F5371](https://proze.yelp.com/tmwebapi/elmah.axd/detail?id=5A4E7ED8-28E8-4E39-9017-F55E2C9F5371) to read on of the logs with the user cookie and secrets 
  1. You can read logs up to older dates, like visit the endpoint [First-Of-Dec](https://proze.yelp.com/tmwebapi/elmah.axd?page=100&size=100) and you'll read logs from the first of Dec.

# Recommendations:
Place an access control over the  Error Log for TMWebAPI on M7WEB-07 `/tmwebapi/elmah.axd`

## Impact

Object-level access control leads to reading the user's full requests, sessions, and error messages

</details>

---
*Analysed by Claude on 2026-05-24*
