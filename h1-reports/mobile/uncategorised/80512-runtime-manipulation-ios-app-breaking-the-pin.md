# Runtime Manipulation iOS App Breaking the PIN

## Metadata
- **Source:** HackerOne
- **Report:** 80512 | https://hackerone.com/reports/80512
- **Submitted:** 2015-08-04
- **Reporter:** kaleemgiet
- **Program:** Coinbase
- **Bounty:** Not specified
- **Severity:** critical
- **Vuln:** Insufficient Runtime Protection, Missing Debugger Detection, Insecure Authentication Flow, Lack of Jailbreak Detection
- **CVEs:** None
- **Category:** uncategorised

## Summary
A researcher bypassed PIN protection on the Coinbase iOS app through runtime manipulation using Snoop-it, a debugging tool that allows direct invocation of Objective-C methods on a jailbroken device. By directly calling the userAuthenticated method on CBPINViewController without authentication, the attacker completely circumvented the PIN-based access control.

## Attack scenario
1. Attacker jailbreaks iOS device and installs Snoop-it runtime inspection tool
2. Attacker configures Snoop-it to target and hook into the Coinbase application process
3. Attacker launches Coinbase app which displays PIN authentication screen as expected
4. Attacker accesses Snoop-it browser interface to view Objective-C class hierarchy of running app
5. Attacker locates CBPINViewController class and identifies userAuthenticated method with no parameters
6. Attacker directly invokes userAuthenticated method via Snoop-it, bypassing all PIN validation logic and gaining authenticated access

## Root cause
The application lacks runtime protection mechanisms including: (1) no debugger attachment detection, (2) no jailbreak detection, (3) authentication state validation performed only in UI layer without cryptographic verification, (4) exposed sensitive methods that can be invoked via runtime manipulation tools, and (5) no anti-tampering controls on the authentication flow.

## Attacker mindset
An attacker with physical device access seeking to bypass authentication controls discovers that jailbreaking tools can directly interact with app internals. By exploring exposed Objective-C methods, they identify a trivial method to achieve full authentication bypass without understanding or validating credentials, demonstrating the app prioritizes convenience over security.

## Defensive takeaways
- Implement debugger detection (ptrace anti-debugging, sysctl checks) to prevent attachment of debugging tools
- Deploy jailbreak/root detection at application startup and during sensitive operations
- Move authentication validation to secure enclave or use cryptographic verification rather than simple method invocation
- Implement code obfuscation and method name mangling to prevent easy method discovery and invocation
- Use certificate pinning and integrity verification to detect runtime tampering
- Perform authentication state validation across multiple independent checks rather than single method calls
- Implement anti-tampering mechanisms and real-time integrity monitoring
- Use Apple's local authentication framework (LocalAuthentication) with biometric or passcode tied to Secure Enclave

## Variant hunting
Search for other methods in authentication-related ViewControllers (CBAuthenticationViewController, CBSecurityViewController) that might have similar unprotected entry points. Check for other state-changing methods that could be invoked to modify app behavior (unlock, granted_access, bypass_mfa, skip_verification). Examine if similar patterns exist in other financial or security-sensitive apps.

## MITRE ATT&CK
- T1518.001 - Gather System Information (device jailbreak status)
- T1057 - Process Discovery (hooking into app process)
- T1547.014 - Modify Authentication Process (bypass PIN validation)
- T1539 - Steal Web Session Cookie (access authenticated app state)
- T1542.005 - Compromise Hardware Driver or Firmware (jailbreak exploitation)

## Notes
This is a critical authentication bypass on a financial application. The vulnerability is straightforward to exploit requiring only a jailbroken device and publicly available tools. The researcher provided clear remediation guidance. The lack of even basic runtime protections (debugger detection) suggests security was deprioritized during development. This would likely receive significant bounty given impact on financial credentials.

## Full report
<details><summary>Expand</summary>

I was able to bypass your pin protection by doing runtime manipulation in iOS app

1.Installed the snoop it in device
2.By going snoop it tool settings choose the coinbase app
3.I already set the the pin in coinbase app
4.Open the coinbase app it is asking for PIN
5.Now browsing the snoopit controlled window from the browser 
6.Go to the Objective C-Classes in snoop it window
7.By directly invoking the userAutheticated method from the coinbase.CBPINViewController I was able to break the PIN protection
8. userAuthenticated method is not taking any arguments just invoking this method bypassed the scree

Please see the POC video
https://www.dropbox.com/s/acvr4g7lv63tti5/runtime%20manipulation%20coinbase.mov?dl=0

You can prevent run time manipulation by do not attaching a debugger to app process
you see here how to prevent

http://resources.infosecinstitute.com/ios-application-security-part-23-defending-runtime-analysis-manipulation/



</details>

---
*Analysed by Claude on 2026-05-24*
