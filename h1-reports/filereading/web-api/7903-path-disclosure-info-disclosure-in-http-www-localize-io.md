# Path Disclosure via PHP Error Messages in Login Form

## Metadata
- **Source:** HackerOne
- **Report:** 7903 | https://hackerone.com/reports/7903
- **Submitted:** 2014-04-17
- **Reporter:** quistertow
- **Program:** localize.io
- **Bounty:** Not specified
- **Severity:** Low
- **Vuln:** Information Disclosure, Path Traversal Information Leak, Improper Error Handling
- **CVEs:** None
- **Category:** web-api

## Summary
The application discloses the full server file path through unhandled PHP warnings when malformed input is submitted to the login form. An attacker submitting array parameters instead of strings triggers a PHP type error that exposes the absolute file path (/var/www/vhosts/lvps178-77-99-228.dedicated.hosteurope.de/httpdocs_localize/index.php) in the error message.

## Attack scenario
1. Attacker identifies the login endpoint at http://www.localize.io/
2. Attacker crafts a POST request with array-type parameters (sign_in[username][] and sign_in[password][]) instead of expected string values
3. The application passes these arrays to the trim() function which expects a string parameter
4. PHP generates a warning that is displayed to the user without suppression or filtering
5. The error message reveals the full server path including hostname and directory structure
6. Attacker uses this information for further reconnaissance (identifying hosting provider, server structure, potential other services)

## Root cause
The application lacks proper input validation and type checking before passing user input to string manipulation functions. Additionally, PHP error reporting is configured to display warnings directly to users rather than logging them server-side, violating the principle of secure error handling.

## Attacker mindset
Reconnaissance-focused; leveraging type confusion to trigger verbose error messages. The attacker seeks to map the server infrastructure and file structure to identify potential attack vectors or vulnerable components.

## Defensive takeaways
- Disable display_errors in production and log errors to server-side files only
- Implement input validation and type casting before using user input in functions
- Use try-catch blocks or isset/is_array checks to validate parameter types before processing
- Set error_reporting to E_ALL in development but ensure errors don't reach clients
- Implement a generic error page for production environments
- Use Web Application Firewalls (WAF) to sanitize error responses

## Variant hunting
Test other form endpoints with array injection (register, password reset, search forms)
Attempt to trigger other PHP warnings through type mismatches (strpos, explode, json_decode)
Check if other built-in functions reveal path information under similar conditions
Test with NULL values, objects, and resource types to trigger different warnings
Search for other pages that may display debug information in error messages

## MITRE ATT&CK
- T1590.002 - Gather Victim Org Information: Identify Cloud Providers
- T1592 - Gather Victim Host Information
- T1190 - Exploit Public-Facing Application
- T1040 - Network Sniffing

## Notes
This is a classic information disclosure vulnerability with low immediate impact but moderate reconnaissance value. The hosting provider (HostEurope) and server structure are now known to attackers. While path disclosure alone cannot be exploited for code execution, it aids in social engineering and identifying other services running on the same infrastructure. The vulnerability demonstrates poor secure coding practices and misconfigured PHP settings.

## Full report
<details><summary>Expand</summary>

Hello,
I found a information disclosure vulnerability.
How to reproduce:
GET : http://www.localize.io/
POST : sign_in[username][]=test&sign_in[password][]=test

The info from page is
Warning: trim() expects parameter 1 to be string, array given in /var/www/vhosts/lvps178-77-99-228.dedicated.hosteurope.de/httpdocs_localize/index.php on line 732
Is disclosed the path of the site.
Regards,
    Florin

</details>

---
*Analysed by Claude on 2026-05-24*
