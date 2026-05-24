# Regular Expression Denial of Service (ReDoS) in is-my-json-valid Email Validation

## Metadata
- **Source:** HackerOne
- **Report:** 317548 | https://hackerone.com/reports/317548
- **Submitted:** 2018-02-19
- **Reporter:** danny_grander
- **Program:** is-my-json-valid
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Regular Expression Denial of Service (ReDoS), Algorithmic Complexity Exploitation, Input Validation Flaw
- **CVEs:** None
- **Category:** memory-binary

## Summary
The is-my-json-valid package used a vulnerable regex pattern (/^\S+@\S+$/) for email validation that is susceptible to ReDoS attacks. An attacker could craft a 90K character input to cause approximately 10 seconds of processing time, blocking the event loop and causing denial of service.

## Attack scenario
1. Attacker identifies that the application uses is-my-json-valid for JSON schema validation
2. Attacker crafts a malicious JSON payload with an email field containing a long string of non-whitespace characters (e.g., 90K+ characters)
3. Application processes the JSON and attempts to validate the email field using the vulnerable regex
4. The regex engine enters catastrophic backtracking due to the greedy \S+ patterns with alternating match/non-match attempts
5. Event loop blocks for extended period (approximately 10 seconds for 90K input)
6. Application becomes unresponsive, causing denial of service for legitimate users

## Root cause
The email validation regex /^\S+@\S+$/ uses greedy quantifiers (\S+) without proper anchoring and backtracking constraints. When input consists entirely of non-whitespace characters without a valid email format, the regex engine experiences exponential backtracking as it attempts multiple combinations before ultimately failing to match.

## Attacker mindset
An attacker would recognize that JSON validation libraries are common entry points and would test email field inputs with pathologically crafted payloads. The goal is to identify processing bottlenecks that can be exploited to achieve denial of service with minimal payload complexity, making it a practical attack vector.

## Defensive takeaways
- Avoid using overly complex or greedy regular expressions for input validation, especially in performance-critical paths
- Use proper email validation libraries or standards-based validation instead of custom regex patterns
- Implement input length limits before regex matching to prevent catastrophic backtracking
- Add timeout mechanisms for regex operations to prevent event loop blocking
- Conduct regular security audits of regex patterns used in validation logic
- Consider using deterministic finite automaton (DFA)-based regex engines instead of backtracking engines
- Test regex patterns with pathological inputs to identify ReDoS vulnerabilities during development

## Variant hunting
Search for other email validation regex patterns in codebase; audit JSON schema validators; check for similar greedy quantifier patterns in URL, username, or domain validation; review any user-supplied input that passes through regex validation; examine npm packages with similar validation responsibilities

## MITRE ATT&CK
- T1190
- T1498

## Notes
This vulnerability was introduced in 2014 and persisted for several years before being identified and fixed. The fix involved replacing the vulnerable regex with a more robust validation approach. ReDoS vulnerabilities are often overlooked during initial development but can have significant operational impact in production environments.

## Full report
<details><summary>Expand</summary>

The issue was already fixed.

**Module:** is-my-json-valid

**Summary:** 
Affected versions of this package are vulnerable to Regular Expression Denial of Service (ReDoS) attacks. It used a regular expression (/^\S+@\S+$/) in order to validate emails. This can cause an impact of about 10 seconds matching time for data 90K characters long.

**Description:** 
Regex:
 formats.js
 exports[‘email’] = /^\S+@\S+$/
(introduced in 2014, 34a1a706)


## Supporting Material/References:

* https://github.com/mafintosh/is-my-json-valid/pull/159
* https://github.com/mafintosh/is-my-json-valid/commit/b3051b277f7caa08cd2edc6f74f50aeda65d2976

## Impact

Denial of service through blocking the event loop.

</details>

---
*Analysed by Claude on 2026-05-24*
