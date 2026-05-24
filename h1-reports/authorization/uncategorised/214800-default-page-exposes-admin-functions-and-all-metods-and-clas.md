# DWR Default Index Page Exposes All Available Methods and Admin Functions

## Metadata
- **Source:** HackerOne
- **Report:** 214800 | https://hackerone.com/reports/214800
- **Submitted:** 2017-03-20
- **Reporter:** daveysec
- **Program:** HackerOne
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Information Disclosure, Improper Access Control, Exposure of Sensitive Functionality, Debug Information Exposure
- **CVEs:** None
- **Category:** uncategorised

## Summary
The DWR (Direct Web Remoting) engine's default index page at /dwr/index.html remains publicly accessible, exposing a complete catalog of all available classes, methods, and functionality including test and admin operations. This information disclosure allows attackers to discover and potentially exploit poorly-secured functions that were never intended for public access, such as admin utilities vulnerable to SQL injection or XSS.

## Attack scenario
1. Attacker discovers the application uses DWR framework through reconnaissance or error messages
2. Attacker navigates to the standard DWR path /dwr/index.html and gains access to the default test/documentation page
3. Attacker reviews the complete enumeration of available classes, methods, and their signatures
4. Attacker identifies admin functions or test utilities that lack proper security controls
5. Attacker tests exposed functions for injection vulnerabilities or unauthorized operations
6. Attacker exploits identified vulnerabilities in inadequately-secured functions to compromise the application

## Root cause
Failure to remove or restrict access to the default DWR installation page in production environments. The framework's default configuration includes a convenient index page for development/testing that was not disabled or protected with authentication in the deployed application.

## Attacker mindset
An attacker leverages the principle of least surprise by checking for default framework pages and paths. The discovery of the DWR index provides a complete function inventory, eliminating guesswork in API reconnaissance. The attacker assumes that functions exposed for testing are likely to have weaker security controls than primary production functions, making them attractive targets for exploitation.

## Defensive takeaways
- Disable or completely remove default framework pages and debug interfaces before deploying to production
- Implement authentication and authorization checks on any remaining framework diagnostic or test pages
- Apply the same security rigor to test/admin functions as production functions, or remove them entirely from production builds
- Use allowlisting to explicitly enable only required DWR functions and disable the index/discovery pages
- Regularly audit deployed applications for common default pages and paths (e.g., /admin, /test, /dwr/index.html, /swagger-ui.html)
- Implement network-level access controls to restrict framework diagnostic pages to trusted networks only
- Remove test and debug code paths from production deployments

## Variant hunting
Other framework default pages: /swagger-ui.html, /api-docs, /graphql, /actuator, /debug, /admin.php
Alternative DWR paths: /dwr/engine.js, /dwr/interface/, /dwr/test/
Other web service frameworks with similar exposition: Struts, Spring, ColdFusion, ASP.NET debug pages
Look for other default framework diagnostic pages left accessible in production
Test for similar information disclosure in WSDL files, WADL files, or OpenAPI/Swagger specs
Check for exposed test fixtures, mock data, or sandbox endpoints

## MITRE ATT&CK
- T1592 - Gather Victim Information
- T1580 - Gather Cloud Infrastructure Information
- T1538 - Cloud Service Discovery
- T1526 - Cloud Service Enumeration
- T1589 - Gather Victim Identity Information
- T1046 - Network Service Discovery

## Notes
This vulnerability is a classic case of insecure defaults. DWR's index.html is intentionally provided for development convenience but must be explicitly disabled in production. The severity is elevated by the fact that the exposed functions may not have undergone the same security review as primary functionality, creating a pathway to secondary vulnerabilities like SQL injection. This report references external research from gerionsecurity.com confirming this is a known DWR security issue.

## Full report
<details><summary>Expand</summary>

**Summary:**
https://████/██████/dwr/index.html is a default installation page of DWR engine that exposes all classes and methods available to the user.

**Description:**
https://█████████/██████████/dwr/index.html is a default installation page of DWR engine that exposes all classes and methods available to the user. This include test methods and classes as well as admin functions. Some of these I have found to be vulnerable to issues like SQL injection and XSS since they may not have had the same attention as other functions that were expected to be in production.

**Source**
http://gerionsecurity.com/2012/09/experiences-in-pentesting-dwr/

## Impact
Attacker easily discovering and abusing actions they should not be able to use or know about. Abusing information to find issues like SQL injection on poorly implemented functions that are not expected to be publicly available.

## Step-by-step Reproduction Instructions

1.visit https://██████/████/dwr/index.html
2.You can now view and execute all the methods and classes available to this application included test and admin functionality.

## Product, Version, and Configuration (If applicable)
Current version of Firefox.

## Suggested Mitigation/Remediation Actions
delete or restrict access to this default page. Remove or restrict access to test and admin functionality that are unneeded.

</details>

---
*Analysed by Claude on 2026-05-24*
