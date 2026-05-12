# Arbitrary File Deletion in WordPress Core via Unsanitized Attachment Metadata

## Metadata
- **Source:** HackerOne
- **Report:** 291878 | https://hackerone.com/reports/291878
- **Submitted:** 2017-11-20
- **Reporter:** b258ea62bf297b02afa9854
- **Program:** WordPress
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Arbitrary File Deletion, Path Traversal, Insufficient Input Validation, Privilege Escalation
- **CVEs:** None
- **Category:** web-api

## Summary
WordPress fails to sanitize the 'thumb' parameter in attachment metadata, allowing authenticated users with media editing permissions to delete arbitrary files via path traversal. This can lead to remote code execution by deleting wp-config.php or information disclosure by removing access control files like .htaccess.

## Attack scenario
1. Attacker with media editing permissions logs into WordPress admin panel
2. Attacker uploads a legitimate image file and obtains its post ID and nonce token
3. Attacker crafts malicious POST request to wp-admin/post.php with action=editattachment and thumb parameter containing path traversal payload (e.g., ../../../../wp-config.php)
4. Unsanitized payload is stored in database via wp_update_attachment_metadata() without validation
5. Attacker deletes the attachment from WordPress admin interface
6. wp_delete_attachment() retrieves the malicious thumb value from database and passes it directly to unlink() function, deleting arbitrary file

## Root cause
WordPress stores user-supplied 'thumb' parameter directly into attachment metadata without sanitization or validation in wp-admin/post.php. The wp_delete_attachment() function later uses this unsanitized value in a file path concatenation and passes it to unlink() without proper path validation or canonicalization.

## Attacker mindset
Attacker with legitimate WordPress account (contributor, editor, or admin with media permissions) seeks to escalate impact by deleting critical files. The attack is subtle because payloads are deleted from database after exploitation and unlink() suppression operator masks failures, making detection difficult in logs.

## Defensive takeaways
- Implement strict whitelist validation for attachment metadata fields - only allow expected filename formats
- Sanitize and validate all user input before storage in database, not just at output
- Canonicalize file paths using realpath() and verify resolved paths stay within expected upload directory
- Implement path traversal detection using basename() validation and reject sequences like ../ in metadata
- Use wp_safe_remote_post() patterns with nonce verification for file operations
- Log all attachment metadata modifications and file deletion attempts with details
- Consider implementing capability checks beyond simple 'edit_post' for attachment modifications
- Use WordPress filesystem API (WP_Filesystem) which provides additional safety checks
- Remove error suppression operator (@) from unlink() to surface failures in debug logs

## Variant hunting
Check other attachment metadata fields for similar unsanitized storage patterns (_wp_attachment_image_alt, etc.)
Search for other uses of unlink() with user-influenced paths throughout WordPress core and plugins
Review all post/attachment edit handlers that directly assign $_POST values to metadata
Examine media handling in multisite installations for similar vulnerabilities
Check plugin ecosystem for similar attachment metadata handling in custom post types
Look for path traversal in other file handling functions using metadata values

## MITRE ATT&CK
- T1190
- T1489
- T1566
- T1083
- T1491

## Notes
This vulnerability requires authentication with media editing capabilities, limiting attack surface. However, it's particularly dangerous in multi-author blogging platforms, WordPress networks, and any setup with untrusted contributors. The ability to delete wp-config.php can trigger automatic WordPress reinstallation wizard, allowing attacker to reconfigure database credentials. The suppression of PHP errors via @ operator is a significant security anti-pattern that masks exploitation.

## Full report
<details><summary>Expand</summary>

Vulnerable place 1: `wp-admin/post.php`
`$newmeta['thumb']` is placed into DB not sanitized directly from user input.
```
case 'editattachment':
    check_admin_referer('update-post_' . $post_id);
    // Don't let these be changed
    unset($_POST['guid']);
    $_POST['post_type'] = 'attachment';
    // Update the thumbnail filename
    $newmeta = wp_get_attachment_metadata( $post_id, true );
    $newmeta['thumb'] = $_POST['thumb'];
    wp_update_attachment_metadata( $post_id, $newmeta );
``` 
Vulnerable place 2: `wp_delete_attachment` 
There we have `$meta = wp_get_attachment_metadata( $post_id );` and below in the code:
```
if ( ! empty($meta['thumb']) ) {
        // Don't delete the thumb if another attachment uses it.
        if (! $wpdb->get_row( $wpdb->prepare( "SELECT meta_id FROM $wpdb->postmeta WHERE meta_key = '_wp_attachment_metadata' AND meta_value LIKE %s AND post_id <> %d", '%' . $wpdb->esc_like( $meta['thumb'] ) . '%', $post_id)) ) {
            $thumbfile = str_replace(basename($file), $meta['thumb'], $file);
            /** This filter is documented in wp-includes/functions.php */
            $thumbfile = apply_filters( 'wp_delete_file', $thumbfile );
            @ unlink( path_join($uploadpath['basedir'], $thumbfile) );
        }
    }
```
This means we can craft any value from the `wp-admin` for `thumb` property and that value to be sent towards `@unlink`

How to reproduce:

1. Upload image via media menu e.g. new
2. Go to edit post (old fashioned way)
3. Grad the `id`, `_wpnonce` and choose your payload `../../../../wp-config.php`
4. Craft your payload(set auth cookies, ua, referrers, ...): 
```
curl 'http://localhost/ripsa/wpvuln/wp-admin/post.php?post=[your_postid]&action=editattachment&_wpnonce=[yournonce]' -H 'place your client headers: ua, cookies in order to mimic the authenticated user ' -d 'thumb=../../../../wp-config-slavco.php' --compressed 
```
5. Delete the file from the admin

Impact:
1. Requires user that have permission to manipulate media files / posts
2. Hard to be spotted because:
2.1 Payload is deleted from DB
2.2 `@unlink` won't rise error in case of any failed attempts
3. Affects many blogging/publishing, e-commerce, ...  setups.

Attack:
1. Delete `wp-config.php` and relaunch wp setup with remote attackers db - RCE 
2. Delete `.htaccess` or any another `index.html`/`index.php` in order to disclose any stored data under web accessible directory


</details>

---
*Analysed by Claude on 2026-05-12*
