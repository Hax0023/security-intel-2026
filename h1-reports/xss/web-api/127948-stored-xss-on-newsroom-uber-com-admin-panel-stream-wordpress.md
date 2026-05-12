# Stored XSS on newsroom.uber.com admin panel via Stream WordPress plugin

## Metadata
- **Source:** HackerOne
- **Report:** 127948 | https://hackerone.com/reports/127948
- **Submitted:** 2016-04-03
- **Reporter:** jouko
- **Program:** Uber
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Stored Cross-Site Scripting (XSS), Insufficient Input Sanitization, Improper Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
The Stream WordPress plugin on newsroom.uber.com fails to sanitize HTTP redirect URLs before logging them, allowing unauthenticated attackers to inject malicious JavaScript into activity logs. When administrators view the logs, the stored XSS payload executes with admin privileges, enabling further compromise including PHP code injection through the plugin editor.

## Attack scenario
1. Attacker crafts a malicious Referer header containing JavaScript payload embedded in a fake plugin-editor.php URL with XSS payload in the 'file' parameter
2. Attacker sends curl request to wp-login.php?action=postpass with the malicious Referer header, triggering a redirect
3. Stream plugin's wp_redirect hook intercepts the redirect and extracts the 'file' parameter without sanitization
4. Plugin logs the unsanitized 'file' parameter value (containing XSS payload) to the Stream activity log in the database
5. Administrator accesses the WordPress Dashboard and clicks the Stream tab to view activity logs
6. Stored JavaScript payload executes in admin's browser with administrator privileges, allowing cookie theft, admin account creation, or PHP code injection via plugin/theme editor

## Root cause
The Stream plugin's connector/installer.php callback_wp_redirect() function extracts the 'file' query parameter from redirected URLs and passes it directly to the self::log() function without HTML sanitization or output encoding. The logged data is subsequently displayed in the admin panel without proper escaping, creating a stored XSS vulnerability.

## Attacker mindset
Exploit the plugin's activity logging feature as an attack vector by abusing WordPress's redirect mechanism to inject malicious payloads without authentication. Leverage the trust administrators place in viewing their own activity logs to bypass security awareness. Escalate from stored XSS to remote code execution by leveraging admin privileges to modify PHP files.

## Defensive takeaways
- Sanitize and validate all user-controlled input before logging, especially URL parameters and HTTP headers
- Apply context-appropriate output encoding (HTML entity encoding) when displaying logged data in the admin panel
- Implement Content Security Policy (CSP) headers to mitigate XSS impact in admin areas
- Use WordPress escaping functions like esc_html(), esc_attr(), or wp_kses_post() when displaying logged content
- Validate redirect URLs against a whitelist of expected domains/paths before logging
- Apply principle of least privilege - restrict plugin/theme editor access when not needed
- Implement security headers to prevent iframe injection of admin panels
- Regularly audit activity logging plugins for proper input validation and output encoding

## Variant hunting
Search for other Stream plugin hooks that capture URL parameters or HTTP headers without sanitization (e.g., wp_safe_remote_get, wp_redirect variants). Examine other WordPress plugins with activity logging features for similar unsanitized parameter logging. Test theme editor paths with the same technique. Check if query parameters from failed login attempts or other early WordPress hooks are logged without sanitization.

## MITRE ATT&CK
- T1190
- T1592
- T1598
- T1539
- T1547

## Notes
The vulnerability is particularly severe because it requires no authentication and can be triggered by simply making a crafted HTTP request to wp-login.php. The attack leverages WordPress's built-in redirect functionality, making it difficult to detect at the HTTP level. The payload execution context (admin privileges) enables complete site compromise and potential server-side code execution through the plugin/theme editor functionality.

## Full report
<details><summary>Expand</summary>

*newsroom.uber.com* uses a WordPress plugin called Stream to log user activity. In some cases the logged events aren't sanitized properly and can contain HTML tags and JavaScript. An unauthenticated user can produce such a log message to inject JavaScript in the admin panel. When an administrator views the log, the script would be evaluated with administrator privilegs and can (under normal setup) be further used to inject attacker-supplied PHP code on the server.

#Reproducing#
The following command line can be used to inject JavaScript in the log with the *curl* tool:
~~~~
curl -v -H 'Referer: /hello?plugin-editor.php&file=aaa%3cscript%3ealert(%27stored%20xss%27);%3c/script%3e' --data 'post-password=foo' 'https://newsroom.uber.com/wp-login.php?action=postpass'
~~~~
Next, if an administrator clicks the Stream tab in the WordPress Dashboard, an alert box should pop up.

#Details#
The Stream plugin hooks many WordPress events to log user activity. In the file *connectors/installer.php* there is a *wp_redirect()* hook - the plugin checks every URL redirection to see if it involved the plugin editor. The code, compacted a bit:

~~~~php
        public static function callback_wp_redirect( $location ) {
                if ( ! preg_match( '#(plugin)-editor.php#', $location, $match ) ) {
                        return $location;
                }
                $type = $match[1];
                list( $url, $query ) = explode( '?', $location );
                $query = wp_parse_args( $query );
                $file  = $query['file'];
                if ( empty( $query['file'] ) ) {
                        return $location;
                }
                /* SNIP ... */ elseif ( 'plugin' === $type ) {
                        global $plugin, $plugins;
                        $plugin_base = current( explode( '/', $plugin ) );
                        foreach ( $plugins as $key => $plugin_data ) {
                                if ( $plugin_base === current( explode( '/', $key ) ) ) {
                                        $name = $plugin_data['Name'];
                                        break;
                                }
                        }
                }
                self::log(
                        _x(
                                'Edited %1$s: %2$s',
                                'Plugin/theme editing. 1: Type (plugin/theme), 2: Plugin/theme name',
                                'stream'
                        ),
                        compact( 'type', 'name', 'file' ),null, array( $type . 's' => 'edited' ));

~~~~
So if there is a redirect to a URL containing the string "plugin-editor.php" with a *file* query parameter, then the activity is logged. The *file* query parameter is included in the log entry.

The event is saved in Stream's database table and shown on the main tab of the plugin without sufficient HTML sanitizing.

There are many ways to generate an HTTP redirect in WordPress. The method used in the above example is requesting *wp-login.php* which, with appropriate arguments, redirects the browser back to the Referer: header's value.

#Impact#
The JavaScript stored by an unauthenticated attacker would get executed with administrator privileges, thus having full control over the site contents. Under a normal WordPress setup it could also modify existing PHP files via the plugin or theme editors, leading to server-side compromise.

I tested this on my local test system with the latest WordPress and Stream 1.4.9.

</details>

---
*Analysed by Claude on 2026-05-12*
