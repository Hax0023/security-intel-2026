# Authorization Bypass in Starknet Snap via enableAuthorize Parameter

## Metadata
- **Source:** HackerOne
- **Report:** 3507241 | https://hackerone.com/reports/3507241
- **Submitted:** 2026-01-12
- **Reporter:** aszx87410
- **Program:** Consensys/Starknet Snap
- **Bounty:** Not specified in report
- **Severity:** critical
- **Vuln:** Authorization Bypass, Missing Input Validation, Insecure Defaults, Logic Error
- **CVEs:** None
- **Category:** business-logic

## Summary
The Starknet Snap contains a critical authorization bypass vulnerability where the `enableAuthorize` parameter can be controlled by malicious websites to skip user confirmation dialogs. When set to `false`, arbitrary messages and transactions can be signed without user approval, enabling asset theft and unauthorized transactions. The vulnerability stems from insecure default behavior and lack of input validation on a security-critical parameter.

## Attack scenario
1. Attacker creates a malicious website that calls the Starknet Snap RPC methods
2. Attacker passes `enableAuthorize: false` in the request parameters to bypass confirmation dialogs
3. Victim visits the malicious website while having MetaMask with Starknet Snap installed
4. Attacker initiates transaction or message signing through the compromised snap interface
5. The snap signs the message/transaction without showing confirmation dialog to the user
6. Attacker's arbitrary transaction is executed with victim's credentials, potentially stealing assets or executing malicious actions

## Root cause
The `enableAuthorize` parameter is a user-controllable boolean that directly gates the confirmation dialog. The snap trusts the caller to provide this parameter correctly, with the comment explicitly noting that `enableAuthorize` should default to `true` but currently defaults to `false`. This allows any website to bypass the security-critical confirmation step.

## Attacker mindset
An attacker would recognize that web-based wallet interactions require user confirmation as a critical security boundary. By discovering that this parameter is exposed and controllable, the attacker can craft exploit payloads that bypass this protection entirely. The attacker would target users who have both MetaMask and the Starknet Snap installed, launching phishing campaigns or compromising legitimate websites to inject malicious code.

## Defensive takeaways
- Always default security-critical parameters to the most restrictive setting (enableAuthorize should default to `true`, not `false`)
- Never allow external callers to disable security confirmations; make authorization dialogs mandatory for sensitive operations
- Implement allowlist-based verification for which origins/dApps can call snap methods with reduced confirmation requirements
- Add warnings/logging when confirmation dialogs are skipped to help users detect suspicious activity
- Validate and sanitize all RPC parameters, especially boolean flags that control security features
- Consider requiring explicit user settings before allowing any confirmation bypasses
- Implement snap-level permission model where dangerous operations require additional approval layers

## Variant hunting
Check other Consensys snap implementations for similar `enableAuthorize` or confirmation-skipping parameters
Review MetaMask snap SDK documentation to identify if other snaps implement similar bypasses
Audit transaction signing RPCs in Starknet Snap for additional authorization bypass vectors
Look for similar patterns in other MetaMask snap plugins (e.g., other blockchain snaps)
Check if other parameters besides `enableAuthorize` can influence confirmation dialog behavior
Investigate if confirmation skipping is possible through RPC method selection or parameter manipulation
Review snap update mechanism to identify if older versions with this vulnerability could persist

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1566 - Phishing (spear phishing via malicious website)
- T1559 - Inter-Process Communication (snap RPC calls)
- T1570 - Lateral Tool Transfer (loading exploit from attacker server)
- T1539 - Steal Web Session Cookie (session hijacking via snap)
- T1187 - Forced Authentication (tricking user into enabling snap)
- T1599 - Network Boundary Bridging (bypassing snap security boundaries)

## Notes
This is a critical vulnerability affecting the Starknet Snap, a MetaMask plugin handling cryptographic operations and transaction signing for Starknet blockchain. The vulnerability allows complete bypass of user authorization, which is the primary security mechanism protecting users from unauthorized transactions. The explicit TODO comment in the code indicates this was a known issue that was never properly resolved. Any user with this snap installed is potentially vulnerable to asset theft through malicious websites. The fix is simple but critical: change the default value of `enableAuthorize` to `true` and potentially remove the ability for external callers to set this parameter.

## Full report
<details><summary>Expand</summary>

## Summary:
The Starknet Snap by Consensys contains a critical security vulnerability that allows malicious websites to bypass user authorization when signing messages or transactions. The vulnerability exists in the `enableAuthorize` parameter which can be controlled by any website. When set to `false`, the confirmation dialog is not shown to the user, allowing a malicious website to sign arbitrary messages or transactions without user approval, potentially leading to asset theft.

## Steps To Reproduce:
1. Make sure MetaMask is installed
2. Visit https://snaps.consensys.io/starknet
3. Click "Connect with MetaMask" button to install the StarkNet Snap
4. Download the html file: "exp-starknet.html" and host it on local port 5555
5. Visit http://localhost:5555/exp-starknet.html
6. Click "start PoC" button
7. Accept the connection request
8. Observe that the signMessage is shown in the page without user approval

## Supporting Material/References:
The vulnerability exists in the following code: https://github.com/Consensys/starknet-snap/blob/main/packages/starknet-snap/src/rpcs/sign-message.ts#L77

```js
  protected async handleRequest(
    params: SignMessageParams,
  ): Promise<SignMessageResponse> {
    const { enableAuthorize, typedDataMessage, address } = params;
    if (
      // Get Starknet expected not to show the confirm dialog, therefore, `enableAuthorize` will set to false to bypass the confirmation
      // TODO: enableAuthorize should set default to true
      enableAuthorize &&
      !(await renderSignMessageUI({
        address,
        typedDataMessage,
        chainId: this.network.chainId,
      }))
    ) {
      throw new UserRejectedOpError() as unknown as Error;
    }

    return await signMessageUtil(
      this.account.privateKey,
      typedDataMessage,
      address,
    );
  }
}
```

* exp-starknet.html - an example exploit
  Attachments: [{"filename":"exp-starknet.html","created_at":"2026-01-12T02:13:56.722Z","hai_attachment_description":null}]

</details>

---
*Analysed by Claude on 2026-05-24*
