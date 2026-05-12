# Stored XSS in Create Groups

## Metadata
- **Source:** HackerOne
- **Report:** 647130 | https://hackerone.com/reports/647130
- **Submitted:** 2019-07-17
- **Reporter:** rioncool22
- **Program:** GitLab
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Cross-Site Scripting (XSS), Stored XSS, Persistent XSS
- **CVEs:** None
- **Category:** web-api

## Summary
A stored XSS vulnerability exists in the GitLab group creation functionality where unsanitized user input is permanently stored and executed in the browser. An attacker can inject malicious JavaScript through the group name field that executes when the group is viewed or when certain group actions are triggered.

## Attack scenario
1. Attacker logs into GitLab and navigates to create a new group
2. Attacker enters XSS payload in the group name field (e.g., '"><img src=x onerror=prompt(123)>')
3. Group is created with the malicious payload stored in the database
4. When the attacker or any user opens the created group, the payload is rendered in HTML
5. Clicking 'NEW PROJECT' or viewing group details triggers the onerror event
6. JavaScript code executes in the victim's browser context with access to session cookies and sensitive data

## Root cause
Insufficient input validation and output encoding when storing and rendering group names. The application fails to sanitize HTML special characters in the group name field before storage and does not properly encode the output when displaying the group name to users.

## Attacker mindset
An attacker would exploit this to perform session hijacking via cookie theft, perform actions on behalf of users, redirect users to malicious sites, deface group pages, or distribute malware. The stored nature makes this particularly dangerous as it affects all users viewing the group.

## Defensive takeaways
- Implement strict input validation and sanitization for all user-supplied data, especially in group/project creation forms
- Apply context-appropriate output encoding (HTML entity encoding) when rendering user-controlled data in HTML contexts
- Use security libraries like DOMPurify or HTML sanitizers to remove potentially dangerous HTML/JavaScript before storage
- Implement Content Security Policy (CSP) headers to restrict inline script execution
- Perform security code review specifically for user input handling in creation/edit endpoints
- Apply principle of least privilege - validate against a whitelist of allowed characters for group names
- Regular security testing including automated XSS scanning in CI/CD pipeline

## Variant hunting
Search for similar XSS vulnerabilities in other user-creation features (teams, projects, issues, comments, profile fields). Check for XSS in API responses where group data is returned as JSON without proper encoding. Test other special characters and HTML entities in group names, descriptions, and other metadata fields.

## MITRE ATT&CK
- T1190
- T1566
- T1203

## Notes
The report is minimal and appears to be a template submission rather than a detailed writeup. The payload demonstrates basic XSS testing. This vulnerability could be chained with CSRF to create groups on behalf of users. The 'NEW PROJECT' action trigger suggests the payload may not execute on group creation but rather on specific user interactions, indicating potential context-dependent rendering issues.

## Full report
<details><summary>Expand</summary>

> NOTE! Thanks for submitting a report! Please replace *all* the (parenthesized) sections below with the pertinent details. Remember, the more detail you provide, the easier it is for us to triage and respond quickly, so be sure to take your time filling out the report!

### Summary

Stored attacks are those where the injected script is permanently stored on the target servers, such as in a database, in a message forum, visitor log, comment field, etc. The victim then retrieves the malicious script from the server when it requests the stored information. Stored XSS is also sometimes referred to as Persistent or Type-I XSS. 

### Steps to reproduce

1. Login to [Gitlab](https://gitlab.com)
2. Create a new group with xss payload
payload i use = "><img src=x onerror=prompt(123)>
3. Open Group
4. To trigger XSS you can click "NEW PROJECT"
5. XSS Trigger

## Impact

Can steal Cookie, Can run javascript code, etc

</details>

---
*Analysed by Claude on 2026-05-12*
