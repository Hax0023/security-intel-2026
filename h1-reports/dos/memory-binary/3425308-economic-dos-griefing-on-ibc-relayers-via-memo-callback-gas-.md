# Economic DoS (Griefing) on IBC Relayers via memo Callback Gas Exploitation

## Metadata
- **Source:** HackerOne
- **Report:** 3425308 | https://hackerone.com/reports/3425308
- **Submitted:** 2025-11-14
- **Reporter:** tychebe
- **Program:** Cosmos/IBC Protocol
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Denial of Service, Economic/Griefing Attack, Gas Limit Bypass, Incentive Manipulation
- **CVEs:** None
- **Category:** memory-binary

## Summary
An attacker can exploit the IBC memo callback feature by deploying a gas-burning contract that consumes just under the hardcoded gas limit (1,000,000) while returning success, bypassing relayer simulations. This forces relayers to execute economically unprofitable transactions, draining their funds and causing channel DoS as they abandon servicing.

## Attack scenario
1. Attacker inspects chain configuration to identify the callback gas limit (1,000,000 gas)
2. Attacker deploys a malicious EVM smart contract designed to consume ~990,000 gas via loops/hashing while returning success without exceeding the limit
3. Attacker sends a standard IBC packet (MsgTransfer) with memo field pointing to the malicious contract address
4. Relayer simulation checks the callback execution, sees success status and gas usage below limit, incorrectly validates transaction as profitable
5. Relayer broadcasts the transaction; chain executes callback consuming full gas but relayer receives minimal/zero profit (0 gas under standard conditions, ~300,000 gas under ICS-29)
6. Attacker repeats attack repeatedly, draining relayer funds until relayer abandons the channel, causing total DoS for dependent applications

## Root cause
The IBC callback middleware enforces a hardcoded gas limit without requiring the original packet sender to explicitly allocate or pay for callback gas. Relayer simulation validates only transaction success status without analyzing profitability (gas consumed vs. fees earned), allowing attackers to craft transactions that pass simulation but are economically destructive.

## Attacker mindset
Sophisticated protocol attacker targeting economic incentives rather than cryptographic weaknesses. Goal is disruption via griefing rather than direct profit. Understands relayer economics, IBC architecture, and can deploy targeted smart contracts. Motivation: network disruption, market manipulation, or sabotage of competing relayer infrastructure.

## Defensive takeaways
- Implement dynamic/explicit gas allocation: require packet senders to declare and pay for maximum callback gas upfront, similar to ICS-29 fee middleware
- Drastically reduce hardcoded gas limits for callbacks to values aligned with realistic relayer profit margins
- Enhance relayer simulation logic to track and report total gas consumption, enabling relayers to set local profitability policies rejecting unprofitable transactions
- Implement per-sender callback gas budgets or rate limiting to prevent repeated exploitation
- Design economic models for cross-chain operations that account for adversarial gas usage patterns
- Add telemetry and monitoring for callback gas consumption to detect griefing patterns early
- Consider whitelisting callback contracts or requiring governance approval for high-gas operations

## Variant hunting
Similar exploitation of other hardcoded gas limits in IBC middleware (packet timeout callbacks, interchain account operations)
Callback chaining attacks: exploiting cascading callbacks across multiple channels to multiply gas costs
Selective callback failures: crafting callbacks that succeed for relayer simulation but fail on-chain execution, causing state inconsistencies
Cross-chain fee market manipulation: using callbacks to artificially inflate gas prices across connected chains
Callback reentrancy: exploiting callback execution context to perform additional expensive operations
Griefing attacks on other permissionless relayer networks (Polygon validators, Optimism sequencers) via similar gas economic asymmetries

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application (IBC protocol exploitation)
- T1498: Network Denial of Service (economic DoS via resource exhaustion)
- T1499: Endpoint Denial of Service (relayer bankruptcy causing service withdrawal)
- T1657: Financial Theft (draining relayer funds)
- T1561: Disk Wipe (functional deletion of channel via relayer abandonment)

## Notes
This is a sophisticated economic attack on blockchain infrastructure, distinct from traditional security vulnerabilities. The core insight is that relayer incentive models assume participants can accurately predict transaction profitability. By creating 'successful' transactions with hidden cost asymmetries, attackers exploit this assumption. The fix requires moving from implicit (hardcoded) to explicit (sender-specified) cost allocation for callbacks. This vulnerability class likely affects multiple chains and protocols with similar callback/middleware architectures. The griefing nature makes it particularly dangerous as it targets the economic sustainability of decentralized infrastructure rather than user assets directly.

## Full report
<details><summary>Expand</summary>

**Summary of Impact**

This vulnerability allows an attacker to bypass the relayer's simulation defense and force permissionless relayers to execute computationally expensive, but 'successful', transactions via the `memo` callback feature.
    
This creates an asymmetric economic attack where the relayer's cost (e.g., ~1,000,000 gas) vastly exceeds their profit leading to financial losses.
    
Relayers will be forced to stop servicing the affected IBC channel to avoid bankruptcy, causing a Denial of Service (DoS) for all applications relying on that channel's callbacks.
    

**Steps to Reproduce**

1.   **Identify the Callback Gas Limit:** An attacker first inspects the chain's application setup file (e.g., `app/app.go`) to find the hardcoded gas limit for the IBC Callbacks middleware.
        
2.   I have confirmed this value is set to **1,000,000 gas** in the main application configuration.
        
3.   **Deploy a Malicious 'Gas Burner' Contract:** The attacker deploys an EVM smart contract that performs computationally expensive operations (e.g., loops, hashing) designed to consume just under the limit (e.g., **990,000 gas**) and then **return 'success'**.
        
4.   This contract must _not_ fail with 'Out of Gas' (OOG).
        
5.   **Send an IBC Packet with Malicious Memo:** The attacker sends a standard IBC packet (e.g., `MsgTransfer`) and includes a `memo` field specifying the address of the 'Gas Burner' contract as the source callback.
        
6.   **Relayer Simulation is Bypassed:** A relayer bot picks up the acknowledgment (`MsgAcknowledgement`) for this packet and runs a simulation.
        
7.   Because the callback consumes 990,000 gas (which is less than the 1,000,000 limit) and returns 'success', the simulation _passes_, falsely identifying the transaction as safe.
        
8.   **Relayer Incurs Financial Loss:** The relayer broadcasts the 'successful' transaction. The chain executes it, including the 990,000 gas callback.
        
9.   The relayer must pay the full gas cost (~1,000,000 gas) but only receives their standard fee (which is 0 if ICS-29 is not used, or ~300,000 gas if it is).
        
10.   **Result (Griefing):** The attacker can repeat this process, draining the relayer's funds at minimal cost, forcing the relayer to abandon the channel.
        

**Mitigation**

-    **1. Reduce the Gas Limit:** The simplest mitigation is to drastically reduce the hardcoded `DefaultGasLimitForCallback` in `app/app.go` from 1,000,000 to a value much closer to a standard relayer's profit margin.
    
-    **2. Implement Dynamic Gas (Better):** A more robust solution is to require the _sender_ of the original packet to explicitly define (and pay for) the maximum gas their callback will use, similar to ICS-29 fees.
    
-    **3. Smarter Simulation:** Relayer clients could be updated to not only check for 'success' but also to _report the total gas consumed_ by the simulation. Relayers could then set a local policy to reject 'successful' transactions that consume an unprofitable amount of gas.

**Reference**

-    **ICS-29 Fee Middleware:** Understanding how relayers are _supposed_ to be paid (and why their profit is often 0 or very low) is key to this economic exploit.
    
-    **Blockchain Griefing Attacks:** This is a classic example of a griefing attack, where the attacker's goal is not direct profit, but to cause financial harm to another party to disrupt the network. [Source: scsfg.io - Smart Contract Security Field Guide]

## Impact

-    **Immediate Relayer Bankruptcy:** Any permissionless relayer servicing this chain's callback-enabled channels will be rapidly drained of funds and forced to shut down.
    
-    **Total Channel DoS:** When relayers stop servicing the channel, all cross-chain applications that depend on IBC callbacks (e.g., cross-chain DeFi, NFT transfers) will cease to function, effectively freezing assets and operations.
    
-    **Loss of Trust:** This attack breaks the fundamental economic incentive for the decentralized relayer network, demonstrating that the chain is economically unsafe to service and undermining trust in the entire IBC ecosystem connected to this chain.

</details>

---
*Analysed by Claude on 2026-05-24*
