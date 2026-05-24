# RCE as Admin via wp_mkdir_p() Path Traversal and Permission Manipulation

## Metadata
- **Source:** HackerOne
- **Report:** 436928 | https://hackerone.com/reports/436928
- **Submitted:** 2018-11-08
- **Reporter:** simonscannell
- **Program:** WordPress
- **Bounty:** Not specified
- **Severity:** critical
- **Vuln:** Path Traversal, Arbitrary File Upload, Privilege Escalation, Remote Code Execution
- **CVEs:** None
- **Category:** memory-binary

## Summary
A critical vulnerability in WordPress's wp_mkdir_p() function allows authenticated administrators to bypass filesystem hardening mechanisms through path traversal and directory permission manipulation. By setting the upload_path option to a crafted traversal payload, attackers can chmod directories to 0777 permissions and subsequently upload and execute arbitrary PHP code, defeating all standard WordPress hardening recommendations.

## Attack scenario
1. Attacker gains admin-level access to WordPress installation (or exploits XSS to admin account)
2. Attacker navigates to wp-admin/options.php and modifies the 'upload_path' option with a crafted path traversal payload containing ../sequences and symlink/relative path manipulation
3. Attacker triggers a media upload action to invoke wp_upload_dir() and wp_mkdir_p()
4. wp_mkdir_p() traverses the malicious path, identifies a writable parent directory (/var/tmp/), and inherits its 777 permissions
5. The function iteratively chmod's each directory component in the traversal path to 0777, including the WordPress installation root directory
6. With restored write permissions, attacker uploads a PHP shell disguised as .txt to the theme directory via the hijacked upload_path
7. Attacker includes the uploaded shell via post meta value _wp_page_template, achieving arbitrary code execution

## Root cause
The wp_mkdir_p() function does not validate or sanitize the upload_path option before processing it. The dirname() iteration for permission inheritance operates on unresolved relative paths containing ../ sequences, allowing traversal outside intended directories. Additionally, the chmod() operation applies inherited permissions to all path components without validating that they reside within safe boundaries.

## Attacker mindset
An administrator with malicious intent or one whose account has been compromised seeks to maintain persistence and execute arbitrary code despite filesystem hardening. The attacker recognizes that wp_mkdir_p() is a trusted internal function and leverages its permission-inheritance logic as a feature rather than a flaw. By combining path traversal with permission manipulation, the attacker defeats both access controls and file permission restrictions in a single attack chain.

## Defensive takeaways
- Sanitize and validate the upload_path option—restrict it to relative paths within wp-content/ and reject any paths containing ../ or absolute paths outside ABSPATH
- Use realpath() to resolve paths to their canonical form before processing, rejecting any paths that escape the intended directory boundary
- Limit chmod operations in wp_mkdir_p() to only the final target directory, not intermediate path components
- Implement a whitelist of permissible upload directories and reject any admin-configurable path that doesn't match
- Apply principle of least privilege: ensure WordPress directories are owned by the web server user with minimal necessary permissions (755 for directories, 644 for files)
- Disable admin access to wp-admin/options.php for all but the most trusted administrators; consider removing this interface entirely in production
- Monitor and alert on unexpected chmod operations or permission changes to WordPress core directories
- Implement file upload restrictions that validate content type and reject PHP/executable files regardless of extension

## Variant hunting
Search for other WordPress functions that accept user-controlled path inputs and process them through dirname() iteration without proper validation. Examine plugin upload handlers, custom media library implementations, and any function wrapping wp_mkdir_p(). Test for similar traversal vulnerabilities in backup/restore plugins, theme installers, and any feature allowing administrators to configure arbitrary directory paths. Check if comparable permission-inheritance logic exists in plugin-specific file operations.

## MITRE ATT&CK
- T1190
- T1548.002
- T1083
- T1548
- T1021

## Notes
This vulnerability is particularly dangerous because it requires only admin-level access, which in WordPress is often accessible through XSS vulnerabilities in plugins or themes. The attack completely nullifies standard hardening recommendations (Safe Mode, read-only directories, disabled file edits, plugin upload restrictions). The vulnerability demonstrates a critical design flaw: trusting dirname() operations on unsanitized user input for security-relevant operations. This report references an accompanying 'Remote Code Execution as Author' vulnerability involving the _wp_page_template post meta, which when combined creates a complete exploitation chain. The vulnerability was filed against WordPress core and represents a fundamental architectural issue in how WordPress handles user-configurable paths.

## Full report
<details><summary>Expand</summary>

This vulnerability was found when I found myself in the following scenario:

My collegue set up WordPress on his local machine and challenged me to hack it. Before he gave me admin access he used the following hardeing mechanisms:

1. PHP Safe mode
2. The entire web directory was not writable
3. Disabled WordPress File edit
4. Disabled the ability to install plugins

The RCE demonsrated here allowed me to bypass all these restrictions and still execute arbitrary code on the machine. 

At fault is the wp_mkdir_p(); function.

## Overwriting directory permissions

wp_mkdir_p() is called by wp_upload_dir() when a user wants to upload a new media file. If the upload directory does not exist, WordPress will attempt to create it. WordPress determines what the upload directory is dynamically by calling get_option('upload_path'). 

```
function _wp_upload_dir( $time = null ) {
	$siteurl = get_option( 'siteurl' );
	$upload_path = trim( get_option( 'upload_path' ) );

	if ( empty( $upload_path ) || 'wp-content/uploads' == $upload_path ) {
		$dir = WP_CONTENT_DIR . '/uploads';
	} elseif ( 0 !== strpos( $upload_path, ABSPATH ) ) {
		// $dir is absolute, $upload_path is (maybe) relative to ABSPATH
		$dir = path_join( ABSPATH, $upload_path );
	} else {
		$dir = $upload_path;
```

Administrators can update that option to an arbitrary value in wp-admin/options.php

The value returned by _wp_upload_dir() is then passed to wp_mkdir_p();

```
function wp_mkdir_p( $target ) {
...

	if ( file_exists( $target ) )
		return @is_dir( $target );

	// We need to find the permissions of the parent folder that exists and inherit that.
	$target_parent = dirname( $target );
	while ( '.' != $target_parent && ! is_dir( $target_parent ) && dirname( $target_parent ) !== $target_parent ) {
		$target_parent = dirname( $target_parent );
	}

	// Get the permission bits.
	if ( $stat = @stat( $target_parent ) ) {
		$dir_perms = $stat['mode'] & 0007777;
	} else {
		$dir_perms = 0777;
	}

	if ( @mkdir( $target, $dir_perms, true ) ) {

		/*
		 * If a umask is set that modifies $dir_perms, we'll have to re-set
		 * the $dir_perms correctly with chmod()
		 */
		if ( $dir_perms != ( $dir_perms & ~umask() ) ) {
			$folder_parts = explode( '/', substr( $target, strlen( $target_parent ) + 1 ) );
			for ( $i = 1, $c = count( $folder_parts ); $i <= $c; $i++ ) {
				@chmod( $target_parent . '/' . implode( '/', array_slice( $folder_parts, 0, $i ) ), $dir_perms );
			}
		}

		return true;
	}

	return false;
}
```
In order to create the directory correctly, WordPress will first find out what the parent directory is by iterating over the path via dirname(). WordPress then copies the permissions of the parent directory so that the new upload directory will inherit those permissions.

if mkdir returns true, a check is made if our umask differs from the $dir_perms. If so, the $target path is exploded and  each part of it is chmod'd with the permissions of the $target_parent.

This function is vulnerable to a path traversal.


If an attacker sets 'upload_path' to

```
../../../../../../../var/tmp/content/../../../../../../home/simon/html/wordpress/../../../../../../var/tmp/content
```

the $target_parent will be 
```
../../../../../../../var/tmp/
```
which is writable, so the target permissions will be 777 (read, write, execute)

Since realpath() of the payload is /var/tmp/content and /var/tmp is writable, the call to mkdir() is successful. Then the call to umask() is made, which we can pass and then the $target path is exploded
and each part of it is appended to $target_parent (../../../../../../../var/tmp/) and then chmod with the permission bit of 777. 

This means at some point in the iteration the following call is made to chmod:

```
chmod('../../../../../../../var/tmp/content/../../../../../../home/simon/html/wordpress/', 0777);
```

This allowed me to set all directories writable again and bypass the first hardening mechanism.


## Uploading and executing a shell

In my other report, 'Remote Code Execution as Author' I have demonstrated how any file in the theme directory can be included and executed via the post meta value of _wp_page_template. Please read that report if the following is unclear.

By setting the upload_path to the theme directory and uploading a shell.txt with the content <?php phpinfo(); ?>

and then including it, I was able to execute arbitrary code.

## Impact

This is a universal code execution for administrators and dangers hardend WordPress installations and pretty much defeats https://codex.wordpress.org/Hardening_WordPress 

Depending on the plugins available of a target site, a simple reflected XSS can lead to RCE, even if all instructions for hardening are followed.

</details>

---
*Analysed by Claude on 2026-05-24*
