# Path Traversal in saveContracts.js File Reading Function

## Metadata
- **Source:** HackerOne
- **Report:** 1196917 | https://hackerone.com/reports/1196917
- **Submitted:** 2021-05-13
- **Reporter:** caon
- **Program:** Sifchain
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Path Traversal, Directory Traversal, Arbitrary File Read
- **CVEs:** None
- **Category:** uncategorised

## Summary
The readFiles() function in saveContracts.js concatenates user-controlled filenames directly into file paths without sanitization, allowing attackers to traverse directories and read arbitrary files on the system. An attacker could craft filenames containing path traversal sequences (e.g., '../../../../etc/passwd') to access sensitive files outside the intended build/contracts/ directory.

## Attack scenario
1. Attacker creates a malicious file or directory entry named '../../../../etc/passwd' within the build/contracts/ directory
2. Attacker triggers the script execution (e.g., by running the deployment or build process)
3. The readFiles() function recursively lists all files in build/contracts/ including the maliciously named entry
4. For each filename, fs.readFile concatenates the directory path with the unsanitized filename: 'build/contracts/../../../../etc/passwd'
5. Path normalization causes the traversal sequence to navigate to the filesystem root, reading the actual /etc/passwd file
6. The script processes and potentially exports sensitive system file contents, exposing user credentials and system configuration

## Root cause
Unsafe string concatenation of directory path and filename without path normalization or validation. The code directly concatenates 'dirname + filename' where filename is user-controlled (derived from directory listing) without resolving relative path components or validating the resulting path stays within the intended directory.

## Attacker mindset
An attacker with filesystem access to the build/contracts/ directory (or ability to influence its contents during the build process) exploits the assumption that directory listing results are trustworthy. The attacker creates symlinks or specially-named files to break out of the intended directory scope and access sensitive system files, credentials, or application secrets that should be restricted.

## Defensive takeaways
- Always sanitize and validate file paths, especially when constructing paths from dynamic input or directory listings
- Use path.resolve() and path.relative() to normalize paths and verify they remain within the intended directory
- Implement a whitelist of allowed filenames rather than trusting directory listing results
- Use path.join() with proper validation to prevent directory traversal sequences
- Avoid simple string concatenation for path operations; use Node.js path module functions
- Apply principle of least privilege - restrict filesystem access to only necessary directories
- Use security scanning tools to detect path traversal patterns during code review

## Variant hunting
Search for other instances of dirname + filename or similar string concatenation in file path operations
Review all fs.readFile(), fs.readdir() combinations for path validation
Check for symlink handling - ensure symlinks cannot escape intended directory boundaries
Audit build scripts and deployment scripts that process dynamic file lists
Look for other concatenation patterns: path + variable, filepath + input, directory + name
Review Truffle contract deployment scripts for similar vulnerabilities in related tools

## MITRE ATT&CK
- T1190
- T1083
- T1552.007

## Notes
This vulnerability specifically affects the smart contract build pipeline in Sifchain. While the impact depends on the execution context (whether the script runs with elevated privileges), it poses a critical risk if the build process has access to sensitive files. The vulnerability is particularly dangerous in automated CI/CD environments where the build agent may have broader filesystem access. The fix requires validating that resolved file paths remain within the build/contracts/ directory using path.normalize() and path.relative() with verification.

## Full report
<details><summary>Expand</summary>

Reference: https://portswigger.net/web-security/file-path-traversal

Directory traversal (also known as file path traversal) is a web security vulnerability that allows an attacker to read arbitrary files on the server that is running an application. This might include application code and data, credentials for back-end systems, and sensitive operating system files. In some cases, an attacker might be able to write to arbitrary files on the server, allowing them to modify application data or behavior, and ultimately take full control of the server.

Inside https://github.com/Sifchain/sifnode/blob/develop/smart-contracts/scripts/saveContracts.js there's a part of the code which is not sanitized; meaning it could allow a path transversal to happen.

```javascript
function readFiles(dirname, onFileContent, onError) {
  fs.readdir(dirname, function(err, filenames) {
    if (err) {
      onError("The build/contracts directory does not exist.\n\nMake sure the build directory exists before running this script.\n\nTo create build directory run `truffle deploy --network develop`\n\n");
      return;
    }
    filenames.forEach(function(filename) {
      fs.readFile(dirname + filename, 'utf-8', function(err, content) {  <<<<<< VULNERABLE
        if (err) {
          onError(filename, err);
          return;
        }
        onFileContent(filename, content);
      });
    });
  });
}
```

Caller:
```javascript
readFiles("build/contracts/", handleFileContents, handleError);
```

# Explanation:
readFiles() function calls the `build/contracts/` path, let' says a file named `../../../../etc/passwd` exists inside the folder. 
Inside readFiles the first part of the script will grab all filenames, meaning it will grab the `../../../../etc/passwd`file. After grabbing the filenames It will proceed to call `fs.readFile` to each of the files.
When `fs.readFile` happens to `../../../../etc/passwd` the call will be something like that:

`build/contracts/../../../../etc/passwd`

Once executed it will show the `passwd` file containing all users and password of the machine because /../../../../ will force the path to root.

## Impact

This transversal allows an attacker to read arbitrary files on the server.

#Fix

Sanitize the inputs in the `filename` variable
If you are using node or express it is a good idea to follow this https://stackoverflow.com/questions/46718772/how-i-can-sanitize-my-input-values-in-node-js/46719000

Kind regards
Caon

</details>

---
*Analysed by Claude on 2026-05-24*
