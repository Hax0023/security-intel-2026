# Stored XSS in Crashlytics Android App via Malicious App Name

## Metadata
- **Source:** HackerOne
- **Report:** 41856 | https://hackerone.com/reports/41856
- **Submitted:** 2014-12-25
- **Reporter:** akhil-reni
- **Program:** Crashlytics/Fabric (Google)
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Stored XSS, HTML Injection, Improper Input Validation, Unsafe Rendering
- **CVEs:** None
- **Category:** web-api

## Summary
The Crashlytics Android app fails to properly sanitize app names when rendering them in the UI, allowing attackers to inject arbitrary HTML/JavaScript through malicious app names. An attacker can create an app with XSS payload in its name, and when invited users download the Crashlytics app, the payload executes in the app's context.

## Attack scenario
1. Attacker creates a new app on fabric.io with a malicious app name containing XSS payload (e.g., '"><img src=x onerror=prompt(1)>')
2. Attacker sends invitations to target users to test the app via Crashlytics invitation mechanism
3. Target users receive invitation and download the Crashlytics Android app to access the project
4. When users open the Crashlytics app, it displays the app name without sanitization
5. The XSS payload executes in the context of the Crashlytics Android app
6. Attacker can steal session tokens, credentials, or perform actions on behalf of the user

## Root cause
The Crashlytics Android application renders user-controlled app names as HTML without proper sanitization or encoding. The backend likely stores the raw app name, and the frontend renders it using unsafe methods (e.g., WebView.loadData() or similar) without stripping HTML tags or encoding special characters.

## Attacker mindset
An attacker with a Fabric.io account seeks to compromise users who download the Crashlytics app by exploiting the trust relationship between developers and their testers. By embedding XSS in the app name, they achieve persistent malicious code execution across all installations.

## Defensive takeaways
- Implement strict input validation and sanitization for all user-provided data (app names, descriptions, etc.) on both client and server
- Use context-aware output encoding: HTML-encode when rendering in HTML contexts, JavaScript-encode for JS contexts
- Avoid rendering user input as raw HTML; use text views or properly escaped components instead of WebView when not necessary
- Implement Content Security Policy (CSP) headers to mitigate XSS impact
- Apply allowlist validation for app names (alphanumeric, hyphens, underscores only)
- Perform security testing including fuzzing with XSS payloads on all user-facing input fields
- Use OWASP ESAPI or similar libraries for secure encoding functions
- Implement automated security scanning in CI/CD pipeline to catch XSS vulnerabilities

## Variant hunting
Check other user-controlled fields in Crashlytics/Fabric for similar XSS: app descriptions, organization names, user display names, custom attributes
Test app icon URLs and media uploads for XXE or path traversal
Examine crash report metadata rendering for stored XSS vectors
Check if organization/team names have the same vulnerability
Test custom event/breadcrumb data for XSS in analytics displays
Verify if user invitations or comments support XSS payloads
Check Fabric dashboard web interface for the same XSS vulnerability

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1204: User Execution
- T1059: Command and Scripting Interpreter
- T1071: Application Layer Protocol

## Notes
This is a classic stored XSS vulnerability with moderate severity due to the social engineering requirement (user must accept invitation). The impact depends on the permissions and data accessible within the Crashlytics app context. The vulnerability affects all invited users, making it a widespread attack vector. The report lacks information about the actual bounty amount awarded and timeline to fix.

## Full report
<details><summary>Expand</summary>

Hey hi,

While in fabric , the app name is rendered as HTML/XSS in android app of Crashlytics  like shown in the screenshot.

Steps to reproduce:
Create an app with the name of payload in my case i have used, "><img src=x>
under the following URL https://www.fabric.io/img-srcx-onerrorprompt03/android/apps/imgsrcxonerrorprompt0.myapplication/beta/releases/latest
(replace the app names wherever needed)
Send invitation to users to test the APP
users will get the invitation and will be forced to download the Crashlytics app,
once downloaded they will see the app name like in the screenshot.


Regards,
Karthik
Wesecureapp

</details>

---
*Analysed by Claude on 2026-05-24*
