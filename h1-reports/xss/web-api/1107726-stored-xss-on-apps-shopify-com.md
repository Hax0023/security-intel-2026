# Stored XSS on apps.shopify.com via Store Contact Email

## Metadata
- **Source:** HackerOne
- **Report:** 1107726 | https://hackerone.com/reports/1107726
- **Submitted:** 2021-02-20
- **Reporter:** luc1d
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Stored Cross-Site Scripting (XSS), Improper Input Validation, Insufficient Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A stored XSS vulnerability exists on apps.shopify.com where malicious JavaScript payload injected into the Store contact email field in General Settings is reflected without proper sanitization. The payload executes in the context of apps.shopify.com when users click 'Get support' on app pages, allowing attackers to steal sensitive information or perform actions on behalf of users.

## Attack scenario
1. Attacker gains access to a Shopify store's admin panel (via phishing, credential theft, or compromised account)
2. Attacker navigates to Settings > General and modifies the Store contact email field with XSS payload: luc1d"><img/src="x"onerror=alert(document.domain)>@wearehackerone.com
3. Attacker saves changes; payload is stored in Shopify's database without sanitization
4. After ~60 minutes, the malicious payload propagates to apps.shopify.com infrastructure
5. Any user visiting an app page on apps.shopify.com and clicking 'Get support' triggers the stored XSS
6. Attacker's JavaScript executes in victim's browser with access to apps.shopify.com domain, enabling session hijacking or malicious actions

## Root cause
The Store contact email field accepts and stores user input without proper input validation or output encoding. When this data is rendered on apps.shopify.com, no Content Security Policy or HTML escaping is applied, allowing injected HTML/JavaScript to execute in the victim's browser.

## Attacker mindset
An attacker with admin access (or who obtained compromised credentials) seeks to escalate impact by injecting persistent malicious code that affects visitors to the public app marketplace. The 60-minute delay suggests cache synchronization between systems, which the attacker must account for in their attack timeline.

## Defensive takeaways
- Implement strict input validation on email fields - reject or sanitize payloads containing HTML/JavaScript special characters
- Apply output encoding (HTML entity encoding) when rendering user-supplied data in web pages
- Deploy Content Security Policy (CSP) headers to prevent inline script execution
- Use a security-focused templating engine that auto-escapes output by default
- Validate email format server-side using proper regex or email parsing libraries
- Implement comprehensive security testing for all user input fields, especially those visible across multiple domains
- Add WAF rules to detect and block common XSS patterns in email fields
- Conduct regular penetration testing of admin-controlled data that appears on public-facing sites

## Variant hunting
Test other email fields in Settings (billing contact, support contact, etc.) for similar XSS vulnerabilities
Attempt stored XSS via store name, store description, and other metadata fields that may propagate to apps.shopify.com
Check if other Shopify subdomains reflect the stored email data without proper encoding
Test for DOM-based XSS variants in JavaScript that processes the email field client-side
Investigate if cached versions of pages contain unescaped email data accessible via cache poisoning
Test SVG-based XSS vectors and other MIME type bypasses in email field

## MITRE ATT&CK
- T1190
- T1566.002
- T1583.006
- T1189
- T1598.002

## Notes
The 60-minute delay before payload execution indicates asynchronous data replication or cache warming. The vulnerability requires initial admin panel access, making it a post-exploitation vector or an account takeover amplifier. The public nature of apps.shopify.com means this affects all users visiting app support pages, making it particularly dangerous for widespread attack scenarios. The use of img tag with onerror handler bypasses basic email validation regex that may only check for @ symbol.

## Full report
<details><summary>Expand</summary>

Steps to reProduce:

1> Write payload `luc1d"><img/src="x"onerror=alert(document.domain)>@wearehackerone.com` as `Store contact email` in General Settings page`(*.myshopify.com/admin/settings/general)`

{F1202181}

-- Wait here around 60 mins (maybe more idk, it was 60 mins for me) for the change to reflect --
(You can confirm the change on here `https://apps.shopify.com/shops/<shopId>`)
2> Visit any app page like `https://apps.shopify.com/local-delivery`
3> Click `Get support` link on sidebar
{F1202116}

4> XSS will be triggered
{F1202211}

PoC Video,
{F1202215}

## Impact

Stored XSS

</details>

---
*Analysed by Claude on 2026-05-12*
