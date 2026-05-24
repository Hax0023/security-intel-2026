# API Does Not Apply Access Controls to Translations

## Metadata
- **Source:** HackerOne
- **Report:** 232994 | https://hackerone.com/reports/232994
- **Submitted:** 2017-05-29
- **Reporter:** 4cad
- **Program:** Weblate
- **Bounty:** Not specified
- **Severity:** Medium
- **Vuln:** Broken Access Control, Authorization Bypass, Information Disclosure
- **CVEs:** None
- **Category:** uncategorised

## Summary
Weblate's API endpoints for translation files bypass access control checks that are enforced in the web UI, allowing unauthenticated users to download translation files from projects they have no permission to access. The vulnerability exists in the `/api/translations/` endpoint which fails to validate user permissions before serving translation file content.

## Attack scenario
1. Attacker identifies a Weblate instance with restricted project access configured via the web UI
2. Attacker discovers the API endpoint structure by navigating to `/api/components/` or similar discovery endpoints
3. Attacker retrieves project and component metadata through the API without authentication
4. Attacker identifies the `file_url` parameter pointing to `/api/translations/{project}/{component}/{language}/file/`
5. Attacker downloads the translation file directly via the API endpoint, bypassing web UI access controls
6. Attacker obtains sensitive translation content that should have been restricted

## Root cause
The API layer implements different authorization logic than the web UI layer. The API file serving endpoint (`/api/translations/.../file/`) does not perform the same permission checks that are enforced when accessing projects through the web interface. This suggests either a missing authorization decorator/middleware or insufficient centralization of access control logic.

## Attacker mindset
An attacker would recognize that web APIs often have different security implementations than their UI counterparts. They would probe API endpoints systematically to find endpoints that bypass UI-level restrictions. The presence of file URLs in API responses provides a roadmap for exploitation. An attacker could use this to extract proprietary translations, competitive intelligence, or content from private projects.

## Defensive takeaways
- Implement centralized authorization checks for all API endpoints, not just the UI layer
- Apply the same permission validation logic across both web UI and API responses
- Use consistent authorization decorators/middleware across all resource serving endpoints
- Test API endpoints with accounts having restricted permissions to verify access control enforcement
- Avoid exposing direct file URLs in API responses without verifying caller permissions
- Implement proper authentication requirements for all API endpoints, even those serving downloadable content
- Audit API endpoints regularly to ensure they enforce the same access control policies as documented

## Variant hunting
Check other API endpoints for similar access control bypasses (e.g., `/api/projects/`, `/api/components/`)
Test other file serving endpoints with restricted accounts
Review all endpoints that return URLs or file paths to ensure they validate permissions before exposure
Check if query parameters or headers can be manipulated to bypass checks
Verify if other API authentication methods (tokens, OAuth) properly enforce the same restrictions
Test API endpoints at different permission levels (anonymous, guest, translator, reviewer, manager)

## MITRE ATT&CK
- T1190
- T1040
- T1526

## Notes
The researcher noted that Weblate's access controls may not be critical to its core mission, but their implementation in the UI suggests they are important to users. The vulnerability is particularly interesting because it demonstrates authorization logic not being consistently applied across different interfaces (web vs API). This is a common pattern in API security issues. The report shows good security awareness in recognizing that file URLs in API responses can be a vector for access control bypass.

## Full report
<details><summary>Expand</summary>

Summary
=======

The /api/ does not enforce access control on the translation files, allowing anyone to download full translation files. See the screenshot for an example project being viewed by an anonymous account that is configured to have no permissions.

Description
=======
On my local setup running Weblate 2.15-dev, I removed all permissions from the Guest group and restarted the server. When I tried to navigate to the test project through the UI the usual way at URL http://192.168.1.129:8000/projects/testproject/, I received an Access Denied message.

However I was able to find the project details through the API at http://192.168.1.129:8000/api/components/testproject/testcomponent/translations/ and even download the translations file by clicking on the "file_url" link, which in my case is "http://192.168.1.129:8000/api/translations/testproject/testcomponent/en_CA/file/".

Assessment
=======
I am marking this as Medium because from what I have seen the access controls are not that important to Weblate's mission and it does not seem designed to keep translations secret, although the existence of access controls through the web app suggests that this is something that people wanted enough to implement. If enforcing the read access controls is of any importance, then I would treat this with higher severity.

</details>

---
*Analysed by Claude on 2026-05-24*
