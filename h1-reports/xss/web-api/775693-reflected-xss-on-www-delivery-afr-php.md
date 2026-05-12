# Reflected XSS on www/delivery/afr.php via QUERY_STRING

## Metadata
- **Source:** HackerOne
- **Report:** 775693 | https://hackerone.com/reports/775693
- **Submitted:** 2020-01-15
- **Reporter:** jacopotediosi
- **Program:** Unknown (HackerOne Report #775693)
- **Bounty:** Not specified in writeup
- **Severity:** High
- **Vuln:** Reflected Cross-Site Scripting (XSS), Improper Input Validation, Improper Output Encoding
- **CVEs:** CVE-2020-8115
- **Category:** web-api

## Summary
The afr.php endpoint directly incorporates the $_SERVER['QUERY_STRING'] parameter into JavaScript code and HTML meta refresh tags without sanitization or encoding. An attacker can inject arbitrary JavaScript by crafting a malicious query string, breaking out of the setTimeout() call context to execute code in the victim's browser.

## Attack scenario
1. Attacker crafts a malicious URL containing JavaScript payload that breaks out of the setTimeout() string context
2. Attacker tricks a user into clicking the malicious link (via phishing, social engineering, or ad injection)
3. User's browser requests the crafted URL to domain.com/www/delivery/afr.php with the payload
4. Server reflects the unencoded QUERY_STRING into both a JavaScript setTimeout() call and an HTML meta refresh tag
5. Browser executes the injected JavaScript in the context of domain.com, allowing access to same-origin cookies and resources
6. Attacker harvests session tokens, performs CSRF actions, or redirects user to credential theft page

## Root cause
The application fails to properly encode user-controlled input (QUERY_STRING) before reflecting it into multiple output contexts (JavaScript string and HTML attribute). The $dest variable containing raw query string parameters is directly concatenated into script tags and meta tags without URL encoding or HTML escaping.

## Attacker mindset
An attacker would recognize this as a straightforward reflected XSS opportunity requiring minimal obfuscation, especially useful for targeting users of ad delivery systems who may have elevated privileges. The presence of two reflection points increases likelihood of exploitation success.

## Defensive takeaways
- Always URL-encode or HTML-escape user input before reflecting it into HTML/JavaScript contexts
- Use context-appropriate encoding: urlencode() for URL parameters, htmlspecialchars() for HTML attributes, JSON escaping for JSON contexts
- Implement Content Security Policy (CSP) headers to restrict inline script execution
- Apply input validation using allow-lists for expected parameter formats
- Use security-focused templating engines that auto-escape by default
- Conduct code review specifically for $_SERVER['QUERY_STRING'] and $_SERVER['REQUEST_URI'] usage patterns
- Implement output encoding in a consistent library/function to prevent inconsistent application

## Variant hunting
Search codebase for direct uses of $_SERVER['QUERY_STRING'], $_SERVER['REQUEST_URI'], $_GET without encoding
Audit all locations where user input is reflected into <script> tags, particularly within string literals
Check meta refresh tags with user-controlled content
Review JavaScript setTimeout/setInterval calls with dynamic parameters
Examine any ad delivery or frame injection code for similar patterns
Test other delivery endpoints (e.g., www/delivery/*.php files) for identical vulnerability patterns
Look for similar patterns in _dev versions of files which may have less scrutiny

## MITRE ATT&CK
- T1190
- T1598
- T1566

## Notes
The PoC elegantly demonstrates the vulnerability by breaking out of the setTimeout() string parameter using ')', then injecting alert(1), then reopening a string context. The payload also appears in the noscript meta-refresh tag, showing multiple reflection points. The suggested fix of using urlencode() is appropriate for URL parameter context but developers should verify it doesn't cause double-encoding issues. The vulnerability appears to be in ad delivery infrastructure, making it a high-value target for attackers seeking to compromise multiple downstream users.

## Full report
<details><summary>Expand</summary>

At line 4381, $_SERVER['QUERY_STRING'], which is an untrusted user input, is assigned to the $dest variable.
Then at lines 4386-4387 $dest is printed into HTML code in two separate places.

PoC:
~~~~
curl "domain.com/www/delivery/afr.php?refresh=10000&\")',10000000);alert(1);setTimeout('alert(\""
<!DOCTYPE html PUBLIC '-//W3C//DTD XHTML 1.0 Transitional//EN' 'http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd'>
<html xmlns='http://www.w3.org/1999/xhtml' xml:lang='en' lang='en'>
<head>
<title>Advertisement</title>

    <script type='text/javascript'><!--// <![CDATA[
        setTimeout('window.location.replace("http://domain.com/www/delivery/afr.php?refresh=10000&")',10000000);alert(1);setTimeout('alert("&loc=")', 10000000);
    // ]]> --></script><noscript><meta http-equiv='refresh' content='10000;url=http://domain.com/www/delivery/afr.php?refresh=10000&")',10000000);alert(1);setTimeout('alert("&loc='></noscript>
    <style type='text/css'>
body {margin:0; height:100%; background-color:transparent; width:100%; text-align:center;}
</style>
</head>
<body>

</body>
</html>
~~~~

Suggested remediation:
I suggest to change line 4381 from `$dest = MAX_commonGetDeliveryUrl($conf['file']['frame']).'?'.$_SERVER['QUERY_STRING'];` to `$dest = MAX_commonGetDeliveryUrl($conf['file']['frame']).'?'.urlencode($_SERVER['QUERY_STRING']);` in both files /www/delivery/afr.php and /www/delivery_dev/afr.php

## Impact

An attacker could use this XSS to steal session cookies (if readable via javascript, I didn't check) or transform it to a CSRF and cause involuntary actions to be performed by a privileged user

</details>

---
*Analysed by Claude on 2026-05-12*
