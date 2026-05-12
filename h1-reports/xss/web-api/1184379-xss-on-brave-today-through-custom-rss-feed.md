# XSS on Brave Today through custom RSS feed via javascript: URL scheme

## Metadata
- **Source:** HackerOne
- **Report:** 1184379 | https://hackerone.com/reports/1184379
- **Submitted:** 2021-05-04
- **Reporter:** nishimunea
- **Program:** Brave
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Cross-Site Scripting (XSS), Insufficient URL scheme validation, Unvalidated redirect/open redirect
- **CVEs:** None
- **Category:** web-api

## Summary
The custom RSS feed feature in Brave iOS fails to validate URL schemes in feed entry links, allowing attackers to inject javascript: URLs that execute arbitrary JavaScript in the privileged localhost:65XX context. When users click a malicious RSS feed entry, XSS payload executes with access to Brave's internal features and sensitive domains.

## Attack scenario
1. Attacker creates a malicious RSS feed containing an entry with href="javascript:alert(document.domain)" or other malicious payload
2. Attacker hosts the RSS feed on a web server (e.g., https://csrf.jp/brave/rss.php)
3. Victim adds the malicious RSS feed through Brave Today settings (Settings > Brave Today > Add Source)
4. Victim enables the feed and views it in a new tab's Brave Today section
5. Victim clicks on the malicious RSS entry, triggering the javascript: URL
6. JavaScript executes in the context of http://localhost:65XX, granting access to internal Brave features, reader-view, and other privileged functionality

## Root cause
The RSS feed parser and link handler in Brave iOS does not validate or restrict URL schemes before rendering them as clickable links. The application fails to whitelist safe schemes (http, https) and reject dangerous ones (javascript, data, etc.), allowing javascript: protocol handlers to execute arbitrary code in a privileged context.

## Attacker mindset
An attacker distributes a seemingly legitimate RSS feed that appears normal in the feed list. Upon user interaction (clicking a link), the attacker's JavaScript payload executes in a privileged domain context, potentially exfiltrating data, modifying browser settings, or pivoting to other Brave internal features without user awareness.

## Defensive takeaways
- Implement strict URL scheme whitelist validation - only permit http:// and https:// schemes for feed entry links
- Use URL parsing libraries that safely reject or sanitize dangerous protocols before rendering links
- Apply Content Security Policy (CSP) headers to localhost:65XX to restrict script execution sources
- Sanitize and validate all user-supplied feed data at ingestion time, not just at display time
- Implement a URL validation layer that blocks javascript:, data:, vbscript:, and other executable schemes
- Test RSS feed parsing with malicious payloads including protocol-based XSS vectors
- Consider sandboxing RSS feed content in a restricted iframe with limited capabilities

## Variant hunting
Test data: URL schemes with base64-encoded payloads in RSS feeds
Test vbscript: and other legacy executable protocol handlers
Attempt XSS through malformed URLs with mixed case (JavaSCript:) to bypass simple filters
Test SVG/XML namespaced attributes in RSS content elements
Attempt XSS through URL encoding variations (%6A%61%76%61%73%63%72%69%70%74:)
Test unicode normalization bypasses in protocol handlers
Check if other feed readers or Brave desktop have similar issues
Test event handlers in RSS content (onclick, onload, etc.)

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1204 - User Execution
- T1059 - Command and Scripting Interpreter
- T1657 - Defense Evasion: Masquerading

## Notes
The vulnerability is particularly severe because it executes in http://localhost:65XX, which is a privileged domain hosting Brave's internal features (reader-view, error pages). This elevates a standard XSS to a potential capability to access or modify internal Brave functionality. The attack requires user interaction (clicking the link) but is disguised as legitimate RSS feed content. The report references a proof-of-concept RSS feed accessible at https://csrf.jp/brave/rss.php demonstrating the exact attack vector.

## Full report
<details><summary>Expand</summary>

## Summary:

Two months ago, the [custom RSS feed feature](https://github.com/brave/brave-ios/pull/3317) was introduced to Brave Today on Brave iOS.

This feature allows to add any RSS feed to Brave Today, and the registered feed entries are shown in a tab with a hyperlink to the original article URL.
Then, Brave iOS doesn't restrict the URL scheme of the original article link, which can cause XSS weakness through `javascript:` URL.

Here is a demonstration RSS feed of this attack.
https://csrf.jp/brave/rss.php

This RSS feed contains `javascript:alert(document.domain)` in an entry tag like this.
```
<entry>
  <title>XSS</title>
  <link rel="alternate" type="text/html" href="javascript:alert(document.domain)" />
  <content type="html"><![CDATA[<img src="https://csrf.jp/test.png">]]></content>
</entry>
```
When user taps the entry on Brave Today, an alert dialog is shown on `http://localhost:65XX`.

## Products affected: 

 * Brave iOS current Nightly build

## Steps To Reproduce:

 * Open "Settings"
 * Tap "Brave Today" in Settings menu
 * Tap "Add Source"
 * Type "https://csrf.jp/brave/rss.php" and tap "Search"
 * RSS feed, that name is PoC, is found, then tap "Add"
 * Enable PoC feed
 * Close the Settings menu and open a new tab
 * Enable Brave Today, then you can find an article entry that name is "XSS"
 * Tap the article, then an alert dialog is shown

## Supporting Material/References:

  * See attached movie file for the demonstration

## Impact

As written in summary, XSS is possible on `http://localhost:65XX`.
Note that `http://localhost:65XX` should be considered as a privileged domain that hosts Brave's internal features such as reader-view, error-pages and so on.

</details>

---
*Analysed by Claude on 2026-05-12*
