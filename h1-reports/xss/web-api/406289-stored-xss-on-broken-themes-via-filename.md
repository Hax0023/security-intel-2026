# Stored XSS on Broken Themes via Malicious Folder Name

## Metadata
- **Source:** HackerOne
- **Report:** 406289 | https://hackerone.com/reports/406289
- **Submitted:** 2018-09-06
- **Reporter:** apapedulimu
- **Program:** WordPress
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Stored Cross-Site Scripting (XSS), Improper Input Validation, Insufficient Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
WordPress fails to sanitize or encode theme folder names when displaying broken theme error messages, allowing an attacker to create a theme folder with XSS payload in its name that executes when viewed on the themes admin page. The vulnerability exists because theme directory names are reflected directly into the page without proper HTML encoding.

## Attack scenario
1. Attacker gains filesystem access to the WordPress themes directory (via compromised hosting, file upload vulnerability, or direct server access)
2. Attacker creates a new folder in wp-content/themes/ with a malicious name containing XSS payload: '<img src=x onerror=alert(1)>'
3. Attacker ensures the theme is broken by removing required files like style.css or adding invalid content
4. Administrator navigates to WordPress Appearance > Themes page
5. WordPress displays the broken theme error message with the unsanitized folder name
6. XSS payload in folder name executes in the administrator's browser, potentially stealing session cookies or performing admin actions

## Root cause
WordPress theme management code displays theme folder/directory names in error messages without applying HTML entity encoding or sanitization. While WordPress sanitizes filenames during upload, it does not validate or encode directory names that already exist on the filesystem when displaying theme information.

## Attacker mindset
An attacker with filesystem access (or via a file upload vulnerability) seeks to achieve stored XSS persistence through metadata that administrators will inevitably view. By exploiting the assumption that filesystem paths are 'safe', the attacker bypasses client-side upload validation that WordPress normally applies.

## Defensive takeaways
- Apply HTML entity encoding (htmlspecialchars/esc_html) to all user-controlled and filesystem-derived data before output, regardless of source
- Validate and sanitize theme directory names on filesystem scan operations, not just during upload
- Implement Content Security Policy (CSP) headers to mitigate XSS impact even if output encoding is missed
- Regularly scan theme directories for malicious or suspicious folder names during theme discovery
- Use a whitelist of allowed characters for theme directory names and reject or sanitize non-compliant names
- Apply the same validation rules to filesystem artifacts as to user-uploaded content

## Variant hunting
Check plugin folder names for similar unencoded output in admin pages
Audit any admin pages that list filesystem directories or files for output encoding gaps
Test for similar issues in theme/plugin error messages, debug logs, or theme information displays
Examine backup/restore functionality for similar vulnerabilities with restored theme names
Look for XSS in theme preview/thumbnail generation functionality
Test multisite installations where theme folder enumeration might be exposed to lower-privileged users

## MITRE ATT&CK
- T1190
- T1598
- T1566

## Notes
This vulnerability requires filesystem access to exploit, but can be chained with file upload vulnerabilities for remote exploitation. The 'stored' nature means any admin viewing the themes page is affected. The POC demonstrates this is reliably exploitable. WordPress's own upload validation shows they are aware of this threat model for uploads but failed to apply it to existing filesystem artifacts.

## Full report
<details><summary>Expand</summary>

Hi, I've found something here, 

##Description 
XSS Stored because filename of theme when broken, So when theme is broken, Wordpress will inform the name of  theme who has been broken which is the folder name of  theme and inform the error with description message.

{F342862}

Looks like the filename is reflected, on the `Name` of the detail broken themes. I try to rename the folder to malicious name ( payload : <img src=x onerror=alert(1)> ) and the payload it'll be execute.

{F342863}

##POC
1. Upload theme
1. Delete the style.css ( or you can make new folder on theme path with payload name )
1.  Rename the folder to `<img src=x onerror=alert(1)>` 
1. See theme page. 

##Video 
https://youtu.be/IuJrcR_BoKo

## Impact

XSS will be execute , because the filename is stored on page without any filter, and this is possible to make stored XSS.

It'll be good to filter / encoding the illegal character, like wordpress do on themes upload.

</details>

---
*Analysed by Claude on 2026-05-12*
