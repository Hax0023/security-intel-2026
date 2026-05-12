# Java Deserialization RCE via JBoss JMXInvokerServlet/EJBInvokerServlet on card.starbucks.in

## Metadata
- **Source:** HackerOne
- **Report:** 153026 | https://hackerone.com/reports/153026
- **Submitted:** 2016-07-21
- **Reporter:** meals
- **Program:** Starbucks (HackerOne)
- **Bounty:** Not specified in report
- **Severity:** critical
- **Vuln:** Unsafe Java Deserialization, Remote Code Execution, Gadget Chain Exploitation, Exposed Admin Interface
- **CVEs:** None
- **Category:** memory-binary

## Summary
An exposed JMXInvokerServlet and EJBInvokerServlet endpoint on card.starbucks.in accepted untrusted serialized Java objects, allowing unauthenticated remote code execution. The vulnerability leveraged Apache Commons Collections gadget chain via ysoserial to execute arbitrary commands on the Windows server.

## Attack scenario
1. Attacker discovers exposed /invoker/EJBInvokerServlet and /invoker/JMXInvokerServlet endpoints on card.starbucks.in
2. Attacker generates malicious serialized payload using ysoserial with CommonsCollections1 gadget chain containing arbitrary command (e.g., cmd.exe)
3. Attacker crafts HTTP POST request with Content-Type: application/x-java-serialized-object and embeds the malicious serialized data
4. JBoss application deserializes the untrusted object without validation, triggering gadget chain execution
5. CommonsCollections gadget chain executes the attacker's command on the server with application privileges
6. Attacker determines command execution success by analyzing error messages (e.g., 'cannot find' errors for non-existent files)

## Root cause
JBoss application server exposed deserialization endpoints (JMXInvokerServlet/EJBInvokerServlet) without authentication and processed untrusted serialized objects. The ClassPathXmlApplicationContext and LazyConnectionDataSourceFactoryBean chain in Apache Commons Collections allowed arbitrary method invocation during deserialization.

## Attacker mindset
Opportunistic reconnaissance of publicly accessible infrastructure combined with knowledge of JBoss invoker patterns. Attacker systematically validated RCE through error-based inference without establishing full interactive shell, suggesting awareness of defensive controls (egress filtering) and pragmatic proof-of-concept methodology.

## Defensive takeaways
- Disable or remove JMXInvokerServlet and EJBInvokerServlet if not required; restrict to trusted networks if necessary
- Implement strict input validation and reject serialized objects from untrusted sources
- Apply JBoss security patches and remove vulnerable gadget chain libraries (Apache Commons Collections <3.2.2)
- Enable Java deserialization filters using JEP 290 (Java 9+) or equivalent serialization filters
- Require authentication and authorization for all invoker endpoints
- Monitor and alert on attempts to access legacy invoker servlets
- Implement network segmentation to restrict access to management interfaces
- Conduct gadget chain inventory and remove unnecessary transitive dependencies

## Variant hunting
Search for other JBoss invoker endpoints (EJBInvokerServlet, RMIInvokerServlet, HttpInvokerServiceExporter), alternative gadget chains (CommonsCollections2-7, Spring, ROME, xbean-propertyeditor), and similar deserialization endpoints in other Java application servers (WebLogic, WebSphere, Tomcat with vulnerable libraries)

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1195: Supply Chain Compromise (gadget chain dependency)
- T1059: Command and Scripting Interpreter
- T1203: Exploitation for Client Execution
- T1055: Process Injection

## Notes
Report demonstrates practical RCE validation through error-based inference without full shell access due to egress filtering. Vulnerability is unauthenticated and requires no user interaction. ysoserial tool is industry-standard for gadget chain generation. CommonsCollections1 was the most reliable gadget chain at time of report. Starbucks card.starbucks.in domain suggests payment/sensitive data exposure risk.

## Full report
<details><summary>Expand</summary>

I found an open JMXInvokerServlet/EJBInvokerServlet and normally I should be able to get a shell just by doing that. However I think due to some egress filtering on the box I've been having issues getting a shell to run.

Invokers: https://card.starbucks.in/invoker/EJBInvokerServlet and https://card.starbucks.in/invoker/JMXInvokerServlet

Command to output serialized data to a file:
$ java -jar ysoserial-0.0.4-all.jar CommonsCollections1 'cmd.exe' > serialdata
{F106535}

This puts the serialized data for executing cmd.exe into a file that I can then paste into burp.

Create a new burp repeater tab and paste in the following (running on https):

POST /invoker/EJBInvokerServlet HTTP/1.1
Host: card.starbucks.in
Accept: */*
Accept-Language: en
ContentType: application/x-java-serialized-object; class=org.jboss.invocation.MarshalledInvocation
User-Agent: Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0)
Connection: close
Content-Length: 0

Then right click an select "Paste from file"
{F106537} 

Hit Go and our burp repeater tab should look like the following:
{F106538} 

You will notice I am searching for the string "cannot find" in the response tab. If a file is not found on the windows host it will return saying "The system cannot find the file specified" as well as another variation of that.  Since the first request is for cmd.exe which IS found on the system this error is not present. This can also be verified by running telnet, ftp, calc.exe.

The following will produce a "The system cannot find the file specified" error:
$ java -jar ysoserial-0.0.4-all.jar CommonsCollections1 'fakefile.exe' > serialdata

Burp Output:
{F106541} 


This is proving that files are being run on the system.

</details>

---
*Analysed by Claude on 2026-05-12*
