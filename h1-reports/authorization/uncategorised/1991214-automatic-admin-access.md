# Automatic Admin Access via Direct URL

## Metadata
- **Source:** HackerOne
- **Report:** 1991214 | https://hackerone.com/reports/1991214
- **Submitted:** 2023-05-17
- **Reporter:** bulldawg
- **Program:** U.S. Department of Defense (HackerOne)
- **Bounty:** Not specified
- **Severity:** critical
- **Vuln:** Broken Authentication, Broken Access Control, Hardcoded Credentials, Session Fixation, Insecure Direct Object Reference
- **CVEs:** None
- **Category:** uncategorised

## Summary
A specific URL automatically authenticates visitors as an administrative user named 'ben auto log user' without requiring credentials. This grants unauthorized access to critical functions including user management, file uploads, data publication, and email functionality. The vulnerability allows complete compromise of application integrity, confidentiality, and availability.

## Attack scenario
1. Attacker obtains or discovers the vulnerable URL pattern
2. Attacker visits the URL and is automatically authenticated as administrative user
3. Attacker gains access to user management panel and retrieves sensitive user data (names, emails)
4. Attacker uploads malicious files through the submission system or modifies existing submissions dating back to 2012
5. Attacker sends spam emails to all application users or escalates privileges by adding administrator role to their own account
6. Attacker deletes user accounts or publications to cause service disruption

## Root cause
The application implements automatic authentication logic triggered by specific URL parameters, likely relying on predictable session identifiers or hardcoded test credentials that were not removed from production. The session management appears to use sequential or predictable tokens (23467499301323) embedded in URLs without proper validation.

## Attacker mindset
An attacker would recognize this as a critical authentication bypass enabling complete account takeover of the most privileged role. They would immediately leverage admin access to exfiltrate sensitive data, create persistence mechanisms, and cause maximum damage while remaining undetected.

## Defensive takeaways
- Implement proper session management using cryptographically random, non-predictable session tokens
- Remove all test, debug, and default credentials from production environments
- Enforce authentication checks on every sensitive endpoint regardless of URL parameters
- Use POST requests with CSRF tokens for state-changing operations instead of GET URLs
- Implement role-based access control (RBAC) with explicit permission verification
- Log all authentication attempts and administrative actions for audit trails
- Use secure session storage without embedding sensitive identifiers in URLs
- Conduct code reviews to identify and remove backdoors or auto-login mechanisms
- Implement conditional access restrictions based on IP, geolocation, or time-based policies
- Use security headers to prevent clickjacking and URL manipulation attacks

## Variant hunting
Search for similar patterns in other endpoints; look for: hardcoded user IDs in parameters, sequential or guessable session tokens, GET requests performing sensitive operations, test users in production, auto-login functionality in codebase, URL patterns with embedded credentials, predictable parameter values across application endpoints

## MITRE ATT&CK
- T1190
- T1078
- T1133
- T1087
- T1485
- T1531
- T1123
- T1005

## Notes
The researcher responsibly refrained from testing destructive functionality, demonstrating good faith. The military domain (.mil) and data spanning 2012 suggest critical infrastructure/data. The specific URL parameter structure (f?p=150:1:SESSION::NO:::) indicates likely Oracle APEX or similar framework. The 'ben auto log user' identifier suggests developer testing credentials left in production.

## Full report
<details><summary>Expand</summary>

URL: https://█████████.mil/apexcrrel/f?p=150:1:23467499301323::NO:::

When visiting the following URL, the user is automatically signed into a user with administrative access. 

███

This user is allowed to:
1. Create new submissions, allowing file uploads

████████

2. See all submissions going back to 2012

██████████

3. Manage users - add, delete, and link users. This user could also add the Administrator role to a user. 

███

████

4. Send spam emails to all users

█████████

5. Access admin tools like publishing data and removing publications

██████████

I did not test all functionality provided by this access as I did not want to damage the integrity of the data on the web application.

Please let me know if you would like me to test adding/deleting users, creating submissions and testing file upload vulnerabilities, etc. This would also allow me to demonstrate the severity of this vulnerability as well as find new vulnerabilities in the application. For example, with permission I would like to test the file upload functionality for vulnerabilities.

## Impact

This is a critical vulnerability. This impacts the integrity, confidentiality, and availability of the application. 

Integrity: Unauthorized users can upload arbitrary data, publish data, and delete publications.
Confidentiality: This exposes names, emails, and submissions.
Availability: This administrative user can delete other user accounts, denying them access.

## System Host(s)
███████.mil

## Affected Product(s) and Version(s)


## CVE Numbers


## Steps to Reproduce
1. Visiting URL: https://███.mil/apexcrrel/f?p=150:24:23467499301323::NO:::
2. View active user in top right corner: "ben auto log user". This user is an administrator.

## Suggested Mitigation/Remediation Actions




</details>

---
*Analysed by Claude on 2026-05-24*
