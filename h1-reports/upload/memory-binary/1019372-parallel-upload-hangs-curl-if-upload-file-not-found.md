# Parallel upload hangs curl if upload file not found

## Metadata
- **Source:** HackerOne
- **Report:** 1019372 | https://hackerone.com/reports/1019372
- **Submitted:** 2020-10-26
- **Reporter:** brumbrum
- **Program:** curl
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Denial of Service, Infinite Loop, Resource Exhaustion, Improper Error Handling
- **CVEs:** None
- **Category:** memory-binary

## Summary
When using curl's parallel upload mode (-Z flag) with a non-existent file specified for upload (-T flag), curl enters an infinite loop and hangs indefinitely without terminating. This causes the curl process to block forever, potentially stalling scripts or binaries that invoke curl, leading to service availability issues.

## Attack scenario
1. Attacker identifies a script or service that uses curl with parallel upload functionality
2. Attacker crafts input or conditions that cause curl to attempt uploading a non-existent file
3. Script invokes curl with -T and -Z flags where the upload file does not exist
4. curl encounters the missing file error but fails to properly exit due to parallel mode logic
5. curl enters infinite loop retrying the operation, consuming resources and blocking execution
6. Parent process or script hangs indefinitely, resulting in service degradation or denial of service

## Root cause
The parallel upload mode implementation in curl does not properly handle the error condition when an upload file is not found. Instead of cleanly exiting, the error handling logic in parallel mode enters an infinite retry loop, continuously attempting to open the non-existent file without ever breaking out of the loop.

## Attacker mindset
An attacker could exploit this by identifying systems or scripts that use curl with parallel uploads. By controlling input parameters or environment conditions to force a non-existent file upload scenario, they could cause curl to hang indefinitely, effectively creating a denial of service condition against dependent services or scripts that rely on curl completing its operations.

## Defensive takeaways
- Implement proper error handling in parallel operation modes to ensure all error conditions result in clean termination
- Add explicit timeout mechanisms to prevent infinite loops in retry logic
- Validate file existence before entering parallel processing logic
- Implement circuit breaker patterns or max-retry limits in parallel operations
- Add watchdog timers to parent processes that invoke curl to detect and handle hangs
- Use --max-time or timeout mechanisms when invoking curl programmatically
- Test error conditions thoroughly in both serial and parallel execution modes

## Variant hunting
Look for similar infinite loop conditions in other parallel operations (downloads, transfers); check parallel mode implementation for other file operations that might exhibit similar behavior; investigate how other flags interact with parallel mode error handling; test other missing resource scenarios in parallel mode (missing destination directories, permission errors, etc.)

## MITRE ATT&CK
- T1499.4
- T1657

## Notes
This is a logic bug in curl's CLI tool, not necessarily in libcurl library. The reporter notes curl has no network traffic during the hang, indicating the loop is local. The issue is particularly dangerous in automated systems where curl is invoked via system calls without proper timeout handling. The --parallel-max and --parallel-immediate flags do not exhibit this behavior, suggesting the issue is specific to certain parallel mode code paths.

## Full report
<details><summary>Expand</summary>

Attempting to upload (-T) a not found file with parallel (-Z) flag present, will cause curl to get stuck and never terminate, potentially stalling scripts that make use of this particular flags. 

curl -T blabla-notexists -Z upload.example.com www.google.com www.cnn.com www.apple.com


Same issue occurs if using -Z or --parallel flags.


$ curl -T blabla-notexists -Z upload.example.com www.google.com www.cnn.com www.apple.com
curl: Can't open 'blabla-notexists'!
curl: try 'curl --help' or 'curl --manual' for more information
DL% UL%  Dled  Uled  Xfers  Live   Qd Total     Current  Left    Speed
--  --      0     0     1     0     1 --:--:--  0:00:01 --:--:--     0      curl: Can't open 'blabla-notexists'!
curl: try 'curl --help' or 'curl --manual' for more information
curl: Can't open 'blabla-notexists'!
curl: try 'curl --help' or 'curl --manual' for more information
curl: Can't open 'blabla-notexists'!
curl: try 'curl --help' or 'curl --manual' for more information
curl: Can't open 'blabla-notexists'!
curl: try 'curl --help' or 'curl --manual' for more information
curl: Can't open 'blabla-notexists'!
curl: try 'curl --help' or 'curl --manual' for more information
curl: Can't open 'blabla-notexists'!
curl: try 'curl --help' or 'curl --manual' for more information
curl: Can't open 'blabla-notexists'!
curl: try 'curl --help' or 'curl --manual' for more information
curl: Can't open 'blabla-notexists'!
curl: try 'curl --help' or 'curl --manual' for more information
curl: Can't open 'blabla-notexists'!
curl: try 'curl --help' or 'curl --manual' for more information
curl: Can't open 'blabla-notexists'!
curl: try 'curl --help' or 'curl --manual' for more information



Doesn't happen with --parallel-max or --parallel-immediate flags.

Observing the network with tcpdump, shows NO traffic at all.


I suspect this is just an ordinary bug, but reporting it in case there is a security angle that might be present. Really the only obvious security issue is that curl will block possibly forever, and if curl tool is used inside a script or binary (via system() for example) could cause that script/binary to stop/block/hang.  In some cases, this could lead to a bad situation, leading to denial of service or loss of service availability for program/process/server/service using curl in such a way.

Not 100% sure, but I suspect that libcurl does not have this issue.  I could be wrong.


Steps to Reproduce:
Upload (-T) a file with curl while in parallel mode (-Z) and the upload file must not exist locally.

curl -T blabla-notexists -Z upload.example.com www.google.com www.cnn.com www.apple.com

## Impact

curl hangs leading to denial of service or loss of service availablity for script or binary using curl CLI tool.


Mitigation:
Don't use -Z parallel flag with -T upload flag.

</details>

---
*Analysed by Claude on 2026-05-24*
