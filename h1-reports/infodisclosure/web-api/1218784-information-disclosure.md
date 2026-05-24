# Exposed Tendermint RPC Endpoint with Sensitive Information Disclosure

## Metadata
- **Source:** HackerOne
- **Report:** 1218784 | https://hackerone.com/reports/1218784
- **Submitted:** 2021-06-07
- **Reporter:** hackerinthewood
- **Program:** Sifchain
- **Bounty:** Unknown
- **Severity:** High
- **Vuln:** Information Disclosure, Exposed Service, Misconfiguration, Sensitive Data in Source Code
- **CVEs:** None
- **Category:** web-api

## Summary
A publicly accessible Tendermint RPC endpoint (rpc.sifchain.finance) exposes sensitive blockchain and node information including node IDs, validator addresses, and network topology. Additionally, hardcoded Vault credentials and Kubernetes commands were discovered in the public GitHub repository, creating a secondary path for infrastructure compromise.

## Attack scenario
1. Attacker discovers rpc.sifchain.finance through reconnaissance and enumerates available endpoints
2. Attacker queries /status endpoint and obtains node information including node ID, IP address (34.228.72.160), validator public key, and network version
3. Attacker uses exposed node ID and network details to perform targeted attacks against the Tendermint P2P network or attempt eclipse attacks
4. Attacker finds GitHub repository with hardcoded Vault credentials and kubectl commands in deploy/rake/cluster.rake
5. Attacker uses credentials or deployment information to access Vault secrets or Kubernetes infrastructure
6. Attacker gains ability to broadcast transactions, query blockchain state, or access sensitive infrastructure

## Root cause
The Tendermint RPC endpoint was left publicly accessible without authentication or access controls, exposing all standard RPC methods. Additionally, infrastructure credentials and deployment scripts were committed to a public GitHub repository without sanitization.

## Attacker mindset
Reconnaissance-focused attacker who systematically searches public repositories and internet-facing services for exposed information. The attacker demonstrates responsible disclosure mentality by reporting uncertainties about impact rather than exploiting them.

## Defensive takeaways
- Restrict RPC endpoint access via firewall rules, VPN, or API gateway with authentication
- Implement whitelist of allowed RPC methods if public exposure is necessary
- Scan GitHub repositories for exposed credentials using automated tools before commits
- Never hardcode credentials, API keys, or infrastructure commands in source code
- Use environment variables, secret management systems, and configuration files for sensitive data
- Implement pre-commit hooks to detect and prevent credential leakage
- Rotate any credentials that were exposed in version control immediately
- Monitor publicly accessible RPC endpoints for suspicious query patterns
- Consider rate limiting on RPC endpoints to mitigate reconnaissance and DoS attacks

## Variant hunting
Search other Sifchain GitHub repositories for additional hardcoded credentials
Check for other publicly accessible Tendermint nodes in the blockchain ecosystem with similar misconfigurations
Query rpc.sifchain.finance for broadcast_tx endpoints to determine if transaction injection is possible
Look for other Kubernetes or infrastructure management files in public repos of blockchain projects
Examine git history of the affected file to identify when credentials were added and what actions occurred
Search for other rpc endpoints on related domains (*.sifchain.*) with similar exposure patterns

## MITRE ATT&CK
- T1526 - Passive Scanning (reconnaissance of public services)
- T1592 - Gather Victim Information (gathering details about target infrastructure)
- T1087 - Account Discovery (identifying validator accounts and node identities)
- T1552 - Unsecured Credentials (hardcoded credentials in source code)
- T1046 - Network Service Scanning (enumerating RPC endpoints)
- T1595 - Active Scanning (querying exposed RPC methods)
- T1040 - Traffic Sniffing (potential network topology learning)

## Notes
The report demonstrates uncertainty about actual exploit potential, which is reasonable but conservative. The exposed RPC endpoint alone enables reconnaissance and potential network-level attacks. The GitHub credentials represent a separate, potentially more critical vulnerability. The reporter's mention of 'not knowing what access it has' suggests they tested boundary without pushing exploitation further—appropriate for responsible disclosure. Tendermint nodes should never expose RPC on public internet without authentication.

## Full report
<details><summary>Expand</summary>

Hi team 

during github recon i find something and I dont know what access it has,  but still i though it would be a good idea to share this finding with you in case it can be used in a way that i dont know.

what i find 

link : https://github.com/Sifchain/sifnode/blob/30f0c45720b964342f3011c124c79c66c4c01a6b/deploy/rake/cluster.rake
      create_test_secret = `kubectl exec --kubeconfig=./kubeconfig -n vault -it vault-0 -- vault kv put kv-v2/staging/test username=test123 password=foobar123`

+
also i find this link 

http://rpc.sifchain.finance/ 

when i open it i find these endpoints 

Available endpoints:

Endpoints that require arguments:
//rpc.sifchain.finance/abci_info?
//rpc.sifchain.finance/abci_query?path=_&data=_&height=_&prove=_
//rpc.sifchain.finance/block?height=_
//rpc.sifchain.finance/block_by_hash?hash=_
//rpc.sifchain.finance/block_results?height=_
//rpc.sifchain.finance/blockchain?minHeight=_&maxHeight=_
//rpc.sifchain.finance/broadcast_evidence?evidence=_
//rpc.sifchain.finance/broadcast_tx_async?tx=_
//rpc.sifchain.finance/broadcast_tx_commit?tx=_
//rpc.sifchain.finance/broadcast_tx_sync?tx=_
//rpc.sifchain.finance/commit?height=_
//rpc.sifchain.finance/consensus_params?height=_
//rpc.sifchain.finance/consensus_state?
//rpc.sifchain.finance/dump_consensus_state?
//rpc.sifchain.finance/genesis?
//rpc.sifchain.finance/health?
//rpc.sifchain.finance/net_info?
//rpc.sifchain.finance/num_unconfirmed_txs?
//rpc.sifchain.finance/status?
//rpc.sifchain.finance/subscribe?query=_
//rpc.sifchain.finance/tx?hash=_&prove=_
//rpc.sifchain.finance/tx_search?query=_&prove=_&page=_&per_page=_&order_by=_
//rpc.sifchain.finance/unconfirmed_txs?limit=_
//rpc.sifchain.finance/unsubscribe?query=_
//rpc.sifchain.finance/unsubscribe_all?
//rpc.sifchain.finance/validators?height=_&page=_&per_page=_


and when i open one of this  i find 

{
  "jsonrpc": "2.0",
  "id": -1,
  "result": {
    "node_info": {
      "protocol_version": {
        "p2p": "7",
        "block": "10",
        "app": "0"
      },
      "id": "b2063fd8e35d1f699a7fab506ef2eb76366051c0",
      "listen_addr": "34.228.72.160:26656",
      "network": "sifchain",
      "version": "0.33.9",
      "channels": "4020212223303800",
      "moniker": "helen",
      "other": {
        "tx_index": "on",
        "rpc_address": "tcp://0.0.0.0:26657"
      }
    },
    "sync_info": {
      "latest_block_hash": "15E4E94C0C11491EFB21E1C41D6532B045BF38F158A41A16A96D249234F65A2A",
      "latest_app_hash": "99B36B8F46BAA06D6E33E0CA6B3E8C000F619758E92A3B4FAFB72AE628E13E1F",
      "latest_block_height": "1767705",
      "latest_block_time": "2021-06-07T03:47:41.661876769Z",
      "earliest_block_hash": "A2D20EE2550E2D962A5ADD95D3CEB2838ECCD622ED2A6A4F47F3F05D4307208C",
      "earliest_app_hash": "",
      "earliest_block_height": "1",
      "earliest_block_time": "2021-02-11T11:59:14.685903388Z",
      "catching_up": false
    },
    "validator_info": {
      "address": "30E8474151D3C6A97BFB942D512317DAF22B9DAD",
      "pub_key": {
        "type": "tendermint/PubKeyEd25519",
        "value": "ubYpBmPNyJFZi401nuYcYPyJcjCpLsPsTMkmunRCJT8="
      },
      "voting_power": "0"
    }
  }
}

## Impact

again I dont know what access it has,  but still i though it would be a good idea to share this finding with you in case it can be used in a way that i dont know.

</details>

---
*Analysed by Claude on 2026-05-24*
