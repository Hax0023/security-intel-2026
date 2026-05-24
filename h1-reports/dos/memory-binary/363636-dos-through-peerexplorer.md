# DoS through PeerExplorer - Memory Exhaustion via Challenge Accumulation

## Metadata
- **Source:** HackerOne
- **Report:** 363636 | https://hackerone.com/reports/363636
- **Submitted:** 2018-06-09
- **Reporter:** z3t
- **Program:** RSK Smart Bitcoin (rskj)
- **Bounty:** Not specified in provided content
- **Severity:** high
- **Vuln:** Denial of Service, Memory Exhaustion, Resource Leak, Improper Resource Management
- **CVEs:** None
- **Category:** memory-binary

## Summary
The peer discovery mechanism in PeerExplorer is vulnerable to memory exhaustion through unbounded accumulation of challenge entries in the activeChallenges map. An attacker can initiate peer discovery handshakes but never respond to challenge pings, causing challenge entries to persist indefinitely and exhaust target node memory. This affects distributed peer-to-peer network resilience by enabling attackers to disable specific nodes.

## Attack scenario
1. Attacker N1 sends initial ping message to target node N2
2. N2 responds with pong and subsequent ping message, adding entry to pendingPingRequests
3. N1 replies with pong to establish connection attempt
4. N2's addConnection fails (NodeDistanceTable bucket full) and calls startChallenge, sending new ping and creating activeChallenges entry
5. N1 deliberately never responds to the challenge ping, leaving entry in activeChallenges permanently
6. Attacker repeats with unique NodeIDs or from multiple source IPs every 30 seconds, accumulating uncleaned challenge entries until target node runs out of memory

## Root cause
The NodeChallengeManager.activeChallenges map only removes entries when a valid pong response arrives matching the challenge messageId. There is no timeout mechanism, garbage collection, or maximum size limit on activeChallenges. Once added, entries persist indefinitely if the challenger never responds, creating a resource leak.

## Attacker mindset
A network attacker aims to disable target peer nodes to partition the blockchain network or perform selective DoS attacks. By exploiting the peer discovery protocol, they can exhaust memory on victim nodes without requiring high bandwidth, making it a cost-effective attack that scales across multiple victims.

## Defensive takeaways
- Implement timeout-based automatic removal of stale challenge entries in activeChallenges (similar to pendingPingRequests expiry)
- Add maximum size limits with eviction policies (LRU/LFU) to activeChallenges map
- Rate limit peer discovery requests per source IP or NodeID
- Implement exponential backoff and cooldown periods for repeated failed challenges from same peer
- Monitor activeChallenges map size and alert on abnormal growth
- Use bounded collections (e.g., LinkedHashMap with removeEldestEntry) instead of unbounded HashMap
- Implement per-peer challenge quotas to prevent single attacker from monopolizing challenge slots

## Variant hunting
Check pendingPingRequests for similar timeout vulnerabilities or unbounded growth conditions
Review other protocol message handlers for missing cleanup/timeout logic on pending state maps
Analyze distanceTable and establishedConnections for similar resource exhaustion vectors
Examine message validation logic for other protocol states that can be held open indefinitely
Search for other unbounded collections in peer discovery that respond to attacker-controlled messages
Test for memory leaks in other network protocol implementations (DHT, routing tables, etc.)

## MITRE ATT&CK
- T1190
- T1561
- T1499

## Notes
The vulnerability demonstrates a class of issues common in P2P protocols where bidirectional handshakes create stale state if one party abandons the exchange. The attack is particularly effective because: (1) peer discovery is often less monitored than consensus mechanisms, (2) attackers can use spoofed NodeIDs to appear as distinct peers, (3) distributed attackers can circumvent per-IP rate limiting. The 30-second pending request cleanup provides no protection since the challenge enters a different, unmanaged collection. Default config allows ~65k connections/minute per attacker IP, but multiple IPs can scale attack significantly.

## Full report
<details><summary>Expand</summary>

**Summary:** The peer discovery implementation is vulnerable to a Denial of Service attack due to improper management of connections.

**Description:** The two main files of interest in detailing this vulnerability are [PeerExplorer.java](https://github.com/rsksmart/rskj/blob/master/rskj-core/src/main/java/co/rsk/net/discovery/PeerExplorer.java) and [NodeChallengeManager.java](https://github.com/rsksmart/rskj/blob/master/rskj-core/src/main/java/co/rsk/net/discovery/NodeChallengeManager.java). To explain the flow of execution I'll be mentioning two theoretical nodes: an attacker, "N1" and a target, "N2".

When N1 sends an initial "ping" message to N2, N2 will reply with a "pong" message and a subsequent ping message to continue the handshake. After this, when N1 replies with a pong message, N2 will attempt to add N1 to its structure holding established connections. The relevant code snippets from `PeerExplorer.java` are below:
```    
public void handlePong(String ip, PongPeerMessage message) {
	PeerDiscoveryRequest request = this.pendingPingRequests.get(message.getMessageId());

	if (request != null && request.validateMessageResponse(message)) {
		this.pendingPingRequests.remove(message.getMessageId());
		NodeChallenge challenge = this.challengeManager.removeChallenge(message.getMessageId());
		if (challenge == null) {
			this.addConnection(message, ip, message.getPort());
		}
	}
}
...
private void addConnection(PongPeerMessage message, String ip, int port) {
	Node senderNode = new Node(message.getNodeId().getID(), ip, port);
	if (!StringUtils.equals(senderNode.getHexId(), this.localNode.getHexId())) {
		OperationResult result = this.distanceTable.addNode(senderNode);

		if (result.isSuccess()) {
			NodeID senderId = senderNode.getId();
			this.establishedConnections.put(senderId, senderNode);
			logger.debug("New Peer found ip:[{}] port[{}]", ip, port);
		} else {
			this.challengeManager.startChallenge(result.getAffectedEntry().getNode(), senderNode, this);
		}
	}
}
```
The `addConnection` method first attempts to add N1 to the `NodeDistanceTable` - a structure designed to hold a limited number of nodes (by default, 4096). If this insertion fails due to the target `NodeDistanceTable` bucket already being full, the attempted connection is instead added to `NodeChallengeManager`. The relevant code snippets from `NodeChallengeManager.java` are below:
```
public NodeChallenge startChallenge(Node challengedNode, Node challenger, PeerExplorer explorer) {
	PingPeerMessage pingMessage = explorer.sendPing(challengedNode.getAddress(), 1, challengedNode);
	String messageId = pingMessage.getMessageId();
	NodeChallenge challenge = new NodeChallenge(challengedNode, challenger, messageId);
	activeChallenges.put(messageId, challenge);
	return challenge;
}

public NodeChallenge removeChallenge(String challengeId) {
	return activeChallenges.remove(challengeId);
}
```

Through the `startChallenge` method N2 will send N1 another ping message, adding a "challenge" to `activeChallenges` with that new ping message's `messageId`. The issue here is that **the entry is only ever removed from `activeChallenges` if N1 replies with a pong that has the same `messageId` as the new ping message** - as seen in `PeerExplorer.handlePong`. Thus, N1 is able to create an arbitrary number of entries in `activeChallenges` by never sending N2 a pong with the challenge ping's `messageId`.

It should be noted that there is a slight limitation as to how this could be exploited by a single host. The relevant code snippets from `PeerExplorer.java` are below:
```
public PingPeerMessage sendPing(InetSocketAddress nodeAddress, int attempt, Node node) {
	PingPeerMessage nodeMessage = checkPendingPeerToAddress(nodeAddress);

	if (nodeMessage != null) {
		return nodeMessage;
	}
	....
}
...
private PingPeerMessage checkPendingPeerToAddress(InetSocketAddress address) {
	for (PeerDiscoveryRequest req : this.pendingPingRequests.values()) {
		if (req.getAddress().equals(address)) {
			return (PingPeerMessage) req.getMessage();
		}
	}

	return null;
}

```
The `sendPing` method will only ever actually send a new ping to N1 if there are no pending pings to its `InetSocketAddress` (which is deemed equal if the host and port match) - as seen in `checkPendingPeerToAddress`. However, pending pings have a set expiry time (by default, 30 seconds) and those that have expired are cleared by `PeerExplorerCleaner` at a fixed rate (by default, every 60 seconds). So due to this limitation, with the default configuration settings a single host can only complete 65,535 handshakes (one per port) every minute - imposing a (perhaps unreachable) limit on the time it takes to exhaust the target node's memory. Though this can obviously be circumvented by using multiple hosts to attack a target node. 


Because most peer discovery functionality identifies nodes by their `NodeID` and not by host/port, it's trivial to send a flood of requests with unique `NodeID`s to fill `NodeDistanceTable` and subsequently make an unrestricted amount of in-memory insertions into `NodeChallengeManager.activeChallenges`. This is further aided by the fact that `NodeChallengeManager` is never purged, so the request flood does not have to occur within a short period of time. Memory exhaustion will eventually occur as the `NodeChallenge` objects begin taking up a significant amount of memory and are not eligible for garbage collection. This is expected to eventually disable node functionality as individual threads die when they throw `OutOfMemoryError`s, but in my testing it ended up crashing the whole JVM after reaching ~200,000 insertions.

## Steps To Reproduce:

I've attached a PoC program that interfaces with the RSKj library for the sake of simplicity. Due to the PoC program being somewhat inefficient and unreliable, I ended up accelerating the testing process by modifying my testing node's `NodeChallengeManager` to make 10 insertions per valid `startChallenge` call. If you're interested in running the PoC despite those issues, follow these steps:
  1. Download a copy of the RSKj code
  2. Move the PoC files into the `co.rsk.net.discovery` package (overwrite `PeerExplorer.java` with my modified version)
  3. Launch a node for testing - ensure peer discovery is enabled
  4. Compile and run the PoC from `PeerFlood` - arguments format: `<local_address> <target_address> <target_port> <num_threads>`
  5. Monitor testing node's logs and stability

If you're developing your own PoC, you need to simply flood a testing node with connections that use random `NodeID`s, completing a single ping<->pong handshake then immediately disconnecting.

## Mitigation
This could be mitigated by implementing expiring challenges that are cleared by `PeerExplorerCleaner`.

## Impact

An attacker could crash any RSKj node with peer discovery enabled (which it is by default).

</details>

---
*Analysed by Claude on 2026-05-24*
