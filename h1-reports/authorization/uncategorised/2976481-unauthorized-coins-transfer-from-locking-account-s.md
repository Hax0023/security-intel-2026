# Unauthorized Coin Transfer from Locking Accounts via Spoofed Sender in MsgExecute

## Metadata
- **Source:** HackerOne
- **Report:** 2976481 | https://hackerone.com/reports/2976481
- **Submitted:** 2025-02-06
- **Reporter:** unknown_feature
- **Program:** Cosmos SDK
- **Bounty:** Not specified
- **Severity:** critical
- **Vuln:** Authorization Bypass, Insufficient Input Validation, Message Sender Spoofing, Privilege Escalation
- **CVEs:** None
- **Category:** uncategorised

## Summary
Locking account implementations in Cosmos SDK fail to properly validate the sender field in nested messages, allowing attackers to spoof the account owner and transfer unlocked funds. The vulnerability exists in the SendCoins function which trusts msg.Sender from packed MsgExecute messages without validating against the actual transaction context, affecting periodic-locking-account and potentially other locking account types.

## Attack scenario
1. Attacker identifies a victim's periodic-locking-account with locked funds
2. Attacker waits for the locking period to expire, allowing funds to become unlocked
3. Attacker crafts a MsgExecute transaction containing a SendCoins message with msg.Sender spoofed to the victim's address
4. Attacker submits the transaction to the blockchain with their own address as the actual transaction sender
5. The locking account's checkSender validation trusts msg.Sender from the packed message instead of extracting the real sender from transaction context
6. Unauthorized funds transfer executes, sending coins from the victim's locking account to the attacker

## Root cause
The SendCoins function in locking accounts validates sender by comparing msg.Sender against the owner, but msg.Sender is an untrusted field from the packed MsgExecute message. Unlike the multisig account implementation which correctly extracts sender from ctx, locking accounts directly use the unvalidated message field without verifying it matches the actual transaction signer in the execution context.

## Attacker mindset
An attacker would target locking accounts with unlocked or expiring funds, recognizing that the message-level sender validation creates a trust boundary violation. The attacker understands the difference between how multisig and locking accounts handle context, and exploits the inconsistent sender validation to impersonate legitimate account owners.

## Defensive takeaways
- Always extract transaction sender from execution context (ctx) rather than trusting sender fields in nested messages
- Implement consistent sender validation patterns across all account types in the SDK
- Validate that msg.Sender matches the actual transaction context sender before authorizing sensitive operations
- Use integration tests that simulate cross-account message execution to catch sender spoofing vulnerabilities
- Apply principle of least privilege: accounts should only process messages from authenticated signers in the transaction context
- Audit all account implementations for message-level sender assumptions vs context-level actual senders

## Variant hunting
Search for other account implementations using msg.Sender without context validation (continuous-locking-account, delayed-locking-account, permanent-locking-account)
Check for similar patterns in x/accounts where messages pack sender fields that bypass context authentication
Look for other MsgExecute message handlers that trust user-supplied sender fields
Audit all account types for inconsistent sender validation patterns between multisig (correct) and locking (vulnerable) implementations
Search for SendCoins calls across the codebase to identify other vulnerable implementations

## MITRE ATT&CK
- T1190
- T1078
- T1556

## Notes
This is a critical authorization bypass affecting financial transactions on the Cosmos SDK. The vulnerability demonstrates a dangerous inconsistency where multisig accounts correctly use context for sender validation while locking accounts trust message-level sender fields. The POC requires waiting for unlock periods but no cryptographic keys are needed - pure message spoofing. The fix requires centralizing sender validation to use ctx instead of msg.Sender across all locking account implementations.

## Full report
<details><summary>Expand</summary>

### Summary of Impact
An attacker can transfer money from the locking account they don't own(if the account has unlocked funds, can be after locking period is over). The POC is done for `periodic-locking-account`. But it seems like more locking accounts are affected because the issue seems to be in [SendCoins](https://github.com/cosmos/cosmos-sdk/blob/7e391959b9aebf055294b24b7f392346709dae64/x/accounts/defaults/lockup/lockup.go#L285-L284).  And it's used by all of them. When it calls the function it passes sender from the message `msg.Sender` in [checkSender](https://github.com/cosmos/cosmos-sdk/blob/7e391959b9aebf055294b24b7f392346709dae64/x/accounts/defaults/lockup/lockup.go#L333) it checks that the sender == owner. But the issue here is that msg.Sender is not validated anywhere bc this message is packed into [MsgExecute](https://github.com/cosmos/cosmos-sdk/blob/7e391959b9aebf055294b24b7f392346709dae64/api/cosmos/accounts/v1/tx.pulsar.go#L4444-L4443).  While executing it sets original sender into the [context ](https://github.com/cosmos/cosmos-sdk/blob/7e391959b9aebf055294b24b7f392346709dae64/x/accounts/keeper.go#L284). And in case of multisig account it correctly takes it from [ctx](https://github.com/cosmos/cosmos-sdk/blob/7e391959b9aebf055294b24b7f392346709dae64/x/accounts/defaults/multisig/account.go#L168) . At least in those places I looked at. But these locking accounts take it from the message. And it can be anything. 

#### POC scenario

1. We first create a periodic-locking-account at  the [victim ](https://gist.github.com/unknownfeature/d0b8cfcf263904d9be4707dded38c706#file-main-rs-L28). Locking period is small so we wouldn't wait long.
2. Then we wait for locking period to end and transfer money to the [attacker](https://gist.github.com/unknownfeature/d0b8cfcf263904d9be4707dded38c706#file-main-rs-L55)

### Steps to Reproduce
Go and Rust required

1. Checkout latest version of [cosmos-sdk](https://github.com/cosmos/cosmos-sdk) and run `make build`. Note the path to binariy and when it's done replace the path [in setup_chain](https://gist.github.com/unknownfeature/d0b8cfcf263904d9be4707dded38c706#file-setup_chain-L18).

 2. Create rust project with attached `Cargo.toml`.  Download all attached *.rs files and put them into `src` folder.

 3. Make sure setup_chain has execute permission. Run `./setup_chain`.  Wait for it to start. And then run the rust project. See the POC video.
{F4027705}

### Workarounds
Doesn't seem like there are any

### Supporting Material/References
1. setup_chain - script that sets up and starts the chain
2. main.rs, types.rs, client.rs, func.rs, msg.rs and Cargo.toml the attack itself. Sorry there are a lot of files. I'll probably push it all somewhere and update the report. 
3. attack.mov - the video of POC

## Impact

An attacker can take over someone's funds that were locked and then unlocked on the locking account. The POC particularly demonstrates `periodic-locking-account`.  But there are reasons to believe more locking accounts are affected.

</details>

---
*Analysed by Claude on 2026-05-24*
