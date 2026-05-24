# http-live-simulator npm module path traversal vulnerability

## Metadata
- **Source:** HackerOne
- **Report:** 384939 | https://hackerone.com/reports/384939
- **Submitted:** 2018-07-21
- **Reporter:** lirantal
- **Program:** HackerOne
- **Bounty:** Unknown
- **Severity:** high
- **Vuln:** Path Traversal, Arbitrary File Read, Improper Input Validation
- **CVEs:** CVE-2019-5423
- **Category:** uncategorised

## Summary
The http-live-simulator npm module fails to restrict file access to a designated root directory, allowing attackers to read arbitrary files from the system via path traversal sequences. An unauthenticated attacker can use relative path traversal (e.g., /../../) in HTTP requests to access sensitive files outside the intended directory.

## Attack scenario
1. Attacker installs http-live-simulator module or identifies a service running it
2. Attacker crafts an HTTP request using path traversal sequences (e.g., curl --path-as-is http://localhost:8181/../../sensitive/file.txt)
3. The module parses the request without validating or canonicalizing the path
4. The traversal sequences are not filtered or blocked, allowing directory escape
5. Sensitive files (config files, private keys, environment files) are returned to attacker
6. Attacker gains unauthorized access to confidential system data

## Root cause
The module lacks path normalization and directory restriction. It does not enforce a chroot-like restriction to a base directory or validate that resolved file paths remain within the intended serving directory. No input sanitization prevents ../ sequences from escaping the root.

## Attacker mindset
Low-skill attacker could easily exploit this to enumerate system files and extract credentials, configuration data, or source code. The simplicity of the exploit (standard path traversal) makes it an attractive reconnaissance vector.

## Defensive takeaways
- Always enforce a root directory restriction when serving files - use path.resolve() and verify the resolved path is within the intended directory
- Normalize and canonicalize all file paths before access to resolve ../ and symlink attacks
- Use allowlists rather than blocklists for file access patterns
- Reject requests containing ../ or encoded traversal sequences
- Implement proper input validation on all user-supplied path components
- Use dedicated static file serving libraries (Express.static with appropriate root configuration) rather than custom implementations
- Run file serving processes with minimal file system permissions (principle of least privilege)

## Variant hunting
Search for similar patterns in other npm modules that serve files or accept file paths as parameters. Look for custom file serving implementations without path validation, especially in modules predating widespread adoption of framework security best practices. Check for similar issues in modules for static file serving, template rendering, or resource loading.

## MITRE ATT&CK
- T1190
- T1083
- T1041

## Notes
This is a straightforward path traversal vulnerability in a low-adoption module (9 weekly downloads). The reporter did not contact the maintainer before disclosure. The vulnerability represents a common security mistake in custom file serving implementations - the absence of path canonicalization and root directory enforcement. Modern frameworks like Express provide secure defaults, but custom implementations frequently miss these protections.

## Full report
<details><summary>Expand</summary>

> NOTE! Thanks for submitting a report! Please replace *all* the [square] sections below with the pertinent details. Remember, the more detail you provide, the easier it is for us to triage and respond quickly, so be sure to take your time filling out the report!

I would like to report Path Traversal vulnerability in http-live-simulator
It allows to read arbitrary files from any location on disk

# Module

**module name:** http-live-simulator
**version:** 1.0.5
**npm page:** `https://www.npmjs.com/package/http-live-simulator`

## Module Description

> Copy description from npm page

## Module Stats

> Replace stats below with numbers from npm’s module page:

[9] weekly downloads

# Vulnerability

## Vulnerability Description

> Description about how the vulnerability was found and how it can be exploited, how it harms package users (data modification/lost, system access, other.

The http-live-simulator module doesn't set a root directory and allows any arbitrary paths to be accessed on the file system and returned to requesting clients

## Steps To Reproduce:

> Detailed steps to reproduce with all required references/steps/commands. If there is any exploit code or reference to the package source code this is the place where it should be put.

1. Install the module locally in an npm project: `npm install http-live-simulator`
2. Run the live server on a specified port: `node_modules/.bin/http-live --port 8181`
3. Attempt to access a file from outside that project's directory, such as `curl --path-as-is http://localhost:8181/../../file.txt`
4. Files output should be returned 

## Supporting Material/References:

> State all technical information about the stack where the vulnerability was found

- MacOS
- Node.js 8.11.3
- npm 5.6.0

# Wrap up

> Select Y or N for the following statements:

- I contacted the maintainer to let them know: [N] 
- I opened an issue in the related repository: [N]

## Impact

path traversal vulnerability leading to read access in arbitrary files on disk

</details>

---
*Analysed by Claude on 2026-05-24*
