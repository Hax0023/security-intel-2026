# Reflected Cross-Site Scripting (XSS) in Revive Adserver 5.5.2 - admin-search.php compact Parameter

## Metadata
- **Source:** HackerOne
- **Report:** 3091390 | https://hackerone.com/reports/3091390
- **Submitted:** 2025-04-14
- **Reporter:** env_bak
- **Program:** Revive Adserver
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Reflected Cross-Site Scripting (XSS), Improper Input Validation, Improper Output Encoding
- **CVEs:** CVE-2025-27208
- **Category:** web-api

## Summary
Revive Adserver 5.5.2 contains a reflected XSS vulnerability in admin-search.php where the 'compact' parameter is directly embedded into HTML output without proper escaping. An attacker can inject arbitrary JavaScript code by crafting a malicious URL, enabling session hijacking and administrative actions on behalf of the victim.

## Attack scenario
1. Attacker identifies the vulnerable compact parameter in admin-search.php and crafts a malicious URL containing JavaScript payload
2. Attacker sends the malicious URL to a victim administrator via email, social engineering, or embedded in a malicious website
3. Victim administrator clicks the link while authenticated to the Revive Adserver admin panel
4. Browser executes the injected JavaScript in the context of the admin session
5. Malicious script extracts session cookies or performs unauthorized administrative actions
6. Attacker gains unauthorized access to sensitive admin functions or escalates privileges

## Root cause
The compact parameter is registered as a global variable via phpAds_registerGlobalUnslashed() without sanitization, then directly assigned to the template engine without HTML entity encoding. The template renders it in a hidden input field using {$compact} syntax without escaping, violating the principle of encoding data based on context (HTML attribute context requires HTML entity encoding).

## Attacker mindset
An attacker would view this as an easy-to-exploit vulnerability requiring minimal technical skill. The attack works against authenticated administrators, making it ideal for targeted attacks against specific organizations running Revive Adserver. The attacker could use this to steal admin credentials, modify advertisements, or establish persistent access to the ad serving infrastructure.

## Defensive takeaways
- Always HTML-encode output when rendering user-controlled data in HTML contexts, especially in attribute values
- Avoid using phpAds_registerGlobalUnslashed() for parameters that will be output; use explicit parameter retrieval and validation instead
- Implement Content Security Policy (CSP) headers to mitigate XSS impact by restricting inline script execution
- Use template engines with auto-escaping enabled by default; explicitly mark data as safe only after validation
- Apply input validation (whitelist expected values like boolean for compact parameter) in addition to output encoding
- Implement HTTPOnly and Secure flags on session cookies to prevent JavaScript access in XSS scenarios
- Conduct regular security code reviews focusing on template rendering and user input handling patterns
- Add automated testing for XSS vectors in all user-controllable parameters before release

## Variant hunting
Search for other instances of phpAds_registerGlobalUnslashed() usage where output is rendered without escaping
Audit all template files for {$variable} patterns without the |escape or |sanitize filters applied
Check other search/filter parameters (keyword, client, campaign, banner, zone, affiliate) in admin-search.php for similar vulnerabilities
Review other admin pages that accept URL parameters and render them in forms or HTML contexts
Test GET/POST parameters in admin panels that might be reflected in error messages or confirmation pages
Look for similar patterns in other Revive Adserver modules that handle user preferences or search criteria

## MITRE ATT&CK
- T1190
- T1566
- T1598
- T1104
- T1005

## Notes
This is a classic reflected XSS vulnerability in an admin panel context, making it particularly dangerous. The POC demonstrates a DOM-based context issue where the parameter should have been a boolean but accepts arbitrary strings. The vulnerability affects authenticated users primarily, but could be chained with CSRF or session fixation for unauthenticated exploitation. Version 5.5.2 appears to be the affected version; checking if later versions contain the fix is important. The use of deprecated phpAds_registerGlobalUnslashed() function suggests the codebase may have other security issues related to global variable handling.

## Full report
<details><summary>Expand</summary>

A reflected Cross-Site Scripting (XSS) vulnerability has been identified in Revive Adserver version 5.5.2. This vulnerability allows an attacker to inject malicious JavaScript code into the application, which is then executed in the context of the victim's browser. The vulnerability is present in the admin-search.php file and can be exploited via the compact parameter.

The vulnerability arises due to insufficient input sanitization of the compact parameter in the admin-search.php file. The compact parameter is directly embedded into the HTML output without proper escaping, allowing an attacker to inject arbitrary JavaScript code.
The affected code is located in lib/templates/admin/layout/search.html:
```
<input type='hidden' name='compact' value='{$compact}'>
```
The compact parameter is passed to the template without proper sanitization in www/admin/admin-search.php:
```
phpAds_registerGlobalUnslashed('keyword', 'client', 'campaign', 'banner', 'zone', 'affiliate', 'compact');
...
if (!isset($compact)) {
    $compact = false;
}
...
$oTpl->assign('compact', $compact);
```

Proof of Concept (POC)

An attacker can exploit this vulnerability by crafting a malicious URL that includes a JavaScript payload in the compact parameter. When the administrator visits this URL, the malicious script is executed in their browser.
```
http://target-ip/www/admin/admin-search.php?affiliate=1&banner=1&campaign=1&client=1&compact=1'><script>alert(document.cookie)</script>&keyword=1&zone=1
```

## Impact

The impact of this vulnerability is significant as it allows an attacker to:
Steal sensitive information such as session cookies.
Perform actions on behalf of the victim.
Redirect the victim to malicious websites.
Deface the application.
This vulnerability can be exploited by any user who can trick a victim into clicking a malicious link, making it a critical security issue that requires immediate attention.

</details>

---
*Analysed by Claude on 2026-05-12*
