# Remote Code Execution in pdf-image via Command Injection

## Metadata
- **Source:** HackerOne
- **Report:** 781664 | https://hackerone.com/reports/781664
- **Submitted:** 2020-01-23
- **Reporter:** gabriel-kimiaie
- **Program:** pdf-image (npm package)
- **Bounty:** Not eligible for bounty (as noted by reporter)
- **Severity:** Critical
- **Vuln:** Command Injection, Improper Input Validation, Unsafe use of child_process.exec
- **CVEs:** CVE-2020-8132
- **Category:** memory-binary

## Summary
The pdf-image npm package is vulnerable to remote code execution when processing user-controlled PDF file paths. The vulnerability stems from unsanitized input being passed directly to child_process.exec() in the PDFImage class constructor and methods like getInfo(). An attacker can bypass intended quoting mechanisms using shell metacharacters or backticks to execute arbitrary commands.

## Attack scenario
1. Attacker identifies application using pdf-image package that accepts PDF file paths from user input (e.g., file upload, URL parameter)
2. Attacker crafts malicious filename containing shell metacharacters: `"; sleep 500 #` or backtick injection: `` `ls;sleep 5` ``
3. Attacker submits the malicious filename to the application (via upload, API parameter, etc.)
4. Application instantiates PDFImage class with the attacker-controlled filename: `new PDFImage(userInput)`
5. PDFImage calls vulnerable methods like getInfo() which internally uses child_process.exec() with the unsanitized path
6. Shell interprets the injected metacharacters and executes arbitrary commands with application privileges

## Root cause
The pdf-image module directly concatenates user-supplied PDF file paths into shell commands executed via child_process.exec() without proper escaping or validation. While the path may be wrapped in quotes, shell metacharacters like backticks and escaped quotes can break out of the quoting context.

## Attacker mindset
An attacker exploiting this would recognize that Node.js applications often accept file paths from untrusted sources and that developers frequently overlook the dangers of child_process.exec(). The simplicity of the exploit (basic command injection) makes it an attractive target for reconnaissance, credential theft, or establishing persistence.

## Defensive takeaways
- Never use child_process.exec() with user-controlled input; use child_process.execFile() with arguments array instead
- If shell functionality is required, use parameterized execution with array-based argument passing to prevent interpretation of shell metacharacters
- Implement strict input validation on file paths using allowlists of permitted characters (alphanumeric, forward slash, hyphen, underscore)
- Use dedicated PDF libraries or safer wrapper functions that handle path sanitization internally
- Employ security scanning tools to detect unsafe child_process usage patterns in dependencies
- Run applications with principle of least privilege to limit damage from successful RCE

## Variant hunting
Search npm packages for: (1) other packages using child_process.exec() with file paths, (2) PDF-related packages accepting user-supplied filenames, (3) ImageMagick wrapper libraries that don't validate input, (4) packages wrapping command-line tools without proper escaping, (5) similar patterns in image processing, document conversion, or media manipulation libraries

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1059 - Command and Scripting Interpreter
- T1203 - Exploitation for Client Execution

## Notes
Reporter noted they did not contact maintainers or open issues before submission. The vulnerability is particularly severe because pdf-image has 8,691 weekly downloads, meaning many applications may be affected. The suggested patch demonstrates proper shell escaping techniques. Modern best practice would be to use execFile() with argument arrays rather than exec() altogether. This is a textbook example of why shell-based command execution should be avoided in favor of direct system calls.

## Full report
<details><summary>Expand</summary>

I would like to report "A simple remote code execution" in "pdf-image".
It allows "a remote attacker to execute arbitrary code when several functions of the PDFImage class are called and the class loaded from user-input value".

# Module

**module name:** pdf-image
**version:** latest
**npm page:** `https://www.npmjs.com/package/pdf-image`

## Module Description

Provides an interface to convert PDF's pages to png files in Node.js by using ImageMagick.

## Module Stats

[1] weekly downloads: 8,691

# Vulnerability

## Vulnerability Description

Hello there ! I understand this bug isn't eligible for a bounty. I am reporting it either way. I've found several code execution in the pdf-image class, I tested one of them. They are simple and of course come from the child_process.exec call with lack of escaping. I tested one of them.

## Steps To Reproduce:

var PDFImage = require("pdf-image").PDFImage;

var pdfImage = new PDFImage('"; sleep 500 #"');
pdfImage.getInfo();

You can also exploit the vulnerability by submitting  backticks (example payload: `ls;sleep 5` which will be executed even though you're double-quoting the input.

## Patch
You can take example on your command-exists npm class:
var isUsingWindows = process.platform == 'win32'
var cleanInput = function(s) {
  if (/[^A-Za-z0-9_\/:=-]/.test(s)) {
    s = "'"+s.replace(/'/g,"'\\''")+"'";
    s = s.replace(/^(?:'')+/g, '') // unduplicate single-quote at the beginning
      .replace(/\\'''/g, "\\'" ); // remove non-escaped single-quote if there are enclosed between 2 escaped
  }
  return s;
}

if (isUsingWindows) {
  cleanInput = function(s) {
    var isPathName = /[\\]/.test(s);
    if (isPathName) {
      var dirname = '"' + path.dirname(s) + '"';
      var basename = '"' + path.basename(s) + '"';
      return dirname + ':' + basename;
    }
    return '"' + s + '"';
  }
}
## Supporting Material/References:

https://github.com/mooz/node-pdf-image/blob/master/index.js#L27

- Linux / centOS
- v6.17.1
- 3.10.10 
- N/A
- Own sample script

# Wrap up

> Select Y or N for the following statements:

- I contacted the maintainer to let them know: [Y/N] N
- I opened an issue in the related repository: [Y/N] N

Thanks!

## Impact

Bad code relying on that class can feel foul to RCE.

</details>

---
*Analysed by Claude on 2026-05-12*
