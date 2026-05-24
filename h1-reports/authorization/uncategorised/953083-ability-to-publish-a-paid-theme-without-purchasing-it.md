# Ability to publish a paid theme without purchasing it via ThemePublishLegacy race condition

## Metadata
- **Source:** HackerOne
- **Report:** 953083 | https://hackerone.com/reports/953083
- **Submitted:** 2020-08-07
- **Reporter:** saltymermaid
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Race Condition, Authorization Bypass, Improper Access Control, Business Logic Bypass
- **CVEs:** None
- **Category:** uncategorised

## Summary
A race condition in Shopify's theme publication system allows attackers to publish paid themes without purchasing them by sending a ThemePublishLegacy GraphQL mutation during the theme installation window. The vulnerability exploits a timing gap where authorization checks are not properly enforced during the installation process, enabling unauthorized access to premium theme files and full ownership capabilities.

## Attack scenario
1. Attacker installs and publishes a free theme to capture the ThemePublishLegacy GraphQL request structure
2. Attacker initiates installation of a target paid theme from themes.shopify.com and immediately navigates to admin themes section
3. During the installation process, attacker monitors network requests to extract the theme ID from ThemesProcessingLegacy responses
4. Within the narrow installation window, attacker executes the ThemePublishLegacy mutation with the paid theme ID before installation completes
5. Publication succeeds due to race condition, granting attacker full ownership and edit capabilities of the paid theme
6. Attacker downloads theme files, modifies code, or publishes as their own, gaining commercial value without payment

## Root cause
The authorization and validation logic for the ThemePublishLegacy mutation does not properly account for themes in the 'installing' state. The application assumes purchased status is already validated, but during installation there is a window where the purchase verification check is not enforced or runs after the publish operation. The publish operation completes before final validation of purchase/licensing status occurs.

## Attacker mindset
An attacker with access to a Shopify store seeks to obtain premium paid themes without purchasing them for cost savings or to steal proprietary theme designs for redistribution. The attacker reverse-engineers the GraphQL API by inspecting network requests, identifies the race condition vulnerability, and automates the timing-sensitive exploitation steps. The motivation is financial gain through theme theft and resale.

## Defensive takeaways
- Implement synchronous authorization checks that verify purchase/license status BEFORE any publish operation begins, not after
- Use database transactions with proper locking to ensure theme state cannot be modified between state transitions
- Validate that themes can only be published after installation is 100% complete and confirmed in database
- Add state machine validation ensuring only valid state transitions (e.g., installing → installed → published, never installing → published)
- Implement rate limiting on ThemePublishLegacy mutations to prevent rapid repeat attempts
- Add audit logging for all theme state changes and publish operations for forensic analysis
- Use optimistic locking with version numbers to prevent concurrent conflicting operations
- Perform purchase status verification at the GraphQL resolver level, not at the service layer
- Add CSRF tokens and additional authentication challenges for high-risk operations like paid theme publishing
- Implement feature flags to disable theme publication during installation state

## Variant hunting
Test other theme-related mutations (ThemeDelete, ThemeUpdate, ThemeRename) during installation window
Attempt to publish themes with conflicting IDs or invalid GIDs during installation
Test race conditions with multiple simultaneous publish requests for same theme
Try publishing themes during other state transitions (updating, duplicating, importing)
Test if theme customization APIs (edit liquid, modify settings) are similarly exploitable during installation
Check if the vulnerability applies to other theme operations like theme duplication or transfer
Attempt to trigger the vulnerability with API tokens instead of session cookies
Test if adding delays between requests can bypass timing-based mitigations
Check for similar race conditions in other Shopify store feature installations (apps, extensions)
Test if preview mode or draft themes have similar authorization bypass windows

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1548 - Abuse Elevation Control Mechanism
- T1110 - Brute Force (timing-based exploitation)
- T1578 - Modify Cloud Compute Infrastructure (theme modification)
- T1537 - Transfer Data to Cloud Account (theme file exfiltration)
- T1199 - Trusted Relationship (abusing Shopify platform trust)

## Notes
This is a follow-up to report #927567, indicating a pattern of authorization bypass vulnerabilities in Shopify's theme system. The exploit requires precise timing and manual intervention, making it more difficult than simple authorization flaws but still reliably exploitable. The POC video referenced demonstrates successful exploitation. The attacker correctly notes that timing optimization could fully automate this attack. The vulnerability affects business logic at a critical revenue point (theme sales), making it high-impact. Shopify should prioritize patching this with comprehensive state machine validation.

## Full report
<details><summary>Expand</summary>

Hi,

##Description
I kept looking for alternatives to my report #927567 and I found another way to publish a paid theme without having to purchase it. This time the trick is to send "*ThemePublishLegacy*"  XHR request while the theme is being installed.

##Requirements
1. Google Chrome suggested because that's what I use to describe my steps

##Steps to reproduce
1. Make sure you have the default theme installed and that it is published
2. Install any free theme
3. Publish the free theme you just installed
4. From your developper tool, copy the `ThemePublishLegacy` XHR request as fetch and paste it in your developper tool console and keep it for later.

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

5. Now, in a new tab, visit https://themes.shopify.com/ and **leave the admin/themes tab open**
6. Choose any paid theme, which should bring you to the selected theme page (e.g. https://themes.shopify.com/themes/mr-parker)
7. Click the "**Try theme**" button to launch the installation
 7.1 **From here, the next steps have to be done as fast as you can, before the theme gets fully installed**
8. Quickly go back  to the **admin/themes** tab you left open at ***step #5*** and refresh the page (your developper tool should still be active for that tab).
 8.1 Once the page is reloaded, you should see in the "*Theme library*" section that the theme is being installed (a spinner animation is shown)
9. Now in your developper tool, open the XHR tab and select the first graphql request that is made to `ThemesProcessingLegacy`
10. Once its selected, open the response preview tab and l look for `data > onlineStore > themes > edges > [0] > node > id`
 11.1 The ID of the theme being installed is the one at the first index
12. Copy the theme ID `gid://shopify/OnlineStoreTheme/[THEME_ID]`
13. Go back to your developper tool console and in the request you saved at ***step #4***, replace the theme ID with the one you just copied at ***step #11*** and send the request (**before the theme installation is complete!**)
14. Once the theme installation is complete, refresh the page and you will see that the paid theme is now publish.

I will be attaching a POC video with this report. You will see in the video that the first time I sent the request, it did not work because of an error (***Role can't be set to main: missing required file layout/theme.liquid***). I believe this attack has to be timed at the right moment for it to work all the time. It seems like for this to work properly, the `ThemePublishLegacy` request should be sent right before the installation is complete, just before the last `ThemesProcessingLegacy` request is made. This could probably be improved and automated with a script.

Also, again, after the theme is published, it seems like we own it. So, at this point, if you publish another theme (the free one), you should see that the the yellow "Theme trial" badge is missing and that you can rename, edit and download the theme files.

## Impact

Ability to install paid theme without purchasing it could lead to content stealing and lost of profit. There is also some unwanted information disclosure since we can edit the theme code and download the files after its published.

If you need extra details, please let me know!

Thank you!

</details>

---
*Analysed by Claude on 2026-05-24*
