# Unauthenticated Remote Code Execution via Exposed Portainer Docker Management Interface

## Metadata
- **Source:** HackerOne
- **Report:** 1332433 | https://hackerone.com/reports/1332433
- **Submitted:** 2021-09-07
- **Reporter:** 0x0luke
- **Program:** Nextcloud
- **Bounty:** Not specified
- **Severity:** critical
- **Vuln:** Insufficient Access Controls, Default Credentials, Exposed Administrative Interface, Remote Code Execution, Information Disclosure
- **CVEs:** None
- **Category:** memory-binary

## Summary
An unconfigured Portainer instance was exposed on a Nextcloud demo server allowing unauthenticated access to Docker container management. An attacker could create administrative accounts, enumerate all running containers including production PostgreSQL databases, and execute arbitrary bash commands within any container.

## Attack scenario
1. Attacker discovers exposed Portainer service on http://spreed-demo.nextcloud.com:9000
2. Attacker accesses Portainer without authentication and finds account creation enabled
3. Attacker registers a new administrator account with default credentials
4. Attacker gains access to Portainer dashboard displaying all 17 running Docker containers
5. Attacker uses Portainer's container shell functionality to execute arbitrary bash commands
6. Attacker achieves full code execution across multiple containers including production systems

## Root cause
Portainer service deployed without authentication enforcement, account registration allowed, and exposed on public-facing network interface. No firewall restrictions or access controls implemented on administrative management port.

## Attacker mindset
Reconnaissance and opportunistic exploitation. Attacker systematically enumerated exposed services, leveraged lack of access controls to gain administrative privileges, then pivoted to container compromise for maximum impact including malware deployment, DDoS hosting, or data exfiltration.

## Defensive takeaways
- Never expose Docker management tools (Portainer, Docker API) directly to untrusted networks
- Enforce strong authentication with MFA on all administrative interfaces before allowing any functionality
- Disable user self-registration on administrative panels or require approval workflows
- Implement network segmentation - isolate container management to internal networks only
- Restrict Portainer to localhost or private networks, access via VPN/bastion hosts only
- Regularly audit open ports and running services, especially demo/staging environments
- Apply principle of least privilege - containers should have minimal required permissions
- Monitor and alert on Docker container access, especially shell/exec operations

## Variant hunting
Similar exposure patterns likely exist in other Portainer deployments, Docker API endpoints, Kubernetes dashboards, or container registry management interfaces. Check for exposed: Docker daemon sockets, Kubernetes dashboards without RBAC, Docker registry UI without authentication, container orchestration tools (Swarm, Rancher), and other infrastructure management tools on non-standard ports.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1133 - External Remote Services
- T1078 - Valid Accounts
- T1110 - Brute Force
- T1059 - Command and Scripting Interpreter
- T1609 - Container Administration Command
- T1562 - Impair Defenses

## Notes
This represents a complete infrastructure compromise. The attacker gained visibility into internal network topology, running services, storage architecture, and full code execution across production systems. The demo/staging environment classification does not reduce impact if production data is replicated there. The disclosure of 17 containers suggests this is a multi-service deployment with significant blast radius.

## Full report
<details><summary>Expand</summary>

## Summary:
I was able to get RCE on 17 different docker containers, ranging from postgres and some prod enviroments

## Steps To Reproduce:
I found that there was a unconfigured portainer.io service running on http://spreed-demo.nextcloud.com:9000

  1. I created an administrator account with the login creds admin:password (please change these credentials!!!)
  2. The site redirected me to the portainer backend, which displayed the docker containers running on the box, see first screen shot
  3. I was able to fully interact with the docker containers running, the site also allows me to execute arbitrary bash commands on the boxes, See second screenshot

Other info that was disclosed to me from the panel:
Internal IP addresses,
Docker disk volumes
Docker images,
The docker stacks

## Supporting Material/References:

{F1439949}
{F1439951}

## Impact

An attacker can directly take over each docker container on this system to deploy his own malware, run DDoS attacks etc from inside Nextclouds services.

</details>

---
*Analysed by Claude on 2026-05-12*
