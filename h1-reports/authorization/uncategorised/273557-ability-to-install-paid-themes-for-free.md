# Ability to Install Paid Themes for Free on themes.shopify.io

## Metadata
- **Source:** HackerOne
- **Report:** 273557 | https://hackerone.com/reports/273557
- **Submitted:** 2017-10-01
- **Reporter:** flashdisk
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Access Control Flaw, Payment Bypass, Insufficient Authorization, Testing Environment Exposure
- **CVEs:** None
- **Category:** uncategorised

## Summary
A subdomain themes.shopify.io intended for testing purposes was publicly accessible without proper access controls, allowing authenticated users to install and download paid themes without completing payment. Users could also modify and republish these themes, enabling intellectual property theft and revenue loss.

## Attack scenario
1. Attacker navigates to https://themes.shopify.io and logs in with valid Shopify credentials
2. Attacker selects a premium/paid theme from the marketplace
3. Attacker clicks 'buy theme' button which initiates a charge approval workflow
4. System displays charge approval screen but does not validate actual payment processing
5. Attacker clicks 'approve charge' button which installs theme without payment verification
6. Attacker gains access to theme files, downloads them, modifies content, and republishes as own creation

## Root cause
The testing subdomain (themes.shopify.io) was deployed with production-like functionality but lacked proper authorization checks for payment-gated features. The application trusted the charge approval workflow without validating actual payment completion or enforcing access controls to restrict this endpoint to internal testing only.

## Attacker mindset
An attacker seeking to bypass payment systems and acquire premium digital assets for free. The ability to modify and redistribute paid themes represents both financial loss and intellectual property theft, motivating attackers to exploit this for resale or commercial use.

## Defensive takeaways
- Never expose testing/staging environments on public-facing subdomains without authentication or network isolation
- Implement authorization checks that verify payment completion before granting access to paid content
- Separate testing infrastructure from production using distinct domains, VPCs, and access control policies
- Use feature flags or environment variables to disable payment-gated functionality in non-production environments
- Implement payment gateway validation callbacks that must succeed before content delivery
- Regularly audit public subdomains and DNS records to identify unintended exposures
- Restrict subdomain access through IP whitelisting or VPN requirements for internal-only services

## Variant hunting
Look for similar payment bypass patterns on other Shopify subdomains (apps.shopify.io, api.shopify.io). Check for other digital goods platforms with exposed staging environments. Search for charge/payment approval flows that lack backend validation. Investigate other theme marketplaces for authorization flaws in download/install endpoints.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1543 - Create or Modify System Process
- T1552 - Unsecured Credentials
- T1078 - Valid Accounts

## Notes
Report quality is moderate - lacks technical depth on how the charge approval mechanism was bypassed. No evidence of payment transaction logs or backend validation failures. Researcher suggests limiting access rather than analyzing the root cause of payment bypass. The vulnerability appears to be improper access control on a testing environment rather than a sophisticated payment gateway bypass.

## Full report
<details><summary>Expand</summary>

Hi,

#Discription
while searching for access control issues on shopify I noticed a subdomain of shopify https://themes.shopify.io which gave me the opportunity to install and download paid 
themes for free.

#POC

1. go to https://themes.shopify.io/login and login
2. select one of the paid themes and press on ``buy theme`` button
3. you will be facing this screen on your shop:
 {F225469}
4. press on ``apporve charge`` button and the theme will be installed after getting to this screen:
{F225470}

#IMPACT

any user can download any paid themes and also can save them and modify them to upload them again 

#FIX

you should limit the access to  https://themes.shopify.io/ since it is for testing only.

thanks.

</details>

---
*Analysed by Claude on 2026-05-24*
