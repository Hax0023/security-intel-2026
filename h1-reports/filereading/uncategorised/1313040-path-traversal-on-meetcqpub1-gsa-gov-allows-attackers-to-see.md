# Path Traversal on meetcqpub1.gsa.gov allows arbitrary file listings

## Metadata
- **Source:** HackerOne
- **Report:** 1313040 | https://hackerone.com/reports/1313040
- **Submitted:** 2021-08-20
- **Reporter:** 0x0luke
- **Program:** GSA/TTS Bug Bounty Program
- **Bounty:** Unknown
- **Severity:** High
- **Vuln:** Path Traversal, Directory Traversal, Information Disclosure
- **CVEs:** None
- **Category:** uncategorised

## Summary
A path traversal vulnerability in the querybuilder.json.css endpoint allows attackers to manipulate the 'path' parameter to enumerate arbitrary directories and files on the server filesystem. By crafting URLs with different path values (e.g., /etc, /home, /var), an attacker can retrieve sensitive directory listings and file information, compromising system confidentiality.

## Attack scenario
1. Attacker identifies the querybuilder.json.css endpoint accepts a 'path' parameter
2. Attacker modifies the path parameter from the default value to /etc to enumerate system directories
3. Server processes the unsanitized path parameter and returns full directory listing with file metadata
4. Attacker iterates through common system paths (/var, /home, /root, /opt) to map the filesystem
5. Attacker identifies sensitive files and obtains their locations for potential secondary exploitation
6. Information gathered can be used to plan further attacks targeting exposed configuration files or credentials

## Root cause
Insufficient input validation and path canonicalization on the 'path' parameter. The application fails to restrict directory traversal by not validating that the resolved path remains within an intended base directory, allowing direct filesystem enumeration through a web-accessible API endpoint.

## Attacker mindset
An attacker seeking reconnaissance would exploit this to map the target system's filesystem structure, identify configuration directories, locate sensitive files, and gather intelligence for privilege escalation or data exfiltration attacks. Low effort, high reward recon opportunity.

## Defensive takeaways
- Implement strict input validation using allowlists of permitted directories rather than blacklists
- Use path canonicalization and verify resolved paths remain within intended base directory using realpath()
- Apply principle of least privilege - expose only necessary files/directories through the API
- Implement rate limiting and access controls on directory listing endpoints
- Use chroot jails or containerization to restrict filesystem access scope
- Disable directory listing functionality where not explicitly required
- Conduct security code review of all path handling operations in querybuilder components
- Implement comprehensive logging and alerting for suspicious path traversal patterns

## Variant hunting
Search for similar parameter handling in: querybuilder endpoints with path/file/dir parameters; CQ (Content Query) or content repository tools; other .css/.json endpoints accepting user input; any web-accessible backend query/search interfaces; legacy GSA/TTS applications with similar architecture patterns

## MITRE ATT&CK
- T1190
- T1566
- T1083
- T1526

## Notes
The reporter noted uncertainty about scope (GSA vs TTS program), suggesting internal coordination challenges. The vulnerability is straightforward - unsanitized path parameter in a query builder endpoint. The p.hits=full and p.limit=-1 parameters suggest a backend search/query engine. This pattern is common in AEM (Adobe Experience Manager), Elasticsearch, or similar content platforms. Check for similar endpoints and instances across GSA infrastructure.

## Full report
<details><summary>Expand</summary>

## Summary:
Path Traversal on meetcqpub1.gsa.gov allows attackers to see arbitrary file listings from a directory of their choice.

I wasn't sure if this page was in scope of this program or the TTS program, hopefully this isn't a problem

## Steps To Reproduce:

  1. Navigate to the following URL - https://meetcqpub1.gsa.gov/bin/querybuilder.json.css?path=/home&p.hits=full&p.limit=-1
  2. The path parameter can be manipulated to show other directories on the system as well, for example /etc.

## Impact

An attacker is able to see files and directories present on the system, breaking the confidentiality section of the CIA Triad.

</details>

---
*Analysed by Claude on 2026-05-24*
