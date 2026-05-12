# Pre-auth RCE on Twitter Pulse Secure SSL VPN via CVE-2019-11510 and CVE-2019-11539 Chain

## Metadata
- **Source:** HackerOne
- **Report:** 591295 | https://hackerone.com/reports/591295
- **Submitted:** 2019-05-28
- **Reporter:** orange
- **Program:** Twitter
- **Bounty:** Not specified
- **Severity:** critical
- **Vuln:** Pre-auth Arbitrary File Reading, Post-auth Command Injection, Stack Buffer Overflow, Post-auth Arbitrary File Writing, Session Hijacking, Credential Exposure, 2FA Bypass
- **CVEs:** CVE-2019-11510, CVE-2019-11542, CVE-2019-11539, CVE-2019-11538, CVE-2019-11508, CVE-2019-11540
- **Category:** memory-binary

## Summary
DEVCORE researchers discovered a critical vulnerability chain in Pulse Secure SSL VPN affecting Twitter. By exploiting CVE-2019-11510 (pre-auth file reading), attackers could extract plaintext credentials and Duo 2FA secrets, then chain this with CVE-2019-11539 (post-auth command injection) to achieve pre-authentication RCE. The vulnerability persisted on Twitter's infrastructure for over one month after patches were released.

## Attack scenario
1. Attacker exploits CVE-2019-11510 to read /data/runtime/mtmp/system file without authentication containing VPN user credentials and Duo integration keys
2. Attacker extracts plaintext passwords from cached LMDB database (dataa/data.mdb) and Duo secret key from system configuration files
3. Attacker bypasses Two-Factor Authentication using extracted Duo credentials or reuses valid sessions from randomVal/data.mdb without Roaming Session enabled
4. Attacker accesses admin interface via web proxy function using URL path traversal (https://0/admin/) after session establishment
5. Attacker leverages CVE-2019-11539 command injection vulnerability in admin interface to execute arbitrary system commands
6. Attacker achieves remote code execution with VPN service privileges, accessing intranet, stealing additional credentials, and compromising connected VPN clients

## Root cause
Pulse Secure SSL VPN contained multiple authentication and authorization flaws: (1) unauthenticated file traversal allowing access to sensitive runtime files, (2) plaintext credential caching in LMDB databases, (3) inadequate session validation enabling reuse, (4) insufficient access controls on admin endpoints, and (5) unvalidated command execution in administrative functions. Missing security patching on Twitter's infrastructure delayed mitigation.

## Attacker mindset
Sophisticated threat actor targeting enterprise VPN infrastructure to establish persistent access to corporate networks. Focus on pre-authentication vectors to bypass security controls, extraction of credential material for privilege escalation and lateral movement, and chaining multiple vulnerabilities to achieve RCE. Interest in accessing internal networks, stealing employee credentials, compromising connected endpoints, and exfiltrating sensitive data from integrated services (Okta, Salesforce, Google).

## Defensive takeaways
- Implement immediate patching procedures for critical VPN infrastructure with maximum 48-72 hour SLA before public exploitation
- Disable plaintext credential caching; use secure credential storage with encryption-at-rest and in-transit
- Enforce strict input validation and parameterized queries to prevent command injection in all administrative functions
- Implement pre-authentication file access controls with whitelist-based path restrictions
- Require certificate-based 2FA with local validation rather than storing external API secrets on VPN appliances
- Enable session binding with device fingerprinting and enforce Roaming Session disabling
- Conduct regular security assessments of VPN infrastructure and maintain vulnerability monitoring dashboards
- Implement network segmentation to limit lateral movement from compromised VPN endpoints
- Monitor VPN admin interface access with anomaly detection and implement rate limiting
- Store cryptographic material and API secrets in hardware security modules, never in config files

## Variant hunting
Hunt for similar pre-auth file traversal vulnerabilities in other SSL VPN products (Cisco AnyConnect, Fortinet FortiClient, SonicWall). Check for plaintext credential storage in LMDB or similar embedded databases. Examine 2FA integration implementations for secret key exposure. Test web proxy path traversal vectors to privileged administrative interfaces. Search for command injection in VPN management APIs. Investigate other Pulse Secure advisory CVEs (CVE-2019-11542, CVE-2019-11538, CVE-2019-11540, CVE-2019-11508) for exploitation chains.

## MITRE ATT&CK
- T1190
- T1133
- T1110
- T1528
- T1550
- T1021
- T1059
- T1039
- T1552
- T1087
- T1555

## Notes
Report demonstrates responsible disclosure with 30+ day grace period before public disclosure. Vulnerability chain demonstrates importance of patching speed in remote access infrastructure. Twitter's delayed patching created extended window of exposure. Researchers presented full exploitation details at Black Hat USA 2019. Redacted sensitive data (passwords, system details) in public report. This incident catalyzed industry-wide attention to SSL VPN security posture across enterprises.

## Full report
<details><summary>Expand</summary>

Hi, we(Orange Tsai and Meh Chang) are the security research team from DEVCORE. Recently, we are doing a research about SSL VPN security, and found several critical vulnerabilities on Pulse Secure SSL VPN! We have reported to vendor and [patches](https://kb.pulsesecure.net/articles/Pulse_Security_Advisories/SA44101) have been released on `2019/4/25`. Since that, we keep monitoring numerous large corporations using Pulse Secure and we noticed that Twitter haven't patched the SSL VPN server over one month!

These vulnerabilities include a pre-auth file reading(CVSS 10) and a post-auth(admin) command injection(CVSS 8.0) which can be chained into a pre-auth RCE! Here are all vulnerabilities we found:

* CVE-2019-11510 - Pre-auth Arbitrary File Reading
* CVE-2019-11542 - Post-auth Stack Buffer Overflow
* CVE-2019-11539 - Post-auth Command Injection
* CVE-2019-11538 - Post-auth Arbitrary File Reading
* CVE-2019-11508 - Post-auth Arbitrary File Writing
* CVE-2019-11540 - Post-auth Session Hijacking


## Our Steps

First, we download following files with CVE-2019-11510:
1. `/etc/passwd`
2. `/etc/hosts`
3. `/data/runtime/mtmp/system`
4. `/data/runtime/mtmp/lmdb/dataa/data.mdb`
5. `/data/runtime/mtmp/lmdb/dataa/lock.mdb`
6. `/data/runtime/mtmp/lmdb/randomVal/data.mdb`
7. `/data/runtime/mtmp/lmdb/randomVal/lock.mdb`

██████████


The VPN user and hashed passwords are stored in the file `mtmp/system`. However, Pulse Secure caches the plain-text password in the `dataa/data.mdb` once the user log-in. Here, we just grep part of username/plain-text-password for proofs and further actions.

*P.S. we mask the password field for security concerns, and we can send to you if you provide your PGP key.*

```
█████████ / ████
█████████ / ██████
█████ / █████████
██████████ / █████████
███ / ██████
```

Once we log into the SSL VPN, we found the server has enabled the Two-Factor Authentication. Here, we listed two methods to bypass the 2FA:

████

1. We observed Twitter using the 2FA solution from Duo.com. With the file `mtmp/system`, we could obtain the integration key, secret key, and API hostname, which should be protected carefully according to the [Duo documentation](https://duo.com/docs/pulseconnect):

    > Treat your secret key like a password
    The security of your Duo application is tied to the security of your secret key (skey). Secure it as you would any sensitive credential. Don't share it with unauthorized individuals or email it to anyone under any circumstances!

    ```
    # secret-key = ██████████
    ████
    dc=███,dc=duosecurity,dc=com
    cn=<USER>

    # LDAP password = ██████████
    ██████████
    █████
    ███████
    uid=<username>
    ```

2. The Pulse Secure stores the user session in the `randomVal/data.mdb`. Without `Roaming Session` option enabled, we can reuse the session and log into your SSL VPN!

██████████



The next, in order to trigger the command injection(CVE-2019-11542). We leverage the web proxy function to access the admin interface with following URL:

```
https://0/admin/
```

████████

We are now trying to crack the admin hash by GPU. It seems takes a long time, but once we cracked, we can achieve RCE absolutely. Actually, we can simply wait for the admin login and obtain the plain-text password directly!
```
███████
███████
```

Anyway, we decided to report to you first, because it's lethal and critical. If you want, we can provide the RCE PoC in admin interface in order to proof the potential risk!


## Impact:

1. Access Intranet(we have accessed the `███████` for proof) ██████████
2. Plenty of staff plain-text passwords
3. Internal server and passwords(such as the LDAP)
4. Attack back all VPN clients(we will detail the step in [Black Hat USA 2019](https://www.blackhat.com/us-19/briefings/schedule/#infiltrating-corporate-intranet-like-nsa---pre-auth-rce-on-leading-ssl-vpns-15545))
5. Private keys
6. Sensitive cookies in Web VPN(such as okta, salesforce, box.com and google)

## Supporting Material/References:

We attached screenshots to proof our actions. For security concern, we didn't attach the `mtmp/system` and the `dataa/data.mdb`. If you want, we can send to you with your PGP key encrypted!

## Recommend Solution

The only and simplest way to solve this problem is to upgrade your SSL VPN to the [latest version](https://kb.pulsesecure.net/articles/Pulse_Security_Advisories/SA44101)!

## Impact

1. Access Intranet(we have accessed the `████████` for proof) ████
2. Plenty of staff plain-text passwords
3. Internal server and passwords(such as the LDAP)
4. Attack back all VPN clients(we will detail the step in [Black Hat USA 2019](https://www.blackhat.com/us-19/briefings/schedule/#infiltrating-corporate-intranet-like-nsa---pre-auth-rce-on-leading-ssl-vpns-15545))
5. Private keys
6. Sensitive cookies in Web VPN(such as okta, salesforce, box.com and google)

</details>

---
*Analysed by Claude on 2026-05-11*
