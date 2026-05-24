# URL Scheme Validation Bypass in Shopify Mobile App Allows JavaScript Execution

## Metadata
- **Source:** HackerOne
- **Report:** 1737358 | https://hackerone.com/reports/1737358
- **Submitted:** 2022-10-17
- **Reporter:** fr4via
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Improper Input Validation, URL Scheme Bypass, WebView JavaScript Injection, Intent-based Attack, Unsafe Intent Handling
- **CVEs:** None
- **Category:** memory-binary

## Summary
The Shopify mobile app (com.shopify.mobile v9.85.1) fails to validate URL schemes passed as intent extras to NavigationActivity, allowing attackers to load arbitrary HTML/JavaScript content in the application's WebView. This enables execution of JavaScript code and potential exploitation of exposed Java interfaces (EASDK, SmartWebview) for further code execution.

## Attack scenario
1. Attacker crafts a malicious intent targeting com.shopify.mobile.navigation.NavigationActivity with an arbitrary URL in the extras parameter
2. The URL bypasses scheme validation checks, allowing non-whitelisted schemes or file:// URIs to be processed
3. Attacker's URL loads arbitrary HTML content containing malicious JavaScript into the application's WebView
4. JavaScript executes in the context of the Shopify app with access to exposed Java interfaces (EASDK, SmartWebview)
5. Attacker uses JavaScript to invoke Java methods through the interfaces, achieving arbitrary code execution
6. Attack could be triggered via deeplinks, other apps, or web pages launching intents to compromise user session/data

## Root cause
The NavigationActivity component does not implement proper URL scheme validation before loading URLs into WebView. The application fails to maintain a whitelist of allowed URL schemes (http, https) and does not reject potentially dangerous schemes (file://, data://, javascript://, etc.), enabling arbitrary content injection.

## Attacker mindset
An attacker seeks to exploit implicit trust in the Shopify app's intent-based navigation system. By bypassing scheme validation, they can inject malicious content without user awareness, leveraging exposed Java bridge interfaces for privilege escalation and data theft or session hijacking.

## Defensive takeaways
- Implement strict URL scheme validation using explicit whitelisting (only allow http:// and https:// schemes)
- Validate domain/host against a whitelist before loading URLs in WebViews
- Use disallowlist approach for dangerous schemes: file://, data://, javascript://, content://, etc.
- Consider using SafeBrowsingHelper or similar safety mechanisms for URL validation
- Restrict or disable Java-to-JavaScript bridge interfaces where possible; if required, minimize exposed methods
- Implement Content Security Policy (CSP) headers when serving content via WebView
- Add intent-filter validation and consider using explicit intents instead of implicit intents
- Audit all exposed EASDK and SmartWebview interface methods for security implications
- Implement deep link validation and verification mechanisms

## Variant hunting
Check other activity components accepting URL parameters for similar validation bypasses
Review all WebView implementations across the application for proper scheme validation
Audit other exposed Java-JavaScript bridge interfaces for security risks
Test custom URL handlers and protocol implementations for bypass techniques
Examine intent extras handling in all navigation-related activities
Search for other uses of loadUrl() without prior URL validation
Test intent injection via other app components (Services, BroadcastReceivers)
Investigate whether data:// or javascript:// schemes can be used to bypass validation

## MITRE ATT&CK
- T1190
- T1203
- T1543
- T1559.001
- T1204.001

## Notes
This vulnerability represents a critical flaw in the app's intent handling and WebView security. The exposed Java interfaces (EASDK, SmartWebview) compound the severity by enabling arbitrary Java method invocation from injected JavaScript. The app version tested was 9.85.1 on SDK target 32. This type of vulnerability is common in mobile apps that use WebViews as rendering engines without proper isolation. The attack surface is likely broadened if the app registers deeplink handlers or allows other apps to interact with NavigationActivity.

## Full report
<details><summary>Expand</summary>

## Summary:

[------------------------------------Package Details---------------------------------------]:
|    Application Name  :Shopify
|    Package Name      :com.shopify.mobile
|    Version code      :33070
|    Version Name      :9.85.1
|    Mimimum SDK       :26
|    Target  SDK       :32
|    Max SDK           :None
|    Sha256            :602982573bab04349ad812799319959e6236a746a41f88c7ec0196157ba15027
[------------------------------------------------------------------------------------------]

## Shops Used to Test:
█████████.myshopify.com 


## Steps To Reproduce:
It was found that the com.shopify.mobile app doesn't validate the scheme of the url given as an extra parameter to the com.shopify.mobile.navigation.NavigationActivity which may allow the loading of arbitrary html content (including js code) in the application's webview and the takeover of the SmartWebview , EASDK js interface. 

To reproduce, use the apk provided 

█████


## Supporting Material:

Expected behaviour:

{F1989590}

## Impact

Execution of js code ,including of running java code via the EASDK and SmartWebview interfaces.

</details>

---
*Analysed by Claude on 2026-05-24*
