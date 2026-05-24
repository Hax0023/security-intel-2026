# The application uses basic authentication.

## Metadata
- **Source:** HackerOne
- **Report:** 151847 | https://hackerone.com/reports/151847
- **Submitted:** 2016-07-17
- **Reporter:** roshanpty
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Improper Authentication - Generic
- **CVEs:** None
- **Category:** auth-crypto

## Summary
Basic authentication is enabled on file access requests
====================
Description
---------------------
Basic authentication is enabled on the server if we request for the direct URL of a file.  The issues of using Basic Authentication can be read here -> [OWASP: Basic Authentication](https://www.owasp.org/index.php/Basic_Authentication). Though your threat model considers brute-forcing as 

## Attack scenario
*(see original)*

## Root cause
*(see original)*

## Attacker mindset
*(see original)*

## Defensive takeaways
*(see original)*

## Variant hunting
*(see original)*

## MITRE ATT&CK
*(see original)*

## Notes
*(see original)*

## Full report
<details><summary>Expand</summary>

Basic authentication is enabled on file access requests
====================
Description
---------------------
Basic authentication is enabled on the server if we request for the direct URL of a file.  The issues of using Basic Authentication can be read here -> [OWASP: Basic Authentication](https://www.owasp.org/index.php/Basic_Authentication). Though your threat model considers brute-forcing as an acceptable risk, it is also worth noting that use of basic authentication makes the brute-force attacks much easier and faster. 

Detailed Steps
---------------------
**Step 1:** Open the browser and request for the direct URL of a file. Eg: (http://nc.hostiso.cloud/remote.php/webdav/Photos/Squirrel.jpg)
{F105383}
**Step 2:** Enter the username and password and capture the request in a proxy tool.
**Step 3:** It can be observed that the header with Base64 encoded username password is being sent in the request to server. 
{F105384}

</details>

---
*Analysed by Claude on 2026-05-24*
