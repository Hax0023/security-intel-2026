# Unauthorized Access to Employee Admin Panel via Client-Side Authentication Bypass

## Metadata
- **Source:** HackerOne
- **Report:** 1063298 | https://hackerone.com/reports/1063298
- **Submitted:** 2020-12-21
- **Reporter:** 7azimo
- **Program:** GSA (General Services Administration) - CARS (Computerized Accident Reporting System)
- **Bounty:** Not specified in report
- **Severity:** critical
- **Vuln:** Insufficient Client-Side Validation, Broken Authentication, Missing Server-Side Authorization, Insecure Direct Object References
- **CVEs:** None
- **Category:** auth-crypto

## Summary
The CARS application relied entirely on client-side JavaScript validation to enforce access control to the admin panel. An attacker could bypass the loginChk() function by directly modifying form values in the browser console, gaining unauthorized access to the employee administration panel without valid credentials. This allowed complete compromise of a critical incident reporting system.

## Attack scenario
1. Attacker navigates to https://cars.fas.gsa.gov/cars/cars and identifies a login form
2. Attacker opens browser developer console (F12) and executes loginChk() function, confirming it returns false
3. Attacker modifies the form's scSelCen field by executing: document.forms[0].scSelCen.value = 'admin'
4. Attacker clicks the CARS login button, bypassing all client-side validation checks
5. Attacker gains access to the admin panel without providing valid credentials
6. Attacker can now view, modify, or delete accident reports and employee data within the system

## Root cause
The application implemented authentication and authorization logic exclusively on the client-side using JavaScript. The loginChk() function validated user input in the browser before submission, but there was no server-side validation. An attacker with access to the browser DOM could modify form values before submission, and the server accepted requests without verifying credentials or authorization tokens.

## Attacker mindset
An opportunistic attacker performing reconnaissance on government web applications. Upon discovering the login form, the attacker took a methodical approach to test the function in the console, realized the weakness, and exploited it with minimal technical effort. The attacker demonstrated restraint by not accessing sensitive data, instead reporting the vulnerability.

## Defensive takeaways
- Never rely on client-side validation for security-critical functions like authentication and authorization
- Implement server-side authentication checks on every request that accesses protected resources
- Validate all form inputs on the server and verify user identity through secure session tokens or JWT tokens
- Use HTTP-only cookies for session management to prevent JavaScript access
- Implement proper role-based access control (RBAC) on the server that cannot be bypassed by DOM manipulation
- Remove or obfuscate sensitive function names from client-side code
- Conduct security code reviews focusing on the server-side logic for all authentication pathways
- Implement Web Application Firewall (WAF) rules to detect suspicious form submissions
- Use Content Security Policy (CSP) to restrict JavaScript execution capabilities

## Variant hunting
Check for other client-side functions that validate access (e.g., roleCheck(), permissionCheck())
Attempt to modify other form fields such as user role, department, or permission levels
Test if direct API calls to backend endpoints bypass the form validation entirely
Examine browser storage (localStorage, sessionStorage) for authentication tokens that can be manipulated
Check if other forms on the application have similar client-side-only validation patterns
Test if credentials can be hardcoded or guessed after bypassing client-side checks
Investigate if the application has other admin panels or sensitive endpoints with similar vulnerabilities

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1199: Trusted Relationship
- T1110: Brute Force
- T1021: Remote Services
- T1589: Gather Victim Identity Information
- T1526: Enumerate External Networks

## Notes
This is a severe vulnerability in a government system responsible for accident reporting. The ease of exploitation (requiring only browser console commands) and the sensitivity of the data involved (accident reports) make this a critical issue. The reporter's responsible disclosure approach and restraint in not accessing data demonstrates good security ethics. The maintenance mention suggests GSA may have taken the system offline for patching after disclosure.

## Full report
<details><summary>Expand</summary>

## Summary:
Hello, 
When hunting for your web application.

I have managed to go https://cars.fas.gsa.gov/cars/cars and get displayed with a form.
I have already tried to login to Cars and without success.
However i've noticed the loginChk() function and change the value of the form hence bypassing it and logging in succesfuly.

## Steps To Reproduce:


  1. go to https://cars.fas.gsa.gov/cars/cars
  2. type loginChk()  function in console. 
  3. It would return false. 
  4. Now  type in console ( can be opened using F12). 
       document.forms[0].scSelCen.value = "admin"
  5. Now try to login by clicking on CARS button.

## Supporting Material/References:
Navigator used : google chrome.

If you need any additional information. feel free to ask me.

PS :  I think the website went for a maintenance right now.
Even though i didn't use anything of that panel.

## Impact

Any attacker would have the access to admin panel and do whatever he wants.
As i can see , it's a platform for reporting accidents.

</details>

---
*Analysed by Claude on 2026-05-24*
