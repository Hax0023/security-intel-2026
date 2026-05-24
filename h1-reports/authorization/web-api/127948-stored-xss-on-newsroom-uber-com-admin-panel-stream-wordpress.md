# Stored XSS in Stream WordPress Plugin via wp_redirect Hook - newsroom.uber.com

## Metadata
- **Source:** HackerOne
- **Report:** 127948 | https://hackerone.com/reports/127948
- **Submitted:** 2016-04-03
- **Reporter:** jouko
- **Program:** Uber
- **Bounty:** Not specified
- **Severity:** critical
- **Vuln:** Stored Cross-Site Scripting (XSS), Improper Input Sanitization, Insufficient Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
The Stream WordPress plugin logs user activity including plugin editor redirects without proper sanitization of the 'file' query parameter. An unauthenticated attacker can inject malicious JavaScript through a crafted Referer header that gets stored in the activity log and executed in the admin panel with administrator privileges. This can lead to complete site compromise and server-side code execution.

## Attack scenario
1. Attacker crafts a malicious HTTP request with a Referer header containing XSS payload in the plugin-editor.php file parameter
2. Attacker sends curl request to wp-login.php?action=postpass which triggers a redirect to the attacker-controlled Referer URL
3. Stream plugin's wp_redirect hook intercepts the redirect and extracts the unsanitized 'file' parameter from the URL
4. The malicious payload is logged to Stream's database table without HTML sanitization
5. When administrator accesses the Stream activity log in WordPress dashboard, the stored JavaScript payload executes with admin privileges
6. Attacker can modify plugin/theme files via WordPress editors or inject PHP code for persistent server compromise

## Root cause
The Stream plugin's callback_wp_redirect function extracts the 'file' query parameter from redirect URLs and logs it directly without sanitization. The logged data is later displayed in the admin panel without proper HTML encoding or escaping, allowing stored XSS execution.

## Attacker mindset
Target widely-used WordPress plugins with logging functionality as they are likely installed on many sites. Exploit the trust administrators place in internal activity logs by injecting malicious content that will be rendered without scrutiny. Leverage unauthenticated access to trigger the vulnerability, making it accessible before any authentication controls.

## Defensive takeaways
- Always sanitize user-controlled input at the point of collection, especially query parameters and HTTP headers
- Apply context-appropriate output encoding when displaying logged data in admin interfaces (HTML escape for HTML context)
- Use WordPress sanitization functions like sanitize_text_field() and esc_html() consistently in logging code
- Implement Content Security Policy (CSP) headers to mitigate XSS impact
- Validate and whitelist expected parameters rather than blindly extracting from URLs
- Apply principle of least privilege - limit what data can be included in logs
- Regularly audit logging and activity monitoring plugins for proper data handling
- Use WordPress escaping functions like wp_kses_post() when rendering user-controlled data in admin panels

## Variant hunting
Search for other WordPress plugins that implement activity logging or audit trails, especially those that hook into wp_redirect, wp_safe_remote_get, or other request-handling functions. Look for plugins that log HTTP headers (Referer, User-Agent, etc.) without sanitization. Check for similar issues in plugins that monitor plugin/theme editor access or file operations. Examine other Stream plugin versions and connectors for similar unsanitized parameter logging.

## MITRE ATT&CK
- T1190
- T1059
- T1505
- T1110

## Notes
This vulnerability demonstrates the danger of logging unsanitized user-controlled data and displaying it in privileged interfaces. The attack is particularly effective because it targets trusted internal tools (activity logs) that administrators may not scrutinize carefully. The combination of unauthenticated access + stored XSS + admin execution context creates a critical severity issue. The vulnerability affects all installations of Stream plugin version 1.4.9 and potentially earlier versions.

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
*Analysed by Claude on 2026-05-24*
