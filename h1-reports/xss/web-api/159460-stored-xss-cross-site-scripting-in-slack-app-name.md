# Stored XSS in Slack App Name Parameter

## Metadata
- **Source:** HackerOne
- **Report:** 159460 | https://hackerone.com/reports/159460
- **Submitted:** 2016-08-15
- **Reporter:** imnarendrabhati
- **Program:** Slack
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Stored Cross-Site Scripting (XSS), Improper Input Validation, Improper Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A stored XSS vulnerability exists in the Slack app configuration page where user-supplied input in the app name parameter is not properly sanitized or encoded before being reflected in the page. An attacker can inject malicious JavaScript code that executes in the browsers of any user viewing the compromised app page, including the app creator and other workspace members.

## Attack scenario
1. Attacker navigates to their Slack app's edit page at https://api.slack.com/apps/[appid]/general
2. Attacker enters a malicious payload such as "/><script>alert(/Bhati/)</script>" in the app name field
3. Attacker saves the changes, storing the malicious payload in the Slack database
4. Any user (including other workspace members) who visits the app page or clicks a link to the app details page triggers the stored XSS
5. The injected JavaScript executes in the victim's browser with their privileges and session context
6. Attacker can steal session cookies, perform actions on behalf of the victim, or redirect to phishing pages

## Root cause
Slack failed to implement proper input validation and output encoding for the app name parameter. The application directly concatenates user input into the HTML/JavaScript without sanitization, allowing script tags and other HTML entities to be stored and executed when the page is rendered.

## Attacker mindset
The attacker discovered that a commonly-edited field (app name) lacked proper XSS protections. They recognized this could affect multiple users accessing the same app configuration page and escalate the impact by sharing malicious links to victims, making it a powerful attack vector for credential theft or further compromise.

## Defensive takeaways
- Implement strict input validation on all user-supplied fields, including app metadata like names and descriptions
- Apply proper output encoding/escaping based on context (HTML entity encoding, JavaScript escaping, URL encoding)
- Use Content Security Policy (CSP) headers to prevent inline script execution
- Utilize parameterized templates or frameworks that automatically escape output by default
- Sanitize HTML input using approved whitelisting libraries rather than blacklisting
- Implement security testing (SAST/DAST) in the CI/CD pipeline to catch XSS vulnerabilities
- Apply principle of least privilege to app configuration permissions
- Conduct regular security audits of all user input handling, particularly in administrative/configuration interfaces

## Variant hunting
Check other app metadata fields (description, instructions, category, etc.) for similar XSS vulnerabilities
Test custom app display names, bot names, and other user-configurable identifiers
Examine integration configuration pages and marketplace app listings for similar issues
Look for XSS in workspace settings, channel descriptions, user profiles, and other collaborative features
Test for DOM-based XSS in app configuration JavaScript and API response handling
Check if the vulnerability affects app directory/marketplace where apps are publicly listed

## MITRE ATT&CK
- T1190
- T1566
- T1598
- T1539
- T1005

## Notes
This is a classic stored XSS vulnerability in a multi-user context where the impact extends beyond a single user. The fact that the malicious link can be shared to other users significantly increases the threat level. The vulnerability appears to have been fixed by Slack (as indicated by the H1 report status), likely through implementation of proper output encoding in the app display pages.

## Full report
<details><summary>Expand</summary>

Hello Slack,

This vulnerability is about a Stored Cross Site Scripting

Slack Stored XSS In App(App Name)

Vulnerable URL(Edit App Page)
https://api.slack.com/apps/[appid]/general

https://api.slack.com/apps/A21B3V9GA/general

Vulnerable Parameter = name

Note -Its also work on other user as well.

Send this link to victim

===================

Reproduction Steps
POC Video - https://youtu.be/3jAbPjfPW1o
Screen shot is also attached.

1) Go to app edit page
https://api.slack.com/apps/[appid]/general
https://api.slack.com/apps/A21B3V9GA/general
2) In app name parameter enter the following payload
"/><script>alert(/Bhati/)</script>
3) Now open the app page in any other tab
https://bhativictim.slack.com/apps/A21B3V9GA--scriptalert-bhati-script
4) You will get a Alert Box
5) We can also send this same link to other user(victim).

Thanks,
Narendra

</details>

---
*Analysed by Claude on 2026-05-12*
