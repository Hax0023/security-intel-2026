# Unsafe yaml.load() Enables Remote Code Execution in Liberapay

## Metadata
- **Source:** HackerOne
- **Report:** 2467232 | https://hackerone.com/reports/2467232
- **Submitted:** 2024-04-17
- **Reporter:** tarun_sec
- **Program:** Liberapay
- **Bounty:** Not specified
- **Severity:** critical
- **Vuln:** Unsafe Deserialization, Remote Code Execution, Arbitrary Code Execution
- **CVEs:** None
- **Category:** memory-binary

## Summary
Liberapay uses yaml.load() instead of yaml.safe_load() to parse YAML documents, allowing attackers to construct arbitrary Python objects and achieve remote code execution. The unsafe deserialization function permits instantiation of any Python class during YAML parsing, which can be leveraged to execute arbitrary commands on the server.

## Attack scenario
1. Attacker identifies an endpoint or functionality in Liberapay that accepts YAML input from users
2. Attacker crafts a malicious YAML document containing a Python object constructor (e.g., using !!python/object syntax)
3. Attacker embeds command execution payload in the YAML using gadget chains (e.g., os.system or subprocess calls)
4. Attacker submits the malicious YAML to the vulnerable endpoint
5. Server parses YAML using yaml.load(), which deserializes and instantiates the malicious object
6. Arbitrary code embedded in the object constructor executes with server privileges, compromising the system

## Root cause
Use of yaml.load() instead of yaml.safe_load(). The unsafe load function instantiates arbitrary Python objects during deserialization, while safe_load() restricts to simple types (strings, lists, dicts, numbers). The developers failed to implement input validation for YAML sources.

## Attacker mindset
An attacker would look for any user-controllable YAML input, test deserialization behaviors, craft Python object payloads using standard YAML gadget chains, and execute system commands to establish persistence or exfiltrate data.

## Defensive takeaways
- Always use yaml.safe_load() for parsing untrusted YAML input
- Never use yaml.load() without Loader=yaml.SafeLoader specification
- Implement input validation and sanitization for all user-supplied serialized data
- Use security code review practices to identify unsafe deserialization patterns
- Consider using alternative serialization formats (JSON) that don't support arbitrary object instantiation
- Apply the principle of least privilege to processes handling YAML parsing
- Monitor and alert on unusual deserialization patterns in logs

## Variant hunting
Search codebase for: yaml.load() calls, yaml.load(stream), pickle.loads(), marshal.loads(), eval() with user input, any other unsafe deserializers (pickle, shelve), and configurations allowing arbitrary object instantiation from external sources.

## MITRE ATT&CK
- T1190
- T1203
- T1059

## Notes
This is a classic unsafe deserialization vulnerability in Python. The fix is trivial but critical - replacing one function call. The vulnerability likely existed in production code at liberapay.com/master branch at line 40 of liberapay/testing/vcr.py. Even though labeled 'testing', if this code path is reachable from production, it's exploitable.

## Full report
<details><summary>Expand</summary>

TL;DR
Yaml.load() has the ability to construct an arbitrary Python object. This is dangerous if you receive a YAML document from an untrusted source.


Proof of concept 
https://github.com/liberapay/liberapay.com/blob/master/liberapay/testing/vcr.py#L40

How do I fix it?
Always use yaml.safe_load(). This function limits this ability to simple Python objects like integers or lists. 

If you have any questions 
please comment on the report 

best regards
mrrobot2050

## Impact

Yaml.load() has the ability to construct an arbitrary Python object. This is dangerous if you receive a YAML document from an untrusted source.

</details>

---
*Analysed by Claude on 2026-05-11*
