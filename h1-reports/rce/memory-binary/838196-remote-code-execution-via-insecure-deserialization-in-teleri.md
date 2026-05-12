# Remote Code Execution via Insecure Deserialization in Telerik UI (CVE-2017-11317 + CVE-2019-18935)

## Metadata
- **Source:** HackerOne
- **Report:** 838196 | https://hackerone.com/reports/838196
- **Submitted:** 2020-04-03
- **Reporter:** sw33tlie
- **Program:** Telerik (via HackerOne)
- **Bounty:** Not specified in writeup
- **Severity:** Critical
- **Vuln:** Insecure Deserialization, Arbitrary File Upload, Remote Code Execution, Chained Vulnerabilities
- **CVEs:** CVE-2017-11317, CVE-2019-18935
- **Category:** memory-binary

## Summary
An outdated Telerik Web UI instance (v2016.2.607.40) was vulnerable to remote code execution through chaining two CVEs: CVE-2017-11317 (arbitrary file upload) and CVE-2019-18935 (unsafe deserialization). The attacker uploaded a malicious DLL file and triggered deserialization to achieve full RCE on the server.

## Attack scenario
1. Attacker identifies outdated Telerik Web UI endpoint (Telerik.Web.UI.WebResource.axd?type=rau)
2. Attacker exploits CVE-2017-11317 to upload arbitrary DLL file to server via the WebResource endpoint
3. Server appends .tmp extension to uploaded file during storage
4. Attacker crafts malicious serialized object referencing the uploaded DLL with .tmp extension
5. Attacker sends serialized payload to trigger deserialization via CVE-2019-18935
6. Unsafe deserialization loads and executes malicious DLL code, achieving RCE

## Root cause
Telerik Web UI versions prior to R3 2019 SP1 contained two critical flaws: (1) insufficient validation on file uploads allowing arbitrary DLL placement, and (2) unsafe deserialization of untrusted data without proper integrity checks or gadget chain protection.

## Attacker mindset
Methodical vulnerability researcher who discovered that individual CVEs could be chained for greater impact. Demonstrated responsible disclosure by using benign proof-of-concept (process sleep) rather than destructive payloads, and identified implementation quirks (filename .tmp extension) requiring exploit adaptation.

## Defensive takeaways
- Immediately patch Telerik Web UI to R3 2019 SP1 (v2019.3.1023) or later
- Implement strict allowlist for file uploads with type validation beyond extension checking
- Never deserialize untrusted data; use safe serialization formats (JSON) when possible
- Monitor Telerik.Web.UI.WebResource.axd endpoints for suspicious activity
- Disable unnecessary Telerik features and endpoints at the application level
- Implement Web Application Firewall (WAF) rules to detect deserialization attacks
- Maintain inventory of all third-party component versions and patch schedules
- Consider network segmentation to limit RCE blast radius

## Variant hunting
Hunt for similar deserialization vulnerabilities in other .NET components (ObjectStateFormatter, BinaryFormatter, NetDataContractSerializer). Investigate whether other Telerik components (ReportServer, Analytics, Kendo UI) share vulnerable deserialization patterns. Check for CVE-2017-11317 and CVE-2019-18935 exploitation signatures in logs. Search for other file upload endpoints that may accept DLL/executable uploads without proper validation.

## MITRE ATT&CK
- T1190
- T1203
- T1187
- T1566
- T1059
- T1204

## Notes
This is a high-quality report demonstrating chained vulnerability exploitation. The researcher demonstrated good judgment by not uploading actual reverse shells. Key technical detail: the server's automatic .tmp extension appending required exploit code modification, highlighting the importance of understanding target-specific behavior. The vulnerability required version enumeration (v2016.2.607.40) which may be exposed in HTTP headers or JavaScript. Multiple compiled DLL payloads were provided to overcome the single-use limitation of DLL execution.

## Full report
<details><summary>Expand</summary>

Hello,
I found an outdated version of Telerik Web UI (v2016.2.607.40) at the following URL: https://███/Telerik.Web.UI.WebResource.axd?type=rau.
This means that we can achieve full RCE by chaining two different CVEs: CVE-2017-11317, which allows us to upload arbitrary files on the server, and CVE-2019-18935, which is a deserialization vulnerability.

First of all, the only thing that I tried to prove that I had successfully achieved code execution was making the server sleep for 10 seconds.
No data was compromised.

Steps to reproduce
---------------------
The steps that I followed are thoroughly described in this blog post: <https://know.bishopfox.com/research/cve-2019-18935-remote-code-execution-in-telerik-ui>.
Here's a quick summary:
- Download the files in the attachments
- Make sure you have pycryptodome installed (pip3 install pycryptodome)
- Run the following command: `python3 CVE-2019-18935.py -u https://█████/Telerik.Web.UI.WebResource.axd?type=rau -v 2016.2.607.40 -f 'C:\Windows\Temp' -p sleep_042020163752,45_amd64.dll`
- The `sleep_042020160430,40_amd64.dll` is supposed to Sleep(10). This will make the server hang for roughly ten seconds, and after that you will get a response like this one: `[*] Response time: 12.88 seconds`
- The exploit worked.

Things to note
---------------------
I had to edit the original exploit code provided in the aforementioned blog post (https://github.com/noperator/CVE-2019-18935) because I noticed that when uploading the .dll file the server added a .tmp at the end of the file name.
That's why the original code was failing to exploit the deserialization part.
I added `+ '.tmp'` at the end of line 95 and after that it worked just fine.

A DLL file can only work once. This means that to test the vulnerability again a new DLL has to be compiled.
For this reason I provided several DLLs in the attachments so you don't have to compile them (especially because a windows machine with Visual Studio installed is required).

I didn't upload a reverse shell because I thought it was not a great idea, but if needed I could do it.

How to fix
---------------------
Just upgrade Telerik for ASP.NET AJAX to R3 2019 SP1 (v2019.3.1023) or later.

## Impact

Full **Remote Code Execution** on the vulnerable server.

</details>

---
*Analysed by Claude on 2026-05-12*
