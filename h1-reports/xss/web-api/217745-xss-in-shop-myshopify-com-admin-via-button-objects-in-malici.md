# XSS in Shopify Admin via Unsanitized Button href in Embedded App SDK

## Metadata
- **Source:** HackerOne
- **Report:** 217745 | https://hackerone.com/reports/217745
- **Submitted:** 2017-04-02
- **Reporter:** bored-engineer
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Cross-Site Scripting (XSS), Improper Input Validation, JavaScript Protocol Handler Abuse
- **CVEs:** None
- **Category:** web-api

## Summary
The Shopify Embedded App SDK fails to sanitize the `href` parameter in button objects, allowing malicious apps to execute arbitrary JavaScript in the admin interface. When a button's href contains a `javascript:` URL, the opened window shares the document.domain property with the opener, enabling XSS attacks through window.opener access.

## Attack scenario
1. Attacker creates a malicious Shopify app with no special permissions required
2. Admin user authorizes the malicious app to install it in their shop
3. Malicious app renders a button using Shopify.API.Bar.initialize() or similar methods with a javascript: URL in the href parameter
4. Admin clicks the button in the embedded app interface
5. window.open() is called with the javascript: URL, creating an about:blank window that shares document.domain with the admin page
6. Attacker executes arbitrary JavaScript in the admin context via window.opener.eval(), potentially stealing session tokens or modifying shop data

## Root cause
The Shopify.EmbeddedAppButtons class does not sanitize or validate the `href` parameter before passing it to the Page.open() method, which wraps window.open(). The browser's document.domain property sharing between the about:blank window and opener allows cross-window script execution despite being in different browsing contexts.

## Attacker mindset
An attacker seeks to create a low-friction attack vector by leveraging the trust relationship between admin and installed apps. Since button clicks require user interaction and no special permissions are needed, adoption is easier. By exploiting document.domain sharing, the attacker bypasses the typical window.open() security model that isolates new windows.

## Defensive takeaways
- Validate and sanitize all href parameters in button objects - reject javascript:, data:, and vbscript: protocols
- Use allowlist-based URL validation (only allow http://, https://, and relative URLs)
- Implement Content Security Policy (CSP) headers to restrict javascript: protocol execution
- Consider using URL.parse() or similar APIs to ensure URLs are properly formed before passing to window.open()
- Apply the same sanitization logic across all SDK methods that accept button objects (Bar.initialize, Modal.open, etc.)
- Add security review process for SDK method parameters that accept user-supplied values
- Consider using a wrapper around window.open() that validates protocols before execution

## Variant hunting
Search for similar patterns in other SDK methods accepting button/link parameters: Shopify.API.Modal, Shopify.API.ResourcePicker, or any method with href/url/link parameters. Check for similar document.domain bypasses in other postMessage-based communication flows. Look for other protocol handlers (data:, vbscript:) that might bypass sanitization. Examine other Shopify SDK implementations for consistent sanitization across all button-rendering contexts.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1539 - Steal Web Session Cookie
- T1204.001 - User Execution: Malicious Link
- T1566.002 - Phishing: Spearphishing Link

## Notes
This report builds on #205701 with the additional requirement of user interaction. The javascript: protocol handler abuse combined with document.domain sharing is a critical insight into a bypass of window.open() security models. The vulnerability affects multiple SDK methods, indicating a systemic sanitization issue rather than an isolated bug. The attack requires app authorization but not specific permissions, lowering the barrier to exploitation. The researcher notes this is part of a class of related vulnerabilities in button object handling across the entire SDK.

## Full report
<details><summary>Expand</summary>

This report is similar in impact, exploitability and root-cause as report #205701 requiring an additional step of user-interaction. 

#Description
The Shopify [Embedded App SDK](https://help.shopify.com/api/sdks/merchant-apps/embedded-app-sdk) is used to facilitate limited interactions with parent page (`/admin/apps/$id`) from an embedded app within the shop admin interface. The SDK has multiple methods which accept a `buttons` parameter which is defined under the [button objects](https://help.shopify.com/api/sdks/shopify-apps/embedded-app-sdk/methods#button-objects) section of the SDK documentation. Buttons can define a `href` parameter which will open when the button is clicked. The `href` parameter is not properly sanitized allowing a malicious app to execute JavaScript in the context of the admin interface.

#Technical Details
When a button is clicked the `clickButton` method is called, the method is defined as follows:
```js
clickButton = function(_, data) {
  if ((data.loading || "undefined" == typeof data.loading && "app" === data.target) && Shopify.Loading.start(), href = data.href) {
    switch (data.target) {
      case "parent":
      case "shopify":
        Page.visit(href, {
          reload: true
        });
        break;
        case "app":
          break;
        default:
          Page.open(href)
    }
  }
}
```
If no `target` parameter is specified (and the application is already loaded) `Page.open` will be called. This method is defined like this:
```
Page.open = function() {
  return window.open.apply(window, arguments);
}
```
You would expect `window.open` is safe to call with untrusted URLs as it will open in a new window/tab however this is not the case. When `window.open` is called with a `javascript:` URL a new window/tab will be opened with the domainless `about:blank` location (or similar depending on the browser) however the `document.domain` property will be shared with the opener window. Because the documents share `document.domain` the new window will be able to access the opener window and trigger JavaScript execution. You can test this yourself like this:
```js
window.open("javascript:window.opener.alert('bored-engineer')")
```
In the context of Shopify this means an application can create a button that will trigger XSS on the admin interface when the button is clicked. The following script was used to demonstrate the issue:
```js
window.parent.postMessage(JSON.stringify({
  message: "Shopify.API.Bar.initialize",
  data: {
    buttons: {
      primary: {
        label: "Click here for XSS",
        href: "javascript:setTimeout('window.close()',1);window.opener.eval('alert(document.domain)');",
      }
    }
  }
}), "*");
```
I wanted to note that this needs to be fixed in the `Shopify.EmbeddedAppButtons` class since this issue affects all methods which render buttons. For example the following script will also trigger XSS using a different method:
```js
window.parent.postMessage(JSON.stringify({
  message: "Shopify.API.Modal.open",
  data: {
    src: "https://attackerdoma.in",
    buttons: {
      primary: {
        label: "Click here for XSS",
        href: "javascript:setTimeout('window.close()',1);window.opener.eval('alert(document.domain)');",
      }
    }
  }
}), "*");
```

#Exploitability
You need to convince an administrator to authorize your malicious application, however the exploit does not require any specific permissions to trigger so an admin may be more willing to authorize the application. Once the administrator has loaded the application it is likely they will click at least one of the multiple entry-points for buttons. 

#Proof of Concept
I've created an example malicious application associated with my partner account `shopify-whitehat-1@bored.engineer` to demonstrate the issue...
Open the following URL on on `$your-shop$.myshopify.com`:
```
/admin/oauth/authorize?client_id=18cc7056a1476994411e3d21971289a7&scope=read_products&redirect_uri=https://attackerdoma.in/1b61d988-374e-48c8-ae6a-6eb28a0f25de.html&state=nonce
```
After authorizing the application and click the "Click here for XSS" button in the upper-right corner. An alert should appear on the `/admin` window containing `document.domain`.

#Remediation
The application should sanitize the `href` parameter for all "button objects" either before creating the elements in the DOM, or in the `clickButton` method before calling `Page.open`. 


</details>

---
*Analysed by Claude on 2026-05-12*
