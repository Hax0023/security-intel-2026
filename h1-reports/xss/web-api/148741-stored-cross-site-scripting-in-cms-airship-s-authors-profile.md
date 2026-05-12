# Stored Cross-Site-Scripting in CMS Airship Author Profiles

## Metadata
- **Source:** HackerOne
- **Report:** 148741 | https://hackerone.com/reports/148741
- **Submitted:** 2016-07-01
- **Reporter:** lukasreschke
- **Program:** CMS Airship
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Stored XSS, Improper Output Encoding, Reflected XSS in HTML Context
- **CVEs:** None
- **Category:** web-api

## Summary
A stored XSS vulnerability exists in CMS Airship's Bridge admin panel where author names are not properly escaped when displayed in page headings and form labels. An attacker can create an author profile with malicious JavaScript in the name field, which executes when other users view the author edit page, potentially compromising admin accounts.

## Attack scenario
1. Attacker registers a new account on the Airship CMS via the public registration endpoint
2. Attacker navigates to /bridge/author/new and creates an author with name '<script>alert(1)</script>' or similar payload
3. Attacker sends the author edit link (e.g., /bridge/author/edit/3) to a higher-privileged user such as the captain/admin
4. When the admin clicks the link and visits the edit page, the stored XSS payload executes in their browser context
5. Attacker can steal CSRF tokens, session cookies, or perform actions as the admin user
6. Attacker escalates privileges or modifies CMS content with admin permissions

## Root cause
The author name parameter is HTML-escaped in form input values (using HTML entities like &lt; &gt;) but not escaped in the page heading context (h2 tag). The template renders the author name directly in the h2 element without proper output encoding, allowing script injection. This is a classic context-specific encoding failure where different output contexts require different escaping strategies.

## Attacker mindset
An attacker with low privileges (basic registered user) looks for ways to escalate to admin level. They discover that author creation is available to all users and test basic XSS payloads. Finding that input validation is weak, they craft a stored XSS to target administrators who will inevitably view author profiles. The attacker leverages the transitive trust between users and admins.

## Defensive takeaways
- Implement consistent output encoding based on context (HTML, JavaScript, URL, CSS) - use a templating engine with auto-escaping enabled by default
- Apply defense-in-depth: validate author names server-side (whitelist alphanumeric + spaces), sanitize output with HTML entity encoding, and implement strong Content Security Policy
- Use a security-focused template engine that escapes by default rather than requiring manual escaping at each output point
- Implement input validation to reject or sanitize special characters in user profile fields that are displayed in administrative interfaces
- Apply principle of least privilege: restrict author creation to trusted users rather than all registered users
- Add security testing for XSS to CI/CD pipeline, including stored XSS scenarios with payloads in user-controlled fields
- Implement comprehensive CSP headers to prevent inline script execution even if XSS payloads bypass encoding

## Variant hunting
Check other user-controllable fields that display in administrative pages (author bio, author email, author slug) for similar encoding issues
Test other admin-facing features that reference user input: author descriptions, article author attribution, comments if enabled
Look for stored XSS in category names, tag names, or other taxonomy fields that admins browse
Test whether the vulnerability exists in different template contexts: page titles, meta tags, JavaScript variable assignments
Check if similar encoding gaps exist in other bridge modules beyond authors (pages, articles, users, settings)
Verify if lower-privileged actions can trigger higher-privileged endpoints, expanding the attack surface

## MITRE ATT&CK
- T1190
- T1598
- T1566
- T1204

## Notes
The vulnerability is particularly dangerous because: (1) stored XSS persists for all future viewers, (2) targets high-privilege users (admins/captains), (3) low barrier to entry (public registration enabled by default), (4) the developer acknowledged CSP provides some mitigation but CSP is not a primary defense mechanism. The reporter notes version 1.1.0 and 1.1.1 appear affected. The fix likely involves escaping the author name in the h2 tag context, though proper fix would use a templating engine with automatic context-aware escaping.

## Full report
<details><summary>Expand</summary>

I'm just checking out CMS Airship and some of the security features look pretty nice. Awesome job on that!

After clicking around a bit I stumbled however upon a stored XSS vulnerability in the Bridge.  As per `/bridge/help` I use 1.1.0 version (installed via Docker), as I couldn't find any reference with regard to this in the 1.1.1 changelog from https://github.com/paragonie/airship/commit/29dc60a1b0178222c3c984915f2eda6322ca3453 I believe that it probably is affected as well.

To reproduce this:

1. Install CMS Airship
2. Make sure to use the default settings (or at least do not uncheck "Enable registration")
3. Take another browser tab and go to http://localhost:8081/bridge/board to register a new account
4. Login with that account at http://localhost:8081/bridge/login
5. Go to http://localhost:8080/bridge/author/new
6. Create a new author with the name "<script>alert(1)</script>"
7. Send the author edit link to another user, such as the captain user (e.g. http://localhost:8080/bridge/author/edit/3)
8. Open it as captain

Then you see the XSS executed, or well, if your browser supports CSP a decent CSP warning in your browser console :-)

{F102848}

The HTML in question is:

```
    <div id="bridge_main">    <h2>Edit Author "<script>alert(1)</script>" Details</h2>
<form method="post"><input type="hidden" name="_CSRF_TOKEN" value="ijYiRqBM1DKBw9Kevvn4zjEw:frKdBMZxXK3VUgI0ZEuQHdHerw9NnVwTx8a62QiJhiY3" />
    <div class="table full-width table-pad-1">
        <div class="table-row">
            <div class="table-cell table-label">
                <label for="author_name">Author Name:</label>
            </div>
            <div class="table-cell">
                <input class="full-width" id="author_name" name="name" placeholder="e.g.&#x20;Information&#x20;Technology&#x20;Department" value="&lt;script&gt;alert&#x28;1&#x29;&lt;&#x2F;script&gt;" type="text" />
            </div>
        </div>
```

Since I don't have libsodium and PECL installed locally on my dev machine I couldn't include a tested patch for this. Sorry :-)

</details>

---
*Analysed by Claude on 2026-05-12*
