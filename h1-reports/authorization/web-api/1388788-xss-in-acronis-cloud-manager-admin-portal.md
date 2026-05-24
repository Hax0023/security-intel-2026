# XSS in Acronis Cloud Manager Admin Portal Swagger UI

## Metadata
- **Source:** HackerOne
- **Report:** 1388788 | https://hackerone.com/reports/1388788
- **Submitted:** 2021-11-02
- **Reporter:** mooimacow
- **Program:** Acronis
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Cross-Site Scripting (XSS), Reflected XSS, Insecure Deserialization of User Input
- **CVEs:** None
- **Category:** web-api

## Summary
The Acronis Cloud Manager Admin Portal exposes a default Swagger UI endpoint vulnerable to reflected XSS via the 'url' parameter. An attacker can craft a malicious URL to inject arbitrary JavaScript that executes in the context of admin users who access the Swagger interface. This allows theft of sensitive API credentials and data accessible only to administrators.

## Attack scenario
1. Attacker identifies the vulnerable Swagger UI endpoint at /swagger/index.html with the 'url' query parameter
2. Attacker crafts a malicious URL containing JavaScript payload in the url parameter (e.g., ?url=javascript:alert(1) or external HTML file with XSS)
3. Attacker sends phishing email or social engineering message to Acronis admin users with the malicious link
4. Admin user clicks the link and the Swagger UI renders the attacker-controlled content, executing JavaScript
5. Malicious script captures admin credentials entered in the Authorize button or exfiltrates sensitive API data
6. Attacker gains unauthorized access to cloud infrastructure and customer data via compromised admin credentials

## Root cause
The Swagger UI implementation uses an outdated version of DOMPurify that fails to properly sanitize user-supplied input in the 'url' parameter before rendering it in the DOM. The application does not validate or restrict the URL parameter to legitimate Swagger specification sources, allowing arbitrary external URLs or JavaScript payloads to be processed.

## Attacker mindset
An external attacker with knowledge of Acronis deployments would recognize that admin portals are high-value targets. By exploiting this XSS in the Swagger interface, the attacker can harvest admin credentials with minimal effort since admins naturally visit this page to test APIs. The vulnerability is trivial to exploit and affects all default installations, making it an attractive reconnaissance and lateral movement vector.

## Defensive takeaways
- Immediately upgrade DOMPurify and all DOM sanitization libraries to latest versions with active security patching
- Implement strict input validation on the 'url' parameter to only accept URLs matching expected Swagger specification patterns (whitelist approach)
- Apply Content Security Policy (CSP) headers to restrict script execution and external resource loading
- Remove or restrict access to default Swagger UI endpoints in production environments, or require authentication before exposure
- Implement output encoding for all user-controlled data rendered in HTML context
- Conduct security testing of all admin-facing interfaces and API documentation portals
- Establish dependency vulnerability scanning in CI/CD pipeline to detect outdated libraries before deployment

## Variant hunting
Look for similar XSS vulnerabilities in other Acronis products that expose Swagger UI or other API documentation frameworks. Check for the same pattern in other query parameters that control resource loading (url, config, spec, definition, etc.). Audit other developer-facing interfaces that may accept external URL inputs without proper validation. Test for CSRF protections on sensitive admin API endpoints that could be combined with this XSS.

## MITRE ATT&CK
- T1190
- T1566.002
- T1598.003
- T1539
- T1555.003

## Notes
The researcher provided excellent reproduction steps and identified the root cause (outdated DOMPurify). This is a reflected XSS requiring social engineering but with high impact due to targeting of privileged users and access to sensitive admin APIs. The vulnerability affects all default installations, making it a widespread exposure. No evidence of a fix or bounty amount in the public report.

## Full report
<details><summary>Expand</summary>

Hello,

Hope you are doing well. I wanted to report the following security vulnerability:

The Acronis Cloud Manager Admin Portal default swagger UI is vulnerable to cross site scripting. I have the API running locally on my machine. I have attached screenshots of the XSS

The URL is:
https://localhost:16080/swagger/index.html?url=███/xss/index.html

Documentation on how to access the API is available here:
https://kb.acronis.com/content/64702

If you would like to reproduce this, you need to setup the Cloud Manager admin portal. To do so, you can take the following steps:
1) Download the cloud manager here (free trial): https://www.acronis.com/en-us/products/cloud-manager/
Once you do that, you will need to install the Acronis Cloud Manager console and the Acronis Cloud Manager web portal. The guide is available here:

https://dl.acronis.com/u/rc/GSG_AcronisCloudManager_5.0_EN-US.pdf?fbclid=IwAR0yOcDjRDPgkXlwNX5Qj0-B4wjOK2d9s76IipnmE_jZiRY_2CSZy3AuJMk

I recommend unzipping the download file in the email and installing this directly on a Windows system rather than using the ISO. I think that will be easier.

In order to get those setup, you need a valid database to connect to. You can use the following links to get one setup.
2) Download sql server express  (https://go.microsoft.com/fwlink/?linkid=866658)
3) Download sql server management studio (https://docs.microsoft.com/en-us/sql/ssms/download-sql-server-management-studio-ssms?view=sql-server-ver15)

Once you have it sql server setup, you need to create a user that you can use to connect to the database from the Acronis setup guide, to get everything working. Once it is setup, the default swagger url available to all installations, is vulnerable to XSS.

## Impact

The swagger site allows you to enter in different credentials to test API methods via the Authorize Button on the right side. The methods in scope are very sensitive based on the nature of this application and generally only admins would be testing the API methods with their credentials.

With XSS here we would have the opportunity to target admin users and access very sensitive data. More information on XSS is available here: https://www.packetlabs.net/cross-site-scripting-xss/

If someone were to deploy this API to the cloud or another location, it would be an easy target. Right now I just have it running locally.

The swagger instance running is using an older version of dom-purfiy. If you upgrade the instance, that should fix this issue.

Let me know if you have questions. Thanks!
Ben

</details>

---
*Analysed by Claude on 2026-05-24*
