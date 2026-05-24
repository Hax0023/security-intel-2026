# Chrome Extension Self-DOS via Large security.txt File Processing

## Metadata
- **Source:** HackerOne
- **Report:** 290955 | https://hackerone.com/reports/290955
- **Submitted:** 2017-11-16
- **Reporter:** sp1d3rs
- **Program:** Chrome Extension Security (implied from context)
- **Bounty:** Not specified in writeup
- **Severity:** low
- **Vuln:** Denial of Service, Resource Exhaustion, Uncontrolled Resource Consumption
- **CVEs:** None
- **Category:** memory-binary

## Summary
A Chrome extension is vulnerable to a self-denial of service condition when processing abnormally large security.txt files (1-2 GB) via AJAX calls without timeout constraints. This causes the browser tab or extension to hang or crash due to excessive memory and CPU consumption during file processing.

## Attack scenario
1. Attacker creates a malicious website with an extremely large security.txt file (1-2 GB in size)
2. Victim visits the attacker's website in Chrome browser
3. The vulnerable Chrome extension automatically attempts to fetch and process the security.txt file via AJAX
4. The extension loads the entire file into memory without size validation or timeout
5. Browser tab or extension process consumes excessive CPU and RAM, causing hang or crash
6. User experience is degraded or the tab becomes unresponsive, constituting a denial of service

## Root cause
The `getSecuritytxt` function performs AJAX requests to fetch security.txt files from untrusted hosts without implementing: (1) file size limits, (2) request timeouts, (3) streaming/chunked processing, or (4) memory constraints. The extension processes every site visited without protection mechanisms.

## Attacker mindset
Attacker recognizes that browser extensions operate with elevated privileges and lack typical HTTP timeout mechanisms. By hosting an excessively large security.txt file, the attacker can trigger resource exhaustion in the extension's context, affecting the user's browsing experience without requiring code execution or privilege escalation.

## Defensive takeaways
- Implement xhr.timeout property on all AJAX calls to untrusted external resources with reasonable values (15-30 seconds)
- Add maximum file size validation before processing remote content
- Implement abort handling for timeouts and oversized responses
- Use streaming/chunked processing for large files instead of loading entire content into memory
- Consider rate limiting or debouncing repeated requests to security.txt across multiple tabs
- Validate content-length headers before initiating downloads
- Implement memory limits or progress monitoring for resource-intensive operations
- Test extension behavior with adversarially large files during security review

## Variant hunting
Check for similar timeout issues in other extension functions making external requests
Search for other AJAX/fetch calls without timeout configurations
Identify other file processing operations that lack size constraints
Review extension permissions and whether security.txt processing requires elevated privileges
Test other metadata file formats (.well-known endpoints, robots.txt, sitemap.xml) for similar issues
Examine if the extension makes requests on every page load (amplification vector)

## MITRE ATT&CK
- T1499.1
- T1561.1

## Notes
This vulnerability demonstrates how browser extensions can inadvertently create denial of service vectors when processing untrusted external content without proper safeguards. The low severity assessment is appropriate as impact is limited to individual tabs rather than system-wide. The suggested fix using xhr.timeout is a minimal mitigation; comprehensive fix should include multiple defensive layers. The writeup mentions a GitHub PR was linked in comments (not visible here) which likely contained the proposed patch.

## Full report
<details><summary>Expand</summary>

##Description
Hello. Before all, thanks for the invite:) Here is keyword: `frog`
I discovered the self-DOS issue, which affects Chrome extension.

##Impact
I marked the impact as low, because it will affect only the browser tab, and will not impact other browser tabs. The issue happens due to processing the large files using AJAX call in the `getSecuritytxt` function.

##Steps to reproduce
1. Create security.txt with the size of 1-2 GB on your host.
2. Navigate to this site in the Chrome Browser (at this time you may notice traffic and CPU utilization increasing due to pre-flight check of the security.txt)
3. Click on the extension. Depending on the Chrome version, amount of RAM and CPU, you can experience one of (or all together):
 * Extension hang
 * Tab hang
 * Tab crash

##Suggested fix
Since we are making AJAX calls to the untrusted hosts, end extension is working for the every site we opened in the tab, we should get rid from such kind of issues. I suggest to implement `timeout` on the AJAX calls using
```
xhr.timeout = 15000; //some value in milliseconds
xhr.ontimeout = function (e) {
//handling timeout
}; 
```
I will link the Github PR in the comment below:)


</details>

---
*Analysed by Claude on 2026-05-24*
