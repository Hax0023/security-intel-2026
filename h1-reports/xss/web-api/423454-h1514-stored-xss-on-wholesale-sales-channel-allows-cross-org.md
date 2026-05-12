# Stored XSS on Wholesale Sales Channel Enables Cross-Organization Data Leakage

## Metadata
- **Source:** HackerOne
- **Report:** 423454 | https://hackerone.com/reports/423454
- **Submitted:** 2018-10-13
- **Reporter:** cablej
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Stored Cross-Site Scripting (XSS), Improper Input Validation, Cross-Organization Authorization Bypass, Shared Domain Security Issue
- **CVEs:** None
- **Category:** web-api

## Summary
A stored XSS vulnerability in Shopify's Wholesale sales channel allows attackers to inject malicious payloads via CSV file name parameters. When the malicious price list is accessed, the XSS payload executes on the shared wholesale.shopifyapps.com domain, enabling cross-organization data leakage and unauthorized access to customer information across multiple shops.

## Attack scenario
1. Attacker gains access to a shop with Apps permission (e.g., via Shopify partners program with legitimate access to one store)
2. Attacker installs Wholesale integration and creates a legitimate price list with CSV import
3. Attacker intercepts the price list modification request and injects XSS payload into the csv_file_name parameter (e.g., sample-csv-sku.csv"-alert(document.domain)-")
4. Attacker shares the malicious price list link with or tricks the store owner into viewing it
5. When the owner accesses the modified price list, JavaScript executes in the shared wholesale.shopifyapps.com domain context
6. Attacker's payload can access wholesale data, customer information, and modify wholesale configurations across all shops the owner manages

## Root cause
The Wholesale application fails to properly sanitize and validate the csv_file_name parameter before storing and rendering it in HTML context. The shared domain (wholesale.shopifyapps.com) across multiple organizations compounds the impact, as XSS execution grants access to all shops associated with the authenticated user.

## Attacker mindset
A malicious partner or user with legitimate limited access to one shop exploits trust relationships and the Shopify partner ecosystem to escalate privileges. The attacker recognizes that stored XSS on a shared domain provides a persistence mechanism for cross-organization data theft without requiring ongoing social engineering.

## Defensive takeaways
- Implement strict input validation and sanitization for all file-related parameters, especially those displayed in HTML contexts
- Use parameterized templates and context-aware output encoding (HTML-encode, JavaScript-encode, URL-encode as appropriate)
- Implement Content Security Policy (CSP) headers to prevent inline script execution on shared domains
- Isolate organizations by subdomain or separate domains to prevent XSS on one organization's data from affecting others
- Apply the principle of least privilege: separate Wholesale session tokens and permissions by shop/organization
- Implement server-side file validation and restrict file names to expected formats
- Use security headers like X-Frame-Options and X-Content-Type-Options to prevent embedding attacks
- Conduct regular security reviews of shared infrastructure where multiple organizations operate on the same domain
- Implement audit logging for price list modifications and access attempts

## Variant hunting
Search for other file upload/import features in Shopify apps that may have similar csv_file_name, file_name, or document_name parameters vulnerable to stored XSS
Test other sales channels (Facebook, Pinterest, Amazon) for similar parameter injection vulnerabilities in file handling
Investigate other Shopify apps hosted on shared domains (*.shopifyapps.com) for XSS vectors affecting cross-app data leakage
Review inventory import, product feed, and bulk operation features for stored XSS in file metadata fields
Test for similar vulnerabilities in customer list imports, order exports, and analytics report generation features

## MITRE ATT&CK
- T1190
- T1566.002
- T1199
- T1598.003
- T1083
- T1087.001

## Notes
The vulnerability is particularly severe due to the multi-tenant nature of the wholesale.shopifyapps.com domain. The attacker only needs Apps permission on one shop (achievable through legitimate partner relationships) to compromise multiple shops. The CSV import workflow is a common attack vector; similar vulnerabilities likely exist in other import features. The lack of organization isolation at the domain level is a systemic issue affecting all shared-domain Shopify integrations.

## Full report
<details><summary>Expand</summary>

**Summary:**

There exists a stored XSS vulnerability via the Wholesale sales channel at https://wholesale.shopifyapps.com. This allows an attacker who shares one shop with an account owner to access the Wholesale sales channel of any shop belonging to the owner.

## Steps To Reproduce:

  1. Visit https://wholesale.shopifyapps.com and add the Wholesale integration to your account.
  1. Navigate to the Wholesale sales channel at https://your-store.myshopify.com/admin/apps/wholesale.
  1. Navigate to create a new price list import.
  1. Modify the sample CSV file at https://help.shopify.com/manual/sell-online/wholesale/channel/price-lists-customers/import-prices/sample-csv-sku.csv to include the SKU of one of your shop's products.
  1. Upload the CSV file.
  1. After creating the price list, modify the price list and intercept the request to `POST /admin/shops/x/price_lists/x`.
  1. Modify the `price_list[csv_file_name]` parameter to include an XSS payload, such as `sample-csv-sku.csv"-alert(document.domain)-"`.
  1. Navigate back to the newly created price list. Observe that when visiting the page, the XSS payload will fire on the embedded domain `https://wholesale.shopifyapps.com`:

    {F360186}

  1. As this domain is shared across shops, this can be exploited to access the Wholesale information of any store a user has access to.

## Impact

An attacker with the `Apps` permission who shares one shop with an owner of multiple stores (e.g. via Shopify partners) can exploit this vulnerability to gain access to the Wholesale sales channel of any shop belonging to the owner.

As stated when authenticating with Wholesale:

> Wholesale will be able to access data such as customer names, e-mail addresses, phone numbers, physical addresses, geolocations, IP addresses, and browser user agents.

As a result, this allows access to extensive customer information, as well as the ability to modify any Wholesale information.

</details>

---
*Analysed by Claude on 2026-05-12*
