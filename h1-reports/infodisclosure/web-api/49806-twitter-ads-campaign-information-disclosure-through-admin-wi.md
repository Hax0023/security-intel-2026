# Twitter Ads Campaign information disclosure through admin without any authentication.

## Metadata
- **Source:** HackerOne
- **Report:** 49806 | https://hackerone.com/reports/49806
- **Submitted:** 2015-03-02
- **Reporter:** avicoder_
- **Program:** Unknown
- **Bounty:** $560
- **Severity:** unknown
- **Vuln:** Improper Authentication - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
Hi Twitter !!

I just wanted to report a major flaw which I found in https://ads.twitter.com , hoping it make twitter more secure and I am glad for being a part of it.

**Vulnerability Name**:  OWASP:A6 Sensitive data Exposure

**Vulnerable URL**: https://ads.twitter.com/admin/accounts_typeahead.json?query=*****

**Vulnerability Overview**: Information Disclosure without any *authenticatio

## Attack scenario
*(see original)*

## Root cause
*(see original)*

## Attacker mindset
*(see original)*

## Defensive takeaways
*(see original)*

## Variant hunting
*(see original)*

## MITRE ATT&CK
*(see original)*

## Notes
*(see original)*

## Full report
<details><summary>Expand</summary>

Hi Twitter !!

I just wanted to report a major flaw which I found in https://ads.twitter.com , hoping it make twitter more secure and I am glad for being a part of it.

**Vulnerability Name**:  OWASP:A6 Sensitive data Exposure

**Vulnerable URL**: https://ads.twitter.com/admin/accounts_typeahead.json?query=*****

**Vulnerability Overview**: Information Disclosure without any *authentication* .

**Proof of Concept:**
   - Log into twitter account first.
   - Go to this URL https://ads.twitter.com/admin/accounts_typeahead.json?query=avicoder
   - Change the query string to any other account or screen_name ex: *microsoft*
   - You can view all the information about the account associated with the  campaign.
   - Usually this information is only visible to members of campaign.
   - Look at user_name_info element in JSON POC which actually exposing the members associated with campaign. 

**I attached the json file when I query my account in private window..
Its gives me all information about members linked to the campaign without any need of being (admin,manager,analyst)**

I made this report short  unlike my previous reports but it is to the point.
Please revert back if more information is needed. 

*Happy to help*
#:)#
**avicoder**



</details>

---
*Analysed by Claude on 2026-05-24*
