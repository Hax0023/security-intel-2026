# Ruby 2.3.x and 2.2.x Bundle DoS Vulnerable libYAML 0.1.6

## Metadata
- **Source:** HackerOne
- **Report:** 235842 | https://hackerone.com/reports/235842
- **Submitted:** 2017-06-02
- **Reporter:** usa
- **Program:** Ruby
- **Bounty:** Not applicable (self-reported by maintainer)
- **Severity:** high
- **Vuln:** Denial of Service, Dependency Vulnerability, Unpatched Third-Party Library
- **CVEs:** CVE-2014-9130
- **Category:** uncategorised

## Summary
Ruby versions 2.3.x and 2.2.x bundle libYAML 0.1.6 which contains CVE-2014-9130, a known Denial of Service vulnerability. Ruby 2.4.x addressed this by upgrading to the patched libYAML 0.1.7, but older supported versions remain vulnerable. This affects all applications using YAML parsing on Ruby 2.3.x and 2.2.x installations.

## Attack scenario
1. Attacker crafts a malicious YAML document designed to trigger the CVE-2014-9130 DoS condition in libYAML 0.1.6
2. Attacker submits the crafted YAML payload to a Ruby application using Ruby 2.3.x or 2.2.x
3. Application calls YAML.load() or similar YAML parsing functions to process the untrusted input
4. The vulnerable libYAML parser consumes excessive resources (CPU or memory) when processing the malicious YAML
5. Application becomes unresponsive or crashes, denying service to legitimate users
6. Attacker can repeat the attack to maintain the DoS condition

## Root cause
Ruby 2.3.x and 2.2.x continue to bundle an outdated version of the libYAML library (0.1.6) that contains a known DoS vulnerability (CVE-2014-9130). While Ruby 2.4.x upgraded to the patched version 0.1.7, the maintenance branches for earlier versions were not updated with the security fix.

## Attacker mindset
An attacker would exploit this to launch resource exhaustion attacks against Ruby applications, particularly those accepting user-supplied YAML input. The predictable nature of the vulnerability makes it attractive for reliable DoS attacks. The attacker assumes the target is running an older but still-supported Ruby version.

## Defensive takeaways
- Upgrade Ruby to version 2.4.x or newer that includes the patched libYAML 0.1.7
- If stuck on Ruby 2.2.x or 2.3.x, build Ruby from source with a separately installed patched libYAML library
- Avoid parsing untrusted YAML input; use safer alternatives like JSON when possible
- Implement input validation and sanitization for YAML parsing
- Use YAML.safe_load() instead of YAML.load() to restrict object instantiation
- Monitor dependency versions in all supported maintenance branches, not just latest releases
- Establish a process for backporting critical security fixes to all actively maintained version branches

## Variant hunting
Search for other libYAML versions bundled in Ruby versions: check Ruby 2.0.x, 2.1.x for libYAML version and CVE-2014-9130 vulnerability status. Investigate if other language implementations (Python, PHP, Node.js) bundle vulnerable libYAML versions. Look for applications that may have frozen or vendored libYAML internally.

## MITRE ATT&CK
- T1190
- T1498

## Notes
This report is noteworthy as it was filed by the Ruby maintainer themselves as a self-reminder to patch the vulnerable dependency. CVE-2014-9130 is from 2014, making this a multi-year lag in patching older maintenance branches. The vulnerability demonstrates the importance of maintaining security updates across all supported version branches, not just the latest releases.

## Full report
<details><summary>Expand</summary>

libYAML 0.1.6 (and 0.1.5) has a DoS vulnerablitity known as [CVE-2014-9130](http://www.cvedetails.com/cve/CVE-2014-9130/).
Now Ruby 2.4.x bundles fixed version 0.1.7, but 2.3.x and 2.2.x still bundle 0.1.6.

Note that I'm the maintainer of Ruby 2.3.x and 2.2.x.
Therefore, this report is a kind of remainder.

</details>

---
*Analysed by Claude on 2026-05-24*
