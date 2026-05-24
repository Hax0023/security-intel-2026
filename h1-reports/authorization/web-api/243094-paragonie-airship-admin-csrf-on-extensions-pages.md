# Paragonie Airship Admin CSRF on Extensions Installation

## Metadata
- **Source:** HackerOne
- **Report:** 243094 | https://hackerone.com/reports/243094
- **Submitted:** 2017-06-25
- **Reporter:** 4cad
- **Program:** Paragonie
- **Bounty:** Unknown
- **Severity:** HIGH
- **Vuln:** Cross-Site Request Forgery (CSRF), Missing CSRF Token Validation, Insecure Direct Object References
- **CVEs:** None
- **Category:** web-api

## Summary
The /bridge/admin/skyport/install endpoint and related extension management endpoints in Airship lack CSRF token validation, allowing attackers to trick authenticated administrators into installing arbitrary packages. This could potentially lead to Remote Code Execution (RCE) if the package installation mechanism executes user-controlled code.

## Attack scenario
1. Attacker identifies that Airship admin endpoints lack CSRF protection
2. Attacker crafts a malicious HTML page with a hidden form that submits to /bridge/admin/skyport/install
3. Attacker tricks an authenticated Airship administrator into visiting the malicious page (via phishing, social engineering, or malicious website)
4. The administrator's browser automatically submits the CSRF request with their valid session cookies
5. Arbitrary package is installed on the Airship instance without administrator awareness
6. Depending on package processing logic, attacker could achieve code execution or system compromise

## Root cause
The Skyport.php controller functions do not validate CSRF tokens (likely missing token generation, validation, and verification steps in the request processing pipeline). The endpoints perform state-changing operations (package installation) via GET/POST requests without proper synchronizer token pattern or SameSite cookie protections.

## Attacker mindset
An attacker would recognize that admin functionality without CSRF protection is a critical vulnerability. They would be specifically interested in package installation endpoints since package managers often execute code, making this a potential RCE vector. The attacker would focus on social engineering to get admins to click malicious links.

## Defensive takeaways
- Implement CSRF token validation on all state-changing endpoints using framework-provided mechanisms
- Generate unique, unpredictable tokens per session/request and validate them before processing
- Use SameSite cookie attribute (Strict or Lax) as defense-in-depth
- Require re-authentication or additional confirmation for sensitive operations like package installation
- Implement rate limiting on admin endpoints to detect automated CSRF attacks
- Add admin alerts/logging for package installation attempts
- Use security headers (CSP, X-Frame-Options) to limit CSRF attack vectors
- Conduct security code review of all admin controllers, not just visible endpoints

## Variant hunting
Check all other admin endpoints in Bridge controller for CSRF vulnerabilities
Audit package management, user management, and configuration modification endpoints
Review if GET requests perform state changes (should be POST/PUT/DELETE)
Test custom middleware or routing that might bypass CSRF checks
Investigate if password-protected extensions add sufficient protection when enabled
Check if API endpoints have similar CSRF issues

## MITRE ATT&CK
- T1190
- T1566
- T1204
- T1021

## Notes
Reporter appropriately noted uncertainty about actual exploitability given potentially non-functional bash-to-php conversion, but severity should be HIGH because: (1) CSRF on admin package installation is inherently dangerous, (2) code may be fixed in future versions, (3) package installation mechanisms commonly execute code. The lack of default password protection on extensions compounds the risk. This is a clear framework-level security issue affecting all extension management functionality.

## Full report
<details><summary>Expand</summary>

Summary
==========

The /bridge/admin/skyport/install endpoint, as well as some of the endpoints around it, are vulnerable to Cross-Site Request Forgery.

Description
=========
The functions in src/Cabin/Bridge/Controller/Skyport.php in the Airship project appear to all be vulnerable to Cross-Site Request Forgery.

I would have put this as a high, but from my code review it appears that not all of these functions actually work - for example, the installPackage function appears to passing a bash script to the "php" command, which just ends up printing the bash script. Code review can be misleading, so I may be wrong about it not working.

I put this as a medium because, if the logic actually does work (or works sometime in the future), then the ability to install packages is the kind of thing that has the potential to be converted into an RCE.

Please revise the severity as you see fit - I don't know your product well enough to do a proper assessment.

Proof of Concept
======
I have attached a simple file which I was able to use to demonstrate the CSRF against airship running in a docker instance. It appears that the extra password-protection of extensions is not enabled by default, although that may be just my developer setup.

See the attached csrf.html. The attached screenshot shows the result that was returned from the server after clicking the submit button in the attached file.

</details>

---
*Analysed by Claude on 2026-05-24*
