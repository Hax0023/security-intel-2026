# Stored XSS in Select Attribute Options via Unescaped Output

## Metadata
- **Source:** HackerOne
- **Report:** 753567 | https://hackerone.com/reports/753567
- **Submitted:** 2019-12-07
- **Reporter:** sunny0day
- **Program:** Concrete5
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Stored Cross-Site Scripting (XSS), Improper Output Encoding, Insufficient Input Validation
- **CVEs:** None
- **Category:** web-api

## Summary
Concrete5 fails to properly escape select attribute option values in the type_form.php file, allowing stored XSS injection. Attackers can inject malicious JavaScript that executes when administrators edit the attribute, or unauthenticated users can exploit this via Express Forms configured to allow user-added options.

## Attack scenario
1. Attacker creates a new select attribute in the Concrete5 dashboard
2. Attacker enters a malicious payload like '<script>alert(XSS)</script>' as an option value
3. Payload is stored in the database without proper sanitization
4. Administrator or authorized user edits the attribute, triggering the unescaped script execution
5. In Express Forms scenario, unauthenticated user submits form with malicious select option value
6. JavaScript executes in victim's browser with stored XSS consequence

## Root cause
The type_form.php file outputs select attribute option values directly to HTML without proper escaping functions, failing to encode special characters that could break out of HTML context and inject script tags.

## Attacker mindset
An attacker recognizes that user-controllable data (form options) are reflected without encoding. They exploit the trust boundary between user input and admin interface output, leveraging stored XSS for privilege escalation, credential theft, or malware distribution.

## Defensive takeaways
- Always escape output context-appropriately: use htmlspecialchars() or equivalent for HTML context, JavaScript escaping for JS context
- Implement Content Security Policy (CSP) headers to mitigate XSS impact
- Validate and sanitize all user inputs server-side, not just client-side
- Apply output encoding consistently across all template files and admin interfaces
- Disable 'Allow users to add to this list' for select attributes unless absolutely necessary, or add extra validation layers
- Implement input length limits and character whitelisting for select options
- Use templating engines with auto-escaping enabled by default

## Variant hunting
Search for similar unescaped output patterns in other attribute types (text, checkbox, radio). Check all dashboard admin forms that display user-controlled data. Look for other form builders or attribute management interfaces with similar data flows.

## MITRE ATT&CK
- T1190
- T1598
- T1566

## Notes
The vulnerability is particularly dangerous in Express Forms with open user submission because it bypasses typical admin-only XSS protections. The stored nature means the payload persists and affects all users viewing the attribute. Concrete5 likely patched this by adding htmlspecialchars() or using a templating engine with auto-escaping in subsequent versions.

## Full report
<details><summary>Expand</summary>

## To reproduce
1. Create a new select attribute.
2. Add a select attribute option with value `<script>alert('XSS')</script>` and hit Save.
3. Edit the newly created attribute again and see XSS dialog.

The vulnerability lays in the type_form.php file, see https://github.com/concrete5/concrete5/blob/develop/concrete/attributes/select/type_form.php#L40

## Unauthenticated use
The vuln can be pretty bad if the website has an Express Form with select attribute associated with it that "Allow users to add to this list.". In that case, an (unauthenticated) user can submit a form that results to stored XSS.

## Screenshot
{F653172}

## Impact

Stored XSS on /index.php/dashboard/pages/attributes/edit/xxx page and when editing an Express Form block.

</details>

---
*Analysed by Claude on 2026-05-12*
