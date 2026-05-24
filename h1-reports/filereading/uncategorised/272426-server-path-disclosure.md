# Server Path Disclosure in Flask and Django Documentation Sites

## Metadata
- **Source:** HackerOne
- **Report:** 272426 | https://hackerone.com/reports/272426
- **Submitted:** 2017-09-27
- **Reporter:** f50c1e7y
- **Program:** Aspen (Flask and Django documentation hosting)
- **Bounty:** Not specified
- **Severity:** low
- **Vuln:** Information Disclosure, Path Disclosure, Sensitive Information Exposure
- **CVEs:** None
- **Category:** uncategorised

## Summary
The researcher discovered that Flask and Django documentation sites hosted on aspen.io expose server path information through directory traversal or misconfigured web server responses. This information disclosure could reveal internal server structure and potentially aid further reconnaissance.

## Attack scenario
1. Attacker visits http://flask.aspen.io/en/latest/ and observes server path disclosures in HTTP responses or error messages
2. Attacker notes the internal directory structure and path patterns exposed
3. Attacker performs similar requests on http://django.aspen.io/en/latest/ to identify consistent patterns
4. Attacker maps out the server filesystem structure from disclosed paths
5. Attacker identifies potential sensitive directories or files that may be accessible
6. Attacker uses this information to plan targeted attacks or identify other vulnerabilities

## Root cause
Misconfigured web server (likely Apache or Nginx) returning full file paths in error messages, HTTP headers, or directory listings; insufficient input validation or error handling that exposes internal path information to unauthenticated users

## Attacker mindset
Information gathering phase of attack; reconnaissance to understand server architecture and identify potential weak points for exploitation; path disclosure enables better targeting of subsequent attacks

## Defensive takeaways
- Configure web servers to suppress or sanitize error messages that reveal full file paths
- Implement custom error pages that don't expose server information
- Disable directory listing and ensure proper access controls
- Review HTTP response headers to ensure no sensitive path information is leaked
- Use web application firewalls to filter out path disclosure in responses
- Implement proper logging and monitoring for reconnaissance attempts
- Regularly audit server configuration for information disclosure vulnerabilities

## Variant hunting
Check for path disclosure in error pages (404, 500, etc.)
Examine HTTP headers (Server, X-Powered-By, etc.) for version/path information
Test directory traversal attempts to see if paths are revealed in responses
Review robots.txt and sitemap.xml for unintended path exposure
Check for path disclosure in stack traces returned by the application
Examine source maps or debug endpoints that may reveal server paths
Test for path disclosure in API responses and error messages

## MITRE ATT&CK
- T1592
- T1598
- T1589
- T1590

## Notes
This is a low-severity information disclosure vulnerability. The report lacks technical detail about exactly how paths are being disclosed (error messages, headers, directory listing, etc.). The researcher appears to have provided minimal proof of concept. While path disclosure alone is not critical, it significantly aids attackers in reconnaissance and should be remediated as part of defense-in-depth strategy. No active exploitation or data compromise appears to have occurred.

## Full report
<details><summary>Expand</summary>

Hi Sir,

I m Mahesh, Individual websecurity Researcher.

i found server path disclosure in flask.io
http://flask.aspen.io/en/latest/
http://flask.aspen.io/en/latest/index.html

i found another path disclosure in django.io
http://django.aspen.io/en/latest/
http://django.aspen.io/en/latest/index.html

</details>

---
*Analysed by Claude on 2026-05-24*
