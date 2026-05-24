# Stored XSS in Hexo-admin Post Editor

## Metadata
- **Source:** HackerOne
- **Report:** 716570 | https://hackerone.com/reports/716570
- **Submitted:** 2019-10-17
- **Reporter:** vu1n
- **Program:** HackerOne
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Stored Cross-Site Scripting (XSS), Improper Input Validation, Insufficient Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
The hexo-admin plugin version 3.9.0 is vulnerable to stored XSS through the post content editor, allowing attackers to inject malicious scripts that persist in saved posts. When posts containing XSS payloads are regenerated and viewed, the malicious scripts execute in the browser of any user accessing the post.

## Attack scenario
1. Attacker gains access to hexo-admin panel (localhost:4000/admin) through authentication bypass or stolen credentials
2. Attacker creates or edits an existing blog post and injects XSS payload in the post content field (e.g., "><img src=x onerror=alert('XSS')>)
3. Attacker saves the post, triggering storage of the malicious payload in the database
4. Attacker triggers hexo clean, hexo generate, and hexo server commands to rebuild the static site with the malicious content
5. When legitimate users visit the published post URL, the stored XSS payload executes in their browser context
6. Attacker can steal session cookies, perform actions on behalf of users, or redirect to phishing pages

## Root cause
The hexo-admin plugin fails to properly sanitize and validate user-supplied content in post editor fields before storage and rendering. Input is not escaped or sanitized when displayed in both the admin editor and the generated static HTML pages, allowing arbitrary HTML/JavaScript execution.

## Attacker mindset
An attacker with admin panel access (or who can bypass authentication) seeks to compromise the blog and its readers by injecting persistent malicious scripts. The attacker leverages the trust users have in the blog content to execute arbitrary code in their browsers for credential theft, malware distribution, or defacement.

## Defensive takeaways
- Implement strict input validation and sanitization for all user-supplied content, especially in content editors
- Apply context-aware output encoding when rendering stored content (HTML entity encoding for HTML context)
- Use established sanitization libraries (e.g., DOMPurify, sanitize-html) to strip dangerous HTML/JavaScript before storage
- Implement Content Security Policy (CSP) headers to prevent inline script execution
- Apply the principle of least privilege - restrict admin panel access through strong authentication and authorization
- Perform security code reviews focusing on data flow from input to output
- Keep all dependencies and plugins updated to patch known vulnerabilities
- Consider using a template engine with auto-escaping enabled by default

## Variant hunting
Test other content fields in hexo-admin for XSS (metadata, excerpts, tags, custom fields)
Investigate if the vulnerability exists in comment functionality or user-generated content areas
Check for DOM-based XSS in admin UI JavaScript that processes post content
Test for XSS in the Hexo core static site generator when processing post content
Look for stored XSS in theme-related fields or configuration areas
Examine API endpoints used by the admin panel for proper sanitization
Test SVG, script tags, and event handler variations as bypass techniques

## MITRE ATT&CK
- T1190
- T1074
- T1566

## Notes
The vulnerability affects the static blog generation workflow, making it particularly dangerous as the malicious payload becomes part of the generated static content. This is a classic stored XSS in a content management system. The reporter properly disclosed to maintainers and npm security team. The plugin appears to lack Content Security Policy and input sanitization mechanisms entirely. Workaround would involve manual content sanitization before saving or using the admin panel with additional WAF protections.

## Full report
<details><summary>Expand</summary>

I would like to report  Stored XSS in Hexo-admin
It allows The Post editor functionality in the hexo-admin plugin 3.9.0 for Node.js is vulnerable to stored XSS via the content of a post.

# Module

**module name:** Hexo-admin
**version:** 3.9.0
**npm page:** `https://www.npmjs.com/package/hexo-admin

## Module Description

An admin UI for the Hexo blog engine. Based off of the Ghost interface, with inspiration from svbtle and prose.io.

## Module Stats

> Replace stats below with numbers from npm’s module page:

[1] 216

# Stored XSS

## Stored XSS occurs when a malicious script is injected directly into a vulnerable web application.

Description about how the vulnerability was found and how it can be exploited, how it harms package users (data modification/lost, system access, other.

## Steps To Reproduce:

Steps of reproduction
==========================
1. Prerequisites are
    - hexojs (Static blog generator)
    - hexo-admin plugin (https://github.com/jaredly/hexo-admin)

2. Start the hexo server from website directory (command: hexo server -d)
3. Access hexo admin panel at localhost:4000/admin
4. Click on the posts section
5. Create the new post and give it a title (Test XSS here) 
6. In the post content you can put the below payloads
    1.  "><img src=x onerror=alert("XSS")>
    2.  "><img src=x onerror=alert(document.domain)>
7. You'll get the XSS pop-up in the post editor
8. Save the post and rebuilt the pages with for changes
9. To generate again, apply below commands
     1. hexo clean
     2. hexo generate
     3. hexo server -d
10. Go to your post "Test XSS"
11. You'll get the XSS pop-up there every time you open that page because it is stored.

## Patch

> NA

## Supporting Material/References:


- Ubuntu
- 12.11.1
- 6.11.3
- Mozilla

# Wrap up

> Select Y or N for the following statements:

- I contacted the maintainer to let them know: Y
- I opened an issue in the related repository: Y 

> Notes:
Hey I've already reported the vulnerability to npm security team directly just wanted to report on hackerone. you can cross verify it with my email. I hope you make it a triaged. sorry for the delay.
this is a github issue (https://github.com/jaredly/hexo-admin/issues/185)

## Impact

Stored XSS allows an attacker to embed a malicious script into a vulnerable page, which is then executed when a victim views the page.

</details>

---
*Analysed by Claude on 2026-05-24*
