# Stored XSS on imgur Profile via HTML Entity Bypass

## Metadata
- **Source:** HackerOne
- **Report:** 484434 | https://hackerone.com/reports/484434
- **Submitted:** 2019-01-23
- **Reporter:** giddsec
- **Program:** Imgur
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Stored Cross-Site Scripting (XSS), Improper Input Validation, Insufficient Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A stored XSS vulnerability exists in imgur's album creation feature that allows attackers to bypass HTML tag filtering using HTML entity encoding. The vulnerability persists even after a previous similar issue was patched, indicating incomplete remediation of the underlying validation logic.

## Attack scenario
1. Attacker identifies that imgur filters < and > characters in album creation fields
2. Attacker discovers that HTML entity encoded versions (&lt; and &gt;) bypass the filter
3. Attacker crafts payload: "/>&lt;script>alert(1)&lt;/script&gt; to inject malicious JavaScript
4. Attacker creates album with the encoded payload stored in profile/album data
5. Victim visits attacker's imgur profile (e.g., gidsumaya.imgur.com)
6. Stored XSS executes in victim's browser, potentially stealing credentials or session cookies

## Root cause
Inadequate input validation that only blacklists literal < and > characters while allowing HTML entity alternatives. The fix for the original vulnerability (report #381553) addressed the symptom rather than implementing comprehensive output encoding or proper HTML sanitization.

## Attacker mindset
Recognize that simple character-based filtering is insufficient and test alternative encoding schemes (HTML entities, URL encoding, unicode). Retest previous vulnerability classes after patches to identify incomplete fixes.

## Defensive takeaways
- Implement output encoding (HTML entity encoding) on display, not just input filtering
- Use allowlist-based HTML sanitization libraries rather than blacklist filtering
- Decode all encoded representations before validation (HTML entities, URL encoding, unicode)
- Conduct comprehensive regression testing after security patches to verify all bypass vectors are closed
- Implement Content Security Policy (CSP) headers as defense-in-depth
- Apply context-appropriate encoding (HTML, JavaScript, URL, CSS) based on where data is rendered

## Variant hunting
Test other HTML entity encodings: &#60; &#x3C; for <, &#62; &#x3E; for >
Try double encoding: &amp;lt; &amp;gt;
Test unicode escapes: \u003C \u003E
Attempt SVG-based payloads: <svg onload=...>
Test event handler attributes: " onmouseover="alert(1)
Probe other input fields in album creation (title, description, tags)
Test image alt text and metadata fields for same vulnerability

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1566.002: Phishing - Spearphishing Link
- T1598.003: Phishing - Spearphishing Link

## Notes
The reporter explicitly notes this is a bypass of a previous patch (report #381553), demonstrating that the original fix was incomplete. The fact that the profile remains accessible with active XSS suggests either slow patch deployment or that the fix only addressed the specific reported payload. This highlights the importance of testing entire vulnerability classes rather than individual payloads.

## Full report
<details><summary>Expand</summary>

Hello, I submitted a report on imgur, but the staff marked it as duplicate. #482841 I reviewed the report of the first submitted report. #381553 We are on the same situation and his case is already fixed because I tried visiting his site too which is https://12test.imgur.com/ and even redoing his steps to reproduce but no XSS is triggered. And I have a different bypass and my bypass succeed. I can still fire up XSS on the said webpage.

Sorry for double posting, but I think his case #381553 is already fixed and mine is different.

There are still bypasses exists in the imgur create album that can cause an Stored XSS. 
Try to visit my site: https://gidsumaya.imgur.com/ and XSS will trigger. F410962:

In my case, I bypassed the filtering using HTML entities for the alternation of <>, because I noticed that it's filtering the <>.
##Payload:
**”/>&_lt;_script>alert(1)&_lt;/scr_ipt&gt”/>** remove the underscores.

And I can still fire up XSS and anyone who visits the link, the XSS will trigger.

I acknowledge that there was another report, for the same issue but that I still have a way to bypass whatever fix they implemented.

## Impact

XSS can use to steal cookies, password or to run arbitrary code on victim's browser

</details>

---
*Analysed by Claude on 2026-05-11*
