# Path Traversal in Ruby Tempfile on Windows via Unsanitized Backslashes

## Metadata
- **Source:** HackerOne
- **Report:** 1131465 | https://hackerone.com/reports/1131465
- **Submitted:** 2021-03-20
- **Reporter:** bugdiscloseguys
- **Program:** Ruby on Rails / Ruby
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Path Traversal, Directory Traversal, Improper Input Validation
- **CVEs:** CVE-2021-28966
- **Category:** uncategorised

## Summary
Ruby's Tempfile class on Windows fails to sanitize backslashes in the basename and ext arguments, allowing attackers to perform path traversal attacks. This vulnerability enables arbitrary file creation in any writable directory on the system, potentially leading to RCE in Rails applications by placing malicious code in accessible directories.

## Attack scenario
1. Attacker identifies user-controlled input being passed to Tempfile.open() as basename or ext parameter
2. Attacker crafts a basename containing traversal sequences like '\..\..\..\Users\target\malicious'
3. Tempfile processes the input without sanitization on Windows, interpreting backslashes as path separators
4. File is created in the traversed directory (e.g., C:\Users\target\) instead of the temp directory
5. Attacker places executable code (e.g., .rb file) in a location where it will be loaded or executed
6. Application loads the malicious file, resulting in arbitrary code execution with application privileges

## Root cause
Tempfile implementation does not sanitize or validate basename and ext arguments for path traversal sequences on Windows. The backslash character is not stripped or escaped, allowing it to function as a path separator despite being in a filename parameter. This is a platform-specific issue as Windows treats backslashes as directory separators.

## Attacker mindset
An attacker would look for any Rails or Ruby application accepting user input for temporary file names, particularly in file upload handlers, caching mechanisms, or logging functions. The attacker recognizes that on Windows, backslashes can be injected into supposedly 'safe' filename parameters to escape the temp directory and place files in sensitive locations. The goal would be to achieve code execution by planting Ruby files in predictable locations or overwriting existing files.

## Defensive takeaways
- Always validate and sanitize file path parameters, including basename and extension arguments to Tempfile
- Implement whitelist-based validation for filename components, rejecting any path separator characters
- Use Path.expand_path() or similar canonical path resolution before file creation to detect traversal attempts
- Avoid accepting user-controlled input directly for basename/ext parameters; use UUIDs or safe identifiers instead
- Implement platform-specific validation logic accounting for different path separator behaviors on Windows vs Unix
- Apply principle of least privilege - ensure temp directories have restricted write permissions
- Use static analysis tools to identify all Tempfile instantiations and audit their input sources
- Consider using Ruby security gems that wrap Tempfile with additional validation

## Variant hunting
Search for similar issues in other temporary file handling libraries and frameworks. Investigate if Dir.mktmpdir(), File.open() in temp directories, and other file creation primitives have similar vulnerabilities. Check if other interpreted languages' standard libraries (Python's tempfile, Node.js fs module) have comparable Windows-specific path traversal issues. Review other Ruby gems that depend on Tempfile.

## MITRE ATT&CK
- T1190
- T1574
- T1036

## Notes
This is a Windows-specific vulnerability that would not manifest on Unix-like systems where backslashes are valid filename characters rather than path separators. The vulnerability is particularly dangerous in Rails applications where user uploads or temporary processing files are common. The fix likely requires platform detection and sanitization of backslash characters in filename parameters on Windows systems only. The report demonstrates excellent practical PoC showing actual file creation in an unintended directory.

## Full report
<details><summary>Expand</summary>

Hi team,

##Summary

We've noticed that both arguments (basename and ext) of Tempfile on Windows are vulnerable to a path traversal which could allow unintentional file creating in arbitrary writable directories. 

Tempfile often has a user control either by basename or ext (or both). 

## PoC

~~~
irb(main):029:0> Tempfile.open(["\\..\\..\\..\\..\\..\\Users\\rootx\\malicious",".rb"])
=> #<Tempfile:C:/Users/rootx/AppData/Local/Temp\..\..\..\..\..\Users\rootx\malicious20210321-22472-fvuodx.rb>
irb(main):030:0> puts `dir C:\\Users\\rootx\\`
 Volume in drive C has no label.
 Volume Serial Number is C0F2-8D87

 Directory of C:\Users\rootx

... REDACTED ...
21-03-2021  00:45                 0 malicious20210321-22472-fvuodx.rb
... REDACTED ...
~~~

The same can be accomplished via ext argument. 

Thanks,
Harsh and Rahul,
HTTPVoid

## Impact

Unintentional file creation in an arbitrary directory. Could potentially cause RCE in RoR applications.

</details>

---
*Analysed by Claude on 2026-05-24*
