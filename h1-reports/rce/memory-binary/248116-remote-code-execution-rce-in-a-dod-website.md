# Remote Code Execution in DoD Website via PrimeFaces Expression Language Injection

## Metadata
- **Source:** HackerOne
- **Report:** 248116 | https://hackerone.com/reports/248116
- **Submitted:** 2017-07-10
- **Reporter:** manoelt
- **Program:** DoD Bug Bounty Program (HackerOne)
- **Bounty:** Not specified in report
- **Severity:** CRITICAL
- **Vuln:** Expression Language Injection, Remote Code Execution, Insecure Deserialization, Java Code Injection
- **CVEs:** None
- **Category:** memory-binary

## Summary
A DoD application running PrimeFaces 5.3 was vulnerable to Expression Language (EL) injection through the DynamicContent generator endpoint. An attacker could inject arbitrary Java code via the 'pfdrid' parameter and achieve remote code execution, demonstrated through DNS exfiltration.

## Attack scenario
1. Attacker generates a malicious EL injection payload using the PrimeFaces 5.3 library with a custom Java class that executes code
2. Payload is encrypted using the default PrimeFaces key ('primefaces') to bypass basic protections
3. Attacker crafts a URL targeting the vulnerable endpoint: /javax.faces.resource/dynamiccontent.properties.xhtml with parameters pfdrt=sc and pfdrid=<encrypted_payload>
4. Victim application receives GET request and processes the dynamiccontent handler, which deserializes and evaluates the malicious payload
5. PrimeFaces framework evaluates the injected expression language code, executing arbitrary Java methods (e.g., File operations, network calls)
6. Attacker receives DNS resolution request from DoD server, confirming RCE and ability to exfiltrate data or perform file operations

## Root cause
PrimeFaces 5.3 uses an insecure deserialization mechanism for the DynamicContent generator that automatically evaluates Expression Language expressions without proper sanitization. The 'pfdrid' parameter accepts Base64-encoded and encrypted payloads that are deserialized and evaluated in a trusted context, allowing arbitrary code execution.

## Attacker mindset
The researcher demonstrated responsible disclosure by identifying the critical RCE vulnerability but deliberately avoiding sensitive actions (file deletion/exfiltration) that could compromise the DoD system. They used DNS as a side-channel to prove code execution rather than direct exploitation, showing ethical restraint while proving impact.

## Defensive takeaways
- Immediately patch PrimeFaces to version 5.3.1+ which addresses CVE-2016-9496 (EL injection vulnerability)
- Implement strict input validation on 'pfdrid' parameter: reject payloads longer than expected legitimate values and implement whitelist validation
- Disable or restrict the StreamedContent ('pfdrt=sc') handler if not required for application functionality
- Rotate default encryption keys used by framework components from hardcoded defaults
- Implement expression language filtering/sandboxing to prevent arbitrary EL evaluation
- Monitor outbound DNS requests and network calls from application servers for anomalous activity
- Apply principle of least privilege to Java application permissions (restrict File class access, network operations)
- Implement WAF rules to detect Base64-encoded Java serialization payloads in URL parameters
- Maintain inventory of third-party library versions and subscribe to security advisories

## Variant hunting
Search for other Java frameworks and libraries with similar deserialization-based template/expression language handling (Spring EL, OGNL, MVEL). Investigate other PrimeFaces endpoints that accept encrypted/encoded parameters for similar injection patterns. Review custom Java libraries that auto-evaluate expressions at request processing time.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1059 - Command and Scripting Interpreter (Java)
- T1203 - Exploitation for Client Execution
- T1005 - Data from Local System
- T1041 - Exfiltration Over C2 Channel
- T1567 - Exfiltration Over Web Service

## Notes
This vulnerability (CVE-2016-9496) affected multiple versions of PrimeFaces and was actively exploited. The use of default encryption keys and automatic expression evaluation in deserialized objects is a critical design flaw. The researcher's DNS-based PoC is clever as it bypasses firewall restrictions while proving code execution capability. The vulnerability required no authentication and could be triggered via simple GET requests, making it highly exploitable.

## Full report
<details><summary>Expand</summary>

**Summary:**
One of the DoD applications uses a java library which is vulnerable to expression language injection. Using only an URL I was able to inject java code. I made a simple PoC that requests a name resolution to a DNS server.

**Description:**
The application at https://███ uses Primefaces version 5.3 which is vulnarable to Expression Language injection through DynamicContent generator.

To prove the injection I made a PoC that tries to submit a HTTP request, but the server blocks the outgoing packets on port 80, on the other hand the server still try to resolve the requested domain and so I receive DNS requests from DoD server. Also, I can delete and maybe read files using the File Java class, but I decided not to try to avoid leak of some private data.

## Impact
Critical.

## Step-by-step Reproduction Instructions

First you need to execute the program attached to generate the payload. To do that you just need the Primefaces-5.3.jar (https://www.primefaces.org/downloads/ ) in your class path.

1. With the code attached generate the payload encrypted with the default key "primefaces". Change the domain (String remoteMalJarUrl) to one that you have control or use one from http://dnsbin.zhack.ca/
2. With the payload from #1, append to the URL: https://████/javax.faces.resource/dynamiccontent.properties.xhtml?pfdrt=sc&ln=primefaces&pfdrid=
3. Send a GET request using curl (curl -vk https://████/javax.faces.resource/dynamiccontent.properties.xhtml?pfdrt=sc&ln=primefaces&pfdrid=<YOUR_PAYLOAD_HERE>
4. You will receive a name resolution request for remoteMalJarUrl from the DoD application

We could use this DNS request to exfiltrate data from the server. And as I said, theoretically I could also delete files from the server using the File class.

## Product, Version, and Configuration (If applicable)
Primefaces 5.3

## Suggested Mitigation/Remediation Actions
- Update Primefaces
- Alternatively by filtering incoming requests with pfdrid parameter (value longer than 16bytes and Base64 encoded) and "pfdrt=sc" is possible to mitigate the attack: "pfdrt=sc" calls the vulnerable StreamedContent Method and pfdrid contains the exploit payload. 

## References
http://blog.mindedsecurity.com/2016/02/rce-in-oracle-netbeans-opensource.html
https://github.com/primefaces/primefaces/issues/1152

</details>

---
*Analysed by Claude on 2026-06-07*
