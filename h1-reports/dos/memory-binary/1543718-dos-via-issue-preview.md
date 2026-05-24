# Denial of Service via Malicious Issue Preview

## Metadata
- **Source:** HackerOne
- **Report:** 1543718 | https://hackerone.com/reports/1543718
- **Submitted:** 2022-04-18
- **Reporter:** legit-security
- **Program:** GitLab
- **Bounty:** Not specified in writeup
- **Severity:** high
- **Vuln:** Denial of Service, Regular Expression Denial of Service (ReDoS), Resource Exhaustion, Inefficient Algorithm
- **CVEs:** None
- **Category:** memory-binary

## Summary
A specially-crafted issue description containing repeated markdown image syntax causes excessive CPU consumption during preview rendering, resulting in request timeout and server unavailability. The vulnerability stems from inefficient processing in the cache_collection_render function when handling large malformed markdown content.

## Attack scenario
1. Attacker creates a GitLab account on target instance (self-registration available on GitLab.com)
2. Attacker crafts issue description with repeated markdown image syntax: '![l' repeated ~349,525 times to reach max description size
3. Attacker triggers preview via UI preview button or preview_markdown API endpoint
4. Server processes malformed markdown through Renderer.cache_collection_render, consuming 100% of a single CPU core for 60 seconds
5. Request times out after 60 seconds while CPU remains maxed
6. Attacker issues multiple parallel requests to exhaust all available CPU cores and render instance completely unavailable

## Root cause
The Renderer.cache_collection_render method inefficiently processes markdown content without proper input validation or resource constraints. The reference extraction and HTML rendering pipeline performs expensive operations on malformed markdown without optimization or early termination mechanisms. No size limits or complexity analysis are enforced on preview operations.

## Attacker mindset
Resource exhaustion through algorithmic complexity exploitation. Attacker identifies that markdown preview operations lack rate limiting and proper input validation, allowing abuse of a public or authenticated API endpoint to cause denial of service with minimal effort. The ability to parallelize requests makes widespread impact possible.

## Defensive takeaways
- Implement strict input validation and size limits on markdown content before processing
- Add rate limiting to preview endpoints, especially for authenticated users
- Implement timeout and resource quotas per request (CPU time, memory allocation)
- Optimize Renderer.cache_collection_render to handle malformed markdown efficiently
- Add complexity analysis/detection for markdown parsing to reject pathological inputs
- Implement request queuing and prioritization to prevent single malicious user from consuming all resources
- Monitor CPU/resource usage per-request and implement circuit breakers
- Consider async/background processing for heavy markdown rendering operations

## Variant hunting
Test other markdown syntax patterns for similar CPU exhaustion (nested emphasis, nested lists, deeply nested quotes)
Check if the vulnerability affects other preview endpoints (comments, wiki pages, merge request descriptions)
Investigate if other Renderer methods have similar inefficiency issues
Test if authenticated vs unauthenticated users have different resource limits
Look for similar patterns in other user-controlled content processing pipelines

## MITRE ATT&CK
- T1190
- T1499.4

## Notes
This is a classic algorithmic complexity attack. The vulnerability is instance-independent and affects both GitLab.com and self-hosted instances. The writeup demonstrates good reproducibility with a one-liner script. The attack is particularly dangerous because it requires minimal privileges (self-registration) and minimal resources from attacker, while causing maximum impact on server. The ability to parallelize makes it effective against even well-resourced instances.

## Full report
<details><summary>Expand</summary>

### Summary
Previewing an issue with a specially-crafted description results in high CPU usage for 60 seconds (request timeout).
Multiple requests can be issued in parallel to create a larger impact.

### Steps to reproduce
1. Given an authorized user (on GitLab.com - anyone can self-register. On EE - depends on instance configuration).
2. Create an issue with the following description (provided a one-line python script to avoid bloating):
3. Hit the preview button.

Steps 2&3 can be accomplished via the preview_markdown API endpoint.

The script:
```python -c "print('![l' * int(1048576 / 3 - 1) + '\n')"```
Note: this is essentially the maximal description size, but a smaller number of repetitions works too.

### Impact
After 60 seconds (timeout) - the request fails.
Meanwhile, on the server end, (a single) CPU is burnt out (verified against a local EE instance).
Issuing multiple requests in parallel results in multiple CPUs burn out.
Using the DockerHub image, the entire server is completely unavailable by repeatedly sending a small number of requests repeatedly.

### Examples
The bug is instance-independent, works on latest versions. Since GitLab.com is open-core - it would work on GitLab too.

### What is the current *bug* behavior?
The HTTP request fails for timeout while the server is burning CPU.

On the code side:
```texts_and_contexts``` is being initialized here:

```
def analyze(text, context = {})
      @texts_and_contexts << { text: text, context: context }
    end
```

It is then used at banzai/reference_extractor.rb:
```
def html_documents
      ...
      @html_documents ||= Renderer.cache_collection_render(@texts_and_contexts)
      ...
```

The CPU utilization is found in the execution of ```cache_collection_render```.

### What is the expected *correct* behavior?
Fix the implementation of ```cache_collection_render```.

### Relevant logs and/or screenshots
### Output of checks
#### Results of GitLab environment info

## Impact

A complete denial of service of a GitLab EE instance.
As this vulnerability impacts GitLab.com, we assume that this vulnerability opens the door for a DDOS attack.

</details>

---
*Analysed by Claude on 2026-05-24*
