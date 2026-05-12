# Stored XSS in Revive Adserver Banner Name Field

## Metadata
- **Source:** HackerOne
- **Report:** 3404968 | https://hackerone.com/reports/3404968
- **Submitted:** 2025-10-30
- **Reporter:** yoyomiski
- **Program:** Revive Adserver
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Stored Cross-Site Scripting (XSS), Improper Input Validation, Insufficient Output Encoding
- **CVEs:** CVE-2025-55123
- **Category:** web-api

## Summary
A stored XSS vulnerability exists in the Banner Name field of Revive Adserver 6.0.0 that allows authenticated attackers to inject malicious JavaScript code. When users granted access to the banner view it, the payload executes in their browser session with full privileges. This enables persistent code execution and session hijacking for all users with banner access.

## Attack scenario
1. Attacker authenticates to Revive Adserver with advertiser privileges
2. Attacker creates or edits a banner and injects payload ("><script>alert(1)</script>) in the Name field
3. Attacker saves the banner; malicious payload is persisted in the database
4. Administrator or another user with User Access grants the attacker's banner access to victim users
5. Victim user logs in and navigates to Banners section to view or manage banners
6. Victim's browser executes the stored JavaScript payload in their authenticated session context

## Root cause
The Banner Name field lacks proper input validation and output encoding. User-supplied input is stored directly in the database and rendered to the DOM without sanitization or HTML entity encoding when displayed to authorized users.

## Attacker mindset
An authenticated advertiser with banner creation privileges seeks to compromise other users with access to their banners. By leveraging the trust placed in the banner management interface, they inject malicious code that executes with the privileges of higher-privileged users (admins/other advertisers), enabling credential theft, session hijacking, or privilege escalation.

## Defensive takeaways
- Implement strict input validation on all user-supplied fields, particularly those used in administrative interfaces
- Apply contextual output encoding: HTML entity encode when rendering text in HTML context, JavaScript encode for JS contexts
- Use templating engines with auto-escaping enabled to prevent accidental XSS
- Deploy Content Security Policy (CSP) headers to mitigate stored XSS impact
- Implement a Web Application Firewall (WAF) rule to detect script tags in banner-related requests
- Conduct security code review of all banner-related input/output handlers
- Sanitize HTML input using allowlist-based libraries (e.g., HTML Purifier) if HTML is legitimately needed
- Apply least privilege: restrict banner creation/editing capabilities to necessary roles only

## Variant hunting
Check other name/title fields across the application: Campaign Name, Advertiser Name, Zone Name, Publisher Name for similar encoding gaps
Audit other text fields that are displayed in administrative dashboards or user-facing pages
Review all fields that support User Access controls for stored XSS vulnerabilities
Test description fields, metadata fields, and custom parameter fields in banner configuration
Examine prepend/append code fields which the report mentions also execute JavaScript
Look for similar issues in other adserver components (zones, placements, campaigns)

## MITRE ATT&CK
- T1190
- T1598
- T1566
- T1204

## Notes
The report explicitly notes this is a legitimate stored XSS finding despite being in the banner context where JavaScript execution is expected. The vulnerability exists because the Name field should not execute scripts—only the actual banner code should. The attacker exploits the fact that authorized users trust the banner management interface, making this a privilege escalation vector from advertiser to admin level access. The persistence in database makes this more severe than reflected XSS as it affects multiple users over time.

## Full report
<details><summary>Expand</summary>

##Version:
==revive-adserver 6.0.0==

##Summary:
A stored Cross-Site Scripting (XSS) vulnerability exists in the Banner → Name field. An attacker can create or edit a banner with a malicious payload in the Name field; that payload is stored and later executed in the browser of users who were added to the banner via User Access (under Advertisers) when they view the banner. This results in persistent JavaScript execution in the context of the victim’s session.

**Note: This Stored-XSS is outside this area as you said: Banners require full Javascript support and so do prepend/append codes. Most of the HTML banners or tracking scripts in fact are just a single <script> tag.**

##Step to reproduce:
1. Go to Banners → Create (or edit an existing banner).
2. In the ==Name field==, insert the payload: `"><script>alert(1)</script>`
3. Save the banner. The name is persisted in the database.
5. Add another user (victim) to the banner under User Access (Advertisers)
6. Log in as that added user. Go to Banners --> XSS

## Impact

- Persistent XSS executing in the browser of users with access to the banner via User Access (Advertisers)

##Video PoC: ███

</details>

---
*Analysed by Claude on 2026-05-12*
