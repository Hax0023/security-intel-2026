# URL Path Manipulation Enables Cache Poisoning of Amazon Affiliate Products in Shopify Linkpop

## Metadata
- **Source:** HackerOne
- **Report:** 1848940 | https://hackerone.com/reports/1848940
- **Submitted:** 2023-01-27
- **Reporter:** saltymermaid
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Cache Poisoning, Path Traversal, URL Manipulation, Insufficient Input Validation
- **CVEs:** None
- **Category:** uncategorised

## Summary
A cache poisoning vulnerability exists in Shopify Linkpop's Amazon product integration where attackers can craft URLs using path traversal sequences (/../) to poison the cache with attacker-controlled products. When victims attempt to add a legitimate Amazon product, they receive the attacker's product instead, allowing affiliate fraud and product spoofing attacks.

## Attack scenario
1. Attacker identifies two Amazon product IDs: a victim product and an attacker-controlled product
2. Attacker crafts a malicious URL using path traversal: https://amazon.ca/dp/[VICTIM-ID]/../[ATTACKER-ID]
3. Attacker adds this crafted URL to their Linkpop account, which resolves to the attacker's product and gets cached
4. Victim attempts to legitimately add the victim product (https://amazon.ca/dp/[VICTIM-ID]) to their Linkpop account
5. The system retrieves the cached entry, which incorrectly maps the victim product ID to the attacker's product
6. Victim's Linkpop page now displays and links to the attacker's Amazon product, generating attacker affiliate commissions

## Root cause
The regex or URL parsing logic fails to normalize or properly validate Amazon product URLs before caching. Path traversal sequences (/../) are not stripped or blocked, allowing the same product ID to resolve to different products depending on URL formatting. The cache key likely uses the unnormalized URL or insufficiently sanitized product ID.

## Attacker mindset
An affiliate fraud operator seeking to steal commissions by manipulating victims' product links. This is a sophisticated supply-chain attack targeting ecommerce influencers and content creators who may not notice their affiliate links have been poisoned.

## Defensive takeaways
- Normalize URLs before parsing (resolve /../ sequences, decode entities, standardize domains)
- Use canonical form of URLs as cache keys to prevent alternate representations mapping to different content
- Validate product IDs against authoritative sources after URL parsing to ensure retrieved product matches requested ID
- Implement cache validation: verify cache contents match the current request parameters before returning
- Add URL allowlist validation: reject URLs with path traversal sequences or suspicious patterns
- Log cache poisoning attempts and alert on mismatches between requested and cached product IDs
- Consider cache headers and TTLs to limit poisoning window duration

## Variant hunting
Test double-encoding: https://amazon.ca/dp/[VICTIM]/%2e%2e/[ATTACKER]
Test alternative path traversal: https://amazon.ca/dp/[VICTIM]/./[ATTACKER]
Test URL parameters: https://amazon.ca/dp/[VICTIM]?ref=[ATTACKER]
Test subdomain variations: https://amazon.ca.attacker.com/dp/[VICTIM]
Test protocol-relative URLs: //amazon.ca/dp/[VICTIM]/../[ATTACKER]
Test case variations: https://AMAZON.CA/dp/[VICTIM]/../[ATTACKER]
Test query string injection: https://amazon.ca/dp/[VICTIM]?id=[ATTACKER]
Test fragment injection: https://amazon.ca/dp/[VICTIM]#[ATTACKER]

## MITRE ATT&CK
- T1190
- T1566
- T1195
- T1021

## Notes
This is a follow-up to a previous report that patched domain redirect validation but missed the underlying URL normalization issue. The vulnerability demonstrates how partial security fixes can leave attack surface intact. Cache poisoning with path traversal is particularly dangerous because it's persistent and affects all subsequent users until cache expiration.

## Full report
<details><summary>Expand</summary>

# Summary
The fix in report ████████ seems to prevent correctly an attacker from redirecting the request to another domain which was the main issue, however, there is still a way for that attacker to "poison" the cache usin the Amazon domain. I believe the regex used to parse the url is the cause.

# Description
If an attacker uses a crafted link such as https://amazon.ca/dp/[VICTIM-PRODUCT-ID]/../[ATTACKER-PRODUCT-ID], anyone who will then try to use the "victim" product link https://amazon.ca/dp/[VICTIM-PRODUCT-ID] will be shown the attacker controlled product. This way works even better because when you click the link button on the victim's page, it will even redirect to the attacker's product.

# Steps to Reproduce
1. Have two Amazon products ID in hands (which haven't been cached yet)
 1.1. Attacker Product ID: `██████` (https://www.amazon.ca/dp/███)
 1.2. Victim Product ID: `████` (https://www.amazon.ca/dp/███████)

2. In your attacker's Linkpop account, add a new Amazon product using the following crafted link `https://amazon.ca/dp/[VICTIM-PRODUCT-ID]/../[ATTACKER-PRODUCT-ID]` and make sure to replace the placholders
 2.1. Based on the ID's in step \#1, you could use the following link `https://amazon.ca/dp/███/../████████`	

3. Now, in the victim's Linkpop account, try to add the following product https://www.amazon.ca/dp/█████████, which is the "victim" product ID from step \#1. At that point you should be faced with the attacker's product (███) instead of the victim's product (███s).

# Notes
You can test the POC with the IDs I've provided. I haven't used them and luckily they won't be in the cache yet. If they are, you should notice it when adding the product as it will resolve very quickly (< 1s). If it doesn't work you you will have to find new product IDs.

## Impact

An attacker is able to manipulate the caching system to its avantage by sending a crafted link which can trick victims to unintentionally link a spoofed Amazon product to their Linkpop accounts.

</details>

---
*Analysed by Claude on 2026-05-24*
