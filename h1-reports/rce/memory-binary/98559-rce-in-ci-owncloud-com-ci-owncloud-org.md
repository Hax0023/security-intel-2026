# RCE in ci.owncloud.com / ci.owncloud.org via Jenkins Java Deserialization

## Metadata
- **Source:** HackerOne
- **Report:** 98559 | https://hackerone.com/reports/98559
- **Submitted:** 2015-11-08
- **Reporter:** tomdev
- **Program:** ownCloud
- **Bounty:** Not specified
- **Severity:** critical
- **Vuln:** Insecure Deserialization, Remote Code Execution, Unsafe Java Object Deserialization
- **CVEs:** None
- **Category:** memory-binary

## Summary
Jenkins instance on ci.owncloud.com/org was vulnerable to a Java deserialization RCE attack via the common library used for object serialization. The vulnerability was exploitable because the Jenkins server was exposed on a public IP address without firewall protection, allowing unauthenticated remote code execution.

## Attack scenario
1. Attacker identifies the publicly accessible Jenkins instance at ci.owncloud.com/org through simple enumeration or GitHub repository references
2. Attacker crafts a malicious serialized Java object payload containing arbitrary code to execute
3. Attacker sends the payload to the specific port where Jenkins is listening and accepting serialized data
4. Jenkins deserializes the malicious object without proper validation, triggering code execution
5. Arbitrary code executes with Jenkins service privileges on the Debian 7 system
6. Attacker gains remote code execution and can read files, execute commands, and compromise the CI/CD infrastructure

## Root cause
Unsafe deserialization of untrusted Java objects from network sources combined with lack of network segmentation and firewall rules protecting the Jenkins instance from public internet access

## Attacker mindset
The attacker demonstrated responsible disclosure by identifying a critical infrastructure vulnerability and providing proof of concept (OS fingerprinting) without fully exploiting it. They motivated the fix by explaining the ease of discovery and the severity of the exposure.

## Defensive takeaways
- Never expose Jenkins or similar build/CI systems directly to the public internet without authentication and authorization controls
- Implement network segmentation using VPNs, firewalls, or private networks for CI/CD infrastructure
- Keep Java and dependent libraries updated to patch deserialization vulnerabilities
- Disable or restrict Java object deserialization features when not required
- Use security serialization filters to validate deserialized objects
- Implement strong authentication and authorization on all Jenkins endpoints
- Conduct regular security audits of infrastructure configuration and exposure
- Use Web Application Firewalls (WAF) to detect and block serialized object payloads

## Variant hunting
Look for other exposed build systems (Travis CI, GitLab CI, GitHub Actions runners) with similar network misconfigurations. Search for other Java-based infrastructure services deserializing untrusted data. Check for similar patterns in other ownCloud infrastructure components.

## MITRE ATT&CK
- T1190
- T1203
- T1059

## Notes
This report references CVE-2015-8103 (Jenkins CLI deserialization RCE). The vulnerability was notable for affecting multiple platforms (WebLogic, WebSphere, JBoss, Jenkins, OpenNMS). The researcher demonstrated exemplary security practices by not including sensitive data (/etc/passwd contents) in the report while providing sufficient proof of exploitation.

## Full report
<details><summary>Expand</summary>

Hi,

I know you are more interested in vulnerabilities found in ownCloud Server, but I do would like to inform you on a RCE that can be executed on ci.owncloud.[com/org]. 

**Vulnerability**
There is a 0day vulnerability in Jenkins that can be exploited in certain circumstances. The Jenkins instance on ci.owncloud.[com/org] is vulnerabile for this attack since it is configured to run on a public IP address and is not firewalled.

The vulnerability exists in the common library used by Java to (de)serialize data. Jenkins will deserialize and execute configuration data sent to a specific port it is listening on. More information on the vulnerability can be found in this [article](http://foxglovesecurity.com/2015/11/06/what-do-weblogic-websphere-jboss-jenkins-opennms-and-your-application-have-in-common-this-vulnerability/).

It was easy to find the Jenkins instance because its name is easy guessable (only later on I found out its also being linked to from your GitHub page).

**POC**
I used a payload to confirm the RCE which tells me ci.jenkins.org is running `Debian 7`. You can use this information as confirmation on the RCE.

I was also able to read the `/etc/passwd` file, but I'd rather not send the data it contains in this report.

**Mitigation**
- Shut down ci.owncloud.com for the time being
- Run ci.owncloud.com on a VPN instead of on a world-accessible public IP address
- Firewall the Jenkins instance

Regards, @tomdev

</details>

---
*Analysed by Claude on 2026-05-12*
