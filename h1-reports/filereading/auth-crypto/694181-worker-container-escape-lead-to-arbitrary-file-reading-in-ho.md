# Worker Container Escape via Symlink Attack - Arbitrary File Reading on Host

## Metadata
- **Source:** HackerOne
- **Report:** 694181 | https://hackerone.com/reports/694181
- **Submitted:** 2019-09-13
- **Reporter:** testanull
- **Program:** HackerOne
- **Bounty:** Not specified in provided content
- **Severity:** High
- **Vuln:** Container Escape, Symlink Attack, Arbitrary File Read, Path Traversal, Insecure File Operations
- **CVEs:** None
- **Category:** auth-crypto

## Summary
A worker container fails to validate log files before copying them from container to host, allowing an attacker to replace the original log file with a symlink pointing to arbitrary host files. When the host machine copies the log file from the container, it inadvertently copies the target of the symlink from the host filesystem, enabling arbitrary file reading on the host machine.

## Attack scenario
1. Attacker gains ability to execute commands in worker container during build process
2. Attacker removes the legitimate build.log file at /opt/out/snapshot/log/build.log
3. Attacker creates a symlink pointing to sensitive host file (e.g., /etc/passwd)
4. Build process completes and host initiates file copy operation from container
5. Host copies the symlink without validation, resolving it against host filesystem instead of container
6. Attacker receives sensitive host files through the copied log artifact

## Root cause
The host machine's file copy mechanism does not validate or sanitize symlinks before copying files from the container. It blindly resolves symlinks using the host's filesystem namespace rather than the container's, combined with insufficient input validation on build artifact paths.

## Attacker mindset
An insider or compromised build process seeks to exfiltrate sensitive host configuration and credentials by leveraging the build system's trust in container artifacts without proper verification.

## Defensive takeaways
- Validate all files copied from containers before transfer, rejecting symlinks or resolving them within container context only
- Implement strict file path whitelisting for artifact collection from containers
- Use container security features to prevent symlink creation in build directories
- Run containers with read-only root filesystems where possible
- Implement proper file ownership verification and remove symlink targets before copying
- Audit and monitor file operations in build containers for suspicious activity
- Use COPY instead of symlink-aware copy commands when transferring container artifacts
- Apply principle of least privilege - containers should not need permissions to create symlinks in artifact directories

## Variant hunting
Search for similar symlink-based escape patterns in CI/CD systems, container runtimes, and artifact management tools. Investigate other file copy operations that may resolve symlinks across namespace boundaries. Check for TOCTOU (time-of-check to time-of-use) vulnerabilities in container artifact handling.

## MITRE ATT&CK
- T1190
- T1611
- T1083
- T1006
- T1548

## Notes
This is a classic symlink-following vulnerability amplified by the container-to-host boundary. The core issue is that symlink resolution uses the host's filesystem context rather than the container's. This attack is particularly dangerous in CI/CD environments where build artifacts are trusted implicitly. The vulnerability demonstrates why file operations across security boundaries require explicit validation rather than relying on filesystem semantics.

## Full report
<details><summary>Expand</summary>

## Summary:
Because lack of security, attacker will be able to remove original log file and replace it will a symlink to other file, 
After finishing job, host machine copy file from docker container.
Because the original log file has been removed, the host machine will copy the symlink file.
But the problem is it doesn't copy the linked file in container, it copys the linked file in the HOST MACHINE.

## Steps To Reproduce:
The attack is very simple, just remove the original build.log file and replace with a symlink file,
I used this configuration to read the ``/etc/passwd``:
```extraction:
  cpp:
    after_prepare:
      - rm -rf /opt/out/snapshot/log/build.log && ln -s /etc/passwd /opt/out/snapshot/log/build.log
```

## PoC
Content of ``/etc/passwd`` is attached below

## Impact

Give attacker ability to explore the host machine, expose more sensitive informations from it.

</details>

---
*Analysed by Claude on 2026-05-24*
