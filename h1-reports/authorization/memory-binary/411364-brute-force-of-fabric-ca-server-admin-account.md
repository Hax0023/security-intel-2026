# Brute Force of Fabric-CA Server Admin Account via Unrestricted Login Attempts

## Metadata
- **Source:** HackerOne
- **Report:** 411364 | https://hackerone.com/reports/411364
- **Submitted:** 2018-09-19
- **Reporter:** xiaoc
- **Program:** Hyperledger Fabric
- **Bounty:** Not specified in report
- **Severity:** critical
- **Vuln:** Brute Force Attack, Insufficient Rate Limiting, Weak Default Configuration, Insecure Network Exposure
- **CVEs:** None
- **Category:** memory-binary

## Summary
Fabric-CA server is vulnerable to brute force attacks against the admin account due to missing rate limiting on failed login attempts, combined with default insecure configurations that expose the service on all network interfaces (0.0.0.0:7054). An attacker can enumerate and compromise the admin account, gaining high-privilege access to add, delete, update, and query blockchain participants.

## Attack scenario
1. Attacker discovers fabric-ca server listening on 0.0.0.0:7054 through network scanning or publicly exposed instances
2. Attacker identifies default configuration with maxenrollments set to -1, enabling unrestricted outside enrollment
3. Attacker obtains or assumes the admin account username (often 'admin' by default)
4. Attacker performs automated brute force attack against the login endpoint with password dictionary/wordlist without encountering rate limiting
5. Upon successful credential compromise, attacker authenticates as admin to the CA server
6. Attacker leverages admin privileges to add fraudulent identities, delete legitimate participants, update certificates, or query sensitive blockchain data

## Root cause
Three compounding configuration and implementation deficiencies: (1) No rate limiting or account lockout mechanism on failed authentication attempts, (2) Default configuration exposing service on all interfaces (0.0.0.0) rather than restricted localhost, (3) maxenrollments parameter set to -1 allowing unrestricted enrollment which increases attack surface

## Attacker mindset
An attacker would target fabric-ca instances as they represent a critical PKI component controlling identity and access in permissioned blockchain networks. Admin account compromise yields maximum privilege escalation with minimal effort due to brute force feasibility. The combination of network accessibility and missing protections makes this an opportunistic, low-effort attack with extremely high impact.

## Defensive takeaways
- Implement exponential backoff and account lockout after N failed login attempts (recommend 5-10 attempts with 30+ second delays)
- Bind fabric-ca to localhost (127.0.0.1) or specific trusted IPs instead of 0.0.0.0, restrict network access via firewall
- Change default maxenrollments from -1 to appropriate restrictive values (0 or 1) in production configurations
- Enforce strong, unique admin credentials and rotate regularly; avoid default usernames
- Implement comprehensive audit logging of all authentication attempts and account activities
- Use multi-factor authentication for admin accounts where supported
- Apply principle of least privilege: limit admin account usage, create role-based accounts for specific operations
- Monitor for suspicious authentication patterns and failed login clusters

## Variant hunting
Search for: (1) Other Hyperledger projects with similar auth endpoint weaknesses (fabric-orderer, peer), (2) PKI/CA systems with absent rate limiting (EJBCA, HashiCorp Vault, cfssl), (3) Services with maxenrollments/-1 equivalent unlimited parameter defaults, (4) Blockchain infrastructure with 0.0.0.0 bindings in production, (5) Other enrollment/registration endpoints accepting unlimited wrong attempts

## MITRE ATT&CK
- T1110.001
- T1110
- T1078.001
- T1021.004
- T1190

## Notes
This vulnerability is particularly severe in blockchain/permissioned network contexts because CA admin compromise breaks the entire identity and access control model. The report references three independent but related security failures that compound each other. Similar patterns exist in other identity management systems. Exploitation requires no sophisticated tooling and can be performed with basic command-line utilities. The fact that default configs were insecure suggests this may have affected numerous production deployments.

## Full report
<details><summary>Expand</summary>

## fabric-ca server
- Default configuration maxenrollments value -1(enable outside enrollment)
- Listening 0.0.0.0:7054(easily discoved and can be reached)
- No limit to wrong password try
Above conditions result in brute force to CA server admin account

## Impact

## Attack gain a high-level permissioned account to permissioned network and can add\delete\update\query

</details>

---
*Analysed by Claude on 2026-05-24*
