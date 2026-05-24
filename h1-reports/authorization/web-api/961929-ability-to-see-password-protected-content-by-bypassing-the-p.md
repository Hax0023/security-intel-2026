# Password Protection Bypass on Shopify Development Store Preview URLs via Token Reuse

## Metadata
- **Source:** HackerOne
- **Report:** 961929 | https://hackerone.com/reports/961929
- **Submitted:** 2020-08-18
- **Reporter:** saltymermaid
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** Medium
- **Vuln:** Authentication Bypass, Information Disclosure, Improper Access Control, Token Reuse Vulnerability
- **CVEs:** None
- **Category:** web-api

## Summary
A vulnerability in Shopify's development store password protection mechanism allows attackers to bypass the password-protected preview page by reusing the `_bt` authentication token from one development store to access another newly created development store (post-August 17, 2020). By copying the `_bt` query parameter from an authorized preview link and appending it to another development store's preview URL, an attacker can gain unauthorized access to password-protected store content without entering the correct password.

## Attack scenario
1. Attacker obtains a preview URL from one development store they have authorized access to
2. Attacker extracts the `_bt=<token>` query parameter from that URL
3. Attacker obtains a preview URL for a different development store (without the password)
4. Attacker appends the copied `_bt` token to the target store's preview URL
5. Attacker accesses the target store's preview page without entering the password
6. Attacker gains unauthorized access to sensitive store content and information

## Root cause
The authentication token (`_bt`) is not properly scoped to individual development stores. The token validation mechanism fails to verify that the token belongs to the specific store being accessed, instead treating the token as globally valid across different development stores. This indicates insufficient token binding or store-level access control validation.

## Attacker mindset
An opportunistic attacker with access to any legitimate preview URL could exploit this to access other development stores they shouldn't have permission to view. The attack requires minimal technical skill and only knowledge of URL manipulation. The motivation would be to gather competitive intelligence, view unreleased products, or access sensitive business information from development stores.

## Defensive takeaways
- Implement store-specific token binding - ensure authentication tokens are scoped to and validated against the specific store instance
- Use cryptographic binding between tokens and resources to prevent cross-store token reuse
- Validate not only token validity but also token ownership/association with the requested resource
- Implement rate limiting and anomaly detection for authentication attempts across different stores
- Add logging and monitoring for token reuse patterns across different store instances
- Consider using short-lived tokens with refresh mechanisms rather than long-lived tokens
- Implement additional context validation (IP, user agent, etc.) as secondary authentication factors
- Conduct security audit of all development store authentication mechanisms post-August 17, 2020

## Variant hunting
Check if other Shopify query parameters are similarly vulnerable to cross-store reuse
Test if the vulnerability extends to non-preview URLs or admin access tokens
Investigate if other Shopify partner features (custom apps, theme previews) have similar token binding issues
Examine whether the `_bt` token has expiration and if expired tokens are still accepted
Test if combining valid `_bt` tokens from multiple stores provides elevated access
Check if the vulnerability affects stores on different plans (trial, paid, development)
Investigate Shopify App Store and Theme Store demo links for similar token reuse vulnerabilities

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1556 - Modify Authentication Process
- T1110 - Brute Force (credential stuffing with tokens)
- T1078 - Valid Accounts (using valid but misscoped tokens)

## Notes
The report demonstrates good security research methodology by including proof-of-concept steps and referencing Shopify's official documentation. The vulnerability is particularly concerning for development stores as they may contain unreleased products, pricing information, and business strategies. The fact that this affects only 'newly created' development stores (post-August 17, 2020) suggests Shopify implemented new security measures that inadvertently introduced this token binding flaw. The low barrier to exploitation (simple URL manipulation) increases the practical risk despite the 'unlikely' scenario the researcher described.

## Full report
<details><summary>Expand</summary>

Hi,

## Description
I have found a way to bypass the password page of a shopify preview URL for new development stores created  as of August 17, 2020. Currenty, with older development stores, when we share a preview url with someone, we are able to see the content of the store without having to enter a password even if the password protectection is on. For newly created development stores, if you share a preview url with someone, you are asked to enter a password before you can go any further, so I believe that as of august 17, 2020, when sharing a preview url of a development store, we also have to provide the store password for someone to preview the content. 

As cited in https://help.shopify.com/en/partners/dashboard/managing-stores/development-stores#the-development-store-password-page :

```
 All newly created development stores are password protected. This means that visitors to development stores can access your development store in the following ways only:

    1. By entering a password on the development store password page
    2. By logging into the development store's admin
    3. Through a Shopify Theme Store or Shopify App Store demo link
       Unlike the customizable password page for a store that's on a free trial or paid plan, the development store password page isn't linked to the online 
       store's theme and can't be customized.

 You can remove the password page only after you transfer the store to a merchant or switch the store to a paid plan.
```

## Steps to reproduce
1. Create a new development store that meets the new standard (August 17, 2020)
2. Go to `Sales channels > Online Store > Themes`
3. At the top of the page, under the **Themes** title, click the **View your store** link button
4. Look at the url in the address bar and copy the `?_bt=<some-long-token>` query parameter
5. Open a preview url that was generated from another store and that also meets the new standard (August 17, 2020).
6. Paste the `?_bt=<some-long-token>` query parameter you copied from step #4 at the end of the preview url in the address bar and send it
7. You should have bypassed the password authentication and be able to see the store content

I will be attaching a POC video, but if you need extra details just let me know.

## Impact

Even if unlikely to happen, if someone had the preview url in hand, but did not have the store password, this method could be used to bypass the password authentication and have access to the store content. This would lead to information disclosure.

</details>

---
*Analysed by Claude on 2026-05-24*
