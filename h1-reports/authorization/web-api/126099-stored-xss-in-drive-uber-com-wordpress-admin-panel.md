# Stored XSS in All In One Event Calendar Plugin - drive.uber.com WordPress Admin

## Metadata
- **Source:** HackerOne
- **Report:** 126099 | https://hackerone.com/reports/126099
- **Submitted:** 2016-03-26
- **Reporter:** jouko
- **Program:** Uber
- **Bounty:** Not specified in report
- **Severity:** critical
- **Vuln:** Stored Cross-Site Scripting (XSS), Improper Input Validation, Error Message Information Disclosure
- **CVEs:** None
- **Category:** web-api

## Summary
The All In One Event Calendar plugin used on drive.uber.com fails to sanitize error messages displayed in the WordPress administrative dashboard. An attacker can inject malicious JavaScript through a malformed HTTP request containing unencoded special characters in URL parameters, which persists in error banners shown to all administrators. When administrators access the dashboard, the injected script executes with administrator privileges, enabling account compromise and server-side attacks.

## Attack scenario
1. Attacker crafts a malformed HTTP request with special characters in the events_per_page parameter (e.g., SQL injection syntax)
2. Attacker includes XSS payload in the xss URL parameter without proper encoding
3. Request is sent directly via raw socket/PERL script to bypass browser URL encoding
4. Plugin encounters error condition and generates error message including unsanitized URL parameter content
5. Plugin stores error message/banner in WordPress dashboard persistent state
6. Administrator logs into WordPress dashboard and views the stored error message, triggering arbitrary JavaScript execution with admin privileges

## Root cause
The All In One Event Calendar plugin's exception handler in wp-content/plugins/all-in-one-event-calendar/lib/exception/handler.php includes user-controlled URL parameters directly in error messages displayed on the administrative dashboard without HTML encoding or sanitization. The plugin does not validate or escape special characters before rendering error details.

## Attacker mindset
An attacker would recognize that administrative error messages are implicitly trusted by administrators and represent a high-value injection point. By bypassing browser URL encoding mechanisms via raw socket requests, the attacker can inject unencoded payloads that plugin code fails to sanitize. The persistence aspect (stored in dashboard) means the attack succeeds against any administrator who logs in, making it a scalable privilege escalation vector.

## Defensive takeaways
- Always HTML-encode user-controlled data before displaying in any context, including error messages and admin panels
- Implement strict input validation on URL parameters before processing, rejecting malformed requests early
- Use WordPress sanitization functions (sanitize_text_field, wp_kses_post) on all user inputs before storage or display
- Apply Content-Security-Policy headers to prevent inline script execution in admin contexts
- Log security-relevant errors separately from user-visible messages to avoid leaking attacker-controlled data
- Implement output escaping at template level (esc_html, esc_attr, esc_url) for all dynamic content
- Disable PHP error detail disclosure in production environments
- Conduct security code review of exception handlers and error reporting mechanisms

## Variant hunting
Search for similar patterns in other WordPress plugins: (1) Exception handlers that include request parameters in error messages, (2) Dashboard widgets displaying user-supplied data without sanitization, (3) Plugins that construct SQL queries from unvalidated URL parameters, (4) Admin-only features that trust persistent stored data without re-validation, (5) Plugins that display raw URL parameters in error/debug output

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1047: Windows Management Instrumentation
- T1059: Command and Scripting Interpreter
- T1133: External Remote Services
- T1078: Valid Accounts (privilege escalation to admin via XSS)

## Notes
Report demonstrates sophisticated understanding of URL encoding bypass via raw socket requests. Attacker notes that browser-based testing wouldn't work due to automatic URL encoding, showing knowledge of transport-layer mechanics. The vulnerability affects not just the initial attacker but any administrator visiting the dashboard, making it a distributed privilege escalation attack. Plugin was apparently already disabled when report submitted, suggesting the vendor may have been notified separately or the issue was discovered during review.

## Full report
<details><summary>Expand</summary>

There is another bug in the All In One Event Calendar plugin used on *drive.uber.com*. An attacker can inject arbitrary JavaScript in the administrative Dashboard of WordPress. The script would be evaluated under administrator privileges (as only logged-in administrators can view the Dashboard). Such script can use AJAX calls to achieve a server-side compromise unless some kind of special protections are in place.

The script can be injected by causing an error condition in the calendar plugin. One way to trigger an error is described below. Whenever this happens, the plugin disables itself and places an error message "banner" in the administrative Dashboard and shows it to any administrator who logs on afterwards.

The error details can be manipulated by the attacker and special HTML characters aren't filtered. The error message includes e.g. the URL which triggered the error, which is controllable by the attacker.

#Reproducing#

The attack requires sending a malformed HTTP request *without* encoding special characters in the URL. Therefore this can't be done with a normal web browser. For example a PERL script like this produces the request:
~~~~perl
#!/usr/bin/perl
open(NC,"|openssl s_client -connect drive.uber.com:443 -quiet") || die;
print NC "GET /oh/?ai1ec_js_widget=ai1ec_agenda_widget&render=true&events_per_page=$%&xss=<svg/onload=alert(/stored-xss/.source)>\r\n";
 HTTP/1.1\r\n";
print NC "Host: drive.uber.com\r\n";
print NC "\r\n";
close(NC);
~~~~
The HTTP response is a redirect back to the "front page", meaning the plugin couldn't render the calendar JSON data as supposed, but encountered an error condition.

Reproducing this of course requires that the plugin is reactivated (it's is currently disabled because I tested this).

Next, when an administrator logs on the system and is presented with the WordPress Dashboard, they should get an alert box, showing that the attacker-supplied JavaScript has been stored in the Dashboard.

Injecting another code won't work until the plugin is reactivated.

#Details#

The error in this case is an invalid format string in an SQL query, caused by the malformed *events_per_page* parameter. The XSS payload is included later in the URL above and gets included in the error message.

I have tested this bug on a local test server running WordPress and the All In One Event Calendar plugin. The difference is that instead of nginx my test server runs Apache. This, or other aspects of your server architecture *might* introduce differences in URL encoding etc. which could prevent the example from working (I'll test with nginx later).

#Impact#

Instead of showing an alert box, the script could use AJAX functions to e.g. create a new administrator user with a known password, or write arbitrary PHP code on the server via the plugin or theme editors. I've referred to such demonstrations in my previous reports.

#Fix#

I haven't reported this to the plugin author yet. One way to protect against this is to comment out the error detail generation in the file wp-content/plugins/all-in-one-event-calendar/lib/exception/handler.php, end of file (not tested).

</details>

---
*Analysed by Claude on 2026-05-24*
