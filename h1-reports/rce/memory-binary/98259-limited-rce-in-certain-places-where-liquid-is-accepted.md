# Limited RCE via Liquid Template Injection in Notification Email Templates and Checkout Pages

## Metadata
- **Source:** HackerOne
- **Report:** 98259 | https://hackerone.com/reports/98259
- **Submitted:** 2015-11-06
- **Reporter:** brakhane
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Template Injection, Information Disclosure, Unsafe Deserialization, Improper Access Control
- **CVEs:** None
- **Category:** memory-binary

## Summary
Liquid template processing in Shopify's notification email templates and checkout thank you pages insufficiently restricts access to Drop object methods and properties, allowing privileged users to call arbitrary instance methods without arguments and read sensitive data via to_yaml serialization. While full RCE was not achieved, attackers can access hidden fields including password hashes and call dangerous methods like systemu, real_call, instance_eval, and instance_exec.

## Attack scenario
1. Attacker gains admin/shop owner access to Shopify store
2. Attacker navigates to Notification settings and edits an email template (New Order, etc.)
3. Attacker injects Liquid code like {{ to_yaml }}, {{ methods }}, {{ class }}, {{ systemu }} into template
4. Attacker clicks Preview button to execute injected code and observe sensitive data output
5. Attacker modifies customer email address to attacker-controlled address via Customer admin interface
6. Attacker resends order confirmation email, causing sensitive data (password hashes, etc.) to be exfiltrated to attacker email

## Root cause
Liquid template engine fails to properly sandbox Drop object instances used in email templates and checkout pages, exposing unrestricted access to instance methods, properties, and dangerous reflection-like methods (to_yaml, methods, class). The template processor does not adequately filter which methods and attributes can be called on Liquid Drops.

## Attacker mindset
Malicious administrator or compromised admin account seeking to exfiltrate sensitive customer and order data (password hashes, personal information) without detection. The attacker leverages their legitimate admin access to modify templates, then exploits the lack of proper Liquid sandboxing to access restricted information and test for RCE capabilities.

## Defensive takeaways
- Implement strict whitelist-based access control for Liquid Drop objects - only expose intentionally safe methods and properties
- Prohibit access to reflection methods (methods, class, to_yaml, instance_eval, instance_exec, systemu) in template contexts
- Use a properly sandboxed Liquid implementation that restricts method invocation to explicitly permitted methods only
- Never expose sensitive data (password hashes, authentication tokens) through serialization methods in template contexts
- Implement audit logging for template modifications and email template rendering to detect suspicious activity
- Consider implementing a restricted Liquid dialect for user-editable templates with explicit method whitelisting
- Validate and sanitize all Drop object exports to prevent unauthorized access to internal object state
- Apply principle of least privilege - limit admin access to template editing based on role requirements

## Variant hunting
Search for similar Liquid template injection vulnerabilities in other templating contexts within Shopify: SMS notification templates, API webhook templates, custom email clients, theme code sections, and any other user-controllable template surfaces. Test whether other Drop types (ProductDrop, CustomerDrop, etc.) are similarly vulnerable. Investigate whether method arguments can be supplied through creative syntax or alternative Liquid filter chains.

## MITRE ATT&CK
- T1190
- T1059
- T1047
- T1552
- T1018
- T1083

## Notes
Researcher notes this may be a Liquid library-level issue requiring upstream fixes. The vulnerability is limited to privileged users (shop owners/admins) but allows escalation of privileges to access sensitive data normally restricted. The researcher expressed disappointment at not achieving full RCE despite the presence of dangerous methods like instance_eval and instance_exec, suggesting argument passing restrictions may be the primary limiting factor. Attack requires at least two steps: template modification + social engineering or account compromise to trigger the template rendering. The thank you page variant is concerning as it may be accessible without admin privileges depending on customization scope.

## Full report
<details><summary>Expand</summary>

Short
====
Certain interfaces where a shop owner/administrator is able to utilize Liquid have access to methods and properties of certain Drops. This allows calling all methods of the object and access to all properties. While this sounds bad, it seems to be very limited and seems to be 'only' usable for Information Disclosure.

PoC
====
 1. Go to your shop admin and navigate to the `Notifcation` settings
 2. Edit the `New Order Template` and place the following text into the textbox (also shown in the `Malicious Template` screenshot:

    {{ methods | json }}
    {{ systemu }}
    {{ class }}
    {{ to_yaml}}

 3. Click the `Preview Button` to have your code executed, results are shown in the `Malicious Template Rendered` screenshot.

Affected parts of the system
====
Almost all of the Notification Email Templates are affected. It looks like one has access to an `OrderDrop` and `DraftOrderDrop` instance (verifyable throigh {{ class }} or similar methods which expose the class name). Please see the attached `Affected Mail Templates` screenshot, all templates which do have a `Revert to default` button rendered are affected.

The `thank you` page of the checkout is also affected, please see the `Checkout Template` and `Checkout Rendering` screenshots which are attached.

Limitations
====
I wasn't able to supply arguments to the methods exposed through this method, but one is still able to call methods which don't accept any. But just because I couldn't find a way doesn't mean there isn't any.

Impact
====
 1. One has (at least) the ability to execute instance methods with no arguments and read access to certain otherwise hidden fields via the `to_yaml` method. Depending on the actual code which is flawed it might be even possible to execute methods with user supplied arguments which would probably result in a server breach (there are very intersting methods like `systemu`, `real_call`, `instance_eval` and `instance_exec`.
 2. This bypasses access restrictions to certain hidden/filtered fields, like a hashed user password. For example,  a malicious admin can force the delivery of the  `Real Order Mail Rendered` to an address controlled by him if he does the following:

1. Ensure the last user who touched an order is a desired victim (e.g. the shop owner)
2. Edit the customers email to an attacker controlled one via the Customer admin interface
3. Resend an order confirmation mail which is prepared to render like `Real Order Rendering` in an Email, by placing `{{ to_yaml }}` in the template

Final words
====
Depending on the real flaw in the code this might be something which needs to be addressed by the Liquid library. I would be very pleased if you could disclose what kind of condition exactly led to this flaw. It might be worth chaning Liquid in a way to guard against this kind of flaw as users expect it to be secure by default.

Please let me know if you need any additional information here, I hope I was clear enough with my explainations. I'm still a little disappointed that I didn't manage to achieve 'real' RCE here, but I'm happy on the other side to report this asap even without 'real' RCE so you could fix this asap. I discovered this approx. 18h ago by accident and couldn't spend that much time on developing a PoC.

</details>

---
*Analysed by Claude on 2026-05-12*
