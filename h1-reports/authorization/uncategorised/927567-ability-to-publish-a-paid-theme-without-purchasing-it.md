# Ability to publish a paid theme without purchasing it on Shopify

## Metadata
- **Source:** HackerOne
- **Report:** 927567 | https://hackerone.com/reports/927567
- **Submitted:** 2020-07-20
- **Reporter:** saltymermaid
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Broken Access Control, Improper Authorization, Client-Side Validation Bypass, GraphQL Authorization Bypass
- **CVEs:** None
- **Category:** uncategorised

## Summary
A merchant can publish and use paid themes without purchasing them by directly invoking the ThemePublishLegacy GraphQL mutation with a paid theme ID. The vulnerability allows unauthorized access to premium theme assets, including the ability to edit, rename, and download theme files that should be restricted to paying customers.

## Attack scenario
1. Attacker installs a free theme and publishes it to establish a working publish flow
2. Attacker identifies a paid theme ID by clicking Customize and extracting the ID from the URL
3. Attacker captures the ThemePublishLegacy GraphQL request when publishing the free theme
4. Attacker modifies the GraphQL mutation body to replace the free theme ID with the paid theme ID
5. Attacker executes the modified GraphQL request via browser console with their authenticated session
6. Paid theme is activated and published without payment; attacker gains full access to edit, rename, and download theme files

## Root cause
The backend authorization check for the ThemePublishLegacy GraphQL mutation does not validate whether the user has purchased or has rights to the theme being published. The authorization is performed only at the UI level (client-side), allowing direct API calls to bypass purchase verification. The server accepts any theme ID in the mutation without verifying ownership or purchase status.

## Attacker mindset
An economically motivated attacker seeking to acquire premium themes without cost. The attacker is technically savvy enough to inspect network requests, modify GraphQL payloads, and execute API calls directly. Secondary motivation includes accessing proprietary theme code for reverse engineering, copying designs, or selling stolen assets.

## Defensive takeaways
- Implement server-side authorization checks that verify the user has legitimately purchased or has licensing rights before allowing theme publication
- Validate theme ownership and licensing status on every backend API call, not just in the UI
- Implement purchase state validation in the GraphQL resolver before executing the ThemePublishLegacy mutation
- Use backend entitlement checks to confirm the requesting user has an active license for the theme being published
- Log and monitor suspicious theme publication attempts, particularly free-to-paid theme transitions
- Consider adding rate limiting or additional verification steps when publishing paid themes
- Never rely solely on client-side validation or UI restrictions for enforcing paid features

## Variant hunting
Check other theme management mutations (ThemePublish, ThemeCreate, ThemeUpdate) for similar authorization bypasses
Test other paid Shopify features (apps, extensions) for similar direct API invocation bypasses
Investigate whether theme editing or downloading endpoints also lack proper authorization
Check if theme duplication or copying features have similar vulnerabilities
Test whether the vulnerability applies to unpublishing or deleting premium themes
Examine other mutations in the online-store admin API for authorization gaps

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1199 - Trusted Relationship
- T1566 - Phishing
- T1531 - Account Access Removal

## Notes
This is a classic authorization bypass where business logic enforcement exists only at the UI layer. The attacker uses legitimate API endpoints with valid authentication but bypasses the payment/entitlement validation. The vulnerability demonstrates why security must be enforced at the API/backend layer, not the presentation layer. The fact that users appear to own the theme after publishing (removal of trial badges) suggests the backend may be incorrectly tracking ownership based on publication status rather than purchase status.

## Full report
<details><summary>Expand</summary>

Hi,

## Description
I found out that it is possible to publish a paid theme without purchasing it. I remember trying this some time ago and it seemed to be safe from this kind of attack.

## Steps to reproduce
1. Make sure you have the default theme installed and that it is published.
2. Install any *free* theme
3. Install any *paid* theme
4. Get the paid theme ID by clicking the "Customize" link and extract the ID from the url (https\://yourshop.myshopify.com/admin/themes/***[theme_id]***/editor) and save it for later.
5. Publish the free theme you install from step #2
6. From your developper tool, copy the "*ThemePublishLegacy*" XHR request as Fetch\

    ```
    fetch("https://yourshop.myshopify.com/admin/online-store/admin/api/unversioned/graphql", {
      "headers": {
        "accept": "application/json",
        "accept-language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
        "cache-control": "no-cache",
        "content-type": "application/json",
        "pragma": "no-cache",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "x-online-store-web": "1"
      },
      "referrerPolicy": "no-referrer",
      "body": "{\"operationName\":\"ThemePublishLegacy\",\"variables\":{\"id\":\"gid://shopify/OnlineStoreTheme/[THEME_ID]\"},\"query\":\"mutation     ThemePublishLegacy($id: ID!) {\\n  onlineStoreThemePublish(id: $id) {\\n    theme {\\n      id\\n      __typename\\n    }\\n    userErrors {\\n      field\\n          message\\n      __typename\\n    }\\n    __typename\\n  }\\n}\\n\"}",
      "method": "POST",
      "mode": "cors",
      "credentials": "include"
    });
```
7. Paste the request in your developer tool console and replace the free theme ID with the paid theme ID you save at step #4
 7.1. `..."body": "{\"operationName\":\"ThemePublishLegacy\",\"variables\":{\"id\":\"gid://shopify/OnlineStoreTheme/`**`[THEME_ID]`**`\"},\"query\":\"mutation...`
8. Refresh the page and you should see that the paid theme is now publish & active.

Also, after the theme is published, it seems like we own it. So, at this point, if you publish another theme (the free one), you should see that the the yellow "Theme trial"  badge is missing and that you can rename, edit and download the theme files.

## Impact

Ability to install paid theme without purchasing it could lead to content stealing and lost of profit. There is also some unwanted information disclosure since we can edit the theme code and download the files after its published.

If you need extra details, images or a POC video, please let me know!

Thank you!

</details>

---
*Analysed by Claude on 2026-05-24*
