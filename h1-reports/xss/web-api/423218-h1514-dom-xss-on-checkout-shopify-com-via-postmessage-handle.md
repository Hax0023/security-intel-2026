# DOM XSS on checkout.shopify.com via postMessage handler on /:id/sandbox/google_maps

## Metadata
- **Source:** HackerOne
- **Report:** 423218 | https://hackerone.com/reports/423218
- **Submitted:** 2018-10-13
- **Reporter:** bored-engineer
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Cross-Site Scripting (XSS), Insecure postMessage Communication, Insufficient Input Validation
- **CVEs:** None
- **Category:** web-api

## Summary
The /:id/sandbox/google_maps and /:id/sandbox/google_autocomplete routes on checkout.shopify.com perform origin validation on postMessages but fail to sanitize the message payload, allowing a malicious shop to inject arbitrary HTML/JavaScript that executes in the checkout context. An attacker can inject XSS payloads through map marker titles that execute with checkout.shopify.com privileges.

## Attack scenario
1. Attacker creates or compromises a Shopify shop and obtains its ID
2. Attacker injects malicious JavaScript into the shop's template/theme code
3. When a user visits the compromised shop, the injected script creates an iframe pointing to checkout.shopify.com/[shop-id]/sandbox/google_maps
4. Once the iframe loads, the attacker sends a postMessage containing XSS payload in the marker title field (e.g., img tag with onerror handler)
5. The sandbox endpoint receives and processes the postMessage after validating the origin matches the shop ID
6. The payload is rendered as HTML in the map marker, executing JavaScript in the checkout.shopify.com context

## Root cause
The application validates the origin of postMessages but does not sanitize or validate the message payload content. The marker title parameter is directly rendered as HTML without escaping, allowing XSS injection through the postMessage communication channel.

## Attacker mindset
An attacker with shop access recognizes that postMessage communication between frames bypasses same-origin policy and identifies that origin validation alone is insufficient. They realize that trusting validated origins implies trusting the message content, leading them to inject XSS payloads through data fields.

## Defensive takeaways
- Always sanitize and validate message payloads separately from origin validation in postMessage handlers
- Use HTML escaping/encoding for all user-controlled data rendered in the DOM, especially in cross-origin contexts
- Implement Content Security Policy (CSP) to restrict inline script execution
- Use postMessage with specific target origins instead of '*' wildcard
- Apply allowlist validation to all structured data in postMessages, not just origin checks
- Consider using safer DOM APIs like textContent instead of innerHTML for dynamic content
- Implement defense-in-depth: validate both origin AND payload structure/content

## Variant hunting
Search for other postMessage handlers on checkout.shopify.com that validate origin but trust payload
Review all sandbox iframe endpoints (/:id/sandbox/*) for similar patterns
Audit Google Autocomplete implementation for similar XSS vectors
Check for other marker/label fields in the createMapAndMarkers payload
Test with different HTML injection vectors beyond img onerror (svg, iframe, script tags)
Investigate if the vulnerability extends to other Shopify domains with similar patterns

## MITRE ATT&CK
- T1190
- T1499
- T1566

## Notes
This vulnerability combines weak validation (origin-only check) with unsafe HTML rendering. The shop ID in the URL provides a false sense of security - it validates the source but not the content. The use of wildcard target origin in postMessage further increases risk. This is a classic example of incomplete security boundary enforcement in cross-origin communication.

## Full report
<details><summary>Expand</summary>

# Description:
The `/:id/sandbox/google_maps` and `/:id/sandbox/google_autocomplete` routes on `checkout.shopify.com` are used to render the Google Map on the "Order Status" page as well as the address prediction on checkout pages. The page performs origin validation on incoming postMessages making sure the origin matches the shop associated with `:id` but then trusts all communication after that validation. A malicious shop can render a Google Map (on checkout.shopify.com) with arbitrary HTML injected as a label which executes on checkout.shopify.com

# Technical Details:
Create a shop, capture it's ID (`4736483384` in this case). Then add the following script to the shop template:
```js
var frame = document.createElement("iframe");
frame.src = "https://checkout.shopify.com/4736483384/sandbox/google_maps";
frame.onload = function() {
  frame.contentWindow.postMessage("shopify_google_api:" + JSON.stringify({
    action: "createMapAndMarkers", 
    body: [{
      title: "<img src=xx: onerror=alert(document.domain)>"
    }]
  }), "*");
}
document.body.appendChild(frame);
```

# Steps To Reproduce:
Open [bored-engineering-whitehat-2.myshopify.com/#pwn](https://bored-engineering-whitehat-2.myshopify.com/#pwn), wait for the popup.

## Impact

XSS on checkout.shopify.com which hosts maps and other information for order statuses and cart checkouts.

</details>

---
*Analysed by Claude on 2026-05-12*
