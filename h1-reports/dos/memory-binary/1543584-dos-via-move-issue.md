# Denial of Service via ReDoS in move_issue through Markdown Pattern Scanning

## Metadata
- **Source:** HackerOne
- **Report:** 1543584 | https://hackerone.com/reports/1543584
- **Submitted:** 2022-04-18
- **Reporter:** legit-security
- **Program:** GitLab
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Regular Expression Denial of Service (ReDoS), Algorithmic Complexity, Denial of Service
- **CVEs:** None
- **Category:** memory-binary

## Summary
A Regular Expression Denial of Service (ReDoS) vulnerability exists in GitLab's issue moving functionality. When moving an issue with a specially-crafted Markdown description containing repeated characters (e.g., '![l' × 100000), the MARKDOWN_PATTERN regex in UploadsRewriter exhibits polynomial time complexity, consuming 100% CPU for ~60 seconds per request. Parallel requests can render an entire GitLab instance unavailable.

## Attack scenario
1. Attacker self-registers or obtains authorization on a GitLab instance
2. Attacker creates a new issue with a malicious description: crafted string with many repeated patterns that trigger ReDoS (e.g., '![l' repeated 100,000+ times)
3. Attacker moves the issue to a different project via the web UI or API
4. The move_issue operation invokes UploadsRewriter which scans the description text against MARKDOWN_PATTERN
5. The vulnerable regex pattern with polynomial backtracking causes catastrophic backtracking, consuming 100% of a CPU core for 60 seconds
6. Attacker repeats steps 2-5 in parallel across multiple issues to exhaust all CPU cores and render the entire instance unresponsive (DoS)

## Root cause
The MARKDOWN_PATTERN regex in lib/gitlab/gfm/uploads_rewriter.rb uses Ruby's default Oniguruma regex engine which exhibits polynomial time complexity due to nested quantifiers and alternation patterns in the expression '\!?\[.*?\]\(/uploads/(?<secret>[0-9a-f]{32})/(?<file>.*?)\)'. When scanning text via @text.scan(@pattern) with specially crafted input containing many repetitions of characters that almost-but-don't-quite match the pattern, the regex engine performs excessive backtracking.

## Attacker mindset
An attacker recognizes that any authenticated user can create and move issues, making this a trivial attack vector requiring minimal privileges. The attacker understands regex complexity theory and crafts input to trigger catastrophic backtracking. By parallelizing requests, the attacker can saturate all available CPU resources and achieve complete service denial with relatively low effort and minimal resource consumption on their end.

## Defensive takeaways
- Always use ReDoS-resistant regex engines (RE2, Rust regex crate) for untrusted user input matching
- Implement rate limiting and resource quotas on issue creation/modification operations
- Add CPU/time-based circuit breakers for expensive regex operations (timeout with fallback behavior)
- Perform regex security audits on all patterns processing user-supplied content
- Use GitLab's existing UntrustedRegexp wrapper class consistently across codebase
- Implement input length limits on description fields before regex processing
- Monitor CPU usage patterns to detect regex-based attacks in real-time
- Consider async processing for issue operations that perform expensive regex scans

## Variant hunting
Search codebase for other uses of scan(), match(), and =~ operators on user-controlled input. Audit all MARKDOWN_PATTERN usages and similar regex patterns in gfm/, markdown/, and upload-related modules. Test issue update, comment creation, and any text processing operations. Check for similar polynomial-complexity patterns in merge request, wiki, and snippet handling. Look for regex patterns with nested quantifiers like (.*?)* or [^x]*y[^x]* applied to untrusted input.

## MITRE ATT&CK
- T1190
- T1499.4

## Notes
This is a classic ReDoS vulnerability exploiting the difference between regex engines. The fix is straightforward: migrate to RE2 or similar linear-time engine. The vulnerability is particularly critical because it requires minimal attacker privileges (self-registration enabled on GitLab.com) and has massive amplification potential. The 60-second timeout allows multiple in-flight requests to accumulate, making parallel exploitation extremely effective. GitLab's own UntrustedRegexp wrapper was available but not used in this code path.

## Full report
<details><summary>Expand</summary>

### Summary
Moving an issue with a specially-crafted description results in high CPU usage for 60 seconds (request timeout).
Multiple requests can be issued in parallel to create a larger impact.

### Steps to reproduce
1. Given an authorized user (on GitLab.com - anyone can self-register. On EE - depends on instance configuration).
2. Create an issue with the following description (provided a one-line python script to avoid bloating):
3. Once created, move the issue to a different project.

The script:
```python -c "print('![l' * 100000 + '\n')"```
Note: works with a lower number of repetitions too.


### Impact
After 60 seconds (timeout) - the request fails.
Meanwhile, on the server end, (a single) CPU is burnt out (verified against a local EE instance).
Issuing multiple requests in parallel (on multiple GitLab issues) results in multiple CPUs burn out.
Using the DockerHub image, the entire server is completely unavailable by repeatedly sending a small number of requests repeatedly.

### Examples
The bug is instance-independent, works on latest versions. Since GitLab.com is open-core - it would work on GitLab too.

### What is the current *bug* behavior?
The HTTP request fails for timeout while the server is burning CPU.

On the code side:
lib/gitlab/gfm/uploads_rewriter.rb / module Gitlab/Gfm / class UploadsRewriter / function files:
```@text.scan(@pattern)```
Where FileUploader::MARKDOWN_PATTERN is assigned to the pattern data member.

MARKDOWN_PATTERN is: 
```\!?\[.*?\]\(/uploads/(?<secret>[0-9a-f]{32})/(?<file>.*?)\)```
The pattern is of a polynomial complexity, thus, the scan results in high CPU utilization.

### What is the expected *correct* behavior?
Instead of using Ruby’s default Regex engine, use the RE2 engine (or the wrapped version at lib/gitlab/untrusted_regexp.rb), with the following pattern:
```\!?\[.*\]\(/uploads/([0-9a-f]{32})/(.*)\)```
As RE2 does not go beyond O(n), this scan becomes linear.
Note: since RE2 does not support named captures, all references should be fixed - assigning the results to secret/identifier local variables.### Relevant logs and/or screenshots

### Output of checks

#### Results of GitLab environment info

## Impact

A complete denial of service of a GitLab EE instance.
As this vulnerability impacts GitLab.com, we assume that this vulnerability opens the door for a DDOS attack.

</details>

---
*Analysed by Claude on 2026-05-24*
