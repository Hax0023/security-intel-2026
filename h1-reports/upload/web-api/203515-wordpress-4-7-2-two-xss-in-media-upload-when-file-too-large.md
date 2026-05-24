# WordPress 4.7.2 - Two XSS Vulnerabilities in Media Upload Error Messages

## Metadata
- **Source:** HackerOne
- **Report:** 203515 | https://hackerone.com/reports/203515
- **Submitted:** 2017-02-05
- **Reporter:** skansing
- **Program:** WordPress
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Stored XSS, DOM-based XSS, Improper Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
An attacker can inject malicious JavaScript into a filename that triggers XSS when WordPress displays file upload error messages to administrators. The vulnerability occurs when a file exceeds the maximum upload size limit, as the unescaped filename is interpolated directly into the DOM without sanitization.

## Attack scenario
1. Attacker creates a file larger than the WordPress upload size limit with a malicious filename containing XSS payload (e.g., 'Dinosaurs secret life<img src=x onerror=alert(1)>.png')
2. Attacker tricks or socially engineers an administrator to upload this file to the WordPress media library
3. WordPress validates file size before type validation and generates an error message in script-loader.php
4. The error message template 'file_exceeds_size_limit' interpolates the untrusted filename using string replace()
5. JavaScript in handlers.min.js appends the message directly to the DOM via jQuery without escaping
6. Malicious script in the filename executes in the administrator's browser with full privileges

## Root cause
The filename from the file upload object is directly interpolated into error messages using string replace() and then appended to the DOM without HTML escaping. The vulnerability exists in the uploadSizeError() function which constructs error messages by replacing placeholder tokens with the unvalidated filename.

## Attacker mindset
An attacker could exploit this to steal administrator session tokens, create backdoor accounts, modify site content, or pivot to server compromise. The attack requires social engineering to trick an admin into uploading a malicious file, but succeeds against all WordPress versions without additional user interaction once the file is selected.

## Defensive takeaways
- Always HTML-escape user-controlled data before inserting into DOM, especially filenames and file paths
- Use safe DOM manipulation methods that automatically escape (e.g., jQuery .text() instead of raw string concatenation with .html())
- Implement a whitelist-based filename sanitization that removes or encodes special characters before processing
- Validate and sanitize file uploads before generating user-facing error messages
- Consider removing filenames entirely from error messages in favor of generic messages
- Apply Content Security Policy (CSP) headers to mitigate XSS impact
- Use security-focused templating engines that escape by default
- Implement file upload restrictions at multiple validation layers

## Variant hunting
Search for similar patterns in: (1) other upload handlers in WordPress core and plugins, (2) error message generation functions that interpolate filenames, (3) JavaScript code using .replace() with user input and .append()/.html(), (4) other file validation routines that generate DOM output, (5) plupload/SWFupload integration points in other applications

## MITRE ATT&CK
- T1190
- T1566
- T1204.001

## Notes
This vulnerability affects freshly installed WordPress 4.7.2. The PoC uses a 20MB file but any file exceeding the configured upload limit will trigger the vulnerability. File type validation occurs after size validation, so any file extension can be used. The vulnerability impacts both plupload and SWFupload code paths. This is a critical issue for sites where administrators may be tricked into uploading files from untrusted sources.

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
*Analysed by Claude on 2026-05-24*
