# XSS on widgets.shopifyapps.com via stripping Attribute Bypass and shop Parameter

## Metadata
- **Source:** HackerOne
- **Report:** 246794 | https://hackerone.com/reports/246794
- **Submitted:** 2017-07-07
- **Reporter:** bored-engineer
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Cross-Site Scripting (XSS), Improper Input Validation, Logic Error in Security Control
- **CVEs:** None
- **Category:** web-api

## Summary
Shopify's widget embedding service fails to properly validate the 'shop' parameter and contains a critical logic flaw in its HTML escaping mechanism. An attacker can craft a malicious JSON response with a 'stripping' attribute set to false, which disables HTML sanitization and allows arbitrary JavaScript execution on widgets.shopifyapps.com.

## Attack scenario
1. Attacker registers or controls a domain (e.g., attackerdoma.in)
2. Attacker hosts malicious JSON files at that domain containing a 'stripping: false' attribute within product variant data
3. Attacker crafts a URL to widgets.shopifyapps.com/products/[product]?shop=attackerdoma.in pointing to the malicious domain
4. Attacker sends the URL to victims or embeds it in a phishing page
5. When the URL is accessed, the widget application fetches product data from the attacker's server
6. The parse method processes the JSON, skips HTML escaping due to the stripping flag, and executes injected JavaScript in the victim's browser

## Root cause
The stripHTMLForObject function checks for the presence of a 'stripping' attribute to prevent recursive escaping, but this same attribute is also used as a control flag to disable escaping entirely. An attacker-controlled data source can inject 'stripping: false' into objects to bypass the escaping logic. Additionally, the 'shop' parameter is not validated to ensure it points to a legitimate Shopify store.

## Attacker mindset
An attacker recognized that a security function intended to prevent double-escaping could be abused as a kill switch for all escaping. By controlling the data source via an unvalidated 'shop' parameter, they could inject the stripping attribute and achieve code execution. This demonstrates thinking about how security flags can become security vulnerabilities if controlled by untrusted input.

## Defensive takeaways
- Never allow user-supplied data to control security features or bypass mechanisms; use internal-only flags for recursion prevention
- Validate the 'shop' parameter against a whitelist of legitimate Shopify stores rather than accepting arbitrary domains
- Implement Content Security Policy (CSP) headers to limit impact of XSS vulnerabilities
- Use a separate internal mechanism (e.g., WeakMap or Symbol) for recursion detection instead of object properties
- Apply HTML escaping at the point of rendering, not just during parsing, as a defense-in-depth measure
- Sanitize all data from external sources regardless of whether it claims to be pre-escaped

## Variant hunting
Search for similar recursive object processing functions that use object properties as control flags. Look for HTML escaping functions that check for attribute presence before sanitization. Examine other Shopify embed/widget services that accept external domain parameters. Review code that uses 'stripping', 'noEscape', 'raw', or similar flags that can be influenced by remote data.

## MITRE ATT&CK
- T1190
- T1598
- T1566

## Notes
This is a sophisticated logic error combining two separate flaws: (1) an unvalidated 'shop' parameter that allows pointing to arbitrary domains, and (2) a recursive escaping function with a bypass condition controllable by remote data. The vulnerability requires no user interaction beyond visiting a URL, making it particularly severe for embedded widgets that may be accessed across many websites.

## Full report
<details><summary>Expand</summary>

# Description
Shopify allows developers to embed widgets (containing product info) on third-party websites via "widgets.shopifyapps.com". When the widget is rendered the `shop` attribute is not filtered allowing any website (not just Shopify shops) to be specified. By providing an attacker controlled domain and serving a specially crafted payload containing the `stripping` object attribute HTML escaping will be disabled resulting in XSS on "widgets.shopifyapps.com".

# Technical Details
This issue occurs in [/assets/widgets/product/application.js](https://widgets.shopifyapps.com/assets/widgets/product/application.js). The `Framework.Models.Collection` class (used for fetching collections of objects) defines a special `parse` method which automatically escapes all strings. This escaping is provided by `Framework.Helpers.stripHTMLForObject` which looks like this (prettified):
```js
Framework.Helpers.stripHTMLForObject = function(obj) {
  obj.stripping = true;
  var idx, val;
  for (idx in obj) {
    if (obj.hasOwnProperty(idx)) {
      var val = obj[inx]
      if("string" == typeof val) {
        obj[idx] = Framework.Helpers.stripHTML(val) 
      } else {
        if(null != val && "object" == typeof val && null == val.stripping) {
          obj[idx] = this.stripHTMLForObject(val)
        }
     }
   }
   delete obj.stripping;
   return obj;
}
``` 
The `Framework.Helpers.stripHTML` function seems to be a implementation of the [Caja compiler](https://developers.google.com/caja/) which we can assume is safe, however by crafting a object with a `stripping` attribute HTML escaping will be disabled. An example product would look like this:
```json
{
	"product": {
		"variants": [{
			"stripping": false,
			"title": "<option/><select/><img src=xx: onerror=alert('bored-engineer')>"
		}, {}],
		"options": [],
		"images": [{}],
		"image": {}
	}
}
```
I've hosted this file (and the other required `meta.json` file) on [attackerdoma.in](https://attackerdoma.in).

# Proof of Concept
Open [widgets.shopifyapps.com/products/stripping-xss?shop=attackerdoma.in](https://widgets.shopifyapps.com/products/stripping-xss?shop=attackerdoma.in)

# Exploitability
Once you locate the escaping issue it's relatively trivial to exploit and requires to user interaction as shown in the PoC.

# Remediation
The application should not allow shops/servers to disable HTML escaping via the `stripping` attribute.

</details>

---
*Analysed by Claude on 2026-05-12*
