# RPC Service Denial of Service via Unbounded Loop in get_fee_estimate

## Metadata
- **Source:** HackerOne
- **Report:** 2338094 | https://hackerone.com/reports/2338094
- **Submitted:** 2024-01-28
- **Reporter:** ptrstr
- **Program:** Monero Project
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Denial of Service, Resource Exhaustion, Integer Overflow/Wraparound, Unbounded Loop
- **CVEs:** None
- **Category:** memory-binary

## Summary
The Monero RPC service's get_fee_estimate endpoint is vulnerable to DOS attacks through the grace_blocks parameter. An attacker can pass a very large uint64_t value (up to 18446744073709551615) that causes an unbounded for loop in get_dynamic_base_fee_estimate_2021_scaling, exhausting CPU resources and rendering the RPC service unresponsive. This affects all versions from v0.18.0.0 through v0.18.3.1 on hard fork version 15 or above.

## Attack scenario
1. Attacker identifies open Monero RPC services on port 18081/28081/38081 using network scanning or Censys queries
2. Attacker verifies target node is running hard fork version 15 or above via hard_fork_info RPC call
3. Attacker crafts malicious get_fee_estimate JSON RPC requests with grace_blocks parameter set to maximum uint64_t value (18446744073709551615)
4. Attacker sends 500+ asynchronous requests to the vulnerable endpoint from multiple sources
5. RPC server threads enter unbounded loops, consuming 100% CPU resources across 2 dedicated RPC threads
6. All subsequent RPC requests timeout as threads are exhausted; service becomes completely unresponsive

## Root cause
The get_dynamic_base_fee_estimate_2021_scaling function contains a for loop that iterates based on the grace_blocks parameter without proper bounds checking. When grace_blocks is set to a very large value, the loop runs for an extremely long time, exhausting CPU resources. The vulnerability exists in the blockchain calculation logic called from the RPC handler when processing fee estimates on hard fork 15+.

## Attacker mindset
Network attacker seeking to disrupt cryptocurrency infrastructure. The attacker likely discovered this vulnerability through code review of open-source Monero repository and recognized the potential for widespread impact. The use of Censys queries to enumerate vulnerable services indicates a sophisticated, scalable attack strategy targeting multiple nodes simultaneously for maximum disruption.

## Defensive takeaways
- Implement strict input validation and bounds checking on all user-supplied numeric parameters, especially those used in loop conditions
- Add maximum iteration limits or timeouts to computationally expensive operations triggered by RPC endpoints
- Separate RPC processing threads from core blockchain threads to prevent resource exhaustion from impacting critical operations
- Implement rate limiting on RPC endpoints to prevent abuse through high-volume requests
- Add telemetry and alerts for unusual CPU consumption patterns on RPC threads
- Review all uint64_t parameters for potential integer overflow/underflow attack vectors
- Consider implementing resource quotas per RPC connection
- Restrict RPC port access to trusted networks when possible

## Variant hunting
Search for similar unbounded loop vulnerabilities in other RPC endpoints that accept large integer parameters (particularly grace_blocks, heights, amounts, or iteration counts). Check other cryptocurrency projects with similar RPC architectures for equivalent vulnerabilities in fee estimation or dynamic scaling calculations. Review any recently introduced scaling calculation functions for missing bounds checks.

## MITRE ATT&CK
- T1190
- T1498
- T1499

## Notes
The vulnerability is triggered specifically on hard fork version 15 or above, indicating a regression introduced in a recent update. The PoC demonstrates reproducibility with 500 concurrent requests. The issue is not logged in standard debug output, making detection difficult without system resource monitoring. Affects nodes that expose RPC to public networks. The attacker provided an XMR address for bounty payment, suggesting good faith disclosure.

## Full report
<details><summary>Expand</summary>

## Summary:
The RPC service running port 18081 (or 28081, 38081) is vulnerable to a DOS rendering the service unusable. This is due to the possibility of a for loop going up until uint64_t's max range (1<<64 - 1).

On the `get_fee_estimate` JSON RPC endpoint, a `uint64_t` parameter `grace_blocks` can be passed. If this parameter is big and the node is on a `hard_fork` version `15` or above, `get_dynamic_base_fee_estimate_2021_scaling` will be called.
https://github.com/monero-project/monero/blob/v0.18.3.1/src/rpc/core_rpc_server.h#L177
{F3012477}

This handler will then be called:
https://github.com/monero-project/monero/blob/v0.18.3.1/src/rpc/core_rpc_server.cpp#L2956
{F3012488}

This function is then called
https://github.com/monero-project/monero/blob/v0.18.3.1/src/cryptonote_core/blockchain.cpp#L3830
{F3012496}

## Releases Affected:
From my research, all versions after commit [b030f207517f59a5122409398549a02ac23829ae](https://github.com/monero-project/monero/commit/b030f207517f59a5122409398549a02ac23829ae) are vulnerable.
  * v0.18.3.1
  * v0.18.3.0
  * v0.18.2.2
  * v0.18.2.1
  * v0.18.2.0
  * v0.18.1.2
  * v0.18.1.1
  * v0.18.1.0
  * v0.18.0.0 

## Steps To Reproduce:
  1. Start a Monero node with the RPC port opened.
  2. Verify the node is using `hard_fork` version `15` or above
    - To do this, you can do the [`hard_fork_info` JSON RPC request](https://www.getmonero.org/resources/developer-guides/daemon-rpc.html#hard_fork_info)
  3. Perform a few asynchronous requests to the [`get_fee_estimate` JSON RPC endpoint](https://www.getmonero.org/resources/developer-guides/daemon-rpc.html#get_fee_estimate) with `grace_blocks` set to a very very large integer (can go up to 18446744073709551615)
  4. The server should now not be responsive on the RPC port.

## Supporting Material/References:
**Attached is a PoC script using Python's `requests` module to send 500 requests to a server.**
*To run the script, make sure to change the `HOST` variable at the top of the file. You can just replace `127.0.0.1` with any IP you want where a Monero node is running.*


CPU exhaustion in `htop`. From my understanding, the RPC server runs on two threads.
{F3012501}

After this, any request to the port times out, furthermore, it is not shown in Monero's log (with `seg_log 4`)

## Housekeeping

1. Be sure to read our policy before submitting
2. Provide an XMR address within the report if you wish to receive bounty (assuming that the report is valid)
    - `47ZpAkp3sYGhHM6HEMUMDK7WBi6uLXy2H9LtB3aVNJfB54a3c12LybvWH3EjAF3echFrthjMvw17k7hn9Sbwr5Uh9VgKNNS`

## Impact

An attacker could find all open Monero RPC services using a Censys query such as:
- `services.port = 18081 and (services.port = 18080 and services=monero)`

https://search.censys.io/search?resource=hosts&sort=RELEVANCE&per_page=25&virtual_hosts=EXCLUDE&q=services.port+%3D+18081+and+%28services.port+%3D+18080+and+services%3Dmonero%29

And bring all those services down.

</details>

---
*Analysed by Claude on 2026-05-24*
