# XSS in Nextcloud Desktop Client via Unvalidated Server Response on Login Form

## Metadata
- **Source:** HackerOne
- **Report:** 685552 | https://hackerone.com/reports/685552
- **Submitted:** 2019-08-31
- **Reporter:** jplopezy
- **Program:** Nextcloud
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Cross-Site Scripting (XSS), HTML Injection, Arbitrary File Execution, Privilege Escalation
- **CVEs:** CVE-2020-8189
- **Category:** web-api

## Summary
The Nextcloud Windows desktop client fails to sanitize error responses displayed in alert dialogs when users attempt to connect to invalid server addresses. An attacker can craft a malicious server that returns HTML/JavaScript in error responses, which are rendered with elevated privileges in the error dialog, allowing execution of arbitrary local files via file:// protocol URLs without user confirmation.

## Attack scenario
1. Attacker sets up a malicious web server or performs MITM attack to intercept legitimate server connection attempt
2. Attacker's server responds to Nextcloud client request with error code (e.g., 403) containing malicious HTML payload in response body
3. Nextcloud client renders error response in alert dialog without sanitization or validation
4. Alert dialog interprets HTML tags and executes embedded links/scripts with higher privileges than normal browser context
5. Attacker crafts file:// protocol URI (e.g., file:///C:/WINDOWS/system32/calc.exe) in href attribute of link
6. User clicks link in error dialog or JavaScript automatically triggers file execution, launching local application without confirmation

## Root cause
The Nextcloud desktop client displays unvalidated HTTP error responses in alert dialogs without HTML sanitization or escaping. The dialog rendering engine interprets HTML markup and allows file:// protocol URIs, which execute with the application's privilege context rather than being blocked or requiring explicit user consent.

## Attacker mindset
An attacker would recognize that error dialogs often receive less security scrutiny than main UI elements. By controlling a server response, they can inject arbitrary HTML into what appears to be a trusted system dialog, bypassing user expectations that dialog boxes are safe. The file:// protocol execution is particularly attractive for achieving code execution on the victim's local machine during what appears to be a legitimate authentication attempt.

## Defensive takeaways
- Implement strict HTML sanitization/escaping for all user-facing content, especially error messages from untrusted sources (servers during authentication)
- Use allowlists for protocols in hyperlinks; explicitly block or restrict file://, javascript://, and data:// protocols in all user interface contexts
- Treat error dialogs and alert boxes with same security rigor as main UI elements; assume attackers will target any rendered content
- Validate and escape HTTP response bodies before displaying in UI, regardless of context
- Require explicit user interaction before executing local file operations; never allow silent execution via protocol handlers in dialogs
- Implement Content Security Policy (CSP) equivalent controls in desktop client frameworks to prevent inline script execution
- Use plain text rendering for error messages rather than HTML rendering, or use a restricted markup language with strict parsing rules
- Perform security review of all alert/dialog boxes and error handling paths during code audits

## Variant hunting
Check if other error dialogs (certificate errors, network errors, timeout messages) have similar unsanitized response rendering
Test if other file:// URIs work (file shares, UNC paths, local script execution via shell:// or other protocols)
Investigate if JavaScript execution is possible in addition to HTML interpretation (e.g., <script> tags or event handlers)
Test redirect-based attacks where initial error is sanitized but redirect target provides unsanitized content
Check if other Nextcloud clients (macOS, Linux) have equivalent vulnerabilities in their error handling
Look for similar patterns in other sync clients and desktop applications (OneDrive, Dropbox, etc.)

## MITRE ATT&CK
- T1190
- T1204.001
- T1566.002
- T1566.001
- T1566.004

## Notes
Report uses somewhat unclear terminology ('cross zone') but clearly describes a rendering context escape where untrusted server responses gain higher privileges in an alert dialog. The file:// protocol execution is the critical escalation from HTML injection to code execution. Video evidence was provided but not visible in text excerpt. The vulnerability assumes attacker can control server response, achievable through compromised server, misconfigured corporate infrastructure, DNS hijacking, or MITM attacks.

## Full report
<details><summary>Expand</summary>

Team!

I have found this vulnerability that in my time would be called "cross zone" but at the moment I don't know.

The problem is found in the latest version of "nextcloud.exe" for your windows version.

The problem occurs with the initial screen where you ask to connect to a website.

Apparently when you put an invalid URI that generates some type of response code like 403, it is reported in a small window, as if it were an alert box, not in the main.

This "alert box" visualizes the response and to my impression (that's why I said the cross zone) has a little more permissions than the internet explorer.

For example, if the response code has an <S> test</S> it will interpret it as IE does.

That's fine, it would only be an html injection.

The problem, for example, is that it allows you to run a file like the calculator locally without any confirmation.

This vector works : <A HREF="file:///C:/WINDOWS/system32/calc.exe">CALC.EXE</A>

In my opinion, response code errors are a problem and must be controlled by the application.

For the demonstration use the burp.

But basically any personal site where the response code building could be controlled could exploit it.

I attach a video to make everything clearer.

## Impact

The impact is that you can run local files without authorization (of the application) in a context where you should warn.

It should be filtered so as not to disturb that it is a vector.

</details>

---
*Analysed by Claude on 2026-05-12*
