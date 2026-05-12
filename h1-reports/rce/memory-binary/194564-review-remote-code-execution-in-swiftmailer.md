# Remote Code Execution in SwiftMailer

## Metadata
- **Source:** HackerOne
- **Report:** 194564 | https://hackerone.com/reports/194564
- **Submitted:** 2016-12-29
- **Reporter:** lukasreschke
- **Program:** SwiftMailer
- **Bounty:** Not specified
- **Severity:** Critical
- **Vuln:** Remote Code Execution, Unsafe Deserialization, Object Injection
- **CVEs:** None
- **Category:** memory-binary

## Summary
SwiftMailer contains a remote code execution vulnerability through unsafe object deserialization. An attacker can execute arbitrary code by crafting malicious serialized objects that are processed by the mail library. The vulnerability affects the email handling pipeline when processing untrusted input.

## Attack scenario
1. Attacker identifies an application using SwiftMailer library to handle email operations
2. Attacker crafts a malicious serialized PHP object containing gadget chain for code execution
3. Attacker injects the payload through email headers or message body parameters that get unserialized
4. SwiftMailer deserializes the malicious object without proper validation
5. Gadget chain executes arbitrary PHP code on the server with application privileges
6. Attacker gains remote code execution and can compromise the entire system

## Root cause
The vulnerability stems from unsafe use of PHP's unserialize() function on user-controlled or attacker-influenced data without proper input validation or type checking. SwiftMailer processes serialized objects in a way that allows exploitation through object injection attacks.

## Attacker mindset
An attacker would recognize that email libraries are common attack vectors and look for unsafe deserialization patterns. They would research available PHP gadget chains and craft payloads targeting SwiftMailer's object handling to achieve code execution without authentication.

## Defensive takeaways
- Never unserialize untrusted data - use safer alternatives like JSON for data exchange
- Implement strict input validation on all email parameters and headers
- Use PHP's serialize_precision and other hardening options
- Employ allowlisting for object classes if deserialization is necessary
- Keep SwiftMailer and all dependencies updated to patched versions
- Monitor for suspicious object instantiation and execution patterns
- Apply principle of least privilege to application processes handling emails
- Use static analysis tools to detect unsafe unserialize() calls in codebase

## Variant hunting
Look for other unsafe deserialization patterns in email handling libraries (PHPMailer, Zend_Mail). Search for unserialize() calls on email headers, attachments, or configuration. Test email processing endpoints with serialized object payloads. Check for similar gadget chain vulnerabilities in other popular PHP libraries used alongside SwiftMailer.

## MITRE ATT&CK
- T1190
- T1203
- T1059
- T1648

## Notes
The original report references GitHub issue #844 for details but indicates research was ongoing at report submission. This suggests a coordinated disclosure process. The vulnerability is particularly critical as email libraries are ubiquitous in web applications and often process data from multiple untrusted sources. SwiftMailer versions prior to the patch are widely deployed.

## Full report
<details><summary>Expand</summary>

See https://github.com/swiftmailer/swiftmailer/issues/844 for details, research is on-going and this issue will be added more details later.

</details>

---
*Analysed by Claude on 2026-05-12*
