# XSS vulnerabilities due to missing checks in tag helpers

## Metadata
- **Source:** HackerOne
- **Report:** 1444151 | https://hackerone.com/reports/1444151
- **Submitted:** 2022-01-08
- **Reporter:** amartinfraguas
- **Program:** Rails
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Cross-Site Scripting (XSS), Reflected XSS, Stored XSS, Improper Input Validation, Insufficient Output Encoding
- **CVEs:** CVE-2022-27777
- **Category:** web-api

## Summary
Rails tag helpers in ActionView::Helpers::FormTagHelper and ActionView::Helpers::TagHelper lack proper input validation for attribute names and tag names, allowing attackers to inject malicious JavaScript through data-*, aria-*, and custom attributes. The vulnerability affects multiple helper methods including check_box_tag, label_tag, radio_button_tag, select_tag, submit_tag, text_area_tag, text_field_tag, tag, and content_tag when user-controlled input is passed as attribute or tag names.

## Attack scenario
1. Attacker identifies a Rails application using tag helpers with user-supplied input from URL parameters, form fields, or database
2. Attacker crafts a payload containing special characters to break out of attribute context, such as 'something="something"><img src="/nonexistent" onerror="alert(1)"><div class'
3. Attacker injects payload through vulnerable helper method parameter, for example: check_box_tag('thename', 'thevalue', false, data: { params[:payload] => 'value' })
4. Vulnerable application renders the malicious payload in HTML without proper escaping of the attribute name
5. Victim user's browser interprets the injected HTML/JavaScript and executes arbitrary code in the context of the vulnerable application
6. Attacker achieves session hijacking, credential theft, stored XSS propagation, or malware distribution depending on payload complexity

## Root cause
Rails tag helpers perform insufficient validation and encoding of user-supplied input when constructing HTML attributes and tag names. The existing XSS protections focus on attribute values but do not adequately restrict or sanitize the character set permitted in attribute names (data-*, aria-*, and custom attributes) or tag names themselves. This allows attribute names containing quotes, angle brackets, and other special characters to break out of the attribute context and inject arbitrary HTML/JavaScript.

## Attacker mindset
An attacker with knowledge of Rails application structure would recognize that tag helpers are commonly used with user input and that the attribute name validation gap presents a reliable XSS vector. The attacker understands HTML parsing rules and can craft payloads that exploit the difference between attribute value encoding (which is implemented) and attribute name validation (which is missing). They target both reflected and stored XSS scenarios depending on application architecture.

## Defensive takeaways
- Implement strict whitelist validation for HTML attribute names, restricting to lowercase letters, digits, hyphens, and underscores matching HTML5 specification
- Implement strict whitelist validation for tag names, restricting to valid HTML5 tag characters only
- Apply validation before any HTML generation, not relying solely on output encoding
- Validate both attribute names in data-*, aria-*, and custom attributes equally
- Add comprehensive test coverage for XSS injection attempts through attribute and tag names in all affected helpers
- Document security best practices for Rails developers regarding tag helper usage with user input
- Consider providing parameterized or safe-by-default alternatives to tag helpers for common use cases
- Apply fixes to all supported Rails versions through security backports

## Variant hunting
Search for similar patterns in other Ruby web frameworks and template engines. Examine any custom tag or HTML generation helpers that accept user input for tag/attribute names. Look for other Rails helpers in ActionView that might have the same gap (button_tag, link_to, image_tag with dynamic tag names, etc.). Test third-party gems that provide custom tag helpers. Check for similar issues in JavaScript template engines and PHP frameworks with comparable helper functions.

## MITRE ATT&CK
- T1190
- T1598
- T1566
- T1657

## Notes
The reporter provided a responsible disclosure with a proposed fix and offered to create a private PR for discussion. This is a framework-level vulnerability affecting all applications using the vulnerable helpers with user input. The vulnerability is particularly dangerous because Rails developers may not realize that attribute names need the same validation as attribute values. The attack surface is large given Rails' popularity and widespread use of these helpers. The fix should be backported to all supported Rails versions to protect existing applications.

## Full report
<details><summary>Expand</summary>

Rails offers some protections against XSS in its helpers for the views. Several tag helpers in ActionView::Helpers::FormTagHelper and ActionView::Helpers::TagHelper are vulnerable against XSS because their current protection does not restrict properly the set of characters allowed in the names of tag attributes and in the names of tags.

I am providing a proposal of changes to fix the problems following the official Rails guide for contributing, including tests, changelogs, etc. It is just a proposal and I am willing to improve it with your feedback and backport it to the supported versions. Let me know if you would like me to add you to a private repository where I can create a pull request and we can discuss the changes comfortably.

The first group of vulnerabilities is related to the `options` argument in methods from `FormTagHelper` like `check_box_tag, label_tag, radio_button_tag, select_tag, submit_tag, text_area_tag, text_field_tag, etc.` In particular in these 3 cases:
- When providing prefixed HTML "data-*" attributes.
- When providing prefixed HTML "aria-*" attributes.
- When providing a hash of other types of non-boolean attributes.

For example:

`check_box_tag('thename', 'thevalue', false, data: { malicious_input => 'thevalueofdata' })`

In that method call, when the variable `malicious_input` is controlled in part or completely by a user of the application, an attacker can provide an input that will break free from the tag and execute arbitrary JavaScript code. For some applications, that code can be executed in the browser of a different user visiting the application. A simplified proof of concept with only reflected XSS would be this HTML ERB view file:

`<%= check_box_tag('thename', 'thevalue', false, data: { params[:payload] => 'thevalueofdata' }) %>`

Followed by a request that included the malicious URL parameter: `http://...?payload=something="something"><img src="/nonexistent" onerror="alert(1)"><div class`

That example only shows an alert window, but it is possible to steal passwords or other private information from the user, substitute parts of the website with fake content, attack other websites visited by the user, perform scans of the network of the user, etc. And some applications are probably using more dangerous stored user input instead of URL parameters, allowing attackers to perform stored XSS attacks on other users.

Here is another example with `aria-*` HTML attributes were the same simple payload can be tested:
`check_box_tag('thename', 'thevalue', false, aria: { malicious_input => 'thevalueofaria' })`

And finally, another example with other non-boolean attributes:
`check_box_tag('thename', 'thevalue', false, malicious_input => 'theothervalue')`

This same vulnerable structure can also be attacked successfully in the other methods listed at the beginning: `label_tag, radio_button_tag, select_tag, submit_tag, text_area_tag, text_field_tag...`

The second group of vulnerabilities is related to the more generig methods `tag` and `content_tag` from `TagHelper`. They are vulnerable in the `options` argument like the previous group of methods, but they are also vulnerable in their first argument, for the names of the generated tags, using the same kind of attack to break free from the tag and execute arbitrary Javascript code. For example:

- `tag(malicious_input)`
- `tag.public_send(malicious_input.to_sym)`
- `content_tag(malicious_input)`

In the 3 cases, this is an example of a simple payload that works:
`img%20src=%22/nonexistent%22%20onerror=%22javascript_payload%22`

As said before for other examples, that only shows an alert window, but it is possible to use the same attack to potentially steal passwords or other private information from the user, substitute parts of the website with fake content, perform scans of the network of the user, etc.

## Impact

As mentioned in the description, the Rails applications that use those helpers with some kind of user-supplied input are vulnerable to XSS attacks. Currently, there are some protections againts XSS in the affected methods, but it is not enough.

In the description I have provided simple payloads as an example that only created an alert window. However, it is possible to use the same attack to potentially steal passwords or other private information from the user, substitute parts of the website with fake content, perform scans of the network of the user, etc. In some applications it is probably possible to perform more dangerous stored XSS attacks. So fixing this problem is recommended and consistent with the Rails security policy ( https://rubyonrails.org/security ).

</details>

---
*Analysed by Claude on 2026-05-12*
