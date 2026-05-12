# Stored XSS in Google Login URI Parameter on Shopify Admin

## Metadata
- **Source:** HackerOne
- **Report:** 691611 | https://hackerone.com/reports/691611
- **Submitted:** 2019-09-10
- **Reporter:** ashketchum
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Cross-Site Scripting (XSS), Improper Input Validation, URL Parameter Injection
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability exists in Shopify's Google Apps login integration where the 'google_apps_uri' parameter is not properly sanitized before being rendered in the login page. An attacker can inject malicious JavaScript code via a crafted URL that will execute in the context of the victim's browser during the Google login process.

## Attack scenario
1. Attacker discovers that the google_apps_uri parameter on the login/identity endpoint accepts arbitrary JavaScript URLs
2. Attacker crafts a malicious URL containing javascript: protocol handler with payload (e.g., javascript:prompt(document.cookie))
3. Attacker shares the crafted URL with a target staff member via phishing email or social engineering
4. Victim clicks the link and arrives at the Shopify login page with the malicious parameter embedded
5. When the victim clicks 'Login with Google' button, the JavaScript payload executes in their browser context
6. Attacker successfully steals session cookies, credentials, or other sensitive data from the victim's session

## Root cause
The google_apps_uri parameter is not being properly validated or URL-encoded before being used in an href attribute or onclick handler. The application fails to implement input validation to reject non-HTTP(S) protocols or sanitize the parameter output.

## Attacker mindset
An attacker would identify this vulnerability as a low-effort, high-impact attack vector for credential theft from staff members. By combining it with phishing, they could target administrative accounts to gain access to Shopify stores.

## Defensive takeaways
- Implement strict URL validation to only allow http:// and https:// protocols for redirect URIs
- Use a whitelist of allowed domains for the google_apps_uri parameter
- Properly HTML-encode and URL-encode all user-supplied parameters before rendering in HTML context
- Implement Content Security Policy (CSP) headers to prevent inline script execution
- Validate that redirect URLs match expected Shopify domain patterns
- Use httpOnly and Secure flags on session cookies to prevent JavaScript access
- Perform server-side validation of all parameters, not just client-side validation

## Variant hunting
Check other authentication providers (Facebook, GitHub, etc.) for similar parameter injection flaws
Test other URL parameters in the login flow (return_to, destination_uuid, state) for XSS
Look for similar patterns in other Shopify login endpoints and OAuth callback handlers
Test for data: URI scheme injection for XSS bypass
Investigate whether other redirect parameters are vulnerable to open redirect or XSS
Check if vbscript: or other protocol handlers are also accepted

## MITRE ATT&CK
- T1190
- T1598
- T1566
- T1539

## Notes
This is a reflected XSS vulnerability requiring user interaction (clicking the crafted link). The report demonstrates understanding of the vulnerability through multiple POCs. The impact is significant as it targets the admin login flow where staff authentication is compromised. The vulnerability could be leveraged for account takeover, data theft, or lateral movement within Shopify stores.

## Full report
<details><summary>Expand</summary>

Hello Security Team,
I have found xss when we enable login services as, 
Allow staff to use external services to log in to Shopify and we enable Google Apps for login
we get the " Log in with Google " option enable 

{F579219}

### Steps to Reproduce:

Step1: Go to https://YOURSHOP.myshopify.com/admin/settings/account
Step2: Login Services: Staff can use Google Apps to log in -->> Enable Google Apps for login
Step3: Now staff can log in using Google
Step4:  Log out from your account
Step5: Now go to following Url and try to log in using Google 

#### NOTE: I have made changes in the URL at google_apps_uri

### POC URL 1: 
https://app.shopify.com/services/login/identity?destination_uuid=79b5c315-b5ac-4b19-bd33-13554433fa31&google_apps_uri=javascript:prompt(document.domain)&return_to=https%3A%2F%2Fapp.shopify.com%2Fservices%2Flogin%2Fidentity_callback%3Fshop_name%3D123ashketchum%26state%3D6a_2K0iBEBMG3sv07qFMrtzfrBFY4gZ9JsN0EJAW2Xck07xlkghl0tmZwGIvYEZ1KZw2mG4d4Omhl_h5oB_7t4dcXoS37UUOMG6f9sOr7BCKyR23PWbLpVlh4A0lMXmNuxOEUeEA55eapNpVZqT6AyfnJkQhn4K89-I5O6TVqcamtHaXWRH7b1EI6U8LvQFddrBPYniYGpggAwsFLvb5UeTvRw-fbvRditQ20YWYTK8%253D&ui_locales=en&upgradeable=true&ux=shop

### POC URL 2:
https://app.shopify.com/services/login/identity?destination_uuid=79b5c315-b5ac-4b19-bd33-13554433fa31&google_apps_uri=javascript:prompt(document.cookie)&return_to=https%3A%2F%2Fapp.shopify.com%2Fservices%2Flogin%2Fidentity_callback%3Fshop_name%3D123ashketchum%26state%3D6a_2K0iBEBMG3sv07qFMrtzfrBFY4gZ9JsN0EJAW2Xck07xlkghl0tmZwGIvYEZ1KZw2mG4d4Omhl_h5oB_7t4dcXoS37UUOMG6f9sOr7BCKyR23PWbLpVlh4A0lMXmNuxOEUeEA55eapNpVZqT6AyfnJkQhn4K89-I5O6TVqcamtHaXWRH7b1EI6U8LvQFddrBPYniYGpggAwsFLvb5UeTvRw-fbvRditQ20YWYTK8%253D&ui_locales=en&upgradeable=true&ux=shop

### XSS will be triggered!!

{F579220}

### I have attached POC Video, Please take a look!!

Regards,
@ashketchum

## Impact

The attacker can steal data from whoever who try to login using Google!!

</details>

---
*Analysed by Claude on 2026-05-12*
