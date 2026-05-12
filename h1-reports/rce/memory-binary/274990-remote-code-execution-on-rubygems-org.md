# Remote Code Execution via YAML Deserialization in rubygems.org Gem Parsing

## Metadata
- **Source:** HackerOne
- **Report:** 274990 | https://hackerone.com/reports/274990
- **Submitted:** 2017-10-06
- **Reporter:** max
- **Program:** rubygems.org
- **Bounty:** Not specified in writeup
- **Severity:** critical
- **Vuln:** Unsafe Deserialization, YAML Deserialization, Insufficient Input Validation, Remote Code Execution
- **CVEs:** CVE-2017-0903
- **Category:** memory-binary

## Summary
rubygems.org was vulnerable to remote code execution when processing uploaded gems due to unsafe YAML deserialization in the checksum file parser. Although the application correctly protected against direct YAML.load attacks on the gem spec using Psych.safe_load, the checksum parsing code in Gem::Package#read_checksums called YAML.load directly on untrusted data, allowing arbitrary code execution through Marshal gadget chains.

## Attack scenario
1. Attacker crafts a malicious .gem file with a poisoned checksums file containing serialized Marshal objects with RCE gadget chains
2. Attacker uploads the malicious gem to rubygems.org via POST to /api/v1/gems endpoint with valid authentication
3. rubygems.org application parses the gem by calling Gem::Package.new(body).spec in app/models/pusher.rb
4. The spec parsing correctly uses Psych.safe_load for YAML protection, but gem processing continues to checksum validation
5. Gem::Package#read_checksums executes YAML.load on the attacker-controlled checksum file, triggering deserialization
6. Marshal.load is invoked on the crafted payload through accessible application classes, executing arbitrary code on the server

## Root cause
Inconsistent security controls: while the application developers correctly identified YAML deserialization risks and patched the spec parser with Psych.safe_load, they missed that the checksum file parsing path in the underlying Gem::Package library also performed unsafe YAML.load operations. This created a bypass of the security controls through a different code path in the same workflow.

## Attacker mindset
The attacker demonstrated sophisticated understanding of Ruby serialization vulnerabilities, specifically how to chain YAML deserialization into Marshal.load exploitation. They recognized that security patches on one code path don't guarantee complete protection if multiple parsing paths exist, and systematically tested alternative deserialization vectors to bypass the intended protections.

## Defensive takeaways
- Apply security controls at the library/framework level rather than relying on application-level patches for inherited libraries
- When mitigating deserialization vulnerabilities, ensure all code paths that handle untrusted data are protected, not just the primary entry point
- Use comprehensive input validation and schema enforcement before any deserialization occurs
- Consider upgrading to or requiring newer versions of gems that have built-in safe deserialization defaults
- Implement allowlisting for which classes can be deserialized rather than relying on blacklisting unsafe methods
- Disable dangerous features like Marshal deserialization when possible, or restrict it to trusted data sources only
- Perform security-focused code audits of external library usage, particularly around data parsing

## Variant hunting
Hunt for similar patterns in Ruby applications using Gem::Package or other libraries that wrap YAML.load, especially cases where monkey-patching or overrides were applied to one parser but sibling code paths were missed. Look for applications that parse uploaded archives (gems, tarballs, zips) where multiple file types within the archive are deserialized with different security levels.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1204 - User Execution
- T1594 - Supply Chain Compromise
- T1651 - Data Obfuscation

## Notes
This is a high-impact vulnerability on the Ruby package ecosystem's central repository. The attacker responsibly disclosed details while withholding full exploitation specifics. The vulnerability demonstrates a critical blind spot in Ruby security: the ease of achieving RCE through Marshal gadget chains when YAML deserialization is available. This likely informed subsequent security improvements in Ruby's serialization handling and stricter validation in package managers.

## Full report
<details><summary>Expand</summary>

When parsing a gem POSTed to the `/api/v1/gems` endpoint, the rubygems.org application immediately calls `Gem::Package.new(body).spec` inside `app/models/pusher.rb`. The authors of the application correctly observed that parsing untrusted YAML is dangerous (since it can serialize more or less arbitrary objects), so they monkey-patched the spec parser to use `Psych.safe_load` set from `config/initializers/forbidden_yaml.rb`.

However, `YAML.load` is called directly when parsing the gem's checksum file in `Gem::Package#read_checksums`. Using classes accessible within the application, I was able to turn this into a call to `Marshal.load` on attacker-controlled data. From there, I was able to use known Marshal exploitation techniques to achieve code execution on the server (I'm omitting some details here for brevity so that I can submit this report right away).

A proof of concept, `poc.gem`, is attached. Run the exploit with the following command:
`cat poc.gem | curl -H 'Content-Type: application/gzip' --data-binary @- -H 'Authorization: █████' https://rubygems.org/api/v1/gems`

I ran the attached PoC twice. It just does a `wget` to my server.

Please let me know if I should clarify anything! Thanks for running this program.

</details>

---
*Analysed by Claude on 2026-05-11*
