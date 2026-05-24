# Unauthorized Access to Private Project Information via Browser Cache

## Metadata
- **Source:** HackerOne
- **Report:** 407763 | https://hackerone.com/reports/407763
- **Submitted:** 2018-09-09
- **Reporter:** 8ayac
- **Program:** GitLab
- **Bounty:** Not specified in report
- **Severity:** Medium
- **Vuln:** Improper Cache Control, Information Disclosure, Insufficient Access Control
- **CVEs:** None
- **Category:** web-api

## Summary
GitLab's private project pages lack adequate cache control headers, allowing unauthorized users to view sensitive project information using browser back button functionality. An attacker with physical access to a victim's computer or shared device can retrieve cached private project contents including source code, commit logs, and issues without authentication.

## Attack scenario
1. Victim user logs into GitLab and creates or views a private project
2. Victim navigates to various private project pages (files, issues, wiki, commits)
3. Attacker gains physical access to victim's computer while logged out or in a different session
4. Attacker clicks the browser's back button to navigate to previously visited private project pages
5. Browser serves cached responses without authentication validation due to missing/inadequate Cache-Control headers
6. Attacker successfully views sensitive project information (source code, commit history, issues, wiki content)

## Root cause
GitLab fails to set proper Cache-Control headers (e.g., 'no-cache', 'no-store', 'private', 'max-age=0') on HTTP responses for private project pages. This allows browsers to serve cached content from browsing history without re-validating access permissions with the server.

## Attacker mindset
Opportunistic physical access exploit targeting shared/office environments. Attacker seeks to extract intellectual property, source code, project roadmaps, and sensitive issue tracking information from cached private projects without requiring authentication credentials.

## Defensive takeaways
- Implement strict Cache-Control headers on all sensitive/authenticated pages: 'Cache-Control: no-store, no-cache, must-revalidate, private'
- Set Pragma: no-cache and Expires headers for legacy browser compatibility
- Use Set-Cookie with Secure, HttpOnly, and SameSite attributes to prevent session exploitation
- Implement CSP headers to prevent cached content manipulation
- Consider edge-side includes and cache invalidation strategies for private resources
- Educate users on clearing browser cache in shared device scenarios
- Implement additional server-side access validation on each request, not relying on HTTP caching alone

## Variant hunting
Check cache control headers on other authenticated resources (user profiles, private repositories, admin panels)
Test other GitLab features with access restrictions (protected branches, confidential issues, snippets)
Verify if merge requests, CI/CD pipelines, and deployment information are similarly affected
Test with different browsers and HTTP/2 implementations for cache behavior variations
Examine CDN cache behavior for private resources if GitLab uses edge caching
Check if API endpoints have similar cache control issues

## MITRE ATT&CK
- T1190
- T1552
- T1526
- T1566
- T1087

## Notes
The vulnerability requires physical access to a victim's device, which limits immediate remote exploitability. However, it represents a significant information disclosure risk in office and shared device scenarios. The issue affects 'most pages' of private projects, suggesting systemic cache control implementation failure rather than isolated oversight. No authentication bypass is achieved, but access control is effectively circumvented through browser caching mechanisms.

## Full report
<details><summary>Expand</summary>

**Summary:**
On the most of pages related to Private projects, cache control is inadequate, so the contents of Private projects may leak to unauthorized users.

**Description:**
For visibility of projects, you can select `Public`, `Internal`, and `Private`.
Among them, Private projects can only be viewed from project members. (In other words, it can not be viewed by who are not project members.)
In also [GitLab Documentation](https://docs.gitlab.com/ee/public_access/public_access.html), it is mentioned as follows:
> Private projects can only be cloned and viewed by project members, ...

However, due to inadequate cache control on the most of pages related to Private projects, an attacker may view these contents using the 'Back' button in browser.
In addition, users without logging in can also exploit this problem.

Note: This issue supports all modern browsers.

## Steps To Reproduce:
1. Sign in to GitLab.
2. Click the "[+]" icon.
3. Click "New Project".
4. Fill out "Project name" form with "PoC".
5. Check the check box of "Private".
6. Click "Create project" button.
7. Sign out from Gitlab.
8. Hit the "Back" button in browser.

Result: The content of the private project "PoC" is displayed without logging in.

## Impact

This issue leads to information leakage.
Cache control is inadequate on the most pages related to Private projects.
Therefore, almost all contents of Private project may leak.

Although the exploitation needs physical access to the victim's PC, It is not very difficult to access someone's PC in the following scenes:
- Office scenario
- Laptop case

The examples of critical information that may leak are as follows:
- List of file names
- Source code
- Commit log
- Issues
- Contents of the wiki

Note: The official document specifies that they will not be viewed by unauthorized users.

</details>

---
*Analysed by Claude on 2026-05-24*
