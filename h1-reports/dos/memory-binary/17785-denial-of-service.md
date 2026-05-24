# Denial of Service - Incomplete Patch

## Metadata
- **Source:** HackerOne
- **Report:** 17785 | https://hackerone.com/reports/17785
- **Submitted:** 2014-06-27
- **Reporter:** coolboss
- **Program:** Unknown (HackerOne Report #17785)
- **Bounty:** Unknown
- **Severity:** high
- **Vuln:** Denial of Service, Resource Exhaustion, Incomplete Patch
- **CVEs:** None
- **Category:** memory-binary

## Summary
A previously reported vulnerability (issue #13748) was not fully patched, leaving the application vulnerable to denial of service attacks. The incomplete fix allows attackers to still trigger the vulnerable code path through alternative means.

## Attack scenario
1. Attacker identifies the original vulnerability report #13748 and its incomplete patch
2. Attacker analyzes the patched code to find remaining exploitation vectors
3. Attacker crafts a request that bypasses the partial fix using an alternative code path
4. Attacker sends the malicious request to the target application
5. Application consumes excessive resources or crashes, causing service unavailability
6. Other legitimate users experience denial of service

## Root cause
The initial patch for vulnerability #13748 addressed only a specific attack vector but failed to fix the underlying root cause, leaving alternative exploitation methods intact.

## Attacker mindset
Opportunistic researcher identifying incomplete security fixes and testing for residual vulnerabilities in patched code.

## Defensive takeaways
- Conduct thorough root cause analysis before implementing patches
- Test patches comprehensively against multiple attack vectors and edge cases
- Implement multiple layers of input validation and resource limiting
- Use security testing to verify complete remediation, not just the reported attack
- Consider regression testing when patches are released
- Implement monitoring for anomalous resource consumption patterns

## Variant hunting
Search for similar incomplete patches across the codebase; identify other code paths that could trigger the same underlying vulnerability; test different input formats and request methods against the patched functionality.

## MITRE ATT&CK
- T1499
- T1499.004

## Notes
This report demonstrates the importance of fixing underlying vulnerabilities rather than just patching specific attack vectors. The reference to a POC video suggests reproducible exploitation was demonstrated. Critical that patch verification includes testing multiple exploitation variants before considering an issue resolved.

## Full report
<details><summary>Expand</summary>

Refering to this #13748

Not yet patched fully.

POC video ---> https://www.dropbox.com/s/4i7qun3nuesbc70/hackerone_error.mp4.mp4

</details>

---
*Analysed by Claude on 2026-05-24*
