# Denial of Service on Hyperledger Indy Validator Nodes via Connection Exhaustion

## Metadata
- **Source:** HackerOne
- **Report:** 1695472 | https://hackerone.com/reports/1695472
- **Submitted:** 2022-09-08
- **Reporter:** cre8
- **Program:** Hyperledger
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Denial of Service, Resource Exhaustion, Connection Pooling Attack, Lack of Rate Limiting
- **CVEs:** CVE-2022-31006
- **Category:** memory-binary

## Summary
An attacker can exhaust validator node connections by sending 500+ parallel read requests, rendering the blockchain network unreachable to legitimate clients. The attack exploits the public readable nature of the ledger combined with insufficient connection limits and timeouts, causing service degradation without data corruption.

## Attack scenario
1. Attacker identifies that Hyperledger Indy validator nodes accept public read requests without authentication or rate limiting
2. Attacker establishes 500 parallel connections to each validator node in the network
3. Upon reaching connection limit, attacker opens additional connections by closing old ones, maintaining persistent load
4. Attacker increases request payload size with random headers/JSON values to consume additional bandwidth and processing resources
5. Legitimate clients attempting read/write requests experience severe latency (multiple seconds) or complete request failures
6. Attack continues for duration of attacker's resource availability; network recovers only after attack ceases

## Root cause
Insufficient connection pooling limits, lack of per-client rate limiting, missing request timeout enforcement, and absence of resource quotas on public-facing read endpoints allow attackers to monopolize server resources and block legitimate traffic.

## Attacker mindset
Resource-conscious adversary seeking service disruption without requiring sustained 24/7 attack; leverages cloud infrastructure for on-demand scaling (2-minute setup) to perform targeted temporary DoS attacks with minimal infrastructure cost.

## Defensive takeaways
- Implement strict per-client connection limits and rate limiting on all public-facing endpoints
- Enforce aggressive connection timeouts and idle connection termination policies
- Add firewall rules to limit request size and enforce bandwidth quotas per source IP
- Implement request queuing with backpressure mechanisms and graceful degradation
- Deploy reverse proxy/load balancer with DDoS mitigation capabilities in front of validator nodes
- Monitor connection metrics and implement alerts for abnormal connection patterns
- Consider authentication/token requirements even for read operations if operationally feasible
- Implement adaptive connection limits based on available system resources
- Scale infrastructure defensively but recognize attacker can also scale on-demand
- Separate validator nodes from public-facing observer nodes to isolate blast radius

## Variant hunting
Slow HTTP DoS attacks with incomplete requests (Slowloris-style attacks)
POST/write request flooding to consensus endpoints if similar protections are absent
Concurrent transaction submission exceeding mempool limits
Connection exhaustion on RPC/JSON-RPC endpoints in other blockchain implementations
Amplified DoS via larger response payloads requested by attacker
Resource exhaustion on WebSocket connections if supported
CPU exhaustion via complex query requests rather than simple connection holds

## MITRE ATT&CK
- T1190
- T1498
- T1498.001
- T1565.002

## Notes
The attack is notable for requiring minimal attacker sophistication (500 simple read requests) while achieving near-complete service denial. The public nature of read access prevents traditional allowlisting defenses. Counterintuitive insight: scaling validator infrastructure does not solve the problem since attackers can elastically scale attack resources on-demand. Architectural separation of validators from public-facing observers is a potential long-term mitigation but shifts the attack surface rather than eliminating it. No blockchain consensus data corruption occurs, limiting impact to availability rather than integrity/authenticity.

## Full report
<details><summary>Expand</summary>

Attack was documented in the in the github repo: https://github.com/hyperledger/indy-node/security/advisories/GHSA-x996-7qh9-7ff7

# Attack:
The attacker sends 500 read requests to each node and opens a new one when
holding 500 parallel connections. Every user is able to send read requests
since it's a public readable registry so setting up an allowlist like it's
done with the nodes' port for the consensus does not work here. To increase
the efficiency:

the custom read request is increased with more bytes (random header or
json values)
the bandwidth of the sender machine is limited
Requirements on the attacker side:
Indy-VDR: comment out the timeouts. Using another tool to send the requests
could be even more efficient
VM: attack can be performed from one or multiple VMs limited connection: using
TC to limit the bandwidth (value depends on the amount of connections)
Sample Implementation
We set up a VON-Network and added the firewall rules. The VM had 32 CPUs
and 64 GB RAM

# Result:
there is no damage to the blockchain, only an unreachable network as long
as the attack is going on .
Other clients are not able to send read or write requests to the nodes. In
the "best case" their requests will go through but with a response time of
multiple seconds, see:
Not available [image: image.png]

Not available [image: image.png]

# Counteractions:
blacklisting actors: It does not matter what is in the body since the
firewall rule acts in front of indy that is processing the information. To
avoid big requests the firewall could set a limit of the request size, but
this could also block valid requests.
Scaling via the observer-pattern: Right now the amount of nodes is
limited so blocking 25*500 connections is very easy. When adding nodes in
front of the validators to prevent accessing from the internet the
validators are save, but then all the observers are under attack
Scalability: Giving the VMs more CPU and RAM to increase the parallel
connections amount can help in first run, but the DoS attack can be
performed as a DDos. An attacker does not have to DoS the network 24/7, but
can scale up the VMs on demand to attack a specific network. The setup is
done in about 2 minutes automatically. In our test we used 500 as the
limit. Maybe there is some kind of algorithm for the node administrators to
calculate the limit based on their CPU. But in this case the attacker can
also increase his ressources.

## Impact

An attacker can max out the number of client connections allowed by the ledger, leaving the ledger unable to be used for its intended purpose.

However, the ledger content will not be impacted and the ledger will resume servicing client requests after the conclusion of the attack.

</details>

---
*Analysed by Claude on 2026-05-24*
