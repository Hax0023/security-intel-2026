# Open TURN Relay Abuse - Lack of Peer Access Control

## Metadata
- **Source:** HackerOne
- **Report:** 843256 | https://hackerone.com/reports/843256
- **Submitted:** 2020-04-08
- **Reporter:** sandrogauci
- **Program:** 8x8 (Atlassian/HipChat)
- **Bounty:** Not specified in writeup
- **Severity:** Critical
- **Vuln:** Unrestricted TURN Relay, Improper Access Control, Internal Network Access, Firewall Bypass
- **CVEs:** None
- **Category:** web-api

## Summary
The TURN server lacked peer access control restrictions, allowing attackers to bypass firewall rules and reach internal services including the coturn telnet management interface and AWS metadata service. Attackers could obtain TURN credentials from the XMPP service and leverage the TURN relay as an unrestricted proxy to access localhost and internal network resources.

## Attack scenario
1. Attacker extracts TURN credentials from XMPP service using browser DevTools (network tab filtering for WS connections and turn type messages)
2. Attacker uses stunner tool to establish authenticated TURN connection to the relay server (tls://host:443)
3. Attacker leverages TURN relay peer mechanism to specify internal peer addresses (127.0.0.1:5766 for telnet, 169.254.169.254 for AWS metadata)
4. Attacker establishes proxied connection to internal services through the TURN relay, bypassing firewall restrictions
5. Attacker connects to coturn telnet management interface and executes reconnaissance commands (pc command showing configuration)
6. Attacker accesses AWS metadata service to retrieve IAM credentials for HipChatVideo-Coturn service account

## Root cause
TURN server configuration lacked validation of peer addresses, failing to restrict relay targets to external addresses only. The 'no-loopback-peers' and firewall egress controls were either disabled or not enforced, allowing relay to localhost and internal networks.

## Attacker mindset
Lateral movement and privilege escalation through service account compromise. By pivoting through the TURN relay, the attacker could enumerate internal infrastructure, access management interfaces, and potentially escalate to RCE via the coturn telnet interface (psd file write commands). Cloud credential theft via metadata service access.

## Defensive takeaways
- Implement strict peer address validation in TURN configuration - only allow external/expected peer addresses, explicitly block RFC1918 ranges and loopback addresses
- Enable and enforce 'no-loopback-peers=ON' and similar restrictions in coturn configuration
- Restrict TURN credential validity with short TTLs and rotate credentials frequently
- Segment TURN server network access - run on isolated network segment without direct access to internal services or metadata endpoints
- Disable telnet management interface (port 5766) or restrict to localhost only with authentication
- Implement egress filtering on TURN server firewall rules - deny connections to internal networks and metadata services
- Use certificate pinning and restrict TLS versions to prevent MITM of TURN connections
- Monitor TURN relay for suspicious peer addresses and connection patterns
- Regularly audit TURN server logs for non-standard peer connections and access to restricted addresses

## Variant hunting
Search for similar TURN/STUN servers lacking peer restrictions; test other Atlassian/8x8 services using TURN infrastructure; examine WebRTC implementations in other video conferencing platforms (Slack reference provided); check for IPv6 bypass possibilities; test for privilege escalation via coturn admin commands; enumerate other internal services potentially accessible through relay abuse

## MITRE ATT&CK
- T1190
- T1570
- T1005
- T1526
- T1110
- T1021.001
- T1078.004
- T1040

## Notes
This is not technically SSRF but functionally equivalent or worse - unrestricted network relay access. The vulnerability was responsibly disclosed with testing limited to read-only operations on metadata service and safe commands on coturn. The presence of both TCP and UDP relay capabilities on one endpoint increased impact. Coturn telnet interface with file write capabilities (psd command) suggests potential RCE path. AWS service account credentials could enable further cloud infrastructure compromise.

## Full report
<details><summary>Expand</summary>

> NOTE: This is not an SSRF vulnerability but an open TURN relay vulnerability. Typically, this security vulnerability has at least the same impact as an SSRF. However it is considered more useful from an attacker's point of view since attacks are not restricted to HTTP.

- Affects: 
    - `█████:443`
    - `████████:443`

## Description

The affected TURN server did not put any restrictions on peer which allows remote attackers to bypass firewall rules and reach internal services on the server itself as well as the AWS internal network. In the case of `██████████:443`, both TCP and UDP peers could be specified, while `███████:443` appeared to restrict TCP and only allow UDP.

## Steps To Reproduce:

1. Retrieved temporary TURN credentials from XMPP by:
    - making use of Chrome's devtools 
    - open the network tab, filter just WS connections
    - in the `xmpp-websocket` messages, set a filter for `type='turn'`
    - observe the TURN hostname and credentials
2. Made use of an internal tool called `stunner` as follows: `stunner recon tls://███████:443 -u ████████`
3. Made use of stunner's port scanner and socks proxy to reach the telnet server, AWS meta-data service and so on

Note that we restricted our tests to just the following to avoid causing denial of service to the system:

- Read access to AWS meta-data service
- Only running `help` and `pc` commands on coturn telnet server (other commands may be destructive)

The following is an excerpt from the connection to the coturn telnet server:


```
proxychains -f config telnet 127.0.0.1 5766
[proxychains] config file found: config
[proxychains] preloading /usr/lib64/proxychains-ng/libproxychains4.so
[proxychains] DLL init: proxychains-ng 4.13
Trying 127.0.0.1...
[proxychains] Dynamic chain  ...  127.0.0.1:9999  ...  127.0.0.1:5766  ...  OK
Connected to 127.0.0.1.
Escape character is '^]'.

> pc

  verbose: ON
  daemon process: ON
  stale-nonce: ON (*)
  stun-only: OFF (*)
  no-stun: OFF (*)
  secure-stun: OFF (*)
  do-not-use-config-file: OFF
  RFC5780 support: ON
  net engine version: 3
  net engine: UDP thread per CPU core
  enforce fingerprints: OFF
  mobility: OFF (*)
  udp-self-balance: OFF
  pidfile: /var/run/turnserver.pid
  process user ID: 0
  process group ID: 0
  process dir: /

  cipher-list: DEFAULT
  ec-curve-name: empty
  DH-key-length: 1066
  Certificate Authority file: empty
  Certificate file: /████████.crt
  Private Key file: /███.key
  Listener addr: 127.0.0.1
  Listener addr: ██████
  Listener addr: ::1
  Listener addr: ███████
  no-udp: OFF
  no-tcp: OFF
  no-dtls: OFF
  no-tls: OFF
  TLSv1.0: ON
    TLSv1.1: ON
  TLSv1.2: ON
  listener-port: 443
  tls-listener-port: 5349
  alt-listener-port: 0
  alt-tls-listener-port: 0


  Relay addr: █████
  Relay addr: ██████████
  server-relay: OFF
  no-udp-relay: OFF (*)
  no-tcp-relay: OFF (*)
  min-port: 49152
  max-port: 65535
  no-multicast-peers: OFF (*)
  no-loopback-peers: OFF (*)

  DB type: SQLite
  DB: /var/lib/turn/turndb

  Default realm: █████
  CLI session realm: █████
...

> q
```

## Supporting Material/References:

- Similar vulnerability: <https://www.rtcsec.com/2020/04/01-slack-webrtc-turn-compromise>

## Impact

Abuse of this vulnerability allows attackers to:

- control Coturn by connecting to the telnet server on port 5766 which in turn, allows for writing of files on disk (e.g. using `psd` command), display and editing of the coturn configuration, stopping the server
- connecting to the AWS meta-data service and retrieving IAM credentials for user `HipChatVideo-Coturn`, viewing user-data configuration etc
- scanning `127.0.0.1` and internal network on `██████` and connecting to internal services

Note that in the case of `██████████:443`, both TCP and UDP peers can be specified, while `███:443` appeared to be restricted to just UDP which somewhat limits the security impact of this vulnerability.

We think that it is likely that abuse of the coturn telnet server could lead to remote code execution on the server and further penetration inside 8x8's infrastructure.

</details>

---
*Analysed by Claude on 2026-05-24*
