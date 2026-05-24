# Path Disclosure in platform0.twitter.com

## Metadata
- **Source:** HackerOne
- **Report:** 44371 | https://hackerone.com/reports/44371
- **Submitted:** 2015-01-20
- **Reporter:** avicoder_
- **Program:** Twitter
- **Bounty:** Not specified
- **Severity:** low
- **Vuln:** Information Disclosure, Path Disclosure
- **CVEs:** None
- **Category:** web-api

## Summary
A path disclosure vulnerability was identified on platform0.twitter.com that exposes internal file system paths or directory structure information. The vulnerability is reproducible by accessing the domain over HTTPS and observing error messages or responses that reveal sensitive path information.

## Attack scenario
1. Attacker navigates to https://platform0.twitter.com
2. Server responds with an error page or response containing full file system paths
3. Attacker documents the exposed path information from the response body or headers
4. Attacker analyzes disclosed paths to identify directory structure and application architecture
5. Information can be used to identify other potential vulnerabilities or sensitive directories
6. Attacker maps out backend infrastructure for further reconnaissance

## Root cause
Server configuration or error handling mechanism fails to sanitize error messages and responses, revealing absolute file paths or internal directory structures to unauthenticated users

## Attacker mindset
Information gathering and reconnaissance phase of an attack. Attacker seeks to understand application structure and identify promising attack vectors through passive enumeration of disclosed paths.

## Defensive takeaways
- Implement custom error pages that do not disclose file paths or system information
- Configure web server to hide sensitive headers and path information in error responses
- Sanitize all error messages returned to clients to exclude internal paths
- Regularly audit error handling and exception messages in applications
- Use security headers and configurations to prevent information leakage
- Implement centralized error handling with generic user-facing messages

## Variant hunting
Search for path disclosure across other Twitter subdomains (api0.twitter.com, dev.twitter.com, etc.), test various error conditions (404, 500, timeouts), check for path leakage in HTTP headers, stack traces, and default error pages on other platforms

## MITRE ATT&CK
- T1592
- T1590
- T1598

## Notes
This is a minimal bug report with limited technical detail. The report lacks screenshot evidence, specific error messages, or HTTP responses demonstrating the vulnerability. The severity is low as path disclosure alone typically enables reconnaissance rather than direct exploitation. Report quality could be improved by providing detailed reproduction steps, sample error outputs, and impact assessment.

## Full report
<details><summary>Expand</summary>

Hi Twitter,

I am going to disclose a vulnerability which I’ve found in **platform0.twitter.com** , hoping this will make **Twitter** more secure place.

   - **Vulnerability Class:**  Path Disclosure 

   - **Proof of Concept :**
      -  Link : https://platform0.twitter.com
      - you must use https instead of http to reproduce POC
      - Screenshot attached.  

Happy to help.
Regards.


</details>

---
*Analysed by Claude on 2026-05-24*
