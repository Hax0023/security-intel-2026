# Local File Inclusion via Path Traversal in Registration Page

## Metadata
- **Source:** HackerOne
- **Report:** 1007799 | https://hackerone.com/reports/1007799
- **Submitted:** 2020-10-13
- **Reporter:** moloshy
- **Program:** HackerOne (Undisclosed Client)
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Local File Inclusion (LFI), Path Traversal, Arbitrary File Read
- **CVEs:** None
- **Category:** uncategorised

## Summary
The registerUserInfoCommand.nextPageName parameter in the registration form is vulnerable to path traversal attacks, allowing attackers to read arbitrary local files from the web server by injecting traversal sequences like ../../../. This vulnerability enables unauthorized access to sensitive configuration files such as web.xml and spring security configurations containing application secrets and structural information.

## Attack scenario
1. Attacker navigates to the registration page at /RegisterUserInfo.htm
2. Attacker intercepts the form submission request using a proxy tool like Burp Suite
3. Attacker modifies the nextPageName parameter to include path traversal sequences (e.g., ../../WEB-INF/web.xml URL-encoded as ..%2f..%2fWEB-INF%2fweb.xml)
4. Attacker forwards the modified request to the server
5. Server processes the traversal path and returns the contents of the requested local file
6. Attacker reads sensitive configuration files, source code paths, security configurations, and other protected data

## Root cause
The application directly uses user-supplied input from the nextPageName parameter to construct file paths without proper validation or sanitization. No whitelist of allowed pages is enforced, and path traversal characters (../) are not filtered, allowing attackers to escape the intended directory.

## Attacker mindset
An attacker could leverage this vulnerability to map the application architecture, discover configuration details, identify security mechanisms, find hardcoded credentials in config files, and locate sensitive application code. This information could be chained with other vulnerabilities for deeper system compromise.

## Defensive takeaways
- Implement a whitelist of allowed page identifiers rather than accepting raw filenames
- Use indirect references (mapping IDs to actual pages) instead of direct file paths in parameters
- Sanitize and validate all user input, explicitly rejecting path traversal sequences (../, .., %2e%2e, etc.)
- Apply strict input validation rules: only alphanumeric characters and specific allowed symbols
- Implement proper access controls and file permissions at the OS level
- Use a template or view resolver that only allows access to designated directories
- Conduct security code review of all file-handling logic in the application
- Implement Web Application Firewall (WAF) rules to detect and block path traversal attempts

## Variant hunting
Search for other parameters that accept file/page names: prevPageName, currPageName, pageName, template, view, page, file, path, include, require. Check for similar vulnerabilities in other registration steps, account management pages, and any dynamic page routing mechanisms. Test for both LFI and Remote File Inclusion (RFI) variants.

## MITRE ATT&CK
- T1190
- T1083
- T1005
- T1552

## Notes
The vulnerability is in a registration flow, suggesting it may be accessible to unauthenticated users, making it a critical finding. The ability to read WEB-INF files is particularly dangerous as these contain application configuration and potentially hardcoded secrets. The report demonstrates good security research methodology with clear reproduction steps and actionable remediation advice.

## Full report
<details><summary>Expand</summary>

**Summary:**
When registering on https://████████ it is possible to use path traversal characters in a parameter allowing an attacker to read local files.

**Description:**
The registerUserInfoCommand.nextPageName parameter within the registration form is vulnerable to file path manipulation, where it is possible to submit a request containing path traversal characters (e.g. ../../../) followed by a local file, which will return the contents of the file. This can be used to read local files including sensitive configuration files such as /WEB-INF/web.xml, /WEB-INF/app-config.xml and /WEB-INF/spring/explicit-security-config.xml.

## Impact
An attacker could read local files on the web server that they would normally not have access to, such as the application source code or configuration files containing sensitive information on how the website is configured. 

## Step-by-step Reproduction Instructions

1. Browse to https://██████/████████/register/RegisterUserInfo.htm
2. Setup an intercepting proxy (e.g. BurpSuite) and click Next, catching the request in Burp (don't worry about filling out the form fields)
3. For ease here I would recommend copying and pasting the below parameters into the request, replacing the parameters that were there originally.  This request will fetch the /WEB-INF/web.xml configuration file, I have also attached two other requests which grab app-config.xml and explicity-security-config.xml. Once the parameters are there, forward the request to the server and you should see the web.xml file.  

```
registerUserInfoCommand.organization=Chantest+Corporation&registerUserInfoCommand.organizationId=49800&registerUserInfoCommand.currPageName=SearchUserOrgInfo.jsp&registerUserInfoCommand.nextPageName=..%2f..%2f..%2fWEB-INF%2fweb.xml&registerUserInfoCommand.prevPageName=jsp%2FRegistration%2FRegisterAccountInfo.jsp&registerUserInfoCommand.submitButton=Choose+This+Organization+and+Continue+%3E
```

## Product, Version, and Configuration (If applicable)
N/A

## Suggested Mitigation/Remediation Actions
Rather than placing the filename of the next page directly in a parameter, it would be better to maintain a whitelist of acceptable filenames and use a unique corresponding identifier to access the file. Then any request containing an invalid identifier can just be rejected. Additionally, you could also sanitise any path traversal characters that may be present in a request.

## Impact

An attacker could read local files on the web server that they would normally not have access to, such as the application source code or configuration files containing sensitive information on how the website is configured.

</details>

---
*Analysed by Claude on 2026-05-24*
