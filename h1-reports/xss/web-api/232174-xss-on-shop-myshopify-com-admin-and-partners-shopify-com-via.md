# XSS via SVG XML Entity Injection in Sales Channel Navigation Icons

## Metadata
- **Source:** HackerOne
- **Report:** 232174 | https://hackerone.com/reports/232174
- **Submitted:** 2017-05-26
- **Reporter:** bored-engineer
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Cross-Site Scripting (XSS), XML Entity Injection, Input Validation Bypass, Whitelist Bypass
- **CVEs:** None
- **Category:** web-api

## Summary
Shopify's SVG whitelist validation for Sales Channel navigation icons could be bypassed by injecting XML entities, allowing developers to include malicious attributes like onload handlers. This resulted in XSS on both partners.shopify.com and shop admin panels ($shop$.myshopify.com/admin/) after authorization. The vulnerability required admin authorization of a malicious sales channel application but executed automatically without user interaction.

## Attack scenario
1. Attacker creates a malicious Sales Channel application in Shopify Partners dashboard
2. Attacker uploads a specially crafted SVG with XML entity declaration containing onload attribute to bypass whitelist validation
3. Attacker distributes OAuth authorization link to target shop administrators or waits for authorization
4. When administrator authorizes the malicious application, the SVG icon is loaded in their admin panel
5. XSS payload executes in the context of $shop$.myshopify.com/admin with admin privileges
6. Attacker can steal session tokens, modify shop settings, access sensitive data, or perform unauthorized actions

## Root cause
The SVG validation whitelist was not properly enforced when XML entities were present in the SVG file. The parser failed to handle entities correctly, allowing validators to be bypassed and arbitrary attributes to be injected into the final rendered SVG.

## Attacker mindset
Exploit the gap between whitelist validation logic and actual SVG rendering. Leverage XML features (entity declarations) to circumvent security controls. Target the supply chain by compromising a widely-used application type that gets loaded in privileged contexts (admin panels). Social engineering shop admins to authorize the malicious application.

## Defensive takeaways
- Implement entity-aware SVG validation that disables XML entity processing entirely (XXE prevention)
- Use dedicated SVG sanitization libraries rather than custom whitelist logic
- Validate SVG content after full parsing/rendering, not just structure validation
- Implement Content Security Policy (CSP) with strict inline script and event handler restrictions on SVG content
- Apply defense-in-depth: validate at upload time, re-validate at render time, and use sandboxing/iframe isolation for untrusted SVG content
- Regular security audits of file upload features with attention to markup languages (SVG, XML, HTML)
- Consider restricting SVG features to safe subset or converting to raster images for display

## Variant hunting
Check for similar whitelist bypasses in other image upload features (favicons, app logos, product images)
Test other XML-based file formats accepted by Shopify (XML feeds, API responses)
Investigate whether HTML entity encoding bypasses work similarly in other contexts
Search for XXE vulnerabilities in SVG processing across different admin/partner features
Test SVG processing in email contexts or exported documents
Check if similar bypass works in other file type validators using entity declarations

## MITRE ATT&CK
- T1190
- T1598
- T1566
- T1204

## Notes
This is a sophisticated bypass of security controls rather than a simple validation failure. The attacker must be registered as a Shopify partner but the barrier is low. The impact is significant since compromised sales channel apps execute in highly privileged contexts (shop admin panels). The vulnerability demonstrates the danger of custom security logic around markup languages without proper entity/encoding handling awareness. Shopify's design guideline restrictions showed intent to limit SVG functionality but implementation failed to properly enforce them.

## Full report
<details><summary>Expand</summary>

# Description
Shopify allows developers to create a special type of application called a "[Sales Channel](https://help.shopify.com/api/sdks/sales-channel-sdk)". Developers are allowed to upload a 16x16 SVG "Navigation Icon" for their app provided the SVG follows the [design guidelines](https://help.shopify.com/api/sdks/sales-channel-sdk/design-guidelines/checklist#navigation-icon) which limits the allowed elements and attributes. For some reason when the SVG contains an XML entity this whitelist is no longer enforced allowing the developer to include malicious attributes such as `onload`. By uploading a malicious SVG a developer can obtain XSS on both partners.shopify.com, as well as any the admin panel of any shop which has authorized the sales channel. 

# Proof of Concept
This is relatively easy to reproduce, first create a new application within the [Partners dashboard](https://partners.shopify.com) then navigate to "Extensions" -> "Sales channel" to convert the application. After saving those changes a new field within the "App info" section titled "Navigation icon". Upload the following SVG:
```xml
<?xml version="1.0" encoding="ISO-8859-1"?>
<!DOCTYPE svg [
    <!ENTITY elem "">
]>
<svg onload="alert(document.domain);" height="16" width="16">
  &elem;
</svg>
```
After saving changes the XSS payload will fire on [partners.shopify.com](https://partners.shopify.com). To fire the payload on `$shop$.myshopify.com/admin/` you'll need to authorize the application on your shop:
I've created an example malicious application associated with my partner account `shopify-whitehat-2+hackerone@bored.engineer` to help demonstrate the issue, you can authorize it by opening the following URL on `$your-shop$.myshopify.com`:
```
/admin/oauth/authorize?client_id=672a937d5eb24e10c756ea256c73bb8c&scope=read_products&redirect_uri=https://attackerdoma.in/93ba4bef-cff1-43b1-922d-0631bd387e2e.html&state=nonce
```
Immediately after authorizing the application (and all future admin panel loads) an alert should appear on the /admin window containing document.domain.

# Exploitability
This seems like a really odd issue, so it may good to see if there are other places this icon could surface (ex. the app store or internal admin panels) to full understand the impact. For the known exploitable use-case via OAuth authorization you do need to convince an administrator to authorize your malicious application, however the exploit does not require any specific permissions to trigger so an admin may be more willing to authorize the application. Once the administrator has loaded the application it will immediately fire without additional user-interaction. 

# Remediation
The application should not allow XML entities in uploaded SVGs (or at least fix the parsing so it handles them correctly).

</details>

---
*Analysed by Claude on 2026-05-12*
