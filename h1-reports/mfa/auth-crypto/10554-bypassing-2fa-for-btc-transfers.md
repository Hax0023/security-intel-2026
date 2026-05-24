# 2FA Bypass via Internal Transfer Parameter Manipulation on Coinbase

## Metadata
- **Source:** HackerOne
- **Report:** 10554 | https://hackerone.com/reports/10554
- **Submitted:** 2014-05-01
- **Reporter:** michiel
- **Program:** Coinbase
- **Bounty:** Not specified in writeup
- **Severity:** critical
- **Vuln:** Authentication Bypass, Authorization Bypass, Insufficient Input Validation, Parameter Tampering
- **CVEs:** None
- **Category:** auth-crypto

## Summary
A critical authentication bypass vulnerability allowed attackers to transfer Bitcoin funds while circumventing mandatory two-factor authentication by manipulating the 'transaction[to]' parameter in internal transfer requests. The internal transfer endpoint failed to validate that the destination wallet belonged to the same account and did not enforce 2FA verification, allowing arbitrary fund transfers to any wallet on the platform.

## Attack scenario
1. Attacker gains access to victim's Coinbase account credentials through phishing or credential compromise
2. Victim has 2FA enabled requiring authentication for any BTC transfer amount
3. Attacker navigates to Manage Accounts and initiates an internal transfer (creates second wallet if needed)
4. Attacker intercepts the POST request to /accounts/transfer_money using proxy tool
5. Attacker modifies 'transaction[to]' parameter from legitimate internal wallet ID to attacker-controlled wallet ID retrieved from DOM or enumeration
6. Attacker forwards modified request, bypassing 2FA and transferring funds to attacker's wallet without authentication challenge

## Root cause
The application implemented 2FA enforcement at the UI/presentation layer rather than at the transaction logic layer. The internal transfer endpoint performed insufficient validation: (1) did not verify destination wallet belonged to same account, (2) did not re-validate 2FA requirement for internal transfers, (3) accepted user-supplied BSON IDs without authorization checks, and (4) lacked server-side business logic to enforce security policy regardless of request origin.

## Attacker mindset
An attacker with existing account access would recognize that security controls are often inconsistently applied across different transaction types. They would test whether 'internal' transfers bypass security requirements and discover that modifying request parameters allows escaping the intended security boundary. This demonstrates opportunistic exploitation of inconsistent security implementation.

## Defensive takeaways
- Enforce security controls (2FA) at the business logic/API layer, never rely solely on client-side or UI enforcement
- Implement authorization checks on all sensitive operations verifying the requestor owns/controls the destination resource
- Apply consistent security policies across all transaction types (internal vs external transfers must have equivalent protections)
- Use consistent, server-side validated identifiers for sensitive resources; validate all ID parameters against user's authorized resources
- Implement rate limiting and transaction verification workflows that cannot be bypassed through parameter manipulation
- Log and alert on suspicious patterns (transfers to new/external wallets, rapid transfers, transfers outside typical user behavior)
- Conduct security testing specifically for parameter tampering across all transaction-related endpoints

## Variant hunting
Test other internal transfer scenarios (inter-account transfers if supported) for similar 2FA bypass
Check payment API endpoints for parameter manipulation allowing destination change
Test withdrawal/deposit endpoints to see if similar authorization bypass exists on external transfers
Examine other 'protected' account operations (password changes, security settings modifications) for similar bypass vectors
Test whether other user roles or account types have inconsistent 2FA enforcement
Investigate if transaction notes or metadata fields can be abused for injection attacks during bypass attempt
Test for race conditions between 2FA validation and transfer execution

## MITRE ATT&CK
- T1110.001 - Brute Force: Credential Stuffing (initial account access assumption)
- T1556.008 - Modify Authentication Process: Modify 2FA Process
- T1078.001 - Valid Accounts: Default Accounts
- T1528 - Steal or Forge Web Session Cookies (if session-based)
- T1190 - Exploit Public-Facing Application
- T1602 - Data from Backup/Cache

## Notes
This is a high-impact financial vulnerability affecting cryptocurrency holdings. The writeup demonstrates excellent exploitation documentation with actual request structure. The root cause reflects a common architectural flaw where security requirements are enforced at presentation layer rather than data/business logic layer. The vulnerability would likely have CVSS 9.0+. Report ID 10554 suggests this was reported to HackerOne's Coinbase program and may have carried significant bounty given the critical nature and financial impact.

## Full report
<details><summary>Expand</summary>

Under advanced settings, users have the ability to protect their wallet by requiring two-factor confirmation when sending bitcoins. Personally, I have configured my account with the most secure option, which requires two factor confirmation when sending any amount of bitcoins. However, a flaw exists that allows an attacker with access to the account to bypass the two-factor authentication step that is required upon sending.

The vulnerability exists in the transfer feature that allows you to transfer funds between all wallets under the same account (internal transfer). This feature is only visually available when you have at least two wallets, but it is not necessary to have two wallets to exploit this vulnerability. Just makes the process a bit easier.

# Easy repro steps
- Enable the account security setting that requires you to enter a valid two-factor code when transferring *any* amount of bitcoins.
- Create a second wallet and go to *Manage Accounts* (https://coinbase.com/accounts).
- Click the *Transfer* button and select the wallet you want to send money from.
- Under *To* select one of the other wallets on the account (this doesn't actually matter).
- Pick an amount and hit the *Transfer* button. Make sure to intercept this request! Use Burp Suite for instance. The request should look similar to this:

```
POST /accounts/transfer_money HTTP/1.1
Host: coinbase.com
[...]

----------422668630
Content-Disposition: form-data; name="transaction[from]"

51cf4e552f31a99ce200001b
----------422668630
Content-Disposition: form-data; name="transaction[to]"

53440a8092adb7d95000001d
----------422668630
Content-Disposition: form-data; name="transaction[amount]"

0.1
----------422668630
Content-Disposition: form-data; name="transaction[notes]"

Bypassin' 2FA.
----------422668630--
```

- Change the `transaction[to]` parameter to the Mongo BSON ID of the wallet you want to transfer the BTCs to. This can be any wallet ID outside the account you were initiating an internal transfer for. It is fairly easy to find the ID of a wallet, for example, it can be found in the DOM:

```html
<li>
  <a href="" class="account-wallet active" data-wallet-id="53440a8092adb7d95000001d">
    <strong>My Wallet</strong> <span>1.00 BTC</span>
  </a>
</li>
```

- Forward the request. The money is now transferred to the Coinbase wallet associated with the ID specified under `transaction[to]`. No two-factor code was entered.

</details>

---
*Analysed by Claude on 2026-05-24*
