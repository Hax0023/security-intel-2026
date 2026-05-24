# Path Traversal in MariaDB Command Line Client Plugin Loading

## Metadata
- **Source:** HackerOne
- **Report:** 637840 | https://hackerone.com/reports/637840
- **Submitted:** 2019-07-08
- **Reporter:** lixtelnis
- **Program:** MariaDB
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Path Traversal, Arbitrary File Load, Code Execution via dlopen
- **CVEs:** None
- **Category:** uncategorised

## Summary
The MariaDB command line client contains a directory traversal vulnerability in plugin loading that allows a malicious server to cause arbitrary shared object files to be loaded via dlopen(). By crafting specially-formed paths with directory traversal sequences and padding with '/' characters to bypass extension checks, an attacker can achieve code execution through constructor/destructor functions.

## Attack scenario
1. Attacker sets up a malicious MariaDB-compatible server that the victim connects to with the command line client
2. Malicious server responds with crafted plugin path containing directory traversal sequences (../) to point to attacker-controlled or predictable locations
3. Attacker pads the path with '/' characters so that strxnmov function drops the .so extension validation
4. The vulnerable client code in client_plugin.c line 368 calls dlopen() on the manipulated path without proper sanitization
5. dlopen() loads a shared object from the traversed path location, executing constructor/destructor functions with client privileges
6. Attacker achieves arbitrary code execution in the context of the MariaDB client process

## Root cause
Insufficient input validation and path sanitization before passing user-supplied plugin paths to dlopen(). The strxnmov function can be bypassed by padding paths with '/' characters, and directory traversal sequences are not filtered.

## Attacker mindset
Man-in-the-middle or malicious server operator who can influence plugin loading paths. Targets systems where predictable writable files exist or where attacker can pre-position malicious .so files at known locations.

## Defensive takeaways
- Implement strict allowlist validation for plugin paths before dlopen() calls
- Canonicalize paths using realpath() to resolve and validate against expected directories
- Enforce plugin loading from secure, restricted directories only
- Validate file ownership and permissions before dynamic loading
- Use absolute paths and reject any relative path traversal sequences
- Consider using safer alternatives to dlopen() or implement additional integrity checks
- Apply principle of least privilege to client process execution context

## Variant hunting
Search for similar dlopen() calls without path validation in C codebases. Check for other plugin loading mechanisms in client tools. Investigate strxnmov() and similar string manipulation functions that may bypass extension checks. Look for other instances where server-provided paths influence file operations.

## MITRE ATT&CK
- T1190
- T1573
- T1105

## Notes
The vulnerability requires either MITM position or connection to attacker-controlled server. The actual exploitability depends on presence of attacker-controlled files at predictable paths or common binaries with constructor functions. The researcher demonstrates dual impact: code execution via init/fini functions and social engineering via dialog plugin password theft.

## Full report
<details><summary>Expand</summary>

The command line client has a directory traversal bug which allows server chosen files to be dlopened when it connects to a malicious server.

The path can also be padded with `/` characters so that `strxnmov` drops the `.so` extension.

The `dlopen` call is performed here: <https://github.com/MariaDB/server/blob/10.5/sql-common/client_plugin.c#L368>

## Impact

In rare situations where the attacker controls a file at a known location on the victim's machine this can lead to code execution using `init/fini` functions. See attached `dlopen.sh`.

Other side effects present in commonly installed software are not to be neglected. The mecanism is far from being uncommon in C files alone according to this search:

<https://codesearch.debian.net/search?q=__attribute__.*constructor+filetype%3Ac&perpkg=1>

Without abusing the path traversal bug the dialog plugin might also be used to fool a user into sending its password unhashed. See attached `dialog.sh`.

</details>

---
*Analysed by Claude on 2026-05-24*
