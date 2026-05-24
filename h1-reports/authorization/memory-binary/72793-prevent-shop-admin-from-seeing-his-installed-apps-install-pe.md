# Prevent Shop Admin From Seeing Installed Apps via Malformed Redirect URI

## Metadata
- **Source:** HackerOne
- **Report:** 72793 | https://hackerone.com/reports/72793
- **Submitted:** 2015-06-26
- **Reporter:** prakharprasad
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Denial of Service, Input Validation Flaw, Improper Error Handling, Application Management Bypass
- **CVEs:** None
- **Category:** memory-binary

## Summary
A Shopify app with a malformed redirect_uri (e.g., 'shit:google.com') causes the app management interface to crash with a 500 error when the app is installed, preventing shop admins from viewing or removing any installed apps. An attacker can create a legitimate Shopify app with an invalid callback URL and trick admins into installing it, effectively locking them out of app management.

## Attack scenario
1. Attacker creates a Shopify app with a malformed Application Callback URL containing an invalid URI scheme (e.g., 'shit:google.com')
2. Attacker crafts an OAuth authorization URL using the malicious app's client_id and tricks a shop admin into visiting it
3. Shop admin clicks 'Install' button on the OAuth permission dialog
4. The app is installed but the invalid redirect_uri causes the OAuth flow to fail without proper error handling
5. When admin visits the apps management page (/admin/apps), Shopify's backend crashes attempting to process the malformed redirect_uri
6. Admin is completely locked out of managing their apps with persistent 500 errors until the malicious app is deleted by the developer

## Root cause
Shopify failed to validate redirect_uri values during app creation and did not implement proper error handling in the app management interface when processing invalid URI schemes. The backend exception when loading the apps list is not caught, causing a denial of service to the admin interface.

## Attacker mindset
An attacker could exploit this to sabotage a competitor's Shopify store by installing an unremovable malicious app, disrupting their operations and access to app management until they contact Shopify support or the app developer for removal.

## Defensive takeaways
- Validate redirect_uri values at app creation time against RFC 3986 URI specifications and maintain a whitelist of allowed schemes
- Implement comprehensive error handling in admin interfaces to prevent single malformed records from crashing entire pages
- Add defensive checks when rendering app lists to skip or isolate apps with invalid configurations
- Implement a force-removal mechanism allowing admins to delete apps even if validation fails
- Add logging and alerting for app installations with invalid URIs to detect abuse
- Implement rate limiting on app installations per user/shop
- Add a safety mechanism to prevent app listing pages from being completely inaccessible due to single bad entries

## Variant hunting
Test other admin pages with collections of user-created data for similar crash-on-load vulnerabilities
Try other invalid URI schemes: 'javascript:', 'data:', custom protocols, extremely long URLs, null bytes
Attempt to create apps with invalid characters in other fields (App Name, Description) that might cause parsing errors
Check if similar validation gaps exist in other OAuth platforms (Microsoft, Google, Facebook app configs)
Test if the crash can be triggered via API rather than UI, enabling programmatic exploitation
Investigate if other admin resource pages (/admin/themes, /admin/webhooks) have similar issues with malformed data

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1561 - Disk Wipe
- T1499 - Endpoint Denial of Service

## Notes
Report demonstrates a critical operational impact vulnerability where a single malicious app install completely prevents legitimate admin access to app management. The vulnerability is particularly severe because it persists until developer intervention. Shopify likely patched by adding URI validation and defensive error handling. The attack requires social engineering to trick admins into installing the app, but the impact is substantial once installed.

## Full report
<details><summary>Expand</summary>

Hi,

This is an interesting vulnerability, when a Shopify app whose `redirect_uri` points to a malformed URI handler like **shit:google.com** gets installed to a Shop then, it will effectively prevent the admins to see and remove installed apps to his/her shop. 

**Reproduction**

1. Create a Shopify App at https://app.shopify.com/services/partners/api_clients/new
2. Enter any for the App and set its **Application Callback URL** to **shit:google.com**
3. Save the App.
4. Create an OAuth URL for the App, Like - https://vulnstore.myshopify.com/admin/oauth/authorize?scope=read_customers&client_id=cad94488c733b0f377a9a1d7952db802
5. Now try to install the app by clicking "Install <AppName>" in the OAuth permission dialogue. It won't redirect after clicking.
6. Go and visit https://vulnstore.myshopify.com/admin/apps The page will throw internal server 500 and usual error message.

This will not let admin remove any of his app till the *malicious app* is deleted by the app developer.

POC App: https://[store].myshopify.com/admin/oauth/authorize?scope=read_customers&client_id=cad94488c733b0f377a9a1d7952db802 

If you have any doubt in reproduction, you can watch the following short screencast as well - https://www.dropbox.com/s/1h8gjg07r5h9gkj/Shopify%20DoS.mov?dl=0

Regards,
Prakhar Prasad

</details>

---
*Analysed by Claude on 2026-05-24*
