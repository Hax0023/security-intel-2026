# RCE as Admin via wp_mkdir_p() Path Traversal Defeats WordPress Hardening

## Metadata
- **Source:** HackerOne
- **Report:** 436928 | https://hackerone.com/reports/436928
- **Submitted:** 2018-11-08
- **Reporter:** simonscannell
- **Program:** HackerOne
- **Bounty:** Not specified in writeup
- **Severity:** critical
- **Vuln:** Path Traversal, Arbitrary File Upload, Remote Code Execution, Privilege Escalation, Improper Access Control
- **CVEs:** None
- **Category:** memory-binary

## Summary
A path traversal vulnerability in WordPress's wp_mkdir_p() function allows authenticated administrators to bypass file permission hardening by manipulating the 'upload_path' option. By crafting a malicious path with directory traversal sequences, an attacker can chmod arbitrary directories to 0777 and subsequently upload executable PHP files to the theme directory for code execution.

## Attack scenario
1. Administrator logs into wp-admin with compromised credentials or XSS
2. Attacker navigates to options.php and modifies the 'upload_path' option to a path traversal payload (e.g., ../../../../../../../var/tmp/content/../../../../../../home/simon/html/wordpress/../../../../../../var/tmp/content)
3. User initiates media upload, triggering wp_upload_dir() which calls wp_mkdir_p() with the malicious path
4. wp_mkdir_p() iterates through path components and chmod's parent directories to 0777, making protected directories writable
5. Attacker uploads a shell.txt file containing PHP code to the now-writable theme directory via the media uploader
6. Attacker includes and executes the uploaded shell via post meta _wp_page_template, achieving arbitrary code execution

## Root cause
wp_mkdir_p() fails to sanitize the upload_path parameter before using it in path operations. The function's chmod loop iterates over unsanitized path segments, allowing traversal sequences (../) to reference and modify permissions on arbitrary parent directories. No realpath() validation prevents the attack.

## Attacker mindset
An authenticated admin-level attacker (or threat actor with admin compromise via XSS) exploits improper path handling to circumvent hardening defenses. The attacker recognizes that chmod operations on traversed paths can escalate permissions, enabling shell upload and code execution even when file editing and plugin installation are disabled.

## Defensive takeaways
- Sanitize and validate all user-supplied paths with realpath() before filesystem operations; reject paths containing traversal sequences
- Use basename() or similar functions to prevent directory traversal in upload path configuration
- Implement strict file upload validation: whitelist allowed upload directories and prevent changes to upload_path via options
- Apply principle of least privilege: restrict admin access to sensitive options like upload_path or disable filesystem modifications entirely
- Monitor and log changes to upload_path option; alert on suspicious patterns containing ../
- Use PHP open_basedir directive to restrict filesystem access beyond configured boundaries
- Remove file inclusion vulnerabilities by avoiding dynamic theme file inclusion (the _wp_page_template weakness)
- Disable file uploads entirely if not required; use object storage (S3) instead of local filesystem

## Variant hunting
Search for similar path traversal in other WordPress functions that manipulate directories: wp_delete_dir(), wp_safe_remote_post(), backup functions
Test other user-configurable path options (home_url, siteurl, theme_root_uri) for similar traversal
Examine chmod operations following mkdir() in other CMS platforms and web applications
Hunt for post-exploitation: check if other functions iterate over path components without sanitization
Investigate whether the _wp_page_template file inclusion can be exploited from lower privilege levels

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1548 - Abuse Elevation Control Mechanism
- T1543 - Create or Modify System Process
- T1555 - Credentials from Password Stores
- T1083 - File and Directory Discovery
- T1222 - File and Directory Permissions Modification

## Notes
This vulnerability is particularly dangerous because it defeats hardening best practices (safe mode, directory restrictions, disabled file editing). The attack chain links path traversal → permission escalation → file upload → code execution. The writeup references a companion RCE-as-Author report for exploitation details. WordPress administrators should immediately patch wp_mkdir_p() and audit instances where user-controlled paths reach filesystem functions.

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
*Analysed by Claude on 2026-05-11*
