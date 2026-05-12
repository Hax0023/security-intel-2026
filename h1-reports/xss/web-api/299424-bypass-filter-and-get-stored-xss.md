# Bypass Filter and Stored XSS via XML Entity in Sales Channel Navigation Icon

## Metadata
- **Source:** HackerOne
- **Report:** 299424 | https://hackerone.com/reports/299424
- **Submitted:** 2017-12-19
- **Reporter:** dr_dragon
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Stored XSS, Input Validation Bypass, Filter Evasion
- **CVEs:** None
- **Category:** web-api

## Summary
Shopify's SVG whitelist validation for Sales Channel navigation icons can be bypassed by including XML entities, allowing attackers to inject malicious JavaScript attributes like onload. This stored XSS affects both partners.shopify.com and shop admin panels of any authorized sales channel.

## Attack scenario
1. Attacker creates a new application in the Shopify Partners dashboard
2. Attacker converts the application to a Sales Channel type
3. Attacker navigates to 'App info' section and accesses 'Navigation icon' upload field
4. Attacker uploads malicious SVG containing XML entity with embedded script (e.g., '<svg><!--?php "--><script>confirm(20)</script>?&gt;</svg>')
5. SVG whitelist filter is bypassed due to XML entity presence, allowing malicious attributes to persist
6. Stored XSS executes when partners or shop admins view the application, stealing session tokens or cookies

## Root cause
The SVG validation whitelist only enforces element and attribute restrictions when XML entities are absent. When XML entities are present in the SVG, the whitelist validation logic is skipped entirely, allowing arbitrary HTML/JavaScript injection to bypass content security controls.

## Attacker mindset
An opportunistic developer or third-party attacker who discovers that SVG validation has a simple bypass condition (presence of XML entities). The low barrier to exploitation (just add a comment with entity syntax) combined with high impact (XSS on trusted domains) makes this an attractive target.

## Defensive takeaways
- Never use blacklist/whitelist filters as sole protection against markup injection; they are inherently bypassable
- Parse and normalize all markup (SVG, HTML, XML) before applying validation rules to prevent bypass techniques
- Use robust SVG parsing libraries that handle entity resolution consistently before whitelist checks
- Implement defense-in-depth with Content Security Policy headers to mitigate XSS impact even if filters fail
- Sanitize SVG output using dedicated libraries (e.g., DOMPurify) rather than custom regex-based filters
- Test security controls with entity encoding, CDATA sections, and other encoding bypass techniques
- Apply the same validation rules regardless of XML entity presence or other structural variations

## Variant hunting
Test other file upload fields accepting SVG with XML entities and CDATA sections
Check if other Shopify features (themes, apps, custom storefronts) have similar SVG validation bypasses
Investigate whether HTML/XML parsing differences in backend vs frontend create validation gaps
Test combinations of XML features: DOCTYPE declarations, external entities, namespace declarations
Review other user-controlled markup fields (rich text editors, custom HTML blocks) for similar validation bypass patterns

## MITRE ATT&CK
- T1190
- T1598
- T1566

## Notes
This vulnerability demonstrates a classic security pattern: conditional logic in validation that can be exploited by manipulating input structure. The presence of XML entities should trigger identical validation rules, not disable them. The high impact stems from the trusted context (Shopify Partners dashboard and shop admin panels) where XSS can compromise merchant and partner accounts at scale.

## Full report
<details><summary>Expand</summary>

# Description

Shopify allows developers to create a special type of application called a "Sales Channel". Developers are allowed to upload a 16x16 SVG "Navigation Icon" for their app provided the SVG follows the design guidelines which limits the allowed elements and attributes. For some reason when the SVG contains an XML entity this whitelist is no longer enforced allowing the developer to include malicious attributes such as onload. By uploading a malicious SVG a developer can obtain XSS on both partners.shopify.com, as well as any the admin panel of any shop which has authorized the sales channel.

# Proof of Concept

This is relatively easy to reproduce, first create a new application within the Partners dashboard then navigate to "Extensions" -> "Sales channel" to convert the application. After saving those changes a new field within the "App info" section titled "Navigation icon". Upload the following SVG:

```
<svg><!--?php "--><script>confirm(20)</script>?&gt;</svg>
```

## Impact

An attacker can use XSS to send a malicious script to an unsuspecting user. The end user’s browser has no way to know that the script should not be trusted, and will execute the script. Because it thinks the script came from a trusted source, the malicious script can access any cookies, session tokens, or other sensitive information retained by the browser and used with that site. These scripts can even rewrite the content of the HTML page. For more details on the different types of XSS flaws

</details>

---
*Analysed by Claude on 2026-05-12*
