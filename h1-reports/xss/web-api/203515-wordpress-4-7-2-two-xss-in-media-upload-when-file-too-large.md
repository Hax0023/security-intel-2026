# WordPress 4.7.2 - Stored XSS in Media Upload Error Messages via Malicious Filenames

## Metadata
- **Source:** HackerOne
- **Report:** 203515 | https://hackerone.com/reports/203515
- **Submitted:** 2017-02-05
- **Reporter:** skansing
- **Program:** WordPress
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Stored Cross-Site Scripting (XSS), Improper Input Validation, Unsafe DOM Manipulation
- **CVEs:** None
- **Category:** web-api

## Summary
WordPress 4.7.2 fails to sanitize filenames in media upload error messages, allowing attackers to inject malicious JavaScript through crafted filenames that exceed upload size limits. When a victim attempts to upload a file with XSS payload in the filename, the error message displayed in the admin panel executes the attacker's script without escaping.

## Attack scenario
1. Attacker crafts a filename containing XSS payload: 'Dinosaurs secret life<img src=x onerror=alert(1)>.png'
2. Attacker creates a file larger than the site's upload limit (e.g., 20MB) with the malicious filename
3. Attacker distributes the file or tricks a WordPress admin into uploading it via media upload interface
4. Administrator navigates to wp-admin/media-new.php and uploads the oversized file
5. WordPress triggers FILE_SIZE_ERROR and passes unsanitized filename to uploadSizeError() function
6. JavaScript in handlers.min.js performs string replacement and appends error message to DOM without escaping, executing the payload

## Root cause
The uploadSizeError() function in handlers.min.js directly interpolates the user-supplied filename into a template string without HTML escaping before appending to the DOM. The filename originates from the file object's 'name' attribute, which is never sanitized throughout the error handling flow.

## Attacker mindset
An attacker recognizes that file upload validation occurs after error message generation, allowing filename-based XSS. By crafting oversized files, the attacker bypasses file type validation and exploits the admin notification system to execute scripts in the victim's browser context with admin privileges.

## Defensive takeaways
- Always HTML-escape user-controlled input before inserting into DOM, especially filenames
- Use textContent or proper escaping utilities instead of string concatenation for DOM manipulation
- Validate and sanitize filenames at the earliest point in the upload pipeline
- Apply Content Security Policy (CSP) to prevent inline script execution
- Validate file uploads before generating user-facing error messages
- Use jQuery methods like .text() instead of direct HTML string concatenation
- Implement defense-in-depth: sanitize at server and client levels

## Variant hunting
Check other WordPress error messages that interpolate filenames (e.g., duplicate file warnings, format validation failures)
Review all uses of plupload and other upload handlers for similar XSS patterns
Search for string.replace() patterns with user input in media upload flows
Audit other AJAX upload handlers (swfupload) mentioned in the vulnerability description
Test other file operations that display filenames (delete, rename, move operations)
Check custom plugins that handle file uploads for identical patterns

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1204 - User Execution
- T1059.007 - Command and Scripting Interpreter (JavaScript)

## Notes
This vulnerability affects the browser-based admin panel and requires victim interaction to upload a file. The attack is pre-authentication possible if media uploads are accessible. The vulnerability exists in client-side JavaScript code (handlers.min.js) but the root cause is insufficient server-side sanitization of the filename in localization messages. Version 4.7.2 is vulnerable; patched versions properly escape filenames using esc_attr() or similar functions.

## Full report
<details><summary>Expand</summary>

Description
-------------------
An attacker can inject a malicious script in to the filename which a victim tries to upload leading to XSS inside the administrators control panel.

Two different "file to large" cases end up in interpolating the file name and appending it into DOM unsanitized leading to XSS.

I have attached pictures of one of the cases, in the attached case the file was 12.4 MB, in a freshly installed environment. For reproduction note that any file type can be used (.jar whatever) as the vuln happens before the type is validated.

PoC
-------------------
Create a 20MB file called 

`Dinosaurs secret life<img src=x  onerror=alert(1)>.png`

Goto your wordpress site `http://127.0.0.1/wp-admin/media-new.php` and drag`n`drop or use file manager or choose the file via. the "Select Files" button.

A error will appear with `... exceeds the maximum upload size for this site.` along with a alert box to display that the payload has been executed.

Details on XSS
-------------------
The file `script-loader.php` prepares an array of messages for use later.

```
	// error message for both plupload and swfupload
	$uploader_l10n = array(
                ...
		'file_exceeds_size_limit' => __('%s  exceeds the maximum upload size for this site.'),
		'big_upload_failed' => __('Please try uploading this file with the %1$sbrowser uploader%2$s.'),
		...
	);
```

The payload will be injected into the `%s` in the key `file_exceeds_size_limit`.

This happens because the `$uploader_l10n` is passed to `handlers.min.js` (non minified version shown)
 and interpolated without escaping the value previously.

First the value passes trough a error case 
```
// $uploader_l10n
case plupload.FILE_SIZE_ERROR:
			uploadSizeError(uploader, fileObj); // fileObj contains the filename payload in name attribute.
			break;
....
if ( max > hundredmb && fileObj.size > hundredmb )
				wpFileError( fileObj, pluploadL10n.big_upload_failed.replace('%1$s', '<a class="uploader-html" href="#">').replace('%2$s', '</a>') );
```

and lastely interpolated and appended to the dom.

```

function uploadSizeError( up, file, over100mb ) {
	var message;

	if ( over100mb )
		message = pluploadL10n.big_upload_queued.replace('%s', file.name) + ' ' + pluploadL10n.big_upload_failed.replace('%1$s', '<a class="uploader-html" href="#">').replace('%2$s', '</a>');
	else
		message = pluploadL10n.file_exceeds_size_limit.replace('%s', file.name);


	jQuery('#media-items').append('<div id="media-item-' + file.id + '" class="media-item error"><p>' + message + '</p></div>');
	up.removeFile(file);
}
```

The critical lines are 
```
message = pluploadL10n.big_upload_queued.replace('%s', file.name) + ' ' + pluploadL10n.big_upload_failed.replace('%1$s', '<a class="uploader-html" href="#">').replace('%2$s', '</a>');
	else
		message = pluploadL10n.file_exceeds_size_limit.replace('%s', file.name);
```

# Suggested fix:
Remove the filename or escape safely in context.

</details>

---
*Analysed by Claude on 2026-05-12*
